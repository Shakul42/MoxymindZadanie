
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # To include parent dir in import

from env_settings import username, password
from playwright.sync_api import Page, sync_playwright, expect


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    # Before each test
    page.goto("https://www.saucedemo.com/")
    yield
    # After each test
    page.close()


# 0th TC Scenario: Press Login button with Empty credentials
# COMMENT: This TC scenario is not important, that's why it has assigned number 0, 
#       but to find out if the correct message is displayed even with empty fields 
def test_empty_credentials(page: Page):
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_have_text("Epic sadface: Username is required")

# 1st TC Scenario: Press Login button with only Correct User filled
# COMMENT: This TC scenario is essential because it checks that user is guided
#       with message to fill password too and is not allowed to login with 
#       only Username filled which would be security violation
def test_only_username(page: Page):
    page.fill('[data-test=\"username\"]', username)   # Using diferent "style" of fill than further
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_have_text("Epic sadface: Password is required")
    expect(page).not_to_have_url("https://www.saucedemo.com/inventory.html")

# 2nd TC Scenario: Press Login button with only Correct Password filled
# COMMENT: This TC scenario is essential because it checks that user is guided
#       with message to fill username field too and is not allowed to login  
#       with only Password filled which would be security violation
def test_only_password(page: Page):
    # page.goto("https://www.saucedemo.com/") # Refreshing page to empty all fields # COMMENT: This line is not needed because of before_each_after_each fixture
    page.locator("[data-test=\"password\"]").fill(password)
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_have_text("Epic sadface: Username is required")
    expect(page).not_to_have_url("https://www.saucedemo.com/inventory.html")

# 3rd TC Scenario: Press Login button with Incorrect credentials
# COMMENT: This TC scenario is essential because it checks that user is NOT
#       logged in using Incorrect credentials which would be security violation
def test_incorrect_credentials(page: Page):
    page.locator("[data-test=\"password\"]").fill(password)
    page.locator("[data-test=\"password\"]").click()    # Doesn't make sense to click, just to simulate how would user do it
    page.locator("[data-test=\"username\"]").fill("S@djm0k_42")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_have_text("Epic sadface: Username and password do not match any user in this service")
    expect(page).not_to_have_url("https://www.saucedemo.com/inventory.html")

"""     # COMMENT: Following section is not needed because of before_each_after_each fixture
    # Removing content of filled username and password /Alternative to reloading page
    page.locator("[data-test=\"username\"]").clear()    # Empty editbox using clear()
    page.locator("[data-test=\"password\"]").click()
    page.locator("[data-test=\"password\"]").press("ControlOrMeta+a") # Select all text
    page.locator("[data-test=\"password\"]").fill("") """

# 4th TC Scenario: Press Login button with Correct credentials
# COMMENT: This TC scenario is very important because it checks main 
#       functionality that user is logged in with correct credentials
def test_correct_credentials(page: Page):
    page.locator("[data-test=\"password\"]").click()
    page.locator("[data-test=\"password\"]").fill(password)
    page.locator("[data-test=\"username\"]").click()
    page.locator("[data-test=\"username\"]").fill(username)
    page.locator("[data-test=\"login-button\"]").click()
    # Testinng of successful login by checking header, URL and Logout button in side menu 
    expect(page.locator("[data-test=\"primary-header\"]")).to_contain_text("Swag Labs")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    page.get_by_role("button", name="Open Menu").click()
    expect(page.locator("[data-test=\"logout-sidebar-link\"]")).to_contain_text("Logout")
