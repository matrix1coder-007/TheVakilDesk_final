"""
-----------------------------------------------------------------------------------
Author: Ishita Katyal
Date created: 08/03/2023
Date modified: 08/03/2023
-----------------------------------------------------------------------------------
To do: Add a source url in the file from user input.
-----------------------------------------------------------------------------------
"""

from typing import Any
import tkinter as tk
from tkinter import *


class Class_TextBox:

    def __init__(self) -> None:
        pass


    def __call__(self) -> Any:
        
        self.add_source_URLs()


    def add_source_URLs(self) -> None:    
        """
        To do: Add source URL for the web-scraper
        Arguments: None
        Returns: None        
        """        
        
        global sourceURLsList
        sourceURLsList = []

        def addSourceURL():

            entry_box = tk.Entry(root_window, width=50)
            entry_box.grid(row=1, column=1)
            sourceURLsList.append(entry_box)

        def saveSourceURL():

            with open('source_urls.txt', 'a') as file_url:
                for source_url in sourceURLsList:
                    file_url.write(source_url.get())
                    file_url.write('\n')
            root_window.destroy()


        print("------------------------------------------------------------------------------")
        # source URL input
        print("MESSAGE: Source URL input process has just begun.. :)")

        root_window = tk.Tk()
        root_window.title = "Add Source URL"
        add_url_button = Button(root_window, text ="Add source URL", command = addSourceURL)
        add_url_button.grid(row=0, column=0)

        save_url_button = Button(root_window, text ="Save", command = saveSourceURL)
        save_url_button.grid(row=0, column=1)

        root_window.mainloop()
        
        print("MESSAGE: Source URL input process has just ended.. :)")

        print("------------------------------------------------------------------------------")

