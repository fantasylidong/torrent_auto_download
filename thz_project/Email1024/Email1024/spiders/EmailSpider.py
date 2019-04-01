# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy import Request
from ..items import Email1024Item
from ..settings import SPIDER_NAME, ROOT_URL, BLOCK_INFO, MAX_PAGES,AUTHOR_NAME


class EmailspiderSpider(scrapy.Spider):
    name = SPIDER_NAME
    root_url = ROOT_URL
    max_pages = MAX_PAGES
    page = 1
    def start_requests(self):
        for key in BLOCK_INFO:
            request_url = self.root_url + "forum-" + str(key) + "-1.html"
            yield Request(url=request_url, callback=self.parse_block_page, meta={'block_name': BLOCK_INFO[key]})


    def parse_block_page(self, response):
        content = response.body
        response_url_list = response.url.split('-')
        page_num = response_url_list[2].split('.')[0]
        soup = BeautifulSoup(content, "html.parser")
        block_name = response.meta['block_name']
        temp_list = soup.find_all('a', attrs={'href': True, 'onclick': True, 'id': False, 'class': 's xst'})
        for item in temp_list:
            if "html" not in item['href']:
                continue
            topic_id = item['href'].split('-')[1]
            if int(topic_id) < 1810000:
                continue
            topic_url = self.root_url + item['href']
            topic_title = item.text
            yield Request(url=topic_url, callback=self.parse_poster_page,
                          meta={'topic_id': topic_id, 'block_name': block_name, 'topic_title': topic_title})
        if int(page_num) < self.max_pages:
            cur_url = response.url
            num = 0 - len(response_url_list[2])
            next_url = cur_url[:num] + str(int(page_num) + 1) + '.html'
            yield Request(url=next_url, callback=self.parse_block_page, meta={'block_name': block_name}, dont_filter=True)

    def parse_poster_page(self, response):
        content = response.body
        soup = BeautifulSoup(content, "html.parser")
        topic_id = response.meta['topic_id']
        block_name = response.meta['block_name']
        topic_title = response.meta['topic_title']
        topic_url = response.url
        print(topic_title)
        img_list = soup.find_all('img', attrs={'border': 0, 'file': True})
        topic_img_list = list()
        image_count = 0
        for item in img_list:
            if image_count < 6:
                if 'file' in item.attrs:
                    topic_img_list.append(item['file'])
                image_count = image_count + 1
            else:
                break
        b_list = soup.find_all('strong')
        a_list = soup.find_all('a', attrs={'onclick': "showWindow('imc_attachad', this.href)"})
        author_name=''
        for item in b_list :
            for key in AUTHOR_NAME:
                if key not in item.text:
                    continue
                else:
                    author_name = key
        if len(author_name) == 0:
            return
        topic_torrent_url = ""
        for item in a_list:
                idtorr=item['href'].split('=')[1]
                topic_torrent_url = ROOT_URL+'/imc_attachad-ad.html?aid='+item['href'].split('=')[1]
        if topic_torrent_url != "":
            yield Request(url=topic_torrent_url, callback=self.parse_torrent_page,
                          meta={'topic_title': topic_title,
                                'topic_img_list': topic_img_list,
                                'topic_url': topic_url,
                                'topic_id': topic_id,
                                'block_name': block_name,
                                'author_name': author_name,
                                'dont_filter' : True,
                                'idtorr': idtorr})

    def parse_torrent_page(self, response):
        content = response.body
        topic_title = response.meta['topic_title']
        soup = BeautifulSoup(content, "html.parser")
        topic_id = response.meta['topic_id']
        topic_url = response.meta['topic_url']
        topic_img_url = response.meta['topic_img_list']
        block_name = response.meta['block_name']
        author_name= response.meta['author_name']
        idtorr = response.meta['idtorr']
        torrent_download_url = ROOT_URL+'forum.php?mod=attachment&aid='+idtorr

        fileItem = Email1024Item()
        fileItem['topic_title'] = topic_title
        fileItem['topic_id'] = topic_id
        fileItem['topic_url'] = topic_url
        fileItem['block_name'] = block_name
        fileItem['topic_img_url'] = topic_img_url
        fileItem['author_name']= author_name
        urlList = [torrent_download_url]
        for img_url in topic_img_url:
            urlList.append(img_url)
        fileItem['file_urls'] = urlList
        return fileItem
