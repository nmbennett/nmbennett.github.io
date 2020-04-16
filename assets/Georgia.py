from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.support.ui import Select
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
import zipfile
import os
from time import sleep

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None
    
def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    print(e)

def cnty_scrape(baseurl):   
    '''
    Will open the web browser and 'click' on each link to download the csv for each county's elections
    '''
    raw_html = simple_get(baseurl)
    html = BeautifulSoup(raw_html, 'html.parser')
    
    browser = webdriver.Chrome('***Location of chrome driver***')
    browser.get(baseurl)
    for i, li in enumerate(html.select('li')):
        if i > 9:
            print(i, li.text) 
            '''
            To open the county results, 
            switch to the window, 
            and download the summary file
            '''
            main_window = browser.current_window_handle
            browser.find_element_by_link_text(li.text).click()
            browser.switch_to.window(li.text)
            sleep(3)
            browser.find_element_by_link_text('Reports').click()
            browser.find_element_by_link_text('summary.zip').click()
            browser.switch_to.window(main_window)
  
def file_clean(state,year,baseurl):
    '''
    This simply saves each of the newly downloaded csv into a directory for later
    '''
    raw_html = simple_get(baseurl)
    html = BeautifulSoup(raw_html, 'html.parser')
        
    for i, li in enumerate(html.select('li')):
           print(i, li.text)     
           zip_ref = zipfile.ZipFile('***Directory the zipped files were saved in***/summary ('+str(i)+').zip', 'r')
           zip_ref.extractall('***Where zipped files will be moved to***/'+state+'/'+year)
           os.rename('***Where zipped files will be moved to***/'+state+'/'+year+'/summary.csv','***Where zipped files will be moved to***/'+state+'/'+year+'/summary_'+li.text+'.csv')
           zip_ref.close()


'''
Georgia 2016 election
http://results.enr.clarityelections.com/GA/
'''    
cnty_scrape('http://results.enr.clarityelections.com/GA/63991/184321/en/select-county.html')   
os.rename('**Downloads folder***/summary.zip','**Downloads folder***/summary (0).zip')  
file_clean('Georgia','2016','http://results.enr.clarityelections.com/GA/63991/184321/en/select-county.html')

'''
Georgia 2012 election
http://results.enr.clarityelections.com/GA/
'''    
cnty_scrape('http://results.enr.clarityelections.com/GA/42277/113204/en/select-county.html')   
os.rename('**Downloads folder***/summary.zip','**Downloads folder***/summary (0).zip') 
file_clean('Georgia','2012','http://results.enr.clarityelections.com/GA/42277/113204/en/select-county.html')
