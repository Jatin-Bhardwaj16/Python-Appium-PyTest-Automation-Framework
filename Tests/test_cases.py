import pytest

from Pages.HomePage import HomePage
from utils.logger import get_logger

logger = get_logger("TestHomePage")

@pytest.mark.device
@pytest.mark.device_info
def test_device_info_check(driver):

    home_page = HomePage(driver)

    logger.info("Checking device information")

    device_info = home_page.device_info_check()

    platform_version = device_info["platform_version"]
    device_name = device_info["device_name"]

    assert platform_version is not None
    assert device_name is not None

@pytest.mark.device
@pytest.mark.installation
def test_app_installation_check(driver):

    home_page = HomePage(driver)

    logger.info("Checking if the app is installed")

    is_installed = home_page.app_installation_check()

    assert is_installed

# Smoke Tests
@pytest.mark.smoke
@pytest.mark.load
def test_home_page_loaded(driver):

    home_page = HomePage(driver)

    logger.info("Verifying home page is displayed")

    assert home_page.load_app()


@pytest.mark.smoke
@pytest.mark.display
def test_is_home_page_displayed(driver):

    home_page = HomePage(driver)

    logger.info("Checking if home page is displayed")

    assert home_page.is_home_page_displayed()


# Sanity Tests
@pytest.mark.sanity
@pytest.mark.app_info
def test_get_package_activity_version_state(driver):

    home_page = HomePage(driver)

    logger.info("Getting current package, activity, app version, and app state")

    package, activity, app_version, app_state = home_page.get_package_activity_version_state()

    logger.info(f"Current package: {package}, Current activity: {activity}, App version: {app_version}, App state: {app_state}"
                )

    assert package is not None
    assert activity is not None
    assert app_version is not None
    assert app_state is not None


@pytest.mark.sanity
@pytest.mark.title
def test_get_page_title(driver):

    home_page = HomePage(driver)

    logger.info("Getting home page title")

    title = home_page.get_page_title()

    logger.info(f"Home page title: {title}")

    assert title == "API Demos"


@pytest.mark.sanity
@pytest.mark.menu
def test_get_all_menu_items(driver):

    home_page = HomePage(driver)

    logger.info("Getting all menu items from home screen")

    menu_items = home_page.get_all_menu_items()

    logger.info(f"Found {len(menu_items)} menu items")

    assert len(menu_items) > 0


# Navigation Tests
@pytest.mark.regression
@pytest.mark.navigation
def test_validate_all_menu_items_navigation(driver):

    home_page = HomePage(driver)

    logger.info("Validating all menu item navigation")

    menu_names = (home_page.validate_all_menu_items_navigation())

    logger.info(f"Validated {len(menu_names)} menu items successfully")

    assert len(menu_names) > 0


# App Lifecycle Tests
@pytest.mark.regression
@pytest.mark.restart
def test_restart_app(driver):

    home_page = HomePage(driver)

    logger.info("Restarting the app")

    assert home_page.restart_the_app()


@pytest.mark.regression
@pytest.mark.background
def test_background_app_for_seconds(driver):

    home_page = HomePage(driver)

    seconds = 5

    logger.info(f"Backgrounding the app for {seconds} seconds")

    assert home_page.background_app_for_seconds(seconds)


@pytest.mark.regression
@pytest.mark.lifecycle
def test_terminate_app_and_verify(driver):

    home_page = HomePage(driver)

    logger.info(f"Terminating the app and verifying it's closed")

    assert home_page.terminate_app_and_verify()

@pytest.mark.notification
@pytest.mark.open_notifications
def test_open_notifications_panel(driver):

    home_page = HomePage(driver)

    logger.info("Opening notifications panel")

    assert home_page.open_notifications_panel()

@pytest.mark.notification
@pytest.mark.full_notifications_open
def test_swipe_down_full_notifications_panel(driver):

    home_page = HomePage(driver)

    logger.info("Verifying full notification panel is displayed")

    assert home_page.open_full_notifications_panel()

@pytest.mark.notification
@pytest.mark.full_notifications_close
def test_close_full_notifications_panel(driver):

    home_page = HomePage(driver)

    logger.info("Closing full notification panel")

    assert home_page.close_full_notifications_panel()