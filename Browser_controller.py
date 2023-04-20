import json
import requests
from bs4 import BeautifulSoup
import re
import os
import getpass
import pickle
import time

while True:
    username=getpass.getuser()
    filename=r'%s.pk' % (username)
    try:
        with open (filename, 'rb') as file:
            emp_blacklist=pickle.load(file)
    except FileNotFoundError:
        emp_blacklist=dict()
    non_listed_url=dict()
    try:
        response = requests.get('http://localhost:9222/json')
        tabs = json.loads(response.content.decode())
        for tab in tabs:
            url = tab['url']
            tab_id=tab['id']
            if url != 'null':
                try:
                    link_list=emp_blacklist['allow predefined sites']
                    url_not_in_list = True
                    for link in link_list:
                        if link.lower() in url.lower():
                            url_not_in_list = False
                            try:
                                non_listed_url.pop(url)
                            except:
                                pass
                            break      
                    if url_not_in_list:
                        non_listed_url[url]=tab_id
                except:
                    non_listed_url[url]=tab_id
    except:
        pass
    try:
        key_word_list=emp_blacklist['allow access on keyword']
        try:
            for url in non_listed_url.keys():
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                html=soup.prettify()
                key_word_in_url=True
                for key_word in key_word_list:
                    if re.findall(key_word.lower(), html.lower()):
                        key_word_in_url=False
                        non_listed_url.pop(url)
                if key_word_in_url:
                    tab_id=non_listed_url[url]
                    requests.post(f'http://localhost:9222/json/close/{tab_id}')
                    non_listed_url.pop(url)
        except:
            pass
    except:
        pass
    try:
        forbidden_word=emp_blacklist['forbidden word restriction']
        try:
           for url in non_listed_url.keys():
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                html=soup.prettify()
                forbidden_word_in_url=True
                for word in forbidden_word:
                    if re.findall(word.lower(), html.lower()):
                        tab_id=non_listed_url[url]
                        requests.post(f'http://localhost:9222/json/close/{tab_id}')
                        non_listed_url.pop(url)
        except:
            pass     
    except:
        pass
    try:
        if len(key_word_list) >= 0:
            pass
    except:
        try:
            if link_list:
                for url in non_listed_url.keys(): 
                    link_list=emp_blacklist['allow predefined sites']
                    url_not_in_list = True
                    for link in link_list:
                        if link.lower() in url.lower():
                            url_not_in_list = False
                            try:
                                non_listed_url.pop(url)
                            except:
                                pass
                            break      
                    if url_not_in_list:
                        tab_id=non_listed_url[url]
                        requests.post(f'http://localhost:9222/json/close/{tab_id}')
        except:
            pass
    time.sleep(3)
