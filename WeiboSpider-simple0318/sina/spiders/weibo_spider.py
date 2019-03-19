#!/usr/bin/env python
# encoding: utf-8
import re
from lxml import etree
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from sina.items import WeiboItem, InformationItem, RelationshipsItem, CommentItem
from sina.spiders.utils import time_fix
import time


class WeiboSpider(Spider):
    name = "weibo_spider"
    base_url = "https://weibo.cn"

    def __init__(self,user_id_list = "",weibo_id_list = "",*args, **kwargs):
        super(WeiboSpider, self).__init__(*args, **kwargs)
        self.user_id_list = user_id_list.split(';')#元组不好传递，所以转化为了字符串，在此拆分为元组
        self.weibo_id_list = weibo_id_list.split(';')
        # print('获取到了待爬用户列表,人数为',len(self.user_id_list),'微博数为',len(self.weibo_id_list))

    def start_requests(self):
        # start_uids = [
        #     # '2010924075'
        #     # '5659628156'
        #     '2803301701',  # 人民日报
        #     # '1699432410'  # 新华社
        # ]
        # for uid in start_uids:
        #     yield Request(url="https://weibo.cn/%s/info" % uid, callback=self.parse_information)
        for uid in self.user_id_list:
            if uid != "":
                print('当前将要开始爬取用户的id为', uid)
                yield Request(url="https://weibo.cn/%s/info" % uid, callback=self.parse_information,meta={'is_need_all_info':1})

        for weibo_id in self.weibo_id_list:
            if weibo_id != "":
                print('当前将要开始爬取10条微博用户的id为', weibo_id)
                yield Request(url=self.base_url + '/{}/profile?page=1'.format(weibo_id),
                              callback=self.parse_weibo_page1,
                              priority=1)
                # print('当前将要开始爬取微博的id为', weibo_id)
                # weibo_id = weibo_id.split('_')
                # yield Request(url="https://weibo.cn/attitude/%s?uid=%s" % (weibo_id[1],weibo_id[0]), callback=self.parse_specific_weibo)



    def parse_specific_weibo(self,response):
        selector = Selector(response)
        text = ";".join(selector.xpath('body/div[not (contains(string(),"原文")) and contains(string(),"赞")]//text()').extract())
        daily_weibo_num = WeiboItem()
        daily_weibo_num['weibo_id']= None
        daily_weibo_num['like_num'] = 0
        daily_weibo_num['repost_num'] = 0
        daily_weibo_num['comment_num'] = 0
        daily_weibo_num['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        like_num = re.findall('赞\[(\d+)\]', text)
        repost_num = re.findall('转发\[(\d+)\]', text)
        comment_num = re.findall('评论\[(\d+)\]', text)
        user_weibo_id = re.search(r'/attitude/(.*?)\?uid=(\d+)',response.url)
        daily_weibo_num['weibo_id'] = '{}_{}'.format(user_weibo_id.group(2), user_weibo_id.group(1))
        if like_num:
            daily_weibo_num['like_num'] = int(like_num[0])
        if repost_num:
            daily_weibo_num['repost_num'] = int(repost_num[0])
        if comment_num:
            daily_weibo_num['comment_num'] = int(comment_num[0])
        yield daily_weibo_num

    def parse_information(self, response):
        """ 抓取个人信息 """
        information_item = InformationItem()
        #初始化为None
        # 所在省 gender,province,city,brief_introduction,birthday,weibos_num,follows_num,fans_num,
        # sex_orientation,sentiment,vip_level,authentication,person_url,crawl_time,labels

        information_item['_id'] = None
        information_item['nick_name'] = None
        information_item['gender'] = None
        information_item['province'] = None
        information_item['city'] = None
        information_item['brief_introduction'] = None
        information_item['weibo_num'] = None
        information_item['follows_num'] = None
        information_item['fans_num'] = None
        information_item['sex_orientation'] = None
        information_item['sentiment'] = None
        information_item['vip_level'] = None
        information_item['authentication'] = None
        information_item['person_url'] = None
        information_item['crawl_time'] = None
        information_item['labels'] = None
        information_item["portrait"] = None
        information_item["birthday"] = None


        information_item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        selector = Selector(response)
        information_item['_id'] = re.findall('(\d+)/info', response.url)[0]
        text1 = ";".join(selector.xpath('body/div[@class="c"]//text()').extract())  # 获取标签里的所有text()
        portrait = selector.xpath('//body/div//img[@alt="头像"]/@src').extract()#//body/div/a/img[@alt="头像"]/@src
        nick_name = re.findall('昵称;?[：:]?(.*?);', text1)
        gender = re.findall('性别;?[：:]?(.*?);', text1)
        place = re.findall('地区;?[：:]?(.*?);', text1)
        briefIntroduction = re.findall('简介;?[：:]?(.*?);', text1)
        birthday = re.findall('生日;?[：:]?(.*?);', text1)
        sex_orientation = re.findall('性取向;?[：:]?(.*?);', text1)
        sentiment = re.findall('感情状况;?[：:]?(.*?);', text1)
        vip_level = re.findall('会员等级;?[：:]?(.*?);', text1)
        authentication = re.findall('认证;?[：:]?(.*?);', text1)
        labels = re.findall('标签;?[：:]?(.*?)更多>>', text1)
        if portrait and portrait[0]:
            information_item["portrait"] = portrait[0]
        if nick_name and nick_name[0]:
            information_item["nick_name"] = nick_name[0].replace(u"\xa0", "")
        if gender and gender[0]:
            information_item["gender"] = gender[0].replace(u"\xa0", "")
        if place and place[0]:
            place = place[0].replace(u"\xa0", "").split(" ")
            information_item["province"] = place[0]
            if len(place) > 1:
                information_item["city"] = place[1]
        if briefIntroduction and briefIntroduction[0]:
            information_item["brief_introduction"] = briefIntroduction[0].replace(u"\xa0", "")
        if birthday and birthday[0]:
            information_item['birthday'] = birthday[0]
        if sex_orientation and sex_orientation[0]:
            if sex_orientation[0].replace(u"\xa0", "") == gender[0]:
                information_item["sex_orientation"] = "同性恋"
            else:
                information_item["sex_orientation"] = "异性恋"
        if sentiment and sentiment[0]:
            information_item["sentiment"] = sentiment[0].replace(u"\xa0", "")
        if vip_level and vip_level[0]:
            information_item["vip_level"] = vip_level[0].replace(u"\xa0", "")
        if authentication and authentication[0]:
            information_item["authentication"] = authentication[0].replace(u"\xa0", "")
        if labels and labels[0]:
            information_item["labels"] = labels[0].replace(u"\xa0", ",").replace(';', '').strip(',')
        request_meta = response.meta
        request_meta['item'] = information_item

        is_need_all_info = response.meta['is_need_all_info']
        print('is_need_all_info',is_need_all_info)
        if is_need_all_info == 1:
            yield Request(self.base_url + '/u/{}'.format(information_item['_id']),
                          callback=self.parse_further_information,
                          meta=request_meta, dont_filter=True, priority=1)
        else:
            information_item['weibo_num'] = 0
            information_item['follows_num'] = 0
            information_item['fans_num'] = 0
            yield information_item

    def parse_further_information(self, response):
        text = response.text
        information_item = response.meta['item']
        weibo_num = re.findall('微博\[(\d+)\]', text)
        if weibo_num:
            information_item['weibo_num'] = int(weibo_num[0])
        follows_num = re.findall('关注\[(\d+)\]', text)
        if follows_num:
            information_item['follows_num'] = int(follows_num[0])
        fans_num = re.findall('粉丝\[(\d+)\]', text)
        if fans_num:
            information_item['fans_num'] = int(fans_num[0])
        yield information_item

        # 获取该用户微博
        yield Request(url=self.base_url + '/{}/profile?page=1'.format(information_item['_id']),
                      callback=self.parse_weibo,
                      priority=1)

        # 获取关注列表
        # yield Request(url=self.base_url + '/{}/follow?page=1'.format(information_item['_id']),
        #               callback=self.parse_follow,
        #               dont_filter=True)
        # 获取粉丝列表
        yield Request(url=self.base_url + '/{}/fans?page=1'.format(information_item['_id']),
                      callback=self.parse_fans,
                      dont_filter=True)

    def parse_weibo(self, response):
        if response.url.endswith('page=1'):
            # 如果是第1页，一次性获取后面的所有页
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                if all_page > 2: # 设置最多爬取10页，100条
                    all_page = 2
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse_weibo, dont_filter=True, meta=response.meta)
        """
        解析本页的数据
        """
        print()
        tree_node = etree.HTML(response.body)
        weibo_nodes = tree_node.xpath('//div[@class="c" and @id]')
        for weibo_node in weibo_nodes:
            try:
                weibo_item = WeiboItem()
                weibo_item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                weibo_repost_url = weibo_node.xpath('.//a[contains(text(),"转发[")]/@href')[0]
                user_weibo_id = re.search(r'/repost/(.*?)\?uid=(\d+)', weibo_repost_url)
                weibo_item['weibo_url'] = 'https://weibo.com/{}/{}'.format(user_weibo_id.group(2),
                                                                           user_weibo_id.group(1))
                weibo_item['user_id'] = user_weibo_id.group(2)
                weibo_item['_id'] = '{}_{}'.format(user_weibo_id.group(2), user_weibo_id.group(1))
                create_time_info = weibo_node.xpath('.//span[@class="ct"]/text()')[-1]
                if "来自" in create_time_info:
                    weibo_item['created_at'] = time_fix(create_time_info.split('来自')[0].strip())
                else:
                    weibo_item['created_at'] = time_fix(create_time_info.strip())
                #原文picurl
                last_pic_url = weibo_node.xpath('div[contains(string(),"原文")]/a/img[@alt="图片" and @class = "ib"]/@src')
                weibo_item['last_pic_url'] = ','.join(last_pic_url)
                #my
                pic_url = weibo_node.xpath('div[not(contains(string(),"原文"))]/a/img[@alt="图片" and @class = "ib"]/@src')
                weibo_item['pic_url'] = ','.join(pic_url)
                like_num = weibo_node.xpath('.//a[contains(text(),"赞[")]/text()')[-1]
                weibo_item['like_num'] = int(re.search('\d+', like_num).group())

                repost_num = weibo_node.xpath('.//a[contains(text(),"转发[")]/text()')[-1]
                weibo_item['repost_num'] = int(re.search('\d+', repost_num).group())

                comment_num = weibo_node.xpath(
                    './/a[contains(text(),"评论[") and not(contains(text(),"原文"))]/text()')[-1]
                weibo_item['comment_num'] = int(re.search('\d+', comment_num).group())

                weibo_content_node = weibo_node.xpath('.//span[@class="ctt"]')[0]

                # 检测由没有阅读全文:
                all_content_link = weibo_content_node.xpath('.//a[text()="全文"]')
                if all_content_link:
                    all_content_url = self.base_url + all_content_link[0].xpath('./@href')[0]
                    yield Request(all_content_url, callback=self.parse_all_content, meta={'item': weibo_item},
                                  priority=1)

                else:
                    all_content = weibo_content_node.xpath('string(.)').replace('\u200b', '').strip()
                    weibo_item['content'] = all_content[0:]
                    yield weibo_item

                # 抓取该微博的评论信息
                comment_url = self.base_url + '/comment/' + weibo_item['weibo_url'].split('/')[-1] + '?page=1'
                yield Request(url=comment_url, callback=self.parse_comment, meta={'weibo_url': weibo_item['weibo_url']})

            except Exception as e:
                self.logger.error(e)


    def parse_weibo_page1(self, response):
        """
        解析本页的数据
        """
        tree_node = etree.HTML(response.body)
        weibo_nodes = tree_node.xpath('//div[@class="c" and @id]')
        for weibo_node in weibo_nodes:
            try:
                weibo_item = WeiboItem()
                weibo_item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                weibo_repost_url = weibo_node.xpath('.//a[contains(text(),"转发[")]/@href')[0]
                user_weibo_id = re.search(r'/repost/(.*?)\?uid=(\d+)', weibo_repost_url)
                weibo_item['weibo_url'] = 'https://weibo.com/{}/{}'.format(user_weibo_id.group(2),
                                                                           user_weibo_id.group(1))
                weibo_item['user_id'] = user_weibo_id.group(2)
                weibo_item['_id'] = '{}_{}'.format(user_weibo_id.group(2), user_weibo_id.group(1))
                create_time_info = weibo_node.xpath('.//span[@class="ct"]/text()')[-1]
                if "来自" in create_time_info:
                    weibo_item['created_at'] = time_fix(create_time_info.split('来自')[0].strip())
                else:
                    weibo_item['created_at'] = time_fix(create_time_info.strip())
                # 原文picurl
                last_pic_url = weibo_node.xpath('div[contains(string(),"原文")]/a/img[@alt="图片" and @class = "ib"]/@src')
                weibo_item['last_pic_url'] = ','.join(last_pic_url)
                # my
                pic_url = weibo_node.xpath('div[not(contains(string(),"原文"))]/a/img[@alt="图片" and @class = "ib"]/@src')
                weibo_item['pic_url'] = ','.join(pic_url)
                like_num = weibo_node.xpath('.//a[contains(text(),"赞[")]/text()')[-1]
                weibo_item['like_num'] = int(re.search('\d+', like_num).group())

                repost_num = weibo_node.xpath('.//a[contains(text(),"转发[")]/text()')[-1]
                weibo_item['repost_num'] = int(re.search('\d+', repost_num).group())

                comment_num = weibo_node.xpath(
                    './/a[contains(text(),"评论[") and not(contains(text(),"原文"))]/text()')[-1]
                weibo_item['comment_num'] = int(re.search('\d+', comment_num).group())

                weibo_content_node = weibo_node.xpath('.//span[@class="ctt"]')[0]

                # 检测由没有阅读全文:
                all_content_link = weibo_content_node.xpath('.//a[text()="全文"]')
                if all_content_link:
                    all_content_url = self.base_url + all_content_link[0].xpath('./@href')[0]
                    yield Request(all_content_url, callback=self.parse_all_content, meta={'item': weibo_item},
                                  priority=1)

                else:
                    all_content = weibo_content_node.xpath('string(.)').replace('\u200b', '').strip()
                    weibo_item['content'] = all_content[0:]
                    yield weibo_item

                # 抓取该微博的评论信息
                comment_url = self.base_url + '/comment/' + weibo_item['weibo_url'].split('/')[-1] + '?page=1'
                # yield Request(url=comment_url, callback=self.parse_comment, meta={'weibo_url': weibo_item['weibo_url']})

            except Exception as e:
                self.logger.error(e)

    def parse_all_content(self, response):
        # 有阅读全文的情况，获取全文
        tree_node = etree.HTML(response.body)
        weibo_item = response.meta['item']
        content_node = tree_node.xpath('//div[@id="M_"]//span[@class="ctt"]')[0]
        all_content = content_node.xpath('string(.)').replace('\u200b', '').strip()
        weibo_item['content'] = all_content[0:]
        yield weibo_item

    def parse_follow(self, response):
        """
        抓取关注列表
        """
        # 如果是第1页，一次性获取后面的所有页
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                if all_page > 5:
                    all_page = 5
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse_follow, dont_filter=True, meta=response.meta)
        selector = Selector(response)
        urls = selector.xpath('//a[text()="关注他" or text()="关注她" or text()="取消关注"]/@href').extract()
        uids = re.findall('uid=(\d+)', ";".join(urls), re.S)
        ID = re.findall('(\d+)/follow', response.url)[0]
        for uid in uids:
            relationships_item = RelationshipsItem()
            relationships_item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            relationships_item["fan_id"] = ID
            relationships_item["followed_id"] = uid
            relationships_item["_id"] = ID + '-' + uid
            yield relationships_item

    def parse_fans(self, response):
        """
        抓取粉丝列表
        """
        # 如果是第1页，一次性获取后面的所有页
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                if all_page > 5:
                    all_page = 5
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse_fans, dont_filter=True, meta=response.meta)
        selector = Selector(response)
        urls = selector.xpath('//a[text()="关注他" or text()="关注她" or text()="移除"]/@href').extract()
        uids = re.findall('uid=(\d+)', ";".join(urls), re.S)
        ID = re.findall('(\d+)/fans', response.url)[0]
        for uid in uids:
            relationships_item = RelationshipsItem()
            relationships_item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            relationships_item["fan_id"] = uid
            relationships_item["followed_id"] = ID
            relationships_item["_id"] = uid + '-' + ID
            yield relationships_item
            yield Request(url="https://weibo.cn/%s/info" % uid, callback=self.parse_information,meta={'is_need_all_info':0})


    def parse_comment(self, response):
        # 如果是第1页，一次性获取后面的所有页
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                if all_page > 5:
                    all_page = 5
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse_comment, dont_filter=True, meta=response.meta)
        selector = Selector(response)
        comment_nodes = selector.xpath('//div[@class="c" and contains(@id,"C_")]')
        for comment_node in comment_nodes:
            comment_user_url = comment_node.xpath('.//a[contains(@href,"/u/")]/@href').extract_first()
            if not comment_user_url:
                continue
            comment_item = CommentItem()
            comment_item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            comment_item['weibo_url'] = response.meta['weibo_url']
            comment_item['comment_user_id'] = re.search(r'/u/(\d+)', comment_user_url).group(1)
            comment_item['content'] = comment_node.xpath('.//span[@class="ctt"]').xpath('string(.)').extract_first()
            comment_item['_id'] = comment_node.xpath('./@id').extract_first()
            created_at = comment_node.xpath('.//span[@class="ct"]/text()').extract_first()
            comment_item['created_at'] = time_fix(created_at.split('\xa0')[0])
            yield comment_item


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl('weibo_spider')
    process.start()
