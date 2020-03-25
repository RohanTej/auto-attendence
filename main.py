from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from os import path
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pickle
import datetime


def get_credentials():
    print("Loading credentials...")
    if not path.exists("credentials.p"):
        username = input("Enter your Registration no.: ")
        password = input("Enter your password: ")
        pickle.dump({'username': username, 'password': password}, open("credentials.p", "wb"))
        return username, password
    credentials = pickle.load(open("credentials.p", "rb"))
    return credentials['username'], credentials['password']

def change_password(driver, username, password):
    print("Changing password...")
    def login(username, password):
        driver.get("https://ums.lpu.in/lpuums/")
        driver.find_element_by_class_name("input_type").send_keys(username)
        driver.find_element_by_class_name("login_box").click()
        driver.find_element_by_class_name("input_type_pass").send_keys(password)
        Select(driver.find_element_by_id("ddlStartWith")).select_by_index(1)
        driver.find_element_by_id("iBtnLogins").click()

    def update_password(old_password, new_password):
        driver.get("https://ums.lpu.in/lpuums/frmchangepassword.aspx")
        driver.find_element_by_id("txtOldPassword").send_keys(old_password)
        driver.find_element_by_id("txtNewPassword").send_keys(new_password)
        driver.find_element_by_id("txtConfirmPassword").send_keys(new_password)
        driver.find_element_by_id("btnUpdate").click()
        
        # dismiss alert
        driver.switch_to.alert.accept()
        time.sleep(5)

    try:
        # change password to a placeholder password
        login(username, password)

        temp_password = "SomeThingStrongWith123&)(*"
        update_password(password, temp_password)

        # change password back to original
        login(username, temp_password)
        update_password(temp_password, password)
    except Exception as e:
        print(e)
        

if __name__ == "__main__":
    driver = webdriver.Chrome(executable_path="./chromedriver")
    try:
        username, password = get_credentials()
        change_password(driver, username, password)

    except Exception as e:
        print(e)
    finally:
        driver.close()
