# Python Appium PyTest Automation Framework

A scalable and maintainable mobile automation framework built using **Python**, **Appium**, **PyTest**, and the **Page Object Model (POM)** design pattern.

This framework is designed for Android mobile application testing and includes reusable utilities, reporting, logging, configuration management, and robust page abstractions.

---

## Features

* Appium-based Android automation
* PyTest test execution and fixtures
* Page Object Model (POM) architecture
* Explicit waits and reusable base page methods
* Android-specific utility methods
* HTML and JUnit XML reporting
* Structured logging
* Config-driven test execution
* Screenshot capture support
* Easy framework scalability

---

## Tech Stack

| Technology                     | Purpose              |
| ------------------------------ | -------------------- |
| Python                         | Programming Language |
| Appium                         | Mobile Automation    |
| PyTest                         | Test Framework       |
| Selenium                       | WebDriver Support    |
| Android Emulator / Real Device | Test Execution       |
| pytest-html                    | HTML Reporting       |
| Logging                        | Execution Logs       |

---

## Project Structure

```text
Python-Appium-PyTest-Automation-Framework
│
├── config/
│   └── settings.py
│
├── Locators/
│   └── HomePage_Locators.py
│
├── Logs/
│
├── Pages/
│   ├── Core_BasePage.py
│   ├── Android_BasePage.py
│   └── HomePage.py
│
├── Reports/
│   ├── html/
│   └── junit/
│
├── Screenshots/
│
├── Tests/
│   └── test_home_page.py
│
├── utils/
│   └── logger.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Framework Architecture

### CoreBasePage

Contains reusable Selenium/Appium actions:

* Element finders
* Wait utilities
* Text operations
* Click actions
* Input actions
* Validation helpers
* Scrolling utilities

### AndroidBasePage

Extends CoreBasePage with Android-specific functionality:

* App lifecycle management
* Device controls
* Android key actions
* Gestures and swipes
* Permission handling
* Notifications handling
* Context switching
* Deep linking
* Screenshot utilities
* Biometric simulation

### Page Objects

Each application screen is represented by a dedicated Page Object containing:

* Locators
* Page-specific actions
* Business workflows
* Assertions

---

## Prerequisites

Install:

* Python 3.10+
* Appium Server
* Android Studio
* Android SDK
* Java JDK
* Node.js

Verify installation:

```bash
python --version
appium --version
adb devices
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Jatin-Bhardwaj16/Python-Appium-PyTest-Automation-Framework.git

cd Python-Appium-PyTest-Automation-Framework
```

### Create Virtual Environment

```bash
python3 -m venv venv
```

Activate:

macOS/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Device

Update desired capabilities in:

```text
config/settings.py
```

Example:

```python
"capabilities": {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "Android Emulator",
    "appPackage": "io.appium.android.apis",
    "appActivity": ".ApiDemos"
}
```

---

## Start Appium Server

```bash
appium
```

Verify:

```bash
adb devices
```

---

## Execute Tests

Run all tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run specific test file:

```bash
pytest Tests/test_home_page.py
```

Run specific test:

```bash
pytest Tests/test_home_page.py::test_device_info_check
```

Run tests by marker:

```bash
pytest -m smoke
```

---

## Reporting

### HTML Report

Generated under:

```text
Reports/html/
```

Open:

```bash
open Reports/html/report.html
```

### JUnit Report

Generated under:

```text
Reports/junit/
```

Useful for CI/CD integrations.

---

## Logging

Execution logs are generated under:

```text
Logs/
```

Example:

```text
2026-05-31 17:21:59 | INFO | main | HomePage | Swiping up
2026-05-31 17:22:01 | INFO | main | HomePage | Checking if element is visible
```

---

## Current Test Coverage

### Home Page Tests

* Device Information Validation
* App Installation Verification
* App Launch Validation
* App State Verification
* Home Page Validation
* Menu Navigation Validation
* App Restart Validation
* App Background Validation
* App Termination Validation
* Notification Panel Validation

---

## Best Practices Followed

* Page Object Model (POM)
* Single Responsibility Principle
* Reusable Components
* Explicit Wait Strategy
* Centralized Configuration
* Structured Logging
* Maintainable Test Design

---

## Future Enhancements

* iOS Support
* Parallel Execution
* Allure Reporting
* GitHub Actions CI/CD
* Device Farm Integration
* Data-Driven Testing
* API Integration Layer

---

## Author

Jatin Bhardwaj

GitHub:
https://github.com/Jatin-Bhardwaj16

---

## License

This project is intended for learning, demonstration, and automation framework development purposes.
