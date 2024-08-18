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

SELECTOR_FIELD_NAMES = [
    'Input_CaseNumber_HearingBenchCode',
    'Input_ComplaintDiaryNumber', 
    'Input_CaseNumber_Complaint_FilingYear_YearOfCase'
    ]

import tkinter as tk
import time
import os
import sys
from tkinter import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from typing import Any

from gen_webscraper import Class_Webscraper
from read_captcha import Class_CaptchaSolver

x = print(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
sys.path.append(x)

from apps.courtcases.models import CaseDetails


class Class_WebScraper_01:


    def __init__(self):
        pass


    def __call__(self) -> Any:
        
        self.collect_parameters()


    @classmethod
    def collect_parameters(self) -> dict:
        """
        To do: Collect parameters
        Arguments: None
        Returns: dict()
            { bench_name: judge_name, complaint_num: case_num, year: year1 }
        """

        global params_dict
        params_dict = {}

        def save_form():
            
            params_dict["name"] = entry_name.get() if entry_name.get() else 'Sh. Rakesh Kumar Goyal'
            params_dict["case"] = entry_case.get() if entry_case.get() else 'GCNo04082022'
            params_dict["year"] = entry_year.get() if entry_year.get() else 2022 
            root_window.destroy()

        print("------------------------------------------------------------------------------")
        # Parameters
        print("MESSAGE: Parameters input process has just begun.. :)")

        root_window = tk.Tk()
        root_window.title = "Parameters"

        label_name = Label(root_window, text='Bench Name')
        label_name.grid(row=1, column=0)

        entry_name = tk.Entry(root_window, width=50)
        entry_name.grid(row=1, column=1, columnspan=3)

        label_case = Label(root_window, text='Case No./Complaint No.')
        label_case.grid(row=2, column=0)

        entry_case = tk.Entry(root_window, width=50)
        entry_case.grid(row=2, column=1, columnspan=3)

        label_year = Label(root_window, text='Year')
        label_year.grid(row=3, column=0)

        entry_year = tk.Entry(root_window, width=50)
        entry_year.grid(row=3, column=1, columnspan=3)

        save_form_button = Button(root_window, text ="Save", command = save_form)
        save_form_button.grid(row=4, column=2)

        root_window.mainloop()
        
        print("MESSAGE: Parameters input process has just ended.. :)")

        print("------------------------------------------------------------------------------")

        self.parse_webpage_data()

    @classmethod
    def parse_webpage_data(self) -> None:
        """
        To do: Parse data from webpage
        Arguments: None
        Returns: None
        """

        cls_instance = Class_Webscraper()
        url_source = cls_instance.read_source_url()

        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        for source_url in url_source:
            browser = webdriver.Chrome(options=chrome_options)
            browser.maximize_window()
            browser.get(source_url)

            # right panel choice
            select_case_panel = browser.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/div/div/div/div[2]/ul/li[2]/a")
            select_case_panel.click()

            # Its already in complaint info section if the URL for the first one is hit
            # bench-name
            select_name_option = browser.find_element(By.NAME, SELECTOR_FIELD_NAMES[0])
            option_names = select_name_option.find_elements(By.TAG_NAME, 'option')
            
            for i in option_names:
                if params_dict["name"] in i.text:                    
                    i.click()
                    
                    
            # complaint number
            select_case = browser.find_element(By.NAME, SELECTOR_FIELD_NAMES[1])
            select_case.send_keys(params_dict["case"])

            # year
            select_year = browser.find_element(By.NAME, SELECTOR_FIELD_NAMES[2])
            select_year.clear()
            select_year.send_keys(params_dict["year"])

            time.sleep(20)

            # captcha
            # cls_captcha_instance = Class_CaptchaSolver()

            # select_captcha = browser.find_element(By.CLASS_NAME, 'capcha-badge')
            # cap_txt = cls_captcha_instance.__call__(select_captcha)
            # print('cap txt', cap_txt)
            # insert_captcha = browser.find_element(By.NAME, 'Input_CaseNumber_CaptchaText')
            # insert_captcha.send_keys(str(cap_txt[1]))

            # submit button for search
            search_btn = browser.find_element(By.ID, 'btn_SearchCaseStatusSubmit')
            search_btn.click()

            # details views per record
            tr_tag_view_buttons = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.ID, "modalOpenerButton")))

            for i in tr_tag_view_buttons:
                i.click()
                # time.sleep(10)

                # self.fetch_database(browser)
                li_items = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div[2]/form/div/div/div/div[4]/div/div/div[2]/div/div/div[2]/form/div/div/div/div")))

                record = {}

                for li_item in li_items:
                    content = li_item.text
                    
                    for i in content.split("\n"):
                        if i.startswith("Case/ Complaint Number "):
                            record["case_id"] = i.split("Case/ Complaint Number ")[1]
                        if i.startswith("Case/ Complaint Type "):
                            record["case_type"] = i.split("Case/ Complaint Type ")[1]
                        if i.startswith("Filing Date "):
                            record["case_filing_date"] = i.split("Filing Date ")[1]
                        if i.startswith("Name of Complainant "):
                            record["complainant_name"] = i.split("Name of Complainant ")[1].split("Name of Respondent ")[0]
                            record["respondent_name"] = i.split("Name of Respondent ")[1]
                        if i.startswith("Registration/ RERA Number to which the Complaint relates "):
                            record["registration_number"] = i.split(" Complaint relates ")[1].split(" Name of the ")[0]
                            record["rera_project"] = i.split("Agent to which the Complaint relates ")[1]
                        if i.startswith("Pending For/ Date"):
                            record["pending_for_date_of_decision"] = i.split("Date of Decision ")[1]
                        if i.startswith("Fixed For"):
                            record["status_fixed_for"] = i.split(" For ")[1]
                        if i.startswith("Bench Name"):
                            record["bench_name"] = i.split("Name ")[1]
                        if i.startswith("Court Complex Address"):
                            record["court_address"] = content.split("Court Complex Address")[1].split("Complainant Details")[0].replace("\n", " ")
                            record["additional_complainant_details"] = content.split("Complainant Address Detail")[1].replace("\n", " ")

                # print('record', record)
                self.insert_into_database(record)

            browser.close()



    @classmethod
    def insert_into_database(self, record) -> None:
        """
        To do: Parse data from webpage to feed the database records
        Arguments: dict()
            1. record of data to be inserted
        Returns: None
        """

        record_db = CaseDetails(
            case_id = record["case_id"],
            case_type = record["case_type"],
            case_filing_date = record["case_filing_date"],
            complainant_name = record["complainat_name"],
            respondent_name = record["respondent_name"],
            registration_rera_number = record["registration_number"],
            rera_project =  record["rera_project"],
            status_fixed_for = record["status_fixed_for"],
            bench_name =  record["bench_name"],
            court_address = record["court_address"],
            pending_for_date_of_decision = record["pending_for_date_of_decision"],
            additional_complainant_details = record["additonal_complainant_details"]
        )
        record_db.save()

