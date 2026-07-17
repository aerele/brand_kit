# Copyright (c) 2026, Aerele Technologies and contributors
# For license information, please see license.txt

from frappe.model.document import Document

from brand_kit.utils.app_ui_settings import raven_branding, setup_branding


class AppUISettings(Document):
	def onload(self):
		from brand_kit.utils.app_ui_settings import sync_installed_apps

		sync_installed_apps()

	def validate(self):
		for idx, row in enumerate(self.apps, start=1):
			row.idx = idx

	def on_update(self):
		before_doc = self.get_doc_before_save()

		# Map previous apps by app_name
		old_apps = {}
		if before_doc:
			old_apps = {row.app_name: row for row in before_doc.apps}

		for app in self.apps:
			setup_branding(app.app_name, app.display_name, app.logo)

			old_name = "Raven"
			if app.app_name in old_apps:
				old_name = old_apps[app.app_name].display_name

			raven_branding(
				app.app_name,
				old_name=old_name,
				new_name=app.display_name,
				logo=app.logo,
			)
