import time
from tqdm import tqdm
import logging
logging.basicConfig(level=logging.INFO)

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from crawler.common import VietStockCommon


class VietStock():
    def __init__(self) -> None:
        self.user = VietStockCommon.EMAIL_LOGIN
        self.password = VietStockCommon.PASSWORD_LOGIN
        self.root_url = VietStockCommon.ROOT_URL

    def quitDriver(self):
        '''Quit web driver'''
        try:
            self.driver.quit()
        except:
            pass

    def resetDriver(self):
        '''Reset web driver '''
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument('--start-maximized')
        edge_options.add_argument('--headless')
        self.driver = webdriver.Edge(options=edge_options)


    def clickByID(self, element_id):
        '''Click element by id'''
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            element.click()
        except:
            self.driver.refresh()
            pass
    
    def sendByID(self, element_id, msg):
        '''Send message to element by id'''
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            element.clear()
            element.send_keys(msg)
        except:
            pass
    
    def login(self):
        '''Login VietStock'''
        self.driver.get(self.root_url)

        try:       
            self.clickByID('btn-request-call-login')
            self.sendByID('txtEmailLogin',self.user)
            self.sendByID('txtPassword',self.password)
            self.clickByID('btnLoginAccount')
        except:
            raise 'Something is wrong when login Vietstock'


class ListingCompanyVietStock(VietStock):
    '''Crawl listing companies from VietStock'''

    def __init__(self) -> None:
        super().__init__()
        self.listing_url = VietStockCommon.LISTING_URL

    def getNumOfPages(self, page):
        num_pages = 0
        try:
            num_pages = int(page.find_all('span', {'class':'m-r-xs'})[1].find_all('span')[1].text)
        except: 
            pass
        return num_pages
    
    def getListingTable(self, html_source) -> pd.DataFrame:
        '''Get listing table from vietstock html source'''
        time.sleep(1)
        list_table = html_source.find_all(
            'table', 
            {'class':'table table-striped table-bordered table-hover table-middle pos-relative m-b'}
        )
        try: 
            return pd.read_html(str(list_table))[0]
        except: 
            return pd.DataFrame(columns=[i.text for i in list_table])

    def run(self) -> pd.DataFrame:
        '''Crawl listing companies'''
        logging.info('Run crawl listing companies')
        self.resetDriver()
        self.login()
        logging.info('Login successfully')
        time.sleep(5)
        self.driver.get(self.listing_url)
        time.sleep(1)

        page_source = self.driver.page_source
        page = BeautifulSoup(page_source, 'html.parser')
        num_pages = self.getNumOfPages(page)

        listing_tables = []
        for page in tqdm(range(num_pages), total=num_pages):
            page_source = BeautifulSoup(self.driver.page_source, 'html.parser')
            listing_table = self.getListingTable(page_source)
            listing_tables.append(listing_table)
            self.clickByID('btn-page-next')
            time.sleep(2)
        self.quitDriver()
        listing_data = pd.concat(listing_tables, axis=0)
        logging.info('Crawl successfully')
        return listing_data
  