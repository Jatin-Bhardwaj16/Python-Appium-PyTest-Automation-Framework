from appium.webdriver.common.appiumby import AppiumBy


class HomePageLocators:

    HOME_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[@text="API Demos"]')

    PAGE_TITLE = (AppiumBy.ID, "android:id/action_bar_title")

    ALL_MENU_ITEMS = (AppiumBy.XPATH, "//android.widget.TextView[@resource-id='android:id/text1']")

    NOTIFICATIONS_PANEL = (AppiumBy.ID, "com.android.systemui:id/notification_panel")

    BRIGHTNESS_SLIDER = (AppiumBy.ACCESSIBILITY_ID, "Display brightness")

   