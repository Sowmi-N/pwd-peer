from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import time
import sys

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://sowmi-n9491:pwd_usr@cluster0.r5tmqfw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Load variables
peer = client["pwd"]["peers"]

instance_peer = peer.find_one(
    {
        "instanceType": sys.argv[1]
    })
username = instance_peer["username"]
password = instance_peer["password"]

# Defining default options for chrome browser
options = Options()
options.binary_location = "/usr/bin/firefox-esr"

# Define service
service = Service("/usr/local/bin/geckodriver")

# Set firefox driver
driver = webdriver.Firefox(service=service, options=options)

# Global variables
to = 30 # Timeout
errors = [NoSuchElementException, ElementNotInteractableException]
wait = WebDriverWait(driver, timeout=to, poll_frequency=.9, ignored_exceptions=errors)
actions = ActionChains(driver)

# Implicit wait
driver.implicitly_wait(to)

# Create variable for docker login page

docker_login_url = "https://login.docker.com/u/login"
pwd_url = "https://labs.play-with-docker.com/"
docker_hub_url = "https://hub.docker.com"

def open_pwd_container():
    # Go to pwd
    old_instance_peer = client["pwd"]["peers"].find_one({"username": username, "password": password})
    cookies = old_instance_peer["cookies"]

    print("##### Getting cookies!    #####")
    print(cookies)
    driver.get(pwd_url)
    driver.delete_all_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    driver.get(old_instance_peer["instanceUrl"])

    print("Sleeping 10 seconds...")
    time.sleep(10)
    print("")

    print(driver.title)
    print(driver.current_url)
    print("")
    input("waiting")

open_pwd_container()
