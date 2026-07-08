# Copyright (c) 2026, Local and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class AppUISettings(Document):
	def onload(self):
		from brand_kit.utils.app_ui_settings import sync_installed_apps

		sync_installed_apps()
