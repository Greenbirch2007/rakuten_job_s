

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
    html = driver.page_source
    return html

def to_fetch_firstUrl(url):
    # 为Chrome配置无头模式


    driver.get(url)
    html = driver.page_source
    selector = etree.HTML(html)
    programe_language = selector.xpath('//*[@id="container"]/section[1]/div/div[1]/div/ul/li/a/text()')
    programe_language_url = selector.xpath('//*[@id="container"]/section[1]/div/div[1]/div/ul/li/a/@href')
    return programe_language,programe_language_url
#
# 可以尝试第二种解析方式，更加容易做计算
# 净收入 d1距离最近，d5最远
# 对于脚本的符合太大！所以季度和年度数据暂时不加入板块
def parse_onePage(html):

    selector = etree.HTML(html)
    job_title = selector.xpath('//*[@id="search-results-list"]/ul/li/a/h2/text()')
    job_url = selector.xpath('//*[@id="search-results-list"]/ul/li/a/@href')
    return job_title,job_url







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





# firstone,firstone_1,firstone_2,firstone_3

if __name__ == '__main__':



    url = "https://corp.rakuten.co.jp/careers/engineer/"
    programe_language, programe_language_url = to_fetch_firstUrl(url)

    response = requests.get(url)
    selector = etree.HTML(response.text)
    job_details= selector.xpath('//*[@id="richTextArea.jobPosting.jobDescription-input--uid10-input"]')

    language_summary = {}
    language_summary_list = []
    programe_language_summary = {}

    summary = []
    one_job_summary = []

    jobs_summary = {}
    for i1,i2 in zip(programe_language,programe_language_url):

        html  = use_selenium_headless(i2)
        selector = etree.HTML(html)
        employee_demand = selector.xpath('//*[@id="search-results"]/h1/text()')
        f_employee_demand = ["".join(re.findall("\d+", employee_demand[0]))]
        total_pages = selector.xpath('//*[@id="pagination-bottom"]/div[1]/span/text()')
        time.sleep(2)
        try:

            f_total_pages = ["".join(re.findall("\d+", total_pages[0]))]
        except IndexError:
            f_total_pages = [0]



        job_title, job_url = parse_onePage(html)


        for one_job_title,one_job_url in zip(job_title,job_url):
            one_job = {}
            one_job["programe_language"] = i1
            one_job["job_title"] = one_job_title
            one_job["job_url"] = one_job_url
            print(one_job)
            one_job_summary.append(one_job)

        programe_language_summary["{0}".format(i1)] = f_employee_demand[0]
        if language_summary_list ==[]:
            language_summary_list.append(programe_language_summary)


        # 开始翻页
        for item in range(int(f_total_pages[0])-1):
            time.sleep(2)

            driver.find_element_by_xpath('//*[@id="pagination-bottom"]/div[2]/a[2]').click()
            html = driver.page_source

            job_title, job_url = parse_onePage(html)


            for one_job_title, one_job_url in zip(job_title, job_url):
                one_job = {}
                one_job["programe_language"] = i1
                one_job["job_title"] = one_job_title
                one_job["job_url"] = one_job_url
                print(one_job)
                one_job_summary.append(one_job)

    language_summary["language_summary"] = language_summary_list
    jobs_summary["jobs_summary"] = one_job_summary
    summary.append(language_summary)
    summary.append(jobs_summary)

    writeinto_jsonfile("rakuten_job_urls.json",summary)




