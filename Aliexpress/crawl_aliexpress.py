import urllib.request
from bs4 import BeautifulSoup
import bs4
import json
import requests
import urllib.request
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException

from selenium.webdriver import ActionChains
''' option install  '''
chrome_options = Options()  
# chrome_options.binary_location = "/usr/lib/chromium-browser/chromium-browser"
chrome_options.add_argument("--headless") # hide popup 
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')
# original link 
website = "https://best.aliexpress.com/?lan=en"
import sys

URL = []

def GetHomePage(website):         
    driver = webdriver.Chrome(executable_path = "C:\\Users\\tlhqu\\Downloads\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options)
    driver.get(website)
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME , 'categories')))
        print("Page is ready!")
    except TimeoutException:
        print ("Loading took too much")

    _page = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    

    categories_list=_page.findAll("dt",{"class":"cate-name"})
    print(len(categories_list))
    cate_name_url = []
    cate_url = []
    cate_id=[]    
    for cate in categories_list:
        cate_name_origin = cate.text.strip()
        cate_url.append(cate.a["href"])
    for url in cate_url:
        cate_name_url.append(url.split("/")[-1].replace('.html',''))
        cate_id.append(url.split("/")[-2])
    list_cate=dict(zip(cate_name_url,cate_url)) 
    for index in list_cate:             
        URL.append(list_cate[index] +"?trafficChannel=af" +"&page=")
    # creat dict include NameCate and Url 
    dict_cate = dict(zip(cate_name_url,URL))
    print(dict_cate)
    return dict_cate
def GetProductList(cate_url,max_num_pages):
      # url cate 
    list_product = []   
    url = "https:" + cate_url   
    for ele in range(1,max_num_pages+1):              
        driver = webdriver.Chrome(executable_path = "C:\\Users\\tlhqu\\Downloads\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options)   
        print(" >> ",url + str(ele) )
        driver.get(url + str(ele))
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME , 'product-container')))
            print("Page is ready!")
        except TimeoutException:
            print ("Loading took too much")
            continue
        scrolls = 6
        while True:
            scrolls -= 1
            time.sleep(1)
            driver.execute_script("window.scrollBy(0, 1080)")
            if scrolls < 0:
                break
        # Lấy html từ page source 
        _page = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
        scate_list = []
        scate_name_field = "Subcate_name"
        scate_link_field = "Subcate_link"
        sub = _page.findAll("ul",{"class":"child-menu"})[0].findAll("li")
        for i in sub: 
            scate_name = i.a.text.strip()
            scate_url = i.a["href"]
            # print(scate)
            scate_str = "{\"" + scate_name_field + "\":\"" + scate_name    + "\",\"" + scate_link_field + "\":\"" + scate_url +"\"}"
            scate_list.append(scate_str)
      


        post=_page.findAll("li",{"class":"list-item"})
        subcate_field = "Subcate"
        product_name_field = "ProName"
        product_url_field = "ProURL"
        product_price_current_field = "ProPriceCur"
        product_price_origin_field = "ProPriceOri"
        product_price_discount_field = "ProPriceDiscount"
        product_shipping_field = "ProShipping"
        product_rate_field = "ProRate"
        product_store_name_field = "ProStoreName"
        product_store_link_field = "ProStoreURL"
        product_img_link_field = "ProImgURL"
        product_img_name_field = "ProImgName"
        list_product_str = []
       
        for i in post:
            
            product_url = i.a["href"]
            product_title = i.text.strip()
            product_price_current = i.findAll("span",{"class":"price-current"})
            product_price_current = product_price_current[0].text.strip() if len(product_price_current)>0 else ""
            product_price_origin =  i.findAll("span",{"class":"price-original"})
            product_price_origin = product_price_origin[0].text.strip() if len(product_price_origin)>0 else ""         
            product_price_discount = i.findAll("span",{"class":"price-discount"})
            product_price_discount = product_price_discount[0].text.strip() if len( product_price_discount)>0 else ""
            product_shipping = i.findAll("span",{"class":"shipping-value"})
            product_shipping = product_shipping[0].text.strip() if len( product_shipping)>0 else ""
            product_rate = i.findAll("span",{"class":"rating-value"})
            product_rate = product_rate[0].text.strip() if len(product_rate)>0 else ""
            product_store = i.findAll("div",{"class":"item-store-wrap"})
            product_store = product_store[0].a.text.strip() if len(product_store)>0 else ""
            product_store_link = i.findAll("div",{"class":"item-store-wrap"})
            product_store_link = product_store_link[0].a['href'] if len(product_store_link)>0 else ""
            product_img_link = i.findAll("div",{"class":"product-img"})[0].a.img["src"].replace(".jpg_220x220xz","")
            product_img_name = i.findAll("div",{"class":"product-img"})[0].a.img["alt"]
            
            product_str = "{\"" + \
            product_name_field              + "\":\"" + product_title           + "\",\"" + \
            product_url_field               + "\":\"" + product_url             + "\",\"" + \
            product_price_current_field     + "\":\"" + product_price_current   + "\",\"" + \
            product_price_origin_field      + "\":\"" + product_price_origin    + "\",\"" + \
            product_price_discount_field    + "\":\"" + product_price_discount  + "\",\"" + \
            product_shipping_field          + "\":\"" + product_shipping        + "\",\"" + \
            product_rate_field              + "\":\"" + product_rate            + "\",\"" + \
            product_store_name_field        + "\":\"" + product_store           + "\",\"" + \
            product_store_link_field        + "\":\"" + product_store_link      + "\",\"" + \
            product_img_link_field          + "\":\"" + product_img_link        + "\",\"" + \
            product_img_name_field          + "\":\"" + product_img_name        + "\"}"

            # print(product_str)
            list_product_str.append(product_str)
        
            # list_subcate_str = 
        data_return = "{\"subcate\":[" + ",".join(scate_list) + "] ,\"data\":[" + ",".join(list_product_str) + "]}"
        # file = open("data.json", "w")
        # file.write(data_return)    

    # data = ", ".join(data.json)
 
        return data_return


# cate = "home-improvement"

# dict_cate = GetHomePage(website)
# cate_url = dict_cate[cate]  
# GetProductList(cate_url,max_num_pages=1)               
           









