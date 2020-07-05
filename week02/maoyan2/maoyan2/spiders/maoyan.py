import scrapy
import json

import scrapy
from furl import furl
from twisted.python.failure import Failure

from ..items import Maoyan2Item

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']


    def __init__(self):
        self.headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'text/plain, */*; q=0.01',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie': 'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593071575,1593071665,1593071730,1593074417; _lxsdk_cuid=172e9578d9fa8-090927fc871c2d-376b4502-1fa400-172e9578da0c8; _lxsdk=922FF590B88111EAA1F189776DB49E05F99C6E83AF29404581A9B8FFB1A3AA86; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593430757; __mta=44389915.1593267725645.1593267850174.1593430757827.4; _lxsdk_s=172ffdfce9b-3b9-0eb-5e3%7C%7C2; uuid_n_v=v1; iuuid=451797E0B9FD11EAA91D41CC1BE79A36DC721E79AA674189B10EEC240568152A; webp=true; ci=50%2C%E6%9D%AD%E5%B7%9E; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22172ffe08ace1d6-05b9eea18d0a5-2d604637-304500-172ffe08acf262%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22172ffe08ace1d6-05b9eea18d0a5-2d604637-304500-172ffe08acf262%22%7D'
        }

    def start_requests(self):
        base_url = "https://m.maoyan.com/ajax/moreClassicList"
        params = {
            'sortId': '1',
            'showType': '3',
            'limit': 100,
            'offset': 0,
            'optimus_uuid': '451797E0B9FD11EAA91D41CC1BE79A36DC721E79AA674189B10EEC240568152A',
            'optimus_risk_level': '71',
            'optimus_code': '10'
        }
        f_url = furl(base_url).add(params)
        
        yield scrapy.Request(f_url.url, meta={'f_url': f_url}, headers=self.headers, errback=self.errback)

    def parse(self, response):
        f_url = response.meta['f_url']
        try:
            if response.css("body > a div.classic-movie"):
                for a in response.css("body > a"):
                    movie_id = a.re_first(r"\d+")
                    div = a.css("div.classic-movie")
                    avatar = div.css("div.avatar img::attr(src)").get()
                    name_cn = div.css("div.movie-info div.title::text").get()
                    name_en = div.css("div.movie-info div.english-title::text").get()
                    type_ = div.css("div.movie-info div.actors::text").get()
                    show_time = div.css("div.movie-info div.show-info::text").get()
                    score = div.css("div.movie-score div.score span.grade::text").get()
                    no_score = div.css("div.movie-score div.no-score::text").get()
                    item = Maoyan2Item()
                    item['movie_id'] = movie_id
                    item['name_cn'] = name_cn
                    item['name_en'] = name_en
                    item['type'] = type_
                    item['show_time'] = show_time
                    item['score'] = score or no_score
                    item['avatar'] = avatar
                    yield item

                f_url.args['offset'] += f_url.args['limit']
                yield scrapy.Request(f_url.url, meta={'f_url': f_url}, headers=self.headers, errback=self.errback)
        except Exception as e:
            self.logger.error(e)


    def errback(self, failure: Failure):
        """
        https://docs.scrapy.org/en/latest/topics/request-response.html
        https://docs.scrapy.org/en/latest/topics/request-response.html#topics-request-response-ref-errbacks
        :param failure:
        :return:
        """
        request = failure.request
        url = request.url
        _id = request.meta.get('_id', '')
        res = {
            '_id': _id,
            'url': url,
            'error_type': f"{failure.type}",
            'msg': failure.getErrorMessage(),
            'traceback': failure.getBriefTraceback(),
        }
        try:
            status = failure.value.response.status
            res.update({'status': status})
        except:
            pass

        self.logger.error(json.dumps(res, ensure_ascii=False))