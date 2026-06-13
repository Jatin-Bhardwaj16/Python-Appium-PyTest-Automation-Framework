from Pages.Android_BasePage import AndroidBasePage
from Locators.HomePage_Locators import HomePageLocators
from config.settings import settings


class HomePage(AndroidBasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def device_info_check(self):

        self.logger.info("Checking device information")

        device_info = self.get_device_info()

        return device_info
    
    def open_notifications_panel(self):

        self.logger.info("Opening notification panel")

        self.open_notifications()

        return self.is_element_visible(HomePageLocators.NOTIFICATIONS_PANEL_LOCATOR)

    def open_full_notifications_panel(self):

        self.logger.info("Opening full notification panel")

        self.open_notifications()

        self.sleep(2)

        self.swipe_down()

        self.sleep(2)

        print(self.driver.page_source)

        return self.is_element_visible(HomePageLocators.BRIGHTNESS_SLIDER_LOCATOR)

    def close_full_notifications_panel(self):

        self.logger.info("Closing full notification panel")

        self.open_notifications()

        self.swipe_down()

        self.swipe_up()

        self.press_back()

        return not self.is_element_visible(HomePageLocators.BRIGHTNESS_SLIDER_LOCATOR)
    
    def get_brightness_value(self):

        self.logger.info("Checking brightness slider presence in notification panel")

        self.open_full_notifications_panel()

        value = self.get_attribute(HomePageLocators.BRIGHTNESS_SEEKBAR_LOCATOR,"text")

        self.logger.info(f"Brightness value: {value}")
    
        return value 
    
    def set_brightness_level(self, percentage):

        percentage = max(0, min(100, percentage))

        print(self.driver.page_source)

        bounds = self.get_element_bounds(HomePageLocators.BRIGHTNESS_SEEKBAR_LOCATOR)

        target_x = bounds["x"] + int(
            bounds["width"] * percentage / 100
        )

        target_y = bounds["y"] + bounds["height"] // 2

        self.drag_to_coordinates(
            HomePageLocators.BRIGHTNESS_SEEKBAR_LOCATOR,
            target_x,
            target_y
        )

        return True

    def validate_brightness_functionality(self, target_percentage=80):

        self.logger.info("Validating brightness functionality")

        panel_opened = self.open_full_notifications_panel()

        if not panel_opened:
            self.logger.error("Brightness slider not visible after opening full notification panel")

            return {
                "panel_opened": False,
                "brightness_set": False,
                "panel_closed": False
            }

        brightness_set = self.set_brightness_level(target_percentage)

        panel_closed = self.close_full_notifications_panel()

        return {
            "panel_opened": panel_opened,
            "brightness_set": brightness_set,
            "panel_closed": panel_closed
        }

    def app_installation_check(self):

        self.logger.info("Checking if the app is installed")

        package = settings["appium"]["capabilities"]["appPackage"]

        is_installed = self.is_app_installed()

        if is_installed:
            self.logger.info(f"App with package '{package}' is already installed.")

        else:
            self.logger.warning(f"App with package '{package}' is not installed.")

        return is_installed

    def load_app(self):

        self.logger.info("Loading the app")

        self.activate_app()

        return self.is_home_page_displayed()

    def get_package_activity_version_state(self):

        package = self.get_current_package()

        activity = self.get_current_activity()

        app_version = self.get_app_version()

        app_state = self.get_app_state()

        self.logger.info(
            f"Current package: {package}, "
            f"Current activity: {activity}, "
            f"App version: {app_version}, "
            f"App state: {app_state}"
        )

        return package, activity, app_version, app_state
    
    def restart_the_app(self):

        self.logger.info("Restarting the app")

        self.restart_app()

        return self.is_home_page_displayed()

    def background_app_for_seconds(self, seconds):

        self.logger.info(f"Backgrounding the app for {seconds} seconds")

        self.background_app(seconds)

        return self.is_home_page_displayed()

    def terminate_app_and_verify(self):

        self.logger.info("Terminating the app and verifying it's closed")

        package = settings["appium"]["capabilities"]["appPackage"]

        self.terminate_app()

        current_package = self.driver.current_package

        is_closed = current_package != package

        if is_closed:
            self.logger.info(
                f"App successfully terminated "
                f"(current package: {current_package})"
            )

        else:
            self.logger.warning(
                f"App may still be running "
                f"(current package: {current_package})"
            )

        app_state = self.get_app_state()
        self.logger.info(f"App state after termination: {app_state}")


        return app_state == 1 and is_closed

    def is_home_page_displayed(self):

        self.logger.info("Verifying ApiDemos home page")

        return self.is_element_visible(HomePageLocators.HOME_TITLE_LOCATOR)

    def get_page_title(self):

        self.logger.info("Getting current page title")

        page_title_visible = self.is_element_visible(HomePageLocators.PAGE_TITLE_LOCATOR)

        if page_title_visible:
            return self.get_text(HomePageLocators.PAGE_TITLE_LOCATOR)

        return self.get_text(HomePageLocators.HOME_TITLE_LOCATOR)

    def get_all_menu_items(self):

        self.logger.info("Getting all menu items from ApiDemos home screen")

        elements = self.find_visible_elements(HomePageLocators.ALL_MENU_ITEMS_LOCATOR)

        menu_items = []

        for element in elements:
            menu_items.append(element.text)

        return menu_items

    def validate_all_menu_items_navigation(self):

        self.logger.info("Validating all menu item navigation")

        menu_names = []

        total_items = len(
            self.find_visible_elements(HomePageLocators.ALL_MENU_ITEMS_LOCATOR))

        for index in range(total_items):

            menu_items = self.find_visible_elements(HomePageLocators.ALL_MENU_ITEMS_LOCATOR)

            current_item = menu_items[index]

            menu_text = current_item.text

            self.logger.info(f"Opening menu: {menu_text}")

            assert current_item.get_attribute("clickable") == "true"

            current_item.click()

            # simple validation
            assert self.driver.current_activity is not None

            menu_names.append(menu_text)

            self.press_back()

        return menu_names
    
    def navigate_to_preference(self):

        self.click(HomePageLocators.PREFERENCE_LOCATOR)
        self.click(HomePageLocators.PREFERENCE_DEPENDENCIES_LOCATOR)
        self.click(HomePageLocators.PREFERENCE_WIFI_CHECKBOX_LOCATOR)
        self.click(HomePageLocators.PREFERENCE_WIFI_SETTINGS_LOCATOR)

        self.clear_and_enter_text(HomePageLocators.PREFERENCE_WIFI_EDIT_LOCATOR, "TestWifi")

        wifi_name = self.get_text(HomePageLocators.PREFERENCE_WIFI_EDIT_LOCATOR)

        self.click(HomePageLocators.PREFERENCE_OK_BUTTON_LOCATOR)

        return wifi_name
    
    def navigate_to_expandable_lists(self):

        self.click(HomePageLocators.VIEWS_LOCATOR)
        self.click(HomePageLocators.EXPANDABLE_LISTS_LOCATOR)
        self.click(HomePageLocators.CUSTOM_ADAPTER_LOCATOR)

        self.click(HomePageLocators.PEOPLE_NAMES_LOCATOR)

        self.long_press(HomePageLocators.ARNOLD_NAME_LOCATOR)

        is_sample_menu_visible = self.is_element_visible(HomePageLocators.SAMPLE_MENU_LOCATOR)
        
        if is_sample_menu_visible:
            self.logger.info("Sample menu is visible after long press on Arnold, clicking on Sample action")

            self.click(HomePageLocators.SAMPLE_ACTION_LOCATOR)

            return True

        else:
            self.logger.warning("Sample menu is NOT visible after long press on Arnold")

            return False
        
    def navigate_to_date_widgets(self):

        self.click(HomePageLocators.VIEWS_LOCATOR)
        self.click(HomePageLocators.DATE_WIDGETS_LOCATOR)
        self.click(HomePageLocators.INLINE_LOCATOR)

        screen_size = self.driver.get_window_size()

        center_y = int(screen_size["height"] * 0.37)
        start_x = int(screen_size["width"] * 0.31)
        end_x = int(screen_size["width"] * 0.69)

        self.swipe_by_coordinates(
            start_x,
            center_y,
            end_x,
            center_y
        )

        return True
    
    def navigate_to_drag_and_drop(self):

        self.click(HomePageLocators.VIEWS_LOCATOR)
        self.click(HomePageLocators.DRAG_AND_DROP_LOCATOR)

        self.drag_and_drop(HomePageLocators.DRAG_DOT_1_LOCATOR, HomePageLocators.DRAG_DOT_2_LOCATOR)

        result_text = self.get_text(HomePageLocators.DRAG_RESULT_TEXT_LOCATOR)

        self.logger.info(f"Drag and drop result text: {result_text}")

        return result_text



        

        



    
    

    



        
        





        