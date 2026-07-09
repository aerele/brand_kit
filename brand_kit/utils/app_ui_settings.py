import frappe

from brand_kit.utils.installed_apps_override import get_apps_screen_titles, get_single_workspace_label

EXCLUDED_APPS = {"frappe", "brand_kit"}


def get_app_title(app):
	titles = frappe.get_hooks("app_title", app_name=app)
	return titles[0] if titles else app


def sync_installed_apps():
	settings = frappe.get_single("App UI Settings")
	existing = {row.app_name for row in settings.apps}

	changed = False
	for app in frappe.get_installed_apps():
		if app in EXCLUDED_APPS or app in existing:
			continue

		title = get_app_title(app)
		settings.append(
			"apps",
			{
				"app_name": app,
				"original_app_name": title,
				"display_name": "",
			},
		)
		changed = True

	if changed:
		settings.save(ignore_permissions=True)


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
	overrides = {
		row.app_name: row.display_name
		for row in frappe.get_all("App UI Setting", fields=["app_name", "display_name"])
		if row.display_name
	}
	if not overrides:
		return
	for app in bootinfo.get("app_data") or []:
		if app.get("app_name") in overrides:
			app["app_title"] = overrides[app["app_name"]]
