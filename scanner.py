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


class DrawScanner():
    TEAMS_XPATH = '/html/body/div[1]/main/div/div[2]/div[2]/div/div[2]/h2'
    ODDS_XPATH = '/html/body/div[1]/main/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]'
    COUNTRY_XPATH = '/html/body/div[1]/main/div/div[1]/ul/li[2]'
    LEAGUE_XPATH = '/html/body/div[1]/main/div/div[1]/ul/li[3]'
    STANDING_XPATH = '/html/body/div[1]/main/div/div[2]/div[3]/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/div/div/div'
    STANDING_XPATH_2 = '/html/body/div[1]/main/div/div[2]/div[3]/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/div/div/div'
    STANDING_XPATH_ERROR = '/html/body/div[1]/main/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div/div[2]/div/div'

    games_to_scan = []
    with open('today_games', 'r') as text_file:
        for line in text_file.readlines():
            games_to_scan.append(line.strip())

    def main(self):
        driver = self.driver_chrome()

        for game in self.games_to_scan:
            driver.get(game)

            country, league, home_team, away_team, home_odd, draw_odd, away_odd = self.get_teams_league_odds(driver)

            self.get_standings(driver, home_team, away_team)

    def get_standings(self, driver, home_team, away_team):

        home_standing = ''
        away_standing = ''
        try:
            WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.XPATH, self.STANDING_XPATH)))
            standing_tokens = driver.find_elements_by_xpath(self.STANDING_XPATH)

            for position in range(2, len(standing_tokens) + 1):
                team_tokens = driver.find_element_by_xpath(self.STANDING_XPATH + f'[{position}]')

                if 'fdibCW' in team_tokens.get_attribute('class'):
                    home_standing = team_tokens.text.split('\n')
                if 'vqXLK' in team_tokens.get_attribute('class'):
                    away_standing = team_tokens.text.split('\n')

        except Exception as ex:
            try:
                WebDriverWait(driver, timeout=10).until(
                    EC.visibility_of_element_located((By.XPATH, self.STANDING_XPATH_2)))
                standing_tokens = driver.find_elements_by_xpath(self.STANDING_XPATH_2)

                for position in range(2, len(standing_tokens) + 1):
                    team_tokens = driver.find_element_by_xpath(self.STANDING_XPATH_2 + f'[{position}]')

                    if 'fdibCW' in team_tokens.get_attribute('class'):
                        home_standing = team_tokens.text.split('\n')
                    if 'vqXLK' in team_tokens.get_attribute('class'):
                        away_standing = team_tokens.text.split('\n')


            except Exception:
                print('VLIZA VTORI EXCEPTION')

        print(home_standing)
        print(away_standing)

    def get_teams_league_odds(self, driver):
        try:
            odds_token = driver.find_element_by_xpath(self.ODDS_XPATH).text.split('\n')
            home_odd, draw_odd, away_odd = odds_token[1].strip(), odds_token[3].strip(), odds_token[5].strip()
            WebDriverWait(driver, timeout=5).until(EC.visibility_of_element_located((By.XPATH, self.ODDS_XPATH)))

        except Exception:
            home_odd, draw_odd, away_odd = '-', '-', '-'

        teams_token = driver.find_element_by_xpath(self.TEAMS_XPATH).text
        home_team, away_team = teams_token.split(' - ')
        country = driver.find_element_by_xpath(self.COUNTRY_XPATH).text
        league = driver.find_element_by_xpath(self.LEAGUE_XPATH).text
        if 'video stream' in league:
            league = ''

        # print(f'{country} {league}\n{home_team} vs {away_team} {home_odd} {draw_odd} {away_odd}')
        return country, league, home_team, away_team, home_odd, draw_odd, away_odd

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
    scanner = DrawScanner()
    scanner.main()
