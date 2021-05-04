import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import json

# Xpaths
xLinkedin = {
    'xEmail': '//input[@name="session_key"]',
    'xPass': '//input[@name="session_password"]',
    'xLogin': '//button[contains(.,"Sign in")]',
    'xProfile': '//div[@data-control-name="identity_welcome_message"]',
    'xCertName': '//input[@placeholder="Ex: Microsoft certified network associate security"]',
    'xCertOrg': '//input[@placeholder="Ex: Microsoft"]',
    'xCredId': '//input[@id="single-line-text-form-component-profileEditFormElement-CERTIFICATION-profileCertification-ACoAADI-i-oBZzsiExXBGep7oC4p5cgLkd4v7kE-1-licenseNumber"]',
    'xCredUrl': '//input[@id="single-line-text-form-component-profileEditFormElement-CERTIFICATION-profileCertification-ACoAADI-i-oBZzsiExXBGep7oC4p5cgLkd4v7kE-1-url"]',
    'xSave': '//button[contains(.,"Save")]'
}


class LinkedIn:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def login(self):
        emailField = driver.find_element_by_xpath(xLinkedin['xEmail'])
        emailField.send_keys(self.email)
        passwordField = driver.find_element_by_xpath(xLinkedin['xPass'])
        passwordField.send_keys(self.password)

        submitBtn = driver.find_element_by_xpath(xLinkedin['xLogin'])
        submitBtn.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, xLinkedin['xProfile']))).click()

    def addCertData(self, name, org, credId, credUrl):
        sleep(5)
        currentUrl = driver.current_url
        driver.get(currentUrl+'edit/forms/certification/new/')
        nameInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, xLinkedin['xCertName'])))
        nameInput.send_keys(name)
        orgInput = driver.find_element_by_xpath(xLinkedin['xCertOrg'])
        orgInput.send_keys(org)
        sleep(4)
        orgInput.send_keys(Keys.ARROW_DOWN + Keys.ENTER)
        credIdInput = driver.find_element_by_xpath(xLinkedin['xCredId'])
        credIdInput.send_keys(credId)
        credUrlInput = driver.find_element_by_xpath(xLinkedin['xCredUrl'])
        credUrlInput.send_keys(credUrl)
        driver.find_element_by_xpath(xLinkedin['xSave']).click()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add your certifications to your LinkedIn Profile")
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-c', '--coursera', type=bool,
                       help="Coursera certification", action='store_true')
    group.add_argument('-u', '--udemy', type=bool,
                       help="Udemy certification", action='store_true')

    args = parser.parse_args()

    # set org according to arguments
    if args.udemy:
        org = 'udemy'
    elif args.coursera:
        org = 'coursera'

    # Chrome environment setup
    opt = webdriver.ChromeOptions()
    opt.add_argument('--disable-gpu')
    opt.add_argument('--headless')
    driver = webdriver.Chrome(
        executable_path='LinkedIn-Certifications-Manager/chromedriver', options=opt)
    driver.get('https://linkedin.com')

    # Get LinkedIn login credentials
    data = json.load(open('LinkedIn-Certifications-Manager/credentials.json'))

    linkedIn = LinkedIn(data['linkedin']['email'],
                        data['linkedin']['password'])
    linkedIn.login()

    # Load course data
    courseData = json.load(open('LinkedIn-Certifications-Manager/data.json'))
    items = courseData[org]

    # Add certifications to linkedin
    for item in items:
        name = item['name']
        credId = item['url'].split('/')[-1]
        credUrl = item['url']
        linkedIn.addCertData(name=name, org=org,
                             credId=credId, credUrl=credUrl)
        print(f'Added: {name}')
    print('Completed!')
