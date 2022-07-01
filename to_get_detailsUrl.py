

# -*- coding:utf-8 -*-

# rakuten_job_infos 2022.6.29
# rakuten_job_s
# https://corp.rakuten.co.jp/careers/engineer/
import datetime
import re
import time

import pymysql
import requests
from requests.exceptions import RequestException
import csv
from lxml import etree
import json
from selenium import webdriver
# 读取txt文件，请求页面－－>如果报错就下一个；没有报错就取值。最终加总即可

driver = webdriver.Chrome()





def use_selenium_headless(url):

    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    return html






def writeinto_detail(filename,data):
    with open(filename,"a",newline="",encoding="utf-8") as f:
        csv_out = csv.writer(f,delimiter=",")
        csv_out.writerow(data)

#
def writeinto_jsonfile(filename,list_data):
    with open(filename, 'w', encoding='utf-8') as fw:
        json.dump(list_data, fw, indent=4, ensure_ascii=False)

def readDatafile(filename):
    line_list = []
    with open(filename,"r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip("\n")
            line_list.append(line)
    return line_list


def readjsonfile(filename):
    with open(filename, 'r', encoding='utf-8') as fw:
        s = json.load(fw)
        return s



# firstone,firstone_1,firstone_2,firstone_3

if __name__ == '__main__':
    summary = []
    one_job_summary = []
    language_summary = {}
    result = readjsonfile("rakuten_job_urls.json")
    language_summary_list = [{'PHP': '55', 'Java': '237', 'Kotlin': '43', 'Swift': '20', 'Ruby': '44', 'Python': '159', 'JavaScript': '113', 'Go': '48', 'C': '117', 'C#': '9', 'C++': '22', 'Rust': '6'}]
    jobs_summary = {}

    for item in result[1].values():
        for it in item:

            one_job = {}
            one_job["programe_language"] = it["programe_language"]
            one_job["job_title"] = it["job_title"]

            html = use_selenium_headless(it["job_url"])
            selector = etree.HTML(html)
            job_details = selector.xpath('//*[@id="richTextArea.jobPosting.jobDescription-input--uid10-input"]//text()')
            f_job_details = "".join(job_details)
            one_job["job_details"] = f_job_details
            print(one_job)
            one_job_summary.append(one_job)



    language_summary["language_summary"] = language_summary_list
    jobs_summary["jobs_summary"] = one_job_summary
    summary.append(language_summary)
    summary.append(jobs_summary)
    writeinto_jsonfile("rakuten_job_urls_details.json",summary)



