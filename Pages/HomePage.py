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

    def is_home_page_displayed(self):

        self.logger.info("Verifying ApiDemos home page")

        return self.is_element_visible(HomePageLocators.HOME_TITLE)

    def get_page_title(self):

        self.logger.info("Getting current page title")

        page_title_visible = self.is_element_visible(HomePageLocators.PAGE_TITLE)

        if page_title_visible:
            return self.get_text(HomePageLocators.PAGE_TITLE)

        return self.get_text(HomePageLocators.HOME_TITLE)

    def get_all_menu_items(self):

        self.logger.info("Getting all menu items from ApiDemos home screen")

        elements = self.find_visible_elements(HomePageLocators.ALL_MENU_ITEMS)

        menu_items = []

        for element in elements:
            menu_items.append(element.text)

        return menu_items

    def validate_all_menu_items_navigation(self):

        self.logger.info("Validating all menu item navigation")

        menu_names = []

        total_items = len(
            self.find_visible_elements(HomePageLocators.ALL_MENU_ITEMS))

        for index in range(total_items):

            menu_items = self.find_visible_elements(HomePageLocators.ALL_MENU_ITEMS)

            current_item = menu_items[index]

            menu_text = current_item.text

            self.logger.info(f"Opening menu: {menu_text}")

            current_item.click()

            # simple validation
            assert self.driver.current_activity is not None

            menu_names.append(menu_text)

            self.press_back()

        return menu_names
    
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

    def open_notifications_panel(self):

        self.logger.info("Opening notification panel")

        self.open_notifications()

        return self.is_element_visible(HomePageLocators.NOTIFICATIONS_PANEL)

    def open_full_notifications_panel(self):

        self.logger.info("Opening full notification panel")

        self.open_notifications()

        self.swipe_down()

        return self.is_element_visible(HomePageLocators.BRIGHTNESS_SLIDER)

    def close_full_notifications_panel(self):

        self.logger.info("Closing full notification panel")

        self.open_notifications()

        self.swipe_down()

        self.swipe_up()

        return not self.is_element_visible(HomePageLocators.BRIGHTNESS_SLIDER)



        
        





        