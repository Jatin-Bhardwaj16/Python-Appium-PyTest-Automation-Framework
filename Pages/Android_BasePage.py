import os
import time
from datetime import datetime

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey

from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction

from Pages.Core_BasePage import CoreBasePage
from config.settings import settings


class AndroidBasePage(CoreBasePage):

    # App Information & State
    # Methods for retrieving application metadata and runtime state.
    def get_current_package(self):
        self.logger.info("Getting current app package")
        return self.driver.current_package

    def get_current_activity(self):
        self.logger.info("Getting current app activity")
        return self.driver.current_activity

    def get_app_version(self):
        self.logger.info("Getting app version")

        package = settings["appium"]["capabilities"]["appPackage"]

        result = self.driver.execute_script(
            "mobile: shell",
            {"command": "dumpsys", "args": ["package", package]}
        )

        for line in result.splitlines():
            if "versionName" in line:
                return line.strip().split("=")[-1]

        return None

    def get_app_state(self):
        self.logger.info("Getting app state")

        package = settings["appium"]["capabilities"]["appPackage"]
        return self.driver.query_app_state(package)

    def is_app_installed(self, package=None):
        package = package or settings["appium"]["capabilities"]["appPackage"]
        self.logger.info(f"Checking if app is installed: {package}")
        return self.driver.is_app_installed(package)

    def get_device_info(self):
        self.logger.info("Getting device information")

        size = self.driver.get_window_size()

        return {
            "device_name": self.driver.capabilities.get("deviceName"),
            "platform_version": self.driver.capabilities.get("platformVersion"),
            "screen_width": size["width"],
            "screen_height": size["height"],
            "udid": self.driver.capabilities.get("udid"),
        }

    # App Lifecycle Management
    # Methods for launching, closing, restarting, and managing apps.
    def launch_app(self):
        self.logger.info("Launching the app")
        self.driver.launch_app()

    def close_app(self):
        self.logger.info("Closing the app")
        self.driver.close_app()

    def activate_app(self, app_package=None):
        app_package = app_package or settings["appium"]["capabilities"]["appPackage"]
        self.logger.info(f"Activating app: {app_package}")
        self.driver.activate_app(app_package)

    def terminate_app(self, app_package=None):
        app_package = app_package or settings["appium"]["capabilities"]["appPackage"]
        self.logger.info(f"Terminating app: {app_package}")
        return self.driver.terminate_app(app_package)

    def background_app(self, seconds):
        self.logger.info(f"Sending app to background for {seconds} seconds")
        self.driver.background_app(seconds)

    def restart_app(self):
        self.logger.info("Restarting app")

        package = settings["appium"]["capabilities"]["appPackage"]

        self.driver.terminate_app(package)
        self.driver.activate_app(package)

    def reset_app(self):
        self.logger.info("Resetting app (full reset)")

        package = settings["appium"]["capabilities"]["appPackage"]

        self.driver.terminate_app(package)
        self.driver.execute_script(
            "mobile: shell",
            {"command": "pm", "args": ["clear", package]}
        )

        self.logger.info("App data cleared")

    def install_app(self, apk_path):
        self.logger.info(f"Installing app from: {apk_path}")
        self.driver.install_app(apk_path)

    def uninstall_app(self, package=None):
        package = package or settings["appium"]["capabilities"]["appPackage"]
        self.logger.info(f"Uninstalling app: {package}")
        self.driver.remove_app(package)

    # Android Hardware Key Actions
    # Methods for interacting with Android hardware buttons.
    def press_back(self):
        self.logger.info("Pressing Android back button")
        self.driver.press_keycode(AndroidKey.BACK)

    def press_enter(self):
        self.logger.info("Pressing Android enter key")
        self.driver.press_keycode(AndroidKey.ENTER)

    def press_home(self):
        self.logger.info("Pressing Android home button")
        self.driver.press_keycode(AndroidKey.HOME)

    def press_recent_apps(self):
        self.logger.info("Pressing Android recent apps button")
        self.driver.press_keycode(AndroidKey.APP_SWITCH)

    def press_volume_up(self):
        self.logger.info("Pressing volume up")
        self.driver.press_keycode(AndroidKey.VOLUME_UP)

    def press_volume_down(self):
        self.logger.info("Pressing volume down")
        self.driver.press_keycode(AndroidKey.VOLUME_DOWN)

    def press_keycode(self, keycode, metastate=None):
        self.logger.info(f"Pressing keycode: {keycode} metastate: {metastate}")

        if metastate is not None:
            self.driver.press_keycode(keycode, metastate)
        else:
            self.driver.press_keycode(keycode)

    # Device Controls
    # Methods for controlling device state and system panels.
    def lock_device(self, seconds=None):
        self.logger.info("Locking device")

        if seconds:
            self.driver.lock(seconds)
        else:
            self.driver.lock()

    def unlock_device(self):
        self.logger.info("Unlocking device")
        self.driver.unlock()

    def is_device_locked(self):
        self.logger.info("Checking if device is locked")
        return self.driver.is_locked()

    def open_notifications(self):
        self.logger.info("Opening notification panel")
        self.driver.open_notifications()

    def get_battery_level(self):
        self.logger.info("Getting battery level")
        info = self.driver.execute_script("mobile: batteryInfo")
        return info.get("level")

    # Clipboard Utilities
    # Methods for reading and writing clipboard content.
    def set_clipboard_text(self, text):
        self.logger.info(f"Setting clipboard text: {text}")
        self.driver.set_clipboard_text(text)

    def get_clipboard_text(self):
        self.logger.info("Getting clipboard text")
        return self.driver.get_clipboard_text()
    
    # Keyboard Actions
    # Methods for interacting with the Android keyboard.
    def hide_keyboard(self):
        self.logger.info("Hiding keyboard")

        try:
            self.driver.hide_keyboard()
        except (
            TimeoutException,
            NoSuchElementException,
            StaleElementReferenceException
        ):
            self.logger.warning("Keyboard not visible or already hidden")

    def is_keyboard_shown(self):
        self.logger.info("Checking keyboard visibility")
        return self.driver.is_keyboard_shown()

    def press_keyboard_key(self, keycode):
        self.logger.info(f"Pressing keyboard keycode: {keycode}")
        self.driver.press_keycode(keycode)

    # Network Management
    # Methods for controlling network connectivity states.
    def set_network_connection(self, connection_type):
        self.logger.info(f"Setting network connection type: {connection_type}")
        self.driver.set_network_connection(connection_type)

    def get_network_connection(self):
        self.logger.info("Getting network connection type")
        return self.driver.network_connection

    def enable_wifi(self):
        self.logger.info("Enabling WiFi")
        self.driver.set_network_connection(6)

    def disable_wifi(self):
        self.logger.info("Disabling WiFi")
        self.driver.set_network_connection(4)

    def enable_airplane_mode(self):
        self.logger.info("Enabling airplane mode")
        self.driver.set_network_connection(1)

    def disable_airplane_mode(self):
        self.logger.info("Disabling airplane mode")
        self.driver.set_network_connection(6)

    # Permission Management
    # Methods for granting, revoking, and handling permissions.
    def grant_permission(self, permission, package=None):
        package = package or settings["appium"]["capabilities"]["appPackage"]
        self.logger.info(f"Granting permission: {permission} to {package}")

        self.driver.execute_script(
            "mobile: shell",
            {"command": "pm", "args": ["grant", package, permission]}
        )

    def revoke_permission(self, permission, package=None):
        package = package or settings["appium"]["capabilities"]["appPackage"]
        self.logger.info(f"Revoking permission: {permission} from {package}")

        self.driver.execute_script(
            "mobile: shell",
            {"command": "pm", "args": ["revoke", package, permission]}
        )

    def accept_permission_dialog(self):
        self.logger.info("Accepting system permission dialog")

        allow_locators = [
            (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"),
            (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button"),
            (AppiumBy.ID, "com.android.packageinstaller:id/permission_allow_button"),
            (AppiumBy.XPATH, '//android.widget.Button[@text="Allow"]'),
            (AppiumBy.XPATH, '//android.widget.Button[@text="ALLOW"]'),
        ]

        for locator in allow_locators:
            try:
                if self.click_if_present(locator):
                    return True
            except (
                    TimeoutException,
                    NoSuchElementException,
                    StaleElementReferenceException
                ):
                continue
        return False

    def deny_permission_dialog(self):
        self.logger.info("Denying system permission dialog")

        deny_locators = [
            (AppiumBy.ID, "com.android.permissioncontroller:id/permission_deny_button"),
            (AppiumBy.ID, "com.android.packageinstaller:id/permission_deny_button"),
            (AppiumBy.XPATH, '//android.widget.Button[@text="Deny"]'),
            (AppiumBy.XPATH, '//android.widget.Button[@text="DENY"]'),
        ]

        for locator in deny_locators:
            try:
                if self.click_if_present(locator):
                    return True
            except (
                    TimeoutException,
                    NoSuchElementException,
                    StaleElementReferenceException
                ):
                continue

        return False

    # Scroll Utilities
    # Methods for scrolling through mobile screens and lists.
    def scroll_to_text(self, text):
        self.logger.info(f"Scrolling to text: {text}")

        locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().text("{text}"))'
        )

        return self.find_present_element(locator)

    def scroll_to_description(self, description):
        self.logger.info(f"Scrolling to description: {description}")

        locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().description("{description}"))'
        )

        return self.find_present_element(locator)

    def scroll_to_resource_id(self, resource_id):
        self.logger.info(f"Scrolling to resource id: {resource_id}")

        locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().resourceId("{resource_id}"))'
        )

        return self.find_present_element(locator)

    def scroll_to_end(self, max_scrolls=10):
        self.logger.info("Scrolling to end of list")

        locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true)).scrollToEnd(10)'
        )

        try:
            self.find_present_element(locator)
        except Exception:
            for _ in range(max_scrolls):
                self.swipe_up()

    def scroll_to_beginning(self, max_scrolls=10):
        self.logger.info("Scrolling to beginning of list")

        locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true)).scrollToBeginning(10)'
        )

        try:
            self.find_present_element(locator)
        except Exception:
            for _ in range(max_scrolls):
                self.swipe_down()

    # Gesture Actions
    # Methods for performing advanced touch gestures.
    def double_tap(self, locator):
        self.logger.info(f"Double tapping on element: {locator}")

        element = self.find_present_element(locator)

        self.driver.execute_script(
            "mobile: doubleClickGesture",
            {"elementId": element.id}
        )

    def long_press(self, locator, duration=2):
        self.logger.info(f"Long pressing on element: {locator} for {duration}s")

        element = self.find_present_element(locator)

        actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))

        actions.pointer_action.move_to(element)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(duration)
        actions.pointer_action.release()

        actions.perform()

    def drag_and_drop(self, source_locator, target_locator):
        self.logger.info(f"Dragging from {source_locator} to {target_locator}")

        source = self.find_present_element(source_locator)
        target = self.find_present_element(target_locator)

        self.driver.execute_script(
            "mobile: dragGesture",
            {
                "startX": source.location["x"] + source.size["width"] // 2,
                "startY": source.location["y"] + source.size["height"] // 2,
                "endX": target.location["x"] + target.size["width"] // 2,
                "endY": target.location["y"] + target.size["height"] // 2,
                "speed": 1000,
            }
        )

    def drag_to_coordinates(self, locator, end_x, end_y, speed=1000):
        self.logger.info(f"Dragging element {locator} to ({end_x}, {end_y})")

        element = self.find_present_element(locator)

        self.driver.execute_script(
            "mobile: dragGesture",
            {
                "startX": element.location["x"] + element.size["width"] // 2,
                "startY": element.location["y"] + element.size["height"] // 2,
                "endX": end_x,
                "endY": end_y,
                "speed": speed,
            }
        )

    # Coordinate-Based Actions
    # Methods for direct screen interaction using coordinates.
    def tap_by_coordinates(self, x, y):
        self.logger.info(f"Tapping by coordinates: ({x}, {y})")

        self.driver.execute_script(
            "mobile: clickGesture",
            {"x": x, "y": y}
        )

    def tap_by_percentage(self, x_percent, y_percent):
        size = self.driver.get_window_size()

        x = int(size["width"] * x_percent)
        y = int(size["height"] * y_percent)

        self.logger.info(f"Tapping by percentage: ({x_percent}, {y_percent}) -> ({x}, {y})")

        self.driver.execute_script(
            "mobile: clickGesture",
            {"x": x, "y": y}
        )

    def long_press_by_coordinates(self, x, y, duration=2000):
        self.logger.info(f"Long pressing at ({x}, {y}) for {duration}ms")

        self.driver.execute_script(
            "mobile: longClickGesture",
            {"x": x, "y": y, "duration": duration}
        )

    def double_tap_by_coordinates(self, x, y):
        self.logger.info(f"Double tapping at ({x}, {y})")

        self.driver.execute_script(
            "mobile: doubleClickGesture",
            {"x": x, "y": y}
        )

    # Swipe Actions
    # Methods for performing directional swipe gestures.
    def swipe_by_coordinates(
        self,
        start_x,
        start_y,
        end_x,
        end_y,
        duration=800
    ):
        self.logger.info(
            f"Swiping from ({start_x}, {start_y}) "
            f"to ({end_x}, {end_y})"
        )

        self.driver.execute_script(
            "mobile: dragGesture",
            {
                "startX": start_x,
                "startY": start_y,
                "endX": end_x,
                "endY": end_y,
                "speed": 1000
            }
        )

    def swipe_up(self):
        self.logger.info("Swiping up")

        size = self.driver.get_window_size()

        self.swipe_by_coordinates(
            size["width"] // 2,
            int(size["height"] * 0.8),
            size["width"] // 2,
            int(size["height"] * 0.2),
        )

    def swipe_down(self):
        self.logger.info("Swiping down")

        size = self.driver.get_window_size()

        self.swipe_by_coordinates(
            size["width"] // 2,
            int(size["height"] * 0.2),
            size["width"] // 2,
            int(size["height"] * 0.8),
        )

    def swipe_left(self):
        self.logger.info("Swiping left")

        size = self.driver.get_window_size()

        self.swipe_by_coordinates(
            int(size["width"] * 0.8),
            size["height"] // 2,
            int(size["width"] * 0.2),
            size["height"] // 2,
        )

    def swipe_right(self):
        self.logger.info("Swiping right")

        size = self.driver.get_window_size()

        self.swipe_by_coordinates(
            int(size["width"] * 0.2),
            size["height"] // 2,
            int(size["width"] * 0.8),
            size["height"] // 2,
        )

    def swipe_on_element(self, locator, direction, percent=0.75, speed=800):
        self.logger.info(f"Swiping {direction} on element: {locator}")

        element = self.find_present_element(locator)

        self.driver.execute_script(
            "mobile: swipeGesture",
            {
                "elementId": element.id,
                "direction": direction,
                "percent": percent,
                "speed": speed,
            }
        )

    # Zoom Gestures
    # Methods for pinch and zoom interactions.
    def pinch_open(self, locator, scale=2.0, speed=750):
        self.logger.info(f"Pinching open on element: {locator}")

        element = self.find_present_element(locator)

        self.driver.execute_script(
            "mobile: pinchOpenGesture",
            {
                "elementId": element.id,
                "scale": scale,
                "speed": speed,
            }
        )

    def pinch_close(self, locator, scale=2.0, speed=750):
        self.logger.info(f"Pinching close on element: {locator}")

        element = self.find_present_element(locator)

        self.driver.execute_script(
            "mobile: pinchCloseGesture",
            {
                "elementId": element.id,
                "scale": scale,
                "speed": speed,
            }
        )

    # Android Element State Checks
    # Methods for validating Android-specific element states.
    def is_element_checked(self, locator):
        self.logger.info(f"Checking if element is checked: {locator}")
        return self.find_present_element(locator).get_attribute("checked") == "true"

    def is_element_focused(self, locator):
        self.logger.info(f"Checking if element is focused: {locator}")
        return self.find_present_element(locator).get_attribute("focused") == "true"

    def is_element_clickable(self, locator):
        self.logger.info(f"Checking if element is clickable: {locator}")
        return self.find_present_element(locator).get_attribute("clickable") == "true"

    def is_element_scrollable(self, locator):
        self.logger.info(f"Checking if element is scrollable: {locator}")
        return self.find_present_element(locator).get_attribute("scrollable") == "true"

    # Element Position Helpers
    # Methods for retrieving element coordinates and dimensions.
    def get_element_bounds(self, locator):
        self.logger.info(f"Getting bounds for element: {locator}")

        element = self.find_present_element(locator)

        return {
            "x": element.location["x"],
            "y": element.location["y"],
            "width": element.size["width"],
            "height": element.size["height"],
        }

    def get_element_center(self, locator):
        self.logger.info(f"Getting center coordinates of element: {locator}")

        element = self.find_present_element(locator)

        return (
            element.location["x"] + element.size["width"] // 2,
            element.location["y"] + element.size["height"] // 2,
        )

    # Alerts & Dialogs
    # Methods for interacting with system alerts and dialogs.
    def get_alert_text(self):
        self.logger.info("Getting alert dialog text")
        return self.driver.switch_to.alert.text

    def accept_alert(self):
        self.logger.info("Accepting alert dialog")
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        self.logger.info("Dismissing alert dialog")
        self.driver.switch_to.alert.dismiss()

    def get_dialog_text(self, locator=None):
        self.logger.info("Getting dialog text")

        if locator is None:
            locator = (AppiumBy.ID, "android:id/message")

        return self.get_text(locator)

    def click_dialog_positive_button(self):
        self.logger.info("Clicking dialog positive button")
        self.click((AppiumBy.ID, "android:id/button1"))

    def click_dialog_negative_button(self):
        self.logger.info("Clicking dialog negative button")
        self.click((AppiumBy.ID, "android:id/button2"))

    def click_dialog_neutral_button(self):
        self.logger.info("Clicking dialog neutral button")
        self.click((AppiumBy.ID, "android:id/button3"))

    # Toast & Snackbar Helpers
    # Methods for reading transient UI messages.
    def get_snackbar_text(self):
        self.logger.info("Getting Snackbar text")

        snackbar_locators = [
            (AppiumBy.ID, "com.google.android.material:id/snackbar_text"),
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.google.android.material:id/snackbar_text"]'),
        ]

        for locator in snackbar_locators:
            try:
                return self.get_text(locator)
            except (
                    TimeoutException,
                    NoSuchElementException,
                    StaleElementReferenceException
                ):
                continue

        return None

    def get_toast_message(self):
        self.logger.info("Getting toast message")

        locator = (AppiumBy.XPATH, "//android.widget.Toast")
        return self.get_text(locator)
    
    # Navigation & Deep Linking
    # Methods for opening deep links and launching activities.
    def open_deep_link(self, url, package=None):
        package = package or settings["appium"]["capabilities"]["appPackage"]
        self.logger.info(f"Opening deep link: {url}")

        self.driver.execute_script(
            "mobile: deepLink",
            {"url": url, "package": package}
        )

    def start_activity(self, app_package, app_activity, app_wait_activity=None):
        self.logger.info(f"Starting activity: {app_package}/{app_activity}")

        self.driver.start_activity(
            app_package,
            app_activity,
            app_wait_activity=app_wait_activity or app_activity
        )

    # ADB & File Operations
    # Methods for executing shell commands and transferring files.
    def send_adb_shell(self, command, args=None):
        self.logger.info(f"Executing ADB shell: {command}")
        return self.driver.execute_script(
            "mobile: shell",
            {"command": command, "args": args or []}
        )

    def push_file(self, destination_path, source_path):
        self.logger.info(f"Pushing file: {source_path} -> {destination_path}")

        with open(source_path, "rb") as f:
            import base64
            data = base64.b64encode(f.read()).decode("utf-8")

        self.driver.push_file(destination_path, data)

    def pull_file(self, device_path, local_path):
        self.logger.info(f"Pulling file: {device_path}")

        import base64
        data = self.driver.pull_file(device_path)

        with open(local_path, "wb") as f:
            f.write(base64.b64decode(data))

        return local_path

    # Context Management
    # Methods for switching between Native and WebView contexts.
    def get_contexts(self):
        self.logger.info("Getting contexts")
        return self.driver.contexts

    def get_current_context(self):
        self.logger.info("Getting current context")
        return self.driver.current_context

    def switch_to_context(self, context_name):
        self.logger.info(f"Switching to context: {context_name}")
        self.driver.switch_to.context(context_name)

    def switch_to_webview(self, index=0):
        self.logger.info("Switching to WEBVIEW")

        webviews = [c for c in self.driver.contexts if "WEBVIEW" in c]

        if not webviews:
            raise Exception("No WEBVIEW context found")

        target = webviews[index]
        self.driver.switch_to.context(target)
        return target

    def switch_to_native(self):
        self.logger.info("Switching to NATIVE_APP")
        self.driver.switch_to.context("NATIVE_APP")

    # Screenshots & Reporting
    # Methods for capturing screenshots for debugging and reports.
    def take_screenshot(self, name=None):
        screenshot_dir = settings["reporting"]["screenshot_folder"]
        os.makedirs(screenshot_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{name}_{timestamp}.png" if name else f"{timestamp}.png"
        filepath = os.path.join(screenshot_dir, filename)

        self.driver.save_screenshot(filepath)
        self.logger.info(f"Screenshot saved: {filepath}")
        return filepath

    def take_element_screenshot(self, locator, name=None):
        self.logger.info(f"Taking element screenshot: {locator}")

        screenshot_dir = settings["reporting"]["screenshot_folder"]
        os.makedirs(screenshot_dir, exist_ok=True)

        element = self.find_present_element(locator)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{name}_{timestamp}.png" if name else f"element_{timestamp}.png"
        filepath = os.path.join(screenshot_dir, filename)

        element.screenshot(filepath)
        return filepath

    # Android Wait Utilities
    # Methods for waiting on app and activity state changes.
    def wait_for_app_to_foreground(self, timeout=10):
        self.logger.info("Waiting for app foreground")

        package = settings["appium"]["capabilities"]["appPackage"]
        deadline = time.time() + timeout

        while time.time() < deadline:
            if self.driver.query_app_state(package) == 4:
                return True
            time.sleep(0.5)

        return False

    def wait_for_activity(self, activity, timeout=10):
        self.logger.info(f"Waiting for activity: {activity}")

        deadline = time.time() + timeout

        while time.time() < deadline:
            if self.driver.current_activity == activity:
                return True
            time.sleep(0.5)

        return False
    
    # Location Services
    # Methods for setting and retrieving device location.
    def set_mock_location(self, latitude, longitude, altitude=0):
        self.logger.info(f"Setting mock location: {latitude},{longitude}")
        self.driver.set_location(latitude, longitude, altitude)

    def get_current_location(self):
        self.logger.info("Getting current location")
        return self.driver.location

    def authenticate_with_biometric(self, match=True):
        self.logger.info(f"Simulating biometric auth: {match}")
        self.driver.finger_print(1 if match else 0)

    