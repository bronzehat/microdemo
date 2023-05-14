"""
This is conftest for Rate&Goods App testing.
Run the test with the command below:
    python -m pytest --junitxml=pytest.xml -s -v test_for_rg.py
        Here --junitxml creates an XML with the tests output to be parsed by Bamboo
"""
import os
import pytest
from appium import webdriver

PRODUCT_NAME = "Snickers super"


@pytest.fixture
def emulated_device(request):
    """
    Fixture of the chosen device
    :param request:
    :return:
    """
    desired_cap = {
        'deviceName': 'emulator-5554', # Emulated Pixel 3 API 29
        'platformName': 'Android',
        'appPackage': 'com.itrustore.ratengoods',
        'appActivity': 'com.itrustore.ratengoods.main.XMainActivity'
    }
    driver = webdriver.Remote(command_executor="http://localhost:4723/wd/hub", desired_capabilities=desired_cap)
    request.addfinalizer(driver.quit)
    return driver


@pytest.fixture
def browserstack_device(request):
    userName = os.getenv("BROWSERSTACK_USER")
    accessKey = os.getenv("BROWSERSTACK_KEY")
    desired_cap = {
        "build": "Python Android",
        'device': 'Google Pixel 3 XL',
        'os_version': '9.0',
        'name': 'Bstack-[Python] Sample Test',
        'browserstack.debug': True,
        'app': 'bs://link'  # Rate&Goods App
    }
    driver = webdriver.Remote(
        ''.join(
            ["http://", userName, ":", accessKey,
             "@hub-cloud.browserstack.com/wd/hub", desired_cap,
             ]
        )
    )
    request.addfinalizer(driver.quit)
    return driver
