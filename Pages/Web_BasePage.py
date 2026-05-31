from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from Pages.Core_BasePage import CoreBasePage


class WebBasePage(CoreBasePage):

    # ===== Initialization =====
    def __init__(self, driver, timeout=None):

        super().__init__(driver, timeout)

        self.actions = ActionChains(driver)

    # ===== Navigation =====
    def open(self, url):

        self.logger.info(f"Opening URL: {url}")

        self.driver.get(url)

    def refresh(self):

        self.logger.info("Refreshing page")

        self.driver.refresh()

    def go_back(self):

        self.logger.info("Navigating back")

        self.driver.back()

    def go_forward(self):

        self.logger.info("Navigating forward")

        self.driver.forward()

    def get_title(self):

        self.logger.info("Getting page title")

        return self.driver.title

    def get_current_url(self):

        self.logger.info("Getting current URL")

        return self.driver.current_url

    def get_page_source(self):

        self.logger.info("Getting page source")

        return self.driver.page_source

    # ===== Browser Window Handling =====
    def get_window_handle(self):

        self.logger.info("Getting current window handle")

        return self.driver.current_window_handle

    def get_window_handles(self):

        self.logger.info("Getting all window handles")

        return self.driver.window_handles

    def switch_to_window(self, window_handle):

        self.logger.info(f"Switching to window: {window_handle}")

        self.driver.switch_to.window(window_handle)

    def switch_to_new_window(self):

        self.logger.info("Switching to new window")

        handles = self.driver.window_handles

        self.driver.switch_to.window(handles[-1])

    def close_current_window(self):

        self.logger.info("Closing current window")

        self.driver.close()

    # ===== Frame Handling =====
    def switch_to_frame(self, locator):

        self.logger.info(f"Switching to frame: {locator}")

        frame = self.find_present_element(locator)

        self.driver.switch_to.frame(frame)

    def switch_to_parent_frame(self):

        self.logger.info("Switching to parent frame")

        self.driver.switch_to.parent_frame()

    def switch_to_default_content(self):

        self.logger.info(f"Switching to default content")

        self.driver.switch_to.default_content()

    # ===== JavaScript Actions =====
    def js_click(self, locator):

        self.logger.info(f"Performing JS click on: {locator}")

        element = self.find_present_element(locator)

        self.driver.execute_script("arguments[0].click();",element)

    def js_scroll_into_view(self, locator):

        self.logger.info(f"Scrolling element into view: {locator}")

        element = self.find_present_element(locator)

        self.driver.execute_script("arguments[0].scrollIntoView(true);",element)

    def execute_js(self, script, *args):

        self.logger.info(f"Executing JavaScript: {script}")

        return self.driver.execute_script(script, *args)

    # ===== Mouse Actions =====
    def hover(self, locator):

        self.logger.info(f"Hovering over element: {locator}")

        element = self.find_visible_element(locator)

        self.actions.move_to_element(element).perform()

    def double_click(self, locator):

        self.logger.info(f"Double clicking element: {locator}")

        element = self.find_clickable_element(locator)

        self.actions.double_click(element).perform()

    def right_click(self, locator):

        self.logger.info(f"Right clicking element: {locator}")

        element = self.find_clickable_element(locator)

        self.actions.context_click(element).perform()

    def drag_and_drop(self, source_locator, target_locator):

        self.logger.info(
            f"Dragging {source_locator} "
            f"to {target_locator}"
        )

        source = self.find_present_element(
            source_locator)

        target = self.find_present_element(
            target_locator)

        self.actions.drag_and_drop(
            source,
            target).perform()

    # ===== Scroll Actions =====
    def scroll_down(self, pixels=500):

        self.logger.info(f"Scrolling down by {pixels}px")

        self.driver.execute_script(f"window.scrollBy(0, {pixels});")

    def scroll_up(self, pixels=500):

        self.logger.info(f"Scrolling up by {pixels}px")

        self.driver.execute_script(f"window.scrollBy(0, -{pixels});")

    def scroll_to_top(self):

        self.logger.info("Scrolling to top")

        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):

        self.logger.info("Scrolling to bottom")

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # ===== Keyboard Actions =====
    def press_enter(self, locator):

        self.logger.info(f"Pressing ENTER on: {locator}")

        element = self.find_visible_element(locator)

        element.send_keys(Keys.ENTER)

    def press_tab(self, locator):

        self.logger.info(f"Pressing TAB on: {locator}")

        element = self.find_visible_element(locator)

        element.send_keys(Keys.TAB)

    # ===== Alerts =====
    def accept_alert(self):

        self.logger.info("Accepting alert")

        alert = self.driver.switch_to.alert

        alert.accept()

    def dismiss_alert(self):

        self.logger.info("Dismissing alert")

        alert = self.driver.switch_to.alert

        alert.dismiss()

    def get_alert_text(self):

        self.logger.info("Getting alert text")

        alert = self.driver.switch_to.alert

        return alert.text

    # ===== Shadow DOM =====
    def get_shadow_root(self, element):

        self.logger.info("Getting shadow root")

        return self.driver.execute_script("return arguments[0].shadowRoot",element)

    def find_shadow_element(self, shadow_path):

        self.logger.info(f"Finding shadow element: {shadow_path}")

        element = self.find_present_element(shadow_path[0])

        shadow_root = self.get_shadow_root(element)

        for locator in shadow_path[1:-1]:

            element = shadow_root.find_element(*locator)

            shadow_root = self.get_shadow_root(element)

        return shadow_root.find_element(*shadow_path[-1])