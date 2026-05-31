import os
from datetime import datetime

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from config.settings import settings
from utils.logger import get_logger

logger = get_logger("AppiumSetup")


def pytest_addoption(parser):

    parser.addoption(
        "--device",
        action="store",
        default=None,
        help="Device name override"
    )

    parser.addoption(
        "--udid",
        action="store",
        default=None,
        help="Real device UDID"
    )

    parser.addoption(
        "--app",
        action="store",
        default=None,
        help="APK path override"
    )

    parser.addoption(
        "--no-reset",
        action="store_true",
        help="Keep app state"
    )

    parser.addoption(
        "--full-reset",
        action="store_true",
        help="Uninstall app before session"
    )


@pytest.fixture(scope="function")
def driver(request):

    driver = None

    try:

        caps = settings["appium"]["capabilities"]

        device_name = (request.config.getoption("--device") or caps["deviceName"])
        udid = request.config.getoption("--udid")
        app_path = (request.config.getoption("--app") or caps["app"])
        no_reset = (request.config.getoption("--no-reset") or caps["noReset"])
        full_reset = (request.config.getoption("--full-reset") or caps["fullReset"])

        logger.info(f"Starting Appium session on device: {device_name}")

        options = UiAutomator2Options()

        options.platform_name = caps["platformName"]
        options.automation_name = caps["automationName"]
        options.device_name = device_name

        options.app = app_path
        options.app_package = caps["appPackage"]
        options.app_activity = caps["appActivity"]

        options.no_reset = no_reset
        options.full_reset = full_reset
        options.auto_grant_permissions = caps["autoGrantPermissions"]
        options.new_command_timeout = caps["newCommandTimeout"]

        if udid:
            options.udid = udid

        server_url = (
            f"http://{settings['appium']['server']['host']}:"
            f"{settings['appium']['server']['port']}"
        )

        if not os.path.exists(app_path):
            raise FileNotFoundError(f"APK not found at path: {app_path}")
        
        logger.info(f"Server URL: {server_url}")
        logger.info(f"App Path: {app_path}")
        logger.info(f"Platform: {caps['platformName']}")
        logger.info(f"Automation: {caps['automationName']}")

        driver = webdriver.Remote(command_executor=server_url, options=options)
        logger.info(f"Session ID: {driver.session_id}")

        driver.implicitly_wait(settings["timeouts"]["implicitWait"])

        logger.info("Appium driver initialized successfully")

        yield driver

    except Exception as e:

        logger.error(f"Driver initialization failed: {e}")

        raise

    finally:

        if driver:

            driver.quit()
            
            logger.info("Appium session closed")

def pytest_runtest_setup(item):

    logger.info(f"START TEST: {item.name}")


def pytest_runtest_teardown(item):

    logger.info(f"END TEST: {item.name}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if (settings["reporting"]["screenshot_on_failure"] and report.when == "call" and report.failed):

        driver = item.funcargs.get("driver")

        if driver:

            screenshot_dir = settings["reporting"]["screenshot_folder"]

            os.makedirs(screenshot_dir, exist_ok=True)

            timestamp = datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S"
            )

            file_name = os.path.join(screenshot_dir, f"{item.name}_{timestamp}.png")

            try:

                driver.save_screenshot(file_name)

                logger.error(f"Screenshot saved: {file_name}")

            except Exception as e:

                logger.error(f"Screenshot capture failed: {e}")