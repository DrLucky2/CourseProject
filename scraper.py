# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 18:46:43 2021

@author: GYMA
"""

from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import re 
import urllib
import time

options = Options()
options.headless = True
driver = webdriver.Chrome('./chromedriver',options=options)

def get_js_soup(url,driver):
    driver.get(url)
    res_html = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html,'html.parser') 
    return soup

def process_bio(bio):
    bio = bio.encode('ascii',errors='ignore').decode('utf-8')      
    bio = re.sub('\s+',' ',bio)   
    return bio


def remove_script(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup


def is_valid_homepage(bio_url,dir_url):
    if bio_url.endswith('.pdf'):
        return False
    try:
     
        ret_url = urllib.request.urlopen(bio_url).geturl() 
    except:
        return False    
    urls = [re.sub('((https?://)|(www.))','',url) for url in [ret_url,dir_url]] 
    return not(urls[0]== urls[1])

def scrape_dir_page(dir_url,driver):
    print ('-'*20,'Scraping directory page','-'*20)
    faculty_links = []
    faculty_base_url = 'https://gatherer.wizards.com/Pages/Card/'
    soup = get_js_soup(dir_url,driver)     
    for link_holder in soup.find_all('div',class_='cell info'): 
        rel_link = link_holder.find('a')['href'] 
        faculty_links.append(faculty_base_url+rel_link) 
    print ('-'*20,'Found {} faculty profile urls'.format(len(faculty_links)),'-'*20)
    return faculty_links

dir_url = 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=476460' 
faculty_links = scrape_dir_page(dir_url,driver)

def scrape_faculty_page(fac_url,driver):
    soup = get_js_soup(fac_url,driver)
    homepage_found = False
    bio_url = ''
    bio = ''
    profile_sec = soup.find(class_='column-two-third')
    if profile_sec is not None:
        all_headers = profile_sec.find_all('h3')
        faculty_last_name = all_headers[0].get_text().lower().split()[-1] 
        faculty_first_name = all_headers[0].get_text().lower().split()[0]
        homepage_txts = ['site','page',faculty_last_name,faculty_first_name]
        exceptions = ['course ','research','group','cs','mirror','google scholar']
      
        
        bio_url = fac_url 
        bio = process_bio(profile_sec.get_text(separator=' '))

    return bio_url,bio

bio_urls, bios = [],[]
tot_urls = len(faculty_links)
for i,link in enumerate(faculty_links):
    print ('-'*20,'Scraping page text{}/{}'.format(i+1,tot_urls),'-'*20)
    bio_url,bio = scrape_faculty_page(link,driver)
    if bio.strip()!= '' and bio_url.strip()!='':
        bio_urls.append(bio_url.strip())
        bios.append(bio)
        
bio_urls = scrape_dir_page(dir_url,driver)

driver.close()


def write_lst(lst,file_):
    with open(file_,'w') as f:
        for l in lst:
            f.write(l)
            f.write('\n')
            
bio_urls_file = 'bio_urls.txt'
bios_file = 'bios.txt'
write_lst(bio_urls,bio_urls_file)
write_lst(bios,bios_file)