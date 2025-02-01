import time
import os
from appium import webdriver
from collections import deque

def create_driver(app_path=None):
    desired_caps = {
        "platformName": "Android",
        "deviceName": "Android Emulator",
        "automationName": "UiAutomator2",
    }
    if app_path:
        desired_caps["app"] = app_path
    # If already installed:
    # desired_caps["appPackage"] = "com.my.mentalhealth.app"
    # desired_caps["appActivity"] = "com.my.mentalhealth.app.MainActivity"

    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
    return driver

def bfs_explore(driver, screenshot_dir="screenshots"):
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    visited = set()
    queue = deque()

    # Let app load
    time.sleep(5)
    start_state = driver.page_source
    queue.append(start_state)
    visited.add(start_state)

    screen_count = 0
    while queue:
        current_state = queue.popleft()

        # Save a screenshot
        screenshot_path = os.path.join(screenshot_dir, f"screen_{screen_count}.png")
        driver.save_screenshot(screenshot_path)
        screen_count += 1

        # Find clickable elements
        clickable_elems = driver.find_elements_by_android_uiautomator(
            'new UiSelector().clickable(true)'
        )

        for elem in clickable_elems:
            try:
                elem.click()
                time.sleep(2)
                new_state = driver.page_source
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append(new_state)
                # Go back
                driver.back()
                time.sleep(1)
            except Exception as e:
                print("Error clicking element:", e)

if __name__ == "__main__":
    app_path = r"C:\path\to\mentalhealth.apk"  # or None if installed
    driver = create_driver(app_path=app_path)
    bfs_explore(driver)
    driver.quit()
