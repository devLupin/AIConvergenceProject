# https://pgh268400.tistory.com/260

import requests
from bs4 import BeautifulSoup
import time
import os
from os.path import getsize
import csv
 
def image_download(title, link, log_csv):
    headers = {
    "Connection" : "keep-alive",
    "Cache-Control" : "max-age=0",
    "sec-ch-ua-mobile" : "?0",
    "DNT" : "1",
    "Upgrade-Insecure-Requests" : "1",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site" : "none",
    "Sec-Fetch-Mode" : "navigate",
    "Sec-Fetch-User" : "?1",
    "Sec-Fetch-Dest" : "document",
    "Accept-Encoding" : "gzip, deflate, br",
    "Accept-Language" : "ko-KR,ko;q=0.9"
    }
 
    res = requests.get(link, headers=headers)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
 
    image_download_contents = soup.select("div.appending_file_box ul li")
    for li in image_download_contents:
        img_tag = li.find('a', href=True)
        img_url = img_tag['href']
 
        file_ext = img_url.split('.')[-1]
        savename = img_url.split("no=")[2]
        headers['Referer'] = link
        
        try:
            response = requests.get(img_url, headers=headers)
        except requests.exceptions.ChunkedEncodingError:
            continue
        
        path = f"crawled images/{savename}"
        file_size = len(response.content)
 
        if os.path.isfile(path) and getsize(path) != file_size:
            if getsize(path) != file_size:
                file = open(path + "[1]", "wb")
                file.write(response.content)
                file.close()
                
                with open(log_csv, 'a') as f:
                    wr = csv.writer(f)
                    wr.writerow([title, link, savename])
            else:
                pass

        else:
            file = open(path , "wb")
            file.write(response.content)
            file.close()
            
            with open(log_csv, 'a') as f:
                wr = csv.writer(f)
                wr.writerow([title, link, savename])
 
def image_check(text):
    text = str(text)
    if "icon_pic" in text:
        return True
    else:
        return False

        
def main():
    log_csv = 'log.csv'
    if not os.path.exists(log_csv):
        with open(log_csv, 'w') as f:
            wr = csv.writer(f)
            wr.writerow(['title', 'link', 'file name'])
            
    BASE_URL = "https://gall.dcinside.com/board/lists/?id="
    # 여자 연예인, 남자 연예인, 히트, 베스트, 인방, 스트리머
    ID_LIST = ["w_entertainer", "m_entertainer_new1", "hit", "dcbest", "ib_new2", "stream_new1&page=1"]
    NUM_NOTICE = [5, 4, 5, 4, 4, 4]
    
    headers = {
    "Connection" : "keep-alive",
    "Cache-Control" : "max-age=0",
    "sec-ch-ua-mobile" : "?0",
    "DNT" : "1",
    "Upgrade-Insecure-Requests" : "1",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site" : "none",
    "Sec-Fetch-Mode" : "navigate",
    "Sec-Fetch-User" : "?1",
    "Sec-Fetch-Dest" : "document",
    "Accept-Encoding" : "gzip, deflate, br",
    "Accept-Language" : "ko-KR,ko;q=0.9"
              }
 
    print(f"[*] Image crawling start")
    
    while(True):
        for i in range(len(ID_LIST)):
            cur_board = BASE_URL + ID_LIST[i]
            cur_num_notice = NUM_NOTICE[i]
            
            res = requests.get(cur_board, headers=headers)
            
            if res.status_code == 200:
                html = res.text
                soup = BeautifulSoup(html, 'html.parser')

                doc = soup.select("td.gall_tit > a:nth-child(1)")
                for i in range(cur_num_notice, len(doc)):   # remove notice
                    link = "https://gall.dcinside.com" + doc[i].get("href")
                    title = doc[i].text.strip()
                    image_insert = image_check(doc[i])

                    print(title)

                    if(image_insert == True):   # if include images
                        image_download(title, link, log_csv)
                    
                    break
                
                time.sleep(5)

if __name__ == '__main__':
    main()