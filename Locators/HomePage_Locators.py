from appium.webdriver.common.appiumby import AppiumBy


class HomePageLocators:

    HOME_TITLE_LOCATOR = (AppiumBy.XPATH, '//android.widget.TextView[@text="API Demos"]')

    PAGE_TITLE_LOCATOR = (AppiumBy.ID, "android:id/action_bar_title")

    ALL_MENU_ITEMS_LOCATOR = (AppiumBy.XPATH, "//android.widget.TextView[@resource-id='android:id/text1']")

    NOTIFICATIONS_PANEL_LOCATOR = (AppiumBy.ID, "com.android.systemui:id/notification_panel")

    BRIGHTNESS_SLIDER_LOCATOR = (AppiumBy.ACCESSIBILITY_ID, "Display brightness")

    BRIGHTNESS_SEEKBAR_LOCATOR = (AppiumBy.ID, "com.android.systemui:id/slider")

    PREFERENCE_LOCATOR = (AppiumBy.ACCESSIBILITY_ID, "Preference")
    
    PREFERENCE_DEPENDENCIES_LOCATOR = (AppiumBy.ACCESSIBILITY_ID, "3. Preference dependencies")

    PREFERENCE_WIFI_CHECKBOX_LOCATOR = (AppiumBy.ID, "android:id/checkbox")

    PREFERENCE_WIFI_SETTINGS_LOCATOR = (AppiumBy.XPATH, "//android.widget.ListView[@resource-id='android:id/list']/android.widget.LinearLayout[2]/android.widget.RelativeLayout")

    PREFERENCE_WIFI_EDIT_LOCATOR = (AppiumBy.ID, "android:id/edit")

    PREFERENCE_OK_BUTTON_LOCATOR = (AppiumBy.ID, "android:id/button1")

    VIEWS_LOCATOR = (AppiumBy.ACCESSIBILITY_ID, "Views")

    EXPANDABLE_LISTS_LOCATOR = (AppiumBy.ACCESSIBILITY_ID, "Expandable Lists")

    CUSTOM_ADAPTER_LOCATOR = (AppiumBy.ACCESSIBILITY_ID, "1. Custom Adapter")

    PEOPLE_NAMES_LOCATOR = (AppiumBy.XPATH, "//android.widget.TextView[@text='People Names']")

    ARNOLD_NAME_LOCATOR = (AppiumBy.XPATH, "//android.widget.TextView[@text='Arnold']")

    SAMPLE_MENU_LOCATOR = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Sample menu")')

    SAMPLE_ACTION_LOCATOR = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Sample action")')

    DATE_WIDGETS_LOCATOR = (AppiumBy.ACCESSIBILITY_ID, "Date Widgets")

    INLINE_LOCATOR = (AppiumBy.ACCESSIBILITY_ID, "2. Inline")

    CLOCK_DIAL_LOCATOR = (AppiumBy.CLASS_NAME, "android.widget.RadialTimePickerView")

    DRAG_AND_DROP_LOCATOR = (AppiumBy.ACCESSIBILITY_ID, "Drag and Drop")

    DRAG_DOT_1_LOCATOR = (AppiumBy.ID, "io.appium.android.apis:id/drag_dot_1")

    DRAG_DOT_2_LOCATOR = (AppiumBy.ID, "io.appium.android.apis:id/drag_dot_2")

    DRAG_DOT_3_LOCATOR = (AppiumBy.ID, "io.appium.android.apis:id/drag_dot_3")

    DRAG_RESULT_TEXT_LOCATOR = (AppiumBy.ID, "io.appium.android.apis:id/drag_result_text")
