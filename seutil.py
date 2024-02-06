"""Provides utility functions for Selenium automation on WhatsApp Web e.g., finding a button and click it.

Note: the choice of using CSS selector rather than XPath to find elements is for better speed, browser support, readability and specificity.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep


def create_chromedriver_options():
    """Set up ChromeDriver options to avoid 2nd login to WhatsApp Web with QR code each time for session persistence along with some extra configuration.
    
    Below you can see the Chrome cmd-line option that specifies the dir where user data (like profiles, settings, etc.) is stored - useful when you want to reuse an existing Chrome user profile, enabling you to persist settings, cookies, and other user-specific data between browser sessions.
    
    Note: "--headless=new" rather than just "--headlesss" for Chrome versions >= 109. Disable headless mode for demo purpose.

    Returns:
        Options: The Configured ChromeDriver options.
    """
    dir_path = os.getcwd()
    profile = os.path.join(dir_path, "profile", "wpp")
    ops = webdriver.ChromeOptions()
    ops.add_argument(f"user-data-dir={profile}")
    ops.add_argument("--start-maximized")
    ops.add_argument('--headless=new')
    ops.add_experimental_option('excludeSwitches', ['enable-logging'])
    ops.add_argument("--log-level=3") 
    # TODO: explore more option arguments to maximize speed and minimize resource usage.
    return ops


def open_whatsapp_web(user: list, msg=""):
    """Create a ChromeDriver with options and open WhatsApp Web in Chrome.
    
    Note: user[2] indicates user's mobile number.

    Args:
        user (list): User's details.
        msg (str, optional): text message to send to a contact. Defaults to "".

    Returns:
        WebDriver: A Chrome WebDriver object.
    """
    ops = create_chromedriver_options()
    link = f"https://web.whatsapp.com/send?phone={user[2]}&text={msg}"
    driver = webdriver.Chrome(options=ops)
    driver.get(link)
    return driver


def click_plus_btn_in_chat(driver):
    """Find the "+" button next to the message text box by its CSS selector and click it.

    Args:
        driver (WebDriver): The Chrome WebDriver object required.
    """
    plus_btn_selector = "#main > footer > div._2lSWV._3cjY2.copyable-area > div > span:nth-child(2) > div > div._2xy_p._1bAtO > div._1OT67 > div > div"
    # TODO: experiment with the wait time to improve speed.
    plus_btn = WebDriverWait(driver, 17).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, plus_btn_selector))
    )
    plus_btn.click()
    
    
def click_send_photo_btn(driver):
    """Find the "Photos & Videos" button by its CSS selector and click it.
    
    Note: increase sleep time for demo purposes. 

    Args:
        driver (WebDriver): The Chrome WebDriver object required
    """
    selector = "#app > div > div.two._1jJ70 > div._2QgSC > div._2Ts6i._2xAQV > span > div > span > div > div > div.g0rxnol2.thghmljt.p357zi0d.rjo8vgbg.ggj6brxn.f8m0rgwh.gfz4du6o.r7fjleex.bs7a17vp > div > div.O2_ew > div._3wFFT > div > div"
    # TODO: experiment with the wait time to improve speed.
    send_btn = WebDriverWait(driver, 17).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    send_btn.click()
    sleep(5)


def click_send_btn(driver):
    """Find the ">" (send) button by its CSS selector and click it.

    Note: increase sleep time for demo purposes. 
    
    Args:
        driver (WebDriver): The Chrome WebDriver object required
    """
    selector = "#main > footer > div._2lSWV._3cjY2.copyable-area > div > span:nth-child(2) > div > div._1VZX7 > div._2xy_p._3XKXx > button"
    # TODO: experiment with the wait time to improve speed.
    send_btn = WebDriverWait(driver, 17).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    send_btn.click()
    sleep(5)