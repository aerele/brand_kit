import os
import shutil

import frappe

from brand_kit.brand_kit.doctype import app_ui_settings
from brand_kit.branding.app_display_names import DEFAULT_APP_DISPLAY_NAMES
from brand_kit.utils.installed_apps_override import get_apps_screen_titles, get_single_workspace_label

EXCLUDED_APPS = {"frappe", "brand_kit"}


def get_app_title(app):
	titles = frappe.get_hooks("app_title", app_name=app)
	return titles[0] if titles else app


def sync_installed_apps(doc=None, method=None):
	settings = frappe.get_single("App UI Settings")
	before_count = len(settings.apps)

	installed_apps = set(frappe.get_installed_apps()) - EXCLUDED_APPS

	changed = False

	# remove apps that are no longer installed
	settings.apps = [row for row in settings.apps if row.app_name in installed_apps]
	if len(settings.apps) != before_count:
		changed = True

	# refresh existing apps after cleanup
	existing = {row.app_name for row in settings.apps}

	# add newly installed apps
	for app in installed_apps:
		if app in existing:
			continue

		title = get_app_title(app)
		display_name = DEFAULT_APP_DISPLAY_NAMES.get(title, title)

		settings.append(
			"apps",
			{
				"app_name": app,
				"original_app_name": title,
				"display_name": display_name,
			},
		)

		changed = True

	if changed:
		settings.save(ignore_permissions=True)


def setup_branding(app, display_name, logo=None):
	field_map = {
		"helpdesk": "HD Settings",
		"crm": "FCRM Settings",
	}

	doctype = field_map.get(app)
	if not doctype:
		return

	settings = frappe.get_doc(doctype, doctype)

	settings.brand_name = display_name

	if logo:
		settings.brand_logo = logo
		settings.favicon = logo
	settings.flags.ignore_mandatory = True
	settings.save(ignore_permissions=True)


def raven_branding(app, old_name="Raven", new_name=None, logo=None):
	if app != "raven":
		return

	if not new_name:
		return

	if old_name != new_name and frappe.db.exists("Raven Workspace", old_name):
		frappe.rename_doc("Raven Workspace", old_name, new_name)
	elif frappe.db.exists("Raven Workspace", "Raven"):
		frappe.rename_doc("Raven Workspace", "Raven", new_name)

	if logo and frappe.db.exists("Raven Workspace", new_name):
		frappe.db.set_value("Raven Workspace", new_name, "logo", logo)


def sync_display_names_to_translations(doc, method):
	before = doc.get_doc_before_save()
	old_values = {r.app_name: r.display_name for r in (before.apps if before else [])}

	for row in doc.apps:
		if row.display_name == old_values.get(row.app_name):
			continue  # unchanged for this app - skip entirely, no DB work

		titles = set(get_apps_screen_titles(row.app_name))
		workspace_label = get_single_workspace_label(row.app_name)
		if workspace_label:
			titles.add(workspace_label)
		app_title = frappe.get_hooks("app_title", app_name=row.app_name)
		if app_title:
			titles.add(app_title[0])

		for title in titles:
			if not row.display_name or row.display_name == title:
				frappe.db.delete("Translation", {"source_text": title, "language": "en"})
			else:
				existing = frappe.db.exists("Translation", {"source_text": title, "language": "en"})
				if existing:
					frappe.db.set_value("Translation", existing, "translated_text", row.display_name)
				else:
					frappe.get_doc(
						{
							"doctype": "Translation",
							"source_text": title,
							"language": "en",
							"translated_text": row.display_name,
						}
					).insert(ignore_permissions=True)
	frappe.clear_cache()


def extend_bootinfo(bootinfo):
	rows = frappe.get_all("App UI Setting", fields=["app_name", "display_name", "logo"])
	title_overrides = {row.app_name: row.display_name for row in rows if row.display_name}
	logo_overrides = {row.app_name: row.logo for row in rows if row.logo}
	if not title_overrides and not logo_overrides:
		return
	for app in bootinfo.get("app_data") or []:
		app_name = app.get("app_name")
		if app_name in title_overrides:
			app["app_title"] = title_overrides[app_name]
		if app_name in logo_overrides:
			app["app_logo_url"] = logo_overrides[app_name]


def get_logo_asset_path(app_name):
	hooks = frappe.get_hooks("add_to_apps_screen", app_name=app_name)
	if not hooks or not hooks[0].get("logo"):
		return None
	relative = hooks[0]["logo"].split(f"/assets/{app_name}/", 1)[-1]
	return frappe.get_app_path(app_name, "public", relative)


def get_uploaded_file_path(file_url):
	if file_url.startswith("/private/files/"):
		return frappe.get_site_path("private", "files", file_url.rsplit("/", 1)[-1])
	return frappe.get_site_path("public", "files", file_url.rsplit("/", 1)[-1])


def sync_logos_to_static_assets(doc, method):
	before = doc.get_doc_before_save()
	old_logos = {r.app_name: r.logo for r in (before.apps if before else [])}

	for row in doc.apps:
		if row.logo == old_logos.get(row.app_name):
			continue

		dest = get_logo_asset_path(row.app_name)
		if not dest:
			continue
		backup = dest + ".original"

		if row.logo:
			if os.path.exists(dest) and not os.path.exists(backup):
				shutil.copyfile(dest, backup)
			shutil.copyfile(get_uploaded_file_path(row.logo), dest)
		elif os.path.exists(backup):
			shutil.copyfile(backup, dest)
	frappe.clear_cache()
