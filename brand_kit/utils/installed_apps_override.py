import frappe


def restore_custom_display_names(doc, method):
	if not (frappe.flags.in_migrate or frappe.flags.in_install or frappe.flags.in_uninstall):
		return  # a normal admin save - don't touch anything, let the edit/clear stand

	old_values = frappe.db.get_all(
		"Installed Application",
		filters={"parent": doc.name, "parentfield": "installed_applications"},
		fields=["app_name", "custom_display_name"],
	)
	old_map = {row.app_name: row.custom_display_name for row in old_values if row.custom_display_name}

	for row in doc.installed_applications:
		if row.app_name in old_map:
			row.custom_display_name = old_map[row.app_name]


def get_apps_screen_titles(app):
	entries = frappe.get_hooks("add_to_apps_screen", app_name=app)
	return [e.get("title") for e in entries if e.get("title")]


def get_single_workspace_label(app):
	modules = frappe.get_all("Module Def", filters={"app_name": app}, pluck="name")
	if not modules:
		return None
	workspaces = frappe.get_all("Workspace", filters={"module": ["in", modules]}, pluck="label")
	if len(workspaces) == 1:
		return workspaces[0]
	return None  # zero, or multiple (hrms/erpnext) - ambiguous, skip entirely


def sync_display_names_to_translations(doc, method):
	before = doc.get_doc_before_save()
	old_values = {r.app_name: r.custom_display_name for r in (before.installed_applications if before else [])}

	for row in doc.installed_applications:
		if row.custom_display_name == old_values.get(row.app_name):
			continue  # unchanged for this app - skip entirely, no DB work

		titles = set(get_apps_screen_titles(row.app_name))
		workspace_label = get_single_workspace_label(row.app_name)
		if workspace_label:
			titles.add(workspace_label)

		for title in titles:
			if not row.custom_display_name or row.custom_display_name == title:
				frappe.db.delete("Translation", {"source_text": title, "language": "en"})
			else:
				existing = frappe.db.exists("Translation", {"source_text": title, "language": "en"})
				if existing:
					frappe.db.set_value("Translation", existing, "translated_text", row.custom_display_name)
				else:
					frappe.get_doc(
						{
							"doctype": "Translation",
							"source_text": title,
							"language": "en",
							"translated_text": row.custom_display_name,
						}
					).insert(ignore_permissions=True)
	frappe.clear_cache()
