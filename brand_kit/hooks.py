app_name = "brand_kit"
app_title = "Brand Kit"
app_publisher = "Local"
app_description = "Centralized UI branding and white-labeling"
app_email = "admin@example.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "brand_kit",
# 		"logo": "/assets/brand_kit/logo.png",
# 		"title": "Brand Kit",
# 		"route": "/brand_kit",
# 		"has_permission": "brand_kit.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/brand_kit/css/brand_kit.css"
# app_include_js = "/assets/brand_kit/js/brand_kit.js"
app_include_js = [
    "/assets/brand_kit/js/brand_kit.js"
]

# include js, css files in header of web template
# web_include_css = "/assets/brand_kit/css/brand_kit.css"
# web_include_js = "/assets/brand_kit/js/brand_kit.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "brand_kit/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "brand_kit/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "brand_kit.utils.jinja_methods",
# 	"filters": "brand_kit.utils.jinja_filters"
# }

# Website Context
# ------------------
# Runs after every website/portal page's own get_context(), including other apps' pages
# (e.g. Raven's /raven route) - lets us overwrite branding context values centrally.

update_website_context = "brand_kit.utils.branding.update_website_context"

# Migration Hooks
# ------------------
# Keeps "App UI Settings" in sync with whatever apps are actually installed, after every
# bench migrate (the normal step after installing/removing any app).

after_migrate = ["brand_kit.utils.app_ui_settings.sync_installed_apps"]

# Boot Session
# ------------
# Overrides each app's boot-time "app_title" (read by the Desk sidebar's app subtitle)
# with its App UI Settings display_name, when one is set.

extend_bootinfo = "brand_kit.utils.app_ui_settings.extend_bootinfo"

# Installation
# ------------

# before_install = "brand_kit.install.before_install"
# after_install = "brand_kit.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "brand_kit.uninstall.before_uninstall"
# after_uninstall = "brand_kit.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "brand_kit.utils.before_app_install"
# after_app_install = "brand_kit.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "brand_kit.utils.before_app_uninstall"
# after_app_uninstall = "brand_kit.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "brand_kit.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "brand_kit.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "Installed Applications": {
	# 	"before_save": "brand_kit.utils.installed_apps_override.restore_custom_display_names",
	# 	"on_update": "brand_kit.utils.installed_apps_override.sync_display_names_to_translations",
	# }

	"App UI Settings": {
		"on_update": [
			"brand_kit.utils.app_ui_settings.sync_display_names_to_translations",
			"brand_kit.utils.app_ui_settings.sync_logos_to_static_assets",
		],
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"brand_kit.tasks.all"
# 	],
# 	"daily": [
# 		"brand_kit.tasks.daily"
# 	],
# 	"hourly": [
# 		"brand_kit.tasks.hourly"
# 	],
# 	"weekly": [
# 		"brand_kit.tasks.weekly"
# 	],
# 	"monthly": [
# 		"brand_kit.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "brand_kit.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "brand_kit.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "brand_kit.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "brand_kit.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["brand_kit.utils.before_request"]
# after_request = ["brand_kit.utils.after_request"]

# Job Events
# ----------
# before_job = ["brand_kit.utils.before_job"]
# after_job = ["brand_kit.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"brand_kit.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

