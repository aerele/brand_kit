frappe.utils._original_get_desktop_icon = frappe.utils.get_desktop_icon;

frappe.utils.get_desktop_icon = function (icon_name, variant) {
	let app = frappe.boot.app_data?.find(
		(app) =>
			app.app_title === icon_name ||
			app.app_name === icon_name ||
			frappe.scrub(app.app_title) === frappe.scrub(icon_name) ||
			app.workspaces?.some(
				(workspace) => frappe.scrub(workspace) === frappe.scrub(icon_name)
			)
	);

	if (app?.app_logo_url) {
		return Array.isArray(app.app_logo_url) ? app.app_logo_url[0] : app.app_logo_url;
	}

	return frappe.utils._original_get_desktop_icon(icon_name, variant);
};

function replaceAppLogos() {
	if (!frappe.boot?.app_data) return;

	document.querySelectorAll("img").forEach((img) => {
		const src = img.getAttribute("src");

		if (!src || !src.startsWith("/assets/")) {
			return;
		}

		// Extract app name from: /assets/<app_name>/
		const parts = src.split("/");
		const app_name = parts[2];

		if (!app_name) {
			return;
		}

		const app = frappe.boot.app_data.find((app) => app.app_name === app_name);

		if (app?.app_logo_url && img.src !== app.app_logo_url) {
			img.src = app.app_logo_url;
		}
	});
}

frappe.after_ajax(() => {
	replaceAppLogos();
});
