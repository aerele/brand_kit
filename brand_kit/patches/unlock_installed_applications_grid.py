import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def execute():
	if frappe.db.exists(
		"Property Setter",
		{"doc_type": "Installed Applications", "field_name": "installed_applications", "property": "read_only"},
	):
		return

	make_property_setter(
		doctype="Installed Applications",
		fieldname="installed_applications",
		property="read_only",
		value="0",
		property_type="Check",
	)
