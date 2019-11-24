#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 12:05:34 2019

@author: miaojunzhang
"""

#%%
from urllib import request
from bs4 import BeautifulSoup

#%%

# look at the current webpage and its components to deside which method to use
download_url = 'https://www.kanshula.com/book/zhiyinmusenanxun/3147601.shtml'

#%%
head = {}
head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
download_req = request.Request(url = download_url, headers = head)
download_response = request.urlopen(download_req)
download_html = download_response.read().decode('utf-8','ignore')
soup_texts = BeautifulSoup(download_html, 'lxml')
book_title = soup_texts.find('title').getText()

#%%
print(book_title)
#%%

next_chap = soup_texts.find('div', class_ = 'bottem2').find_all('a')[2].get('href')

print(next_chap)
#%%

texts = soup_texts.find('div', id = 'content').getText()
soup_text = BeautifulSoup(str(texts), 'lxml').text.replace('</p></body></html>', '')

#%%
print(soup_texts)

#%%

def get_book_from_web(web_page, chap_1_link, num_chapters, output_filename):
    
    head = {}
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    
    file_ = open(output_filename, 'w')
    #start from charpter 1
    current_url = chap_1_link

    for i in range(1, num_chapters+1):
        download_url = web_page + current_url
        download_req = request.Request(url = download_url, headers = head)
        download_response = request.urlopen(download_req)
        download_html = download_response.read().decode('utf-8','ignore')
        # get the soup
        soup_texts = BeautifulSoup(download_html, 'lxml')
        # current charpter info
        session_name = soup_texts.find('title').getText()
        texts = soup_texts.find('div', id = 'content').getText()
        session_text = BeautifulSoup(str(texts), 'lxml').text.replace('</p></body></html>', '')
        # write into file
        file_.write('\r'+session_name+'\r\n')
        file_.write(session_text)
        
        # get next charpter
        current_url = soup_texts.find('div', class_ = 'bottem2').find_all('a')[2].get('href')
        # end of loop
    
    file_.close()


#%%
get_book_from_web('https://www.kanshula.com', '/book/zhiyinmusenanxun/3147601.shtml', 102, '只因暮色难寻.txt') 

#%%
#end
