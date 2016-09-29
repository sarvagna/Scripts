# -*- coding: utf-8 -*-
# linkedin_people_profile_india.py

import sys
reload(sys)
sys.dont_write_bytecode = True
sys.setdefaultencoding('utf-8')

# -------------Builtin modules-------------------------------------------------
from csv import QUOTE_ALL, writer
from re import sub
from math import ceil
from scrapy.selector import HtmlXPathSelector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from sys import argv
from time import sleep


# ------------Cleaning string function-----------------------------------------
def get_cleaned_string(string):
    string = string.replace('\n', ' ')
    string = string.replace('\r', ' ')
    string = string.replace('\t', ' ')
    string = sub(r'[ ]+', ' ', string)
    string = string.strip()
    return string


# ------------Extracting information from linkedin website---------------------
def linkedin_process(company):
    # Static variable initializaiton
    items = []
    # Do not remove the following line, or various programs
    # that require network functionality will fail.
    browser = webdriver.Firefox()
    browser.get('https://www.linkedin.com/nhome')

    # Find input tag to provide username, password and to find submit options
    username = browser.find_element_by_id("session_key-login")
    password = browser.find_element_by_id("session_password-login")
    submit = browser.find_element_by_id("signin")

    # This writes/provides username and password to login page
    username.send_keys("Your_LinkedIn_Email_Id")
    password.send_keys("Associated_Password")

    # Click on the submit button
    submit.click()
    # Create wait obj with 10 seconds timeout, and default 0.10 poll frequency
    WebDriverWait(browser, 10)
    # Wait for 30 seconds
    sleep(15)
    # Fetch name of the submit button
    submit = browser.find_element_by_id("advanced-search").click()
    # Create wait obj with 10 seconds timeout
    WebDriverWait(browser, 10)
    # Sending get request with company name
    browser.get(
        'https://www.linkedin.com/vsearch/p?company=%(company)s&'
        'openAdvancedForm=true&companyScope=C&locationType=I&countryCode=in'
        % {
            'company': company
        }
    )
    # Create wait obj with 10 seconds timeout
    WebDriverWait(browser, 10)
    # Wait for 30 seconds
    sleep(15)
    # execute script is to get html source from page
    source = browser.execute_script(
        'return document.documentElement.innerHTML'
    )
    # HtmlXPathSelector for working with HTML documents
    hxs = ''
    try:
        hxs = HtmlXPathSelector(text=source)
    except:
        pass
    # Use Xpath to get total pages
    pages = ''
    try:
        pages = get_cleaned_string(hxs.select(
            '//*[@id="results_count"]/div/p/strong[1]/text()'
        ).extract()[0])
    except:
        pass
    if pages:
        # Looping through pages
        for page in range(1, int(ceil(float(pages) / 10)) + 1):
            browser.get(
                'https://www.linkedin.com/vsearch/p?company=%(company)s&'
                'openAdvancedForm=true&companyScope=C&locationType=I&'
                'countryCode=in&page_num=%(page)s'
                % {
                    'company': company,
                    'page': page
                }
            )
            # Webdriver to wait 10 seconds
            WebDriverWait(browser, 10)
            # Wait for 15 seconds
            sleep(15)
            # execute script is to get html source from page
            source = browser.execute_script(
                'return document.documentElement.innerHTML'
            )
            # HtmlXPathSelector for working with HTML documents
            hxs = ''
            try:
                hxs = HtmlXPathSelector(text=source)
            except:
                pass
            # Use Xpath to get required data from the response
            name_ = ''
            try:
                name_ = hxs.select('//a[@class="title"]/text()').extract()
            except:
                pass
            current_position_ = ''
            try:
                current_position_ = hxs.select(
                    '//div[@class="description"]'
                ).extract()
            except:
                pass
            location_ = ''
            try:
                location_ = hxs.select('//dd[@class="separator"]').extract()
            except:
                pass
            urls = ''
            try:
                urls = hxs.select('//a[@class="title"]/@href').extract()
            except:
                pass
            # Looping through fetched data i.e. names, positions locations etc.
            for name, current_position, location, url in zip(
                name_, current_position_, location_, urls
            ):
                current_position = get_cleaned_string(
                    sub('<[^>]*>', '', ''.join(current_position))
                )
                location = get_cleaned_string(
                    sub('<[^>]*>', '', ''.join(location))
                )
                items.append([name, current_position, location, url])
    # Close browser
    browser.close()
    # Variable is assigned with column header
    row_title = ['Name', 'Current Position', 'Location', 'Url']
    # Builtin function to open file, write header and Dump data into file
    with open('%(company)s.csv' % {'company': company}, 'w') as resource:
        writer(
            resource,
            delimiter=',',
            doublequote=True,
            lineterminator='\n',
            quoting=QUOTE_ALL,
            skipinitialspace=False,
        ).writerow(row_title)
        writer(
            resource,
            delimiter=',',
            doublequote=True,
            lineterminator='\n',
            quoting=QUOTE_ALL,
            skipinitialspace=False,
        ).writerows(items)
    # Quit web browser
    try:
        browser.quit()
    except:
        pass

# -------start here------------------------------------------------------------
# argv[1]: Provide Company Name
linkedin_process(argv[1])