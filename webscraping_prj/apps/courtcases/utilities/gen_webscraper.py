"""
-----------------------------------------------------------------------------------
Author: Ishita Katyal
Date created: 08/03/2023
Date modified: 08/03/2023
-----------------------------------------------------------------------------------
To do: Build a web-scraper for the following URL-
    https://rera.punjab.gov.in/reraindex/courtview/ComplaintCaseStatusInfo
-----------------------------------------------------------------------------------
"""

import requests
import json
from typing import Any


from add_source_url import Class_TextBox
from read_captcha import Class_CaptchaSolver


class Class_Webscraper:


    def __init__(self) -> None:
        pass


    
    def __call__(self) -> Any:
        
        print("------------------------------------------------------------------------------")
        # Source URL fetch
        print("MESSAGE: Source URL fetch process has just begun.. :)")

        add_url_bool = input('Do you want to add a source URL? (Y/N) [default=N]')
        if add_url_bool != 'Y':
            print('MESSAGE: No more URLs to be added.. :)\n')

        elif add_url_bool == 'Y':
            cls_instance = Class_TextBox()
            cls_instance.__call__()

        print("MESSAGE: Source URL fetch process has just ended.. :)")

        print("------------------------------------------------------------------------------")

        # Base-folder directory for source URLs JSON data 
        cls_instance = Class_CaptchaSolver()
        cls_instance.create_folders(today_dir='source_urls_dir')

        print('MESSAGE: Initiating webscraping.. :)')

        print("MESSAGE: Source URL read process has just begun.. :)")
        # Source URL read
        source_Urls_List = self.read_source_url()

        print("MESSAGE: Source URL read process has just ended.. :)")

        print("------------------------------------------------------------------------------")

        print("MESSAGE: Source URL write in file process has just begun.. :)")
        # Source URL write in file
        i = 1
        for urls in source_Urls_List:
            url_data = self.fetch_url_data(urls)
            
            with open("source_urls_dir//" + str(i)+".json", "w", encoding='UTF-8') as url_file:
                url_file.write(str(url_data))
                i += 1

        print("MESSAGE: Source URL write in file process has just ended.. :)")

        print("------------------------------------------------------------------------------")



    @classmethod
    def read_source_url(self) -> list:
        """
        To do: Fetch source URLs from the file: source_urls.txt
        Arguments: None
        Returns: 
            1. list: source URLs
        """
    
        source_urls_list = []

        with open('source_urls.txt', "r") as urls_file:
            data = urls_file.read()       

        for url in data.split('\n'):
            if url not in ['', ' ', " ", '\n']:
                source_urls_list.append(url)

        return source_urls_list



    @classmethod
    def fetch_url_data(self, url) -> json:
        """
        To do: Fetch source URL data
        Arguments: 
            1. str: source_url to be web-scraped
        Returns: 
            1. json: source_url data JSON
        """

        url_data = requests.get(url)
        url_data_json = url_data.text

        return url_data_json

