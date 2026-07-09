import frappe


def sync_app_name(brand_settings=None):
	brand_settings = brand_settings or frappe.get_cached_doc("Brand Settings")
	if not brand_settings.app_name:
		return

	frappe.db.set_single_value("Website Settings", "app_name", brand_settings.app_name)
	frappe.db.set_single_value("System Settings", "app_name", brand_settings.app_name)
	frappe.clear_cache()


def get_app_name_for_route(route):
	for app in frappe.get_installed_apps():
		for entry in frappe.get_hooks("add_to_apps_screen", app_name=app):
			entry_route = (entry.get("route") or "").strip("/").split("/")[0]
			if entry_route and entry_route == route:
				return app
	return None


def update_website_context(context):
	route = (frappe.local.request.path or "").strip("/").split("/")[0]
	app = get_app_name_for_route(route)
	if not app:
		return

	display_name = frappe.db.get_value("App UI Setting", {"app_name": app}, "display_name")
	if display_name:
		return {"app_name": display_name}
