import re
import time
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

def web_table_into_dataframe(soup):
    cur_table = soup.find('table', attrs={'class':'tablesorter'})
    cur_table_rows = cur_table.find_all('tr')

    table_header = cur_table_rows[0]
    cur_table_rows = cur_table_rows[1:]
    header_names = [i.text for i in table_header.find_all('th')]
    
    table_as_dict = {}
    cur_id = 0
    for tr in cur_table_rows:
        td = tr.find_all('td')
        cur_td_elements = [] 
        for i in td:
            link_element = i.find('a')
            if link_element != None:
                value = i.find('a').attrs['href'].split('/')[-1].strip('GetDataset?ID=')
            else:
                value = i.text
            cur_td_elements.append(value)
        table_as_dict[cur_id] = dict(zip(header_names, cur_td_elements))
        cur_id += 1
        
    return pd.DataFrame(table_as_dict).T

def get_page_sources(link, waitTime=5, fullDump=True):
    # ensure chromedriver.exe is in PATH, or, pass in the file path as an argument below
    d = webdriver.Chrome()
    d.get(link)
    time.sleep(waitTime)
    pager_element = d.find_element_by_class_name('pager')
    page_size_element = pager_element.find_element_by_class_name('pagesize')
    select_object = Select(page_size_element)
    time.sleep(waitTime)
    select_object.select_by_value('1000')
    num_pages = int(pager_element.find_element_by_class_name('pagedisplay').get_attribute('value').split("/")[-1])
    
    full_dataframe = pd.DataFrame()

    for i in range(num_pages):
        soup = BeautifulSoup(d.page_source, features='lxml')
        full_dataframe = pd.concat([full_dataframe, web_table_into_dataframe(soup)])
        time.sleep(1.5)
        pager_element.find_elements_by_class_name('next')[0].click()

    full_dataframe = full_dataframe.drop_duplicates()
    full_dataframe.to_csv('full_metadata_of_PX.tsv', index=False, sep='\t')
    print("Web scraping complete.")

# get all databases from ProteomeXchange
get_page_sources('http://proteomecentral.proteomexchange.org/cgi/GetDataset')
full_dataframe = pd.read_csv('full_metadata_of_PX.tsv', sep='\t')

# filter the full dataframe for human, pediatric cancer datasets
full_dataframe['Species'] = full_dataframe['Species'].str.lower()
full_dataframe['Title'] = full_dataframe['Title'].str.lower()
full_dataframe['Keywords'] = full_dataframe['Keywords'].str.lower()

filtered_df = full_dataframe[full_dataframe['Species'].str.contains('homo sapiens') | full_dataframe['Species'].str.contains('human')]

pediatric_cancer_k_list = ['child', 'pediatric', 'paediatric', 'leukemia', 'medulloblastoma', 'astrocytoma', 'glioma', 'retinoblastoma', 'ewing'
                          , 'osteosarcoma', 'lymphoma', 'all', 'aml', 'rhabdomyosarcoma', 'wilm', 'nephroblastoma', 'glioblastoma', 'ependymoma', 'atrt'
                          , 'oligodendroglioma', 'pnet', 'pineoblastoma', 'rhabdoid', 'craniopharyngioma', 'dnet', 'schwannoma', 'meningioma', 
                           'choroid plexus', 'chordoma', 'neuroma', 'teratoma', 'youth', 'teen', 'infant', 'babies', 'choriocarinoma', 'bone cancer', 'neuroblastoma', 'embryonal', 'neurilemmoma']

def keyword_matching(data, column2look=['Title', 'Keywords'], keyword_list=pediatric_cancer_k_list):
    binary_matches = pd.DataFrame()
    for col in column2look:
        binary_matches[col] = data[col].str.contains((r'\b(?:{})\b'.format('|'.join(keyword_list))))
    return binary_matches
    
filtered_df = filtered_df[keyword_matching(filtered_df).sum(axis=1) > 0]
filtered_df.to_csv('filtered_metadata_of_PX.tsv', index=False, sep='\t')
print("Dataset filtering complete.")