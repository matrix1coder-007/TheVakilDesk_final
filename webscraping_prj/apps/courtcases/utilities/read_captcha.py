"""
-----------------------------------------------------------------------------------
Author: Ishita Katyal
Date created: 08/02/2023
Date modified: 08/03/2023
-----------------------------------------------------------------------------------
To do: Read a number-captcha from an image.
-----------------------------------------------------------------------------------
"""

import os
import time
import requests
import datetime
from datetime import date, datetime

import easyocr


BASE_DIR = os.getcwd()
# print('BASE DIR', BASE_DIR)

MAX_ATTEMPTS = 3


class Class_CaptchaSolver:

    def __init__(self):
        pass


    def __call__(self, select_captcha_element) -> str:

        print("------------------------------------------------------------------------------")
        # Folder creation
        print("MESSAGE: Folder creation process and verification has just begun.. :)")

        self.create_folders()
        todays_date_str = str(date.today())
        self.create_folders(today_dir=todays_date_str, home_dir='captchas_dir')

        print("MESSAGE: Folder creation process and verification has just ended.. :)")

        print("------------------------------------------------------------------------------")
        # Captcha file download
        print("MESSAGE: Captcha image download process has just begun.. :)")
        
        x = self.save_captcha_file(select_captcha_element)

        print("MESSAGE: Captcha image download process has just ended.. :)")

        print("------------------------------------------------------------------------------")

        return x


    @classmethod
    def create_folders(self, today_dir: str = 'captchas_dir', home_dir=BASE_DIR) -> None:
        """
        To do: Create the base folders/directories for parsing captcha images
        Arguments: None
        Returns: None
        """

        today_dir_path = os.path.join(home_dir, today_dir)
        folder_present_bool = False

        if today_dir == 'captchas_dir' and os.path.isdir(today_dir):
            folder_present_bool = True
            print('MESSAGE: Folder-', today_dir, 'already exists.. :)')

        if today_dir != 'captchas_dir' and os.path.isdir(today_dir_path):
            folder_present_bool = True
            print('MESSAGE: Folder-', today_dir, 'already exists.. :)')

        if folder_present_bool:
            return 

        i_tries = 0
        while i_tries < MAX_ATTEMPTS and (not folder_present_bool):

            try:
                os.makedirs(today_dir_path)
                folder_present_bool = True
                print('SUCCESS: Folder: ', today_dir, ' creation successful.. in attempt-', i_tries, ':)')
            except OSError as e:
                print('FAILURE: Folder: ', today_dir, ' creation failed.. in attempt-', i_tries, ':(')
                folder_present_bool = True
                
            i_tries += 1



    @classmethod
    def save_captcha_file(self, select_captcha_ele, dir_save: str = str(date.today())) -> str:
        """
        To do: Save the captcha file from the source URL
        Arguments: 
            1. browser.find_element: select_captcha_element is the browser.find_element
            2. str: folder_name string marked by default on the date in str format
        Returns: str: captch_text
        """

        captcha_save_folder_path = os.path.join("captchas_dir", dir_save)
        captcha_save_file_name = str(datetime.now().time()).split(".")[0]
        captcha_save_file_name = str(captcha_save_file_name).replace(":", "-") + '.png'
        file_save = os.path.join(captcha_save_folder_path, captcha_save_file_name)

        resp = requests.get(select_captcha_ele.get_attribute('src'))
        time.sleep(10)

        with open(file_save, 'wb') as out_file:
            out_file.write(resp.content)

        # Captcha file read
        print("MESSAGE: Captcha read process has just begun.. :)")

        return self.read_captcha(file_save)


    @classmethod
    def read_captcha(self, captcha_file_name: str) -> str:
        """
        To do: Read the string of charcaters from a captcha
        Arguments: 
            1. str: image file name
        Returns: str: text from captcha
        """
   
        reader = easyocr.Reader(['en'])
        captcha_txt = reader.readtext(captcha_file_name, detail = 100)

        return captcha_txt[0]
    
    