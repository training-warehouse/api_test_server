from urllib.parse import quote
import time
import random

from lxml import etree

import requests

search = '活力测度'

random_range = list(range(4, 16))
detail_range = list(range(1, 3))
page = 23
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Host': 'xueshu.baidu.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-platform': "Windows"
}

cookies = {
    'BAIDUID': 'AB5E68512CC9AF010AB0D7CF1E39221B:SL=0:NR=10:FG=1',
    'BAIDUID_BFESS': 'AB5E68512CC9AF010AB0D7CF1E39221B:SL=0:NR=10:FG=1',
    'BA_HECTOR': '8l8l85042gah8gakl91h5qor70r',
    'BCLID_BFESS': '12546445818386479153',
    'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
    'BDRCVFR[w2jhEs_Zudc]': 'mbxnW11j9Dfmh7GuZR8mvqV',
    'BDSFRCVID_BFESS': 'TiKOJeC62AZSU-3D5V8HUwLxujrZdOnTH6ao7etx23KqJQLnoKmlEG0PVU8g0KAb9Ib-ogKKBmOTHnuF_2uxOjjg8UtVJeC6EG0Ptf8g0f5'
}

titles = ['社区级公共服务设施活力测度及影响因素研究']
while 1:
    print(f'开始抓取{page + 1}页...')
    url = f'https://xueshu.baidu.com/s?wd={quote(search)}&pn={page * 10}&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&sc_hit=1'
    response = requests.get(url, headers=headers, cookies=cookies)
    html = etree.HTML(response.text)
    a_list = html.xpath('//div[@class="result sc_default_result xpath-log"]/div/h3/a')

    for a_node in a_list:
        href = a_node.attrib['href']

        detail = requests.get(href, headers=headers, cookies=cookies)
        detail_html = etree.HTML(detail.text)

        try:
            # 排除书籍
            title = detail_html.xpath('//div[@id="dtl_l"]/div[@class="main-info"]/h3/a/text()')[0].strip()
        except:
            continue
        if title in titles:
            break

        print(title)
        description = next(iter(detail_html.xpath(
            '//div[@id="dtl_l"]/div[@class="main-info"]/div[@class="c_content"]/div[@class="abstract_wr"]/p[@data-sign]/text()'
        )), '')
        keyword_nodes = detail_html.xpath(
            '//div[@id="dtl_l"]/div[@class="main-info"]/div[@class="c_content"]/div[@class="kw_wr"]/p/span/a'
        )
        try:
            keywords = '; '.join(n.text for n in keyword_nodes)
        except:
            keywords = ''

        with open('xueshu.txt', 'a') as f:
            f.write(f'{title}\n{keywords}\n{description}\n{href}\n\n')

        time.sleep(random.choice(detail_range))

    time.sleep(random.choice(random_range))
    page += 1
