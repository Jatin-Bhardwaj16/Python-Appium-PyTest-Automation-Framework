import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)

from config.settings import settings
from utils.logger import get_logger


class CoreBasePage:

    # Initialization and common utilities for all pages
    def __init__(self, driver, timeout=None):
        self.driver = driver
        timeout = timeout or settings["timeouts"]["explicitWait"]
        self.wait = WebDriverWait(driver, timeout, ignored_exceptions=(StaleElementReferenceException,))
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info("CoreBasePage initialized")

    #wait helper for fixed sleep (use sparingly)
    def sleep(self, seconds):
        self.logger.info(f"Sleeping for {seconds} seconds")
        time.sleep(seconds)

    # Page Source Helpers 
    # Methods for retrieving and validating page source content.
    def get_page_source(self):
        self.logger.info("Getting page source")
        return self.driver.page_source

    def page_source_contains(self, text):
        self.logger.info(f"Checking page source for text: '{text}'")
        return text in self.driver.page_source

    # Element Finders and Actions
    # Methods for locating single or multiple elements.
    def find_present_element(self, locator):
        self.logger.info(f"Finding present element: {locator}")

        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException as e:
            msg = (f"Element not present in DOM after timeout: {locator}")
            self.logger.error(msg)
            raise TimeoutException(msg) from e

    def find_visible_element(self, locator):
        self.logger.info(f"Finding visible element: {locator}")

        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException as e:
            msg = (f"Element not visible after timeout: {locator}")
            self.logger.error(msg)
            raise TimeoutException(msg) from e

    def find_clickable_element(self, locator):
        self.logger.info(f"Finding clickable element: {locator}")

        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException as e:
            msg = (f"Element not clickable after timeout: {locator}")
            self.logger.error(msg)
            raise TimeoutException(msg) from e

    def find_present_elements(self, locator):
        self.logger.info(f"Finding present elements: {locator}")

        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException as e:
            msg = (f"No elements present in DOM after timeout: {locator}")
            self.logger.error(msg)
            raise TimeoutException(msg) from e

    def find_visible_elements(self, locator):
        self.logger.info(f"Finding visible elements: {locator}")

        try:
            return self.wait.until(EC.visibility_of_all_elements_located(locator))
        except TimeoutException as e:
            msg = (f"No visible elements found after timeout: {locator}")
            self.logger.error(msg)
            raise TimeoutException(msg) from e

    # Element State Checks
    # Methods for verifying presence, visibility, enabled state, and selection state of elements.
    def is_element_present(self, locator):
        self.logger.info(f"Checking if element is present: {locator}")

        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_visible(self, locator):
        self.logger.info(f"Checking if element is visible: {locator}")

        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_absent(self, locator):
        self.logger.info(f"Checking if element is absent: {locator}")

        return len(self.driver.find_elements(*locator)) == 0
    
    def is_element_enabled(self, locator):
        self.logger.info(f"Checking if element is enabled: {locator}")
        return self.find_present_element(locator).is_enabled()
    
    def is_element_selected(self, locator):
        self.logger.info(f"Checking if element is selected: {locator}")
        return self.find_present_element(locator).is_selected()

    # Text & Attribute Helpers
    # Methods for reading text, values, and element attributes.
    def get_text(self, locator):
        self.logger.info(f"Getting text from element: {locator}")
        return self.find_visible_element(locator).text.strip()

    def get_texts(self, locator):
        self.logger.info(f"Getting text from all elements: {locator}")

        return [
            el.text.strip()
            for el in self.find_visible_elements(locator)
        ]
    
    def get_attribute(self, locator, attribute):
        self.logger.info(f"Getting attribute '{attribute}' from element: {locator}")

        element = self.find_present_element(locator)
        return element.get_attribute(attribute)

    def get_hint_text(self, locator):
        hint = self.get_attribute(locator, "hint")
        return hint.strip() if hint else None

    # Text Verification Helpers
    # Methods for validating element text content.
    def element_contains_text(self, locator, expected_text):
        self.logger.info(f"Checking if element contains text '{expected_text}': {locator}")

        try:
            actual = self.get_text(locator)
            return expected_text in actual
        except (
            TimeoutException,
            NoSuchElementException,
            StaleElementReferenceException):
            return False

    def element_has_exact_text(self, locator, expected_text):
        self.logger.info(f"Checking if element has exact text '{expected_text}': {locator}")

        try:
            return self.get_text(locator) == expected_text
        except (
            TimeoutException,
            NoSuchElementException,
            StaleElementReferenceException):
            return False

    # Input Field Actions
    # Methods for entering, clearing, and updating text fields.
    def enter_text(self, locator, text):
        self.logger.info(f"Entering text '{text}' into element: {locator}")
        self.find_clickable_element(locator).send_keys(text)

    def clear_text(self, locator):
        self.logger.info(f"Clearing text in element: {locator}")
        self.find_clickable_element(locator).clear()

    def clear_and_enter_text(self, locator, text):
        self.logger.info(f"Clearing and entering text '{text}' into element: {locator}")

        element = self.find_clickable_element(locator)
        element.clear()
        element.send_keys(text)

    def get_input_value(self, locator):
        self.logger.info(f"Getting input value from element: {locator}")

        element = self.find_present_element(locator)
        value = element.get_attribute("value") or element.get_attribute("text")
        return value.strip() if value else ""

    # Click Actions
    # Methods for interacting with clickable elements.
    def click(self, locator):
        self.logger.info(f"Clicking element: {locator}")

        try:
            self.find_clickable_element(locator).click()
        except ElementClickInterceptedException:
            self.logger.warning(f"Click intercepted on {locator} — retrying once")

            element = self.find_clickable_element(locator)
            element.click()

    def click_if_present(self, locator):
        self.logger.info(f"Clicking element if present: {locator}")

        try:
            self.find_clickable_element(locator).click()
            return True
        except (TimeoutException, NoSuchElementException):
            self.logger.info(f"Element not present — skipping click: {locator}")
            return False
    
    # Wait Utilities
    # Methods for synchronizing tests with UI state changes.
    def wait_until(self, condition):
        return self.wait.until(condition)

    def wait_for_element_present(self, locator):
        return self.find_present_element(locator)

    def wait_for_element_visible(self, locator):
        return self.find_visible_element(locator)

    def wait_for_element_clickable(self, locator):
        return self.find_clickable_element(locator)

    def wait_for_element_to_disappear(self, locator):
        self.logger.info(f"Waiting for element to disappear: {locator}")

        try:
            return self.wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            self.logger.warning(f"Element still visible after timeout: {locator}")
            return False

    def wait_for_text_in_element(self, locator, text):
        self.logger.info(f"Waiting for text '{text}' in element: {locator}")

        try:
            return self.wait.until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            self.logger.warning(f"Text '{text}' not found in element after timeout: {locator}")
            return False

    def wait_for_exact_text_in_element(self, locator, text):
        self.logger.info(f"Waiting for exact text '{text}' in element: {locator}")

        def _exact_text(driver):
            try:
                element = driver.find_element(*locator)
                return element.text.strip() == text
            except (NoSuchElementException, StaleElementReferenceException):
                return False

        try:
            return self.wait.until(_exact_text)
        except TimeoutException:
            self.logger.warning(f"Exact text '{text}' never matched element after timeout: {locator}")
            return False

    def wait_for_attribute_value(self, locator, attribute, value):
        self.logger.info(f"Waiting for attribute '{attribute}' = '{value}' on {locator}")

        def _attr_matches(driver):
            try:
                el = driver.find_element(*locator)
                return el.get_attribute(attribute) == value
            except (NoSuchElementException, StaleElementReferenceException):
                return False

        try:
            return self.wait.until(_attr_matches)
        except TimeoutException:
            self.logger.warning(f"Attribute '{attribute}' never reached '{value}' after timeout: {locator}")
            return False

    # Element Collection Helpers
    # Methods for counting and validating collections of elements.
    def get_element_count(self, locator):
        self.logger.info(f"Counting elements: {locator}")

        try:
            return len(self.driver.find_elements(*locator))
        except (
            StaleElementReferenceException):
            return 0

    def wait_for_element_count(self, locator, expected_count):
        self.logger.info(f"Waiting for {expected_count} elements: {locator}")

        def _count_matches(driver):
            try:
                return len(driver.find_elements(*locator)) == expected_count
            except (
                StaleElementReferenceException):
                return False

        try:
            return self.wait.until(_count_matches)
        except TimeoutException:
            actual = self.get_element_count(locator)
            self.logger.warning(
                f"Expected {expected_count} elements but found {actual} "
                f"after timeout: {locator}")
            return False

    def wait_for_minimum_element_count(self, locator, min_count):
        self.logger.info(f"Waiting for at least {min_count} elements: {locator}")

        def _min_count(driver):
            try:
                return len(driver.find_elements(*locator)) >= min_count
            except (
                StaleElementReferenceException):
                return False

        try:
            return self.wait.until(_min_count)
        except TimeoutException:
            self.logger.warning(
                f"Minimum element count of {min_count} not reached after "
                f"timeout: {locator}")
            return False
        
    def wait_for_element_absent(self, locator):
        self.logger.info(f"Waiting for element to be absent: {locator}")

        def _element_absent(driver):
            return len(driver.find_elements(*locator)) == 0

        try:
            return self.wait.until(_element_absent)
        except TimeoutException:
            self.logger.warning(
                f"Element still present after "
                f"timeout: {locator}"
            )
            return False

    # Scrolling Helpers
    # Methods for bringing elements into the viewport.
    def scroll_element_into_view(self, locator):
        self.logger.info(f"Scrolling element into view: {locator}")

        element = self.find_present_element(locator)

        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

        return element
