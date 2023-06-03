# This program is written by: Mahsa Radinmehr
# for more information please visit:
#     https: // github.com/rodinmehr/google-translate-subtitle-translator

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyautogui
import pyperclip
from bs4 import BeautifulSoup
import re
from datetime import datetime

def main():
    current_directory = os.getcwd()
    source_file = current_directory+"/input.srt"
    parsed_file = current_directory+"/input_parsed.txt"
    driver_path = current_directory+"/chromedriver"
    options = Options()
    options.add_argument("start-maximized")

    # first off, we should parse the subtitle file
    # and fetch all of the words
    with open(source_file) as f:
        lines = f.readlines()
    subtitle_sections = 0
    extracted_sentences = ""
    has_same_section = False
    for i in range(len(lines)):
        if subtitle_sections == 0:
            i+=2
            subtitle_sections+=1
            while (i < len(lines) and lines[i] != "\n"):
                if(has_same_section):
                    extracted_sentences = extracted_sentences[0:-1]
                    extracted_sentences += lines[i]
                else:
                    extracted_sentences += lines[i]
                i+=1
                has_same_section = True
            has_same_section = False
        if lines[i]=="\n":
            subtitle_sections+=1
            i+=3
            while (i < len(lines) and lines[i] != "\n"):
                if (has_same_section):
                    extracted_sentences = extracted_sentences[0:-1]
                    extracted_sentences += lines[i]
                else:
                    extracted_sentences += lines[i]
                i += 1
                has_same_section = True
            has_same_section = False

    # print(extracted_sentences)
    with open(parsed_file, "w") as text_file:
        text_file.write(extracted_sentences)
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    # driver = webdriver.Chrome(driver_path, options=options)
    driver.get("https://translate.google.com/?sl=auto&tl=fa&op=translate")
    time.sleep(5)
    # source_text = driver.find_elements_by_xpath("//*[@id='yDmH0d']/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea")
    source_text = driver.find_element(by=By.CLASS_NAME, value="er8xn")
    if(source_text):
        if(len(extracted_sentences)<5000):
            source_text.clear()
            source_text.send_keys(extracted_sentences)
        else:
            parsed_length = 5000
            source_text.clear()
            source_text.send_keys(extracted_sentences[0:parsed_length])
    time.sleep(5)
    copy_translation = driver.find_element(
        by=By.CLASS_NAME, value="VfPpkd-Bz112c-LgbsSe")
    copy_translation.click()
    output_text = pyperclip.paste()
    # print(output_text)
    


if __name__ == "__main__":
    main()