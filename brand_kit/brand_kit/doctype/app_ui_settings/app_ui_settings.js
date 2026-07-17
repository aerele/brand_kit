// Copyright (c) 2026, Aerele Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("App UI Settings", {
	refresh(frm) {
		frm.set_df_property("apps", "cannot_add_rows", true);
		frm.set_df_property("apps", "cannot_delete_rows", true);
	},
});
