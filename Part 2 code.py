from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

#function to extract description
def get_description(soup):
    
    try:
        description=soup.find("span",attrs={"id",'productTitle'})
        description_value=description.text
        description_string=description_value.strip()

    except AttributeError:
        description_string=""

    return description_string

#function to get ASIN
def get_ASIN(soup):

    try:
        asin=soup.find("td",attrs={"class","a-size-base prodDetAttrValue"}).string.strip()
    
    except AttributeError:
        asin=""

    return asin

#function to get product description
def get_proddescription(soup):

    try:      
        prod_desc=soup.find("span",attrs={"class","a-list-item"}).string.strip()

    except AttributeError:
        prod_desc=""

    return prod_desc

#function to get manufacturer name
def get_manufacturer(soup):

    try:
        manufacturer=soup.find("a",attrs={"id","bylineInfo"})

    except AttributeError:
        manufacturer=""

    return manufacturer

if __name__=='__main__':

    hdr=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0','Accept-Language': 'en-US, en;q=0.5'})
    df=pd.read_csv('amazon_data.csv')
    df=df['product URL']
    url_list=[]
    
    d={"Description":[],"ASIN":[],"Product Description":[],"Manufacturer":[]}
    
    for URL in df:
        webpage=requests.get(URL,headers=hdr)
        soup=BeautifulSoup(webpage.content,"html.parser")
        d["Description"].append(get_description(soup))
        d["ASIN"].append(get_ASIN(soup))
        d['Product Description'].append(get_proddescription(soup))
        d["Manufacturer"].append(get_manufacturer(soup))
    
    amazon_df=pd.DataFrame.from_dict(d)
    amazon_df.to_csv("amazon_data_2.csv",header=True, index=False)