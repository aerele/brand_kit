from brand_kit.utils.app_ui_settings import sync_installed_apps


def after_install():
	sync_installed_apps()
