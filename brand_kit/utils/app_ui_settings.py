import frappe

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
				"display_name": title,
			},
		)
		changed = True

	if changed:
		settings.save(ignore_permissions=True)
