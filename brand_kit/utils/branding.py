import frappe


def sync_app_name(brand_settings=None):
	brand_settings = brand_settings or frappe.get_cached_doc("Brand Settings")
	if not brand_settings.app_name:
		return

	frappe.db.set_single_value("Website Settings", "app_name", brand_settings.app_name)
	frappe.db.set_single_value("System Settings", "app_name", brand_settings.app_name)
	frappe.clear_cache()


def update_website_context(context):
	brand_settings = frappe.get_cached_doc("Brand Settings")
	if brand_settings.app_name:
		return {"app_name": brand_settings.app_name}
