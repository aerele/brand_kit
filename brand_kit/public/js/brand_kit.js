frappe.utils._original_get_desktop_icon = frappe.utils.get_desktop_icon;

frappe.utils.get_desktop_icon = function (icon_name, variant) {
    let app = frappe.boot.app_data?.find((app) => 
        app.app_title === icon_name || 
        app.app_name === icon_name ||
        frappe.scrub(app.app_title) === frappe.scrub(icon_name)
    );

    if (app?.app_logo_url) {
        return Array.isArray(app.app_logo_url)
            ? app.app_logo_url[0]
            : app.app_logo_url;
    }

    return frappe.utils._original_get_desktop_icon(icon_name, variant);
};