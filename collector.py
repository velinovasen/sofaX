from bs4 import BeautifulSoup
from time import sleep, perf_counter
import re

# from webdriver_manager.firefox import GeckoDriverManager
import csv
from selenium.webdriver import FirefoxOptions, Firefox, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DC
from selenium.webdriver.support.wait import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions, Chrome, ActionChains


class GameCollector:
    GAME_A_LINK_HREF = '/html/body/div[1]/main/div/div[2]/div/div[3]/div[2]/div/div/div/div/div/a'
    ALL_GAMES_BUTTON_XPATH = '/html/body/div[1]/main/div/div[2]/div/div[3]/div[2]/div/button'

    def main(self):
        driver = self.driver_chrome()

        driver.get('https://www.sofascore.com/football')

        all_hrefs = self.gather_hrefs(driver)

    def gather_hrefs(self, driver):
        all_hrefs = []

        WebDriverWait(driver, timeout=15) \
            .until(EC.visibility_of_element_located
                   ((By.XPATH, '/html/body/div[1]/main/div/div[2]/div/div[3]/div[2]/div/div/div/div/div[1]')))

        a_links = driver.find_elements_by_xpath(self.GAME_A_LINK_HREF)

        [all_hrefs.append(link.get_attribute('href')) for link in a_links]

        while True:
            a_tokens = driver.find_elements_by_xpath(self.GAME_A_LINK_HREF)
            ActionChains(driver).move_to_element(a_tokens[-1]).perform()
            sleep(2)
            new_a_links = driver.find_elements_by_xpath(self.GAME_A_LINK_HREF)
            new = False
            for link in new_a_links:
                if link.get_attribute('href') not in all_hrefs:
                    all_hrefs.append(link.get_attribute('href'))
                    new = True
            if not new:
                break

        try:
            token = driver.find_element_by_xpath('/html/body/div[1]/footer/div/div[1]/div[1]/div/p')
            ActionChains(driver).move_to_element(token).perform()
            button = driver.find_element_by_xpath(self.ALL_GAMES_BUTTON_XPATH)
            button.click()
            # sleep(2)
        except Exception:
            pass

        while True:
            a_tokens = driver.find_elements_by_xpath(self.GAME_A_LINK_HREF)
            ActionChains(driver).move_to_element(a_tokens[-1]).perform()
            # sleep(2)
            new_a_links = driver.find_elements_by_xpath(self.GAME_A_LINK_HREF)
            new = False
            for link in new_a_links:
                if link.get_attribute('href') not in all_hrefs:
                    all_hrefs.append(link.get_attribute('href'))
                    new = True
            if not new:
                break

        with open('today_games', 'w') as text_file:
            [text_file.write(href + '\n') for href in all_hrefs]
        [print(href) for href in all_hrefs]
        text_file.close()
        print(len(all_hrefs))
        return all_hrefs

    def driver_chrome(self):
        """
        Open and set the settings for the browser
        :param link:
        :param token:
        :return driver:
        """
        CHROME_PATH = '/usr/bin/google-chrome'
        CHROMEDRIVER_PATH = '/home/velinov/Desktop/scrp-drivers/chromedriver'

        chrome_options = ChromeOptions()
        chrome_options.binary_location = CHROME_PATH
        chrome_options.headless = False  # IF YOU WANT TO SEE THE BROWSER -> FALSE

        capa = DC.CHROME
        # capa["pageLoadStrategy"] = "none"

        driver = Chrome(options=chrome_options, executable_path=CHROMEDRIVER_PATH, desired_capabilities=capa)
        driver.maximize_window()
        return driver


if __name__ == '__main__':
    scanner = GameCollector()
    scanner.main()
