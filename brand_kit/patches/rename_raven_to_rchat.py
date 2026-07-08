import frappe


def execute():
	if frappe.db.exists("Translation", {"source_text": "Raven", "language": "en"}):
		return

	frappe.get_doc(
		{
			"doctype": "Translation",
			"source_text": "Raven",
			"language": "en",
			"translated_text": "R-Chat",
		}
	).insert(ignore_permissions=True)
