# Copyright (c) 2026, Local and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class BrandSettings(Document):
	def on_update(self):
		from brand_kit.utils.branding import sync_app_name

		sync_app_name(self)
