from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from selenium.webdriver.chrome.options import Options

class scraper_base:
    def __init__(self, headless=True):
        dirname = os.path.dirname(__file__)
        print(dirname)

        #### make sure you have the right versions here

        phantomjs_path = os.path.join(dirname, "phantomjs-2.1.1-macosx/bin/phantomjs")
        chromedriver_path = os.path.join(dirname, "chromedriver")

        ###############################################

        if headless:
            options = Options()
            options.headless = True
            browser = webdriver.Chrome(chromedriver_path, chrome_options=options)
        else:
            browser = webdriver.Chrome(executable_path=chromedriver_path)
            browser.set_window_size(1124, 850)

        self.browser = browser

    def getPage(self, pageURL):
        return self.browser.get(pageURL)

    ## take 1 for trying to wait for the loading to finish
    def wait_for_element(self, delay, xpath):
        try:
            WebDriverWait(self.browser, delay).until(
                EC.presence_of_element_located(self.browser.find_elements_by_xpath(xpath))
            )
            print("Page Ready!")
        except TimeoutException:
            print("Couldn't load page")

    def getXpath(self, section, name, value, specifics=""):
        xpathString = "//" + section + "[@" + name + "='" + value + "']" + specifics
        return xpathString

    def getElements(self, xpath):
        elements = self.browser.find_elements_by_xpath(xpath)
        return elements

    def getElement(self, xpath):
        element = self.browser.find_element_by_xpath(xpath)
        return element

    def sendKeys(self, section, name, value, keyToSend, specifics=""):
        xpath = self.getXpath(section, name, value, specifics)
        element = self.getElement(xpath)
        element.send_keys(keyToSend)

    def click(self, text):
        self.browser.find_element_by_link_text(text).click()

    def pressButton(self, section, name, value, specifics=""):
        xpath = self.getXpath(section, name, value, specifics)
        button = self.getElement(xpath)
        print(button.text)
        button.click()

    def getNonRepeatedName(self):
        full, first, middle, last, dob = self.getName()
        self.currentName = full
        if self.currentName == self.previousName:
            full, first, middle, last, dob = self.getNonRepeatedName()
            return full, first, middle, last, dob

        else:
            self.previousName = self.currentName
            return full, first, middle, last, dob

    def getName(self):
        count = 0
        with open(self.copyFile, "r") as f:
            lines = f.readlines()
        with open(self.copyFile, "w") as f:
            for line in lines:
                if count == 1:
                    fullName, firstName, middleName, lastName, actualDOB = self.grabNextName(line)
                else:
                    f.write(line)
                count += 1
        return fullName, firstName, middleName, lastName, actualDOB

    def grabNextName(self, lineString):
        # print(lineString)
        stringArray = lineString.split("\t")
        fullName = stringArray[0]
        nameArray = fullName.split(" ")
        dob = stringArray[1]
        actualDOB = dob
        middleName = ""
        if len(nameArray) != 3:
            firstName = nameArray[0]
            lastName = nameArray[1]
        else:
            firstName = nameArray[0]
            middleName = nameArray[1]
            lastName = nameArray[2]

        return fullName, firstName, middleName, lastName, actualDOB

    def selectScrollable(self, value, id="", xpath="", hasId=True):
        if hasId:
            select = Select(self.browser.find_element_by_id(id))
        else:
            select = Select(self.browser.find_element_by_xpath(xpath))

        select.select_by_value(value)


    # take 2 for waiting for the loading to be done
    def doesExist(self, xpath, textCheck):
        try:
            group = self.getElements(xpath)
            for element in group:
                if element.text == textCheck:
                    return True
            return False
        except NoSuchElementException:
            return False
