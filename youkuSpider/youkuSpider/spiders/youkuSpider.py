# -*-coding:utf-8 -*-
# author: mrz_power
# datetime : 20180917
# import json, random
# import requests
# from bs4 import BeautifulSoup
#
# def main():
#     res = requests.get("https://so.youku.com/search_video/q_爱情")
#     soup = BeautifulSoup(res.content, 'html.parser')
#     # 爬取视屏链接
#     for item in soup.find_all("script"):
#         if item.contents:
#             if item.contents[0].find('"domid":"bpmodule-main"') >= 0:
#                 view_html = item.contents[0].replace("bigview.view(", "")
#                 view_html = view_html[:-1]
#                 view_data = json.loads(view_html)
#                 html_data = view_data.get("html")
#                 view_soup = BeautifulSoup(html_data, 'html.parser')
#                 data = view_soup.find_all("a", {"data-spm": "dtitle"})
#                 for item in data[0:4]:
#                     if item['href'].find("//") == 0:
#                         vid = item['href'][item['href'].find("id_") + 3:-5]
#                         headers = {
#                             'Referer': "https://m.youku.com/video/id_" + vid + ".html?source="
#                         }
#                         s = requests.session()
#                         s.cookies.clear()
#                         res = s.get(
#                             "https://ups.youku.com/ups/get.json?vid="+vid+"&ccode=0501&client_ip=0.0.0.0&client_ts=1537174809&fu=0&vr=0&rst=mp4&dq=mp4&os=ios&bt=phone&bd=&tict=0&d=0&needbf=1&site=1&aw=w&vs=1.0&pver=1&wintype=xplayer_m3u8&utid=W2RgEzXo0B0CASp4Sm1PIsnw&ckey=112%23Zbg4oc4WBHc%2B4sbiF%2Bq%2BTAEPoz8pDk%2BeqMOzqkDpbdfGN4bxCpFZ6mQ%2BfwVxxYn1IcWsmfbwBBYqrpt6k35b4mY2Xqed%2FVGZO2Fhb1f%2F%2Fc%2BAmPmYjJO8%2BmWs5Bmh%2BEFL8vZcTnEnlmIPMWDCzZH4aI9NIMrjGvkv3CwUzeVlnP9SyEOS0Cu3pIDt3vENCvm%2FDW6G1lpXlTHWLoKZTNiVXeEBoFbErJ85uRryyVqnflPQVupCz4VEA5f%2B%2B7E5lDNlrd13fHixiSkIjVjOSJ39S3LSK7vmO90TEwbnPAjy0dXgzAftGn1mcv1FS4ls3NKwNMy%2B%2FoHdC6%2Bpt0I2Z%2FIOLYdei2m23GJ48U7%2F0zq9mqxRobeTWShxo%2BULdsmDpgbUeBrnub1fCyN%2FSowRLiVpHPD43gGujwuPs%2FECHJ3nKk3TrdqAicCW6ASZT4oRXl1xCxuHXXwIljGgdm1KBrmfbg1JNpuQNzk6o0G4H9hLaErK5hVbLQp8J0joWQ0FL5QYd1K2F6eY", headers=headers)
#                         s.cookies.clear()
#                         print(res.text)
#                         res_data = json.loads(res.text)
#                         stream_list = res_data.get("data").get("stream")
#                         with open(vid+".mp4", "ab+") as video_file:
#                             for stream_item in stream_list:
#                                 stream_res = requests.get(stream_item.get("segs")[0].get("cdn_url"))
#                                 video_file.write(stream_res.content)
#
#
# if __name__ == "__main__":
#     main()
import json
import scrapy
import requests
from youkuSpider.items import YoukuspiderItem
from bs4 import BeautifulSoup


class YoukuSpider(scrapy.spiders.Spider):
    name = "youku"
    allowed_domains = ["*"]
    start_urls = [
        "https://so.youku.com/search_video/q_爱情",
    ]

    def __init__(self, category="篮球教学", *args, **kwargs):
        super(YoukuSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://so.youku.com/search_video/q_{}'.format(category)]

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # 爬取视屏链接
        for item in soup.find_all("script"):
            if item.contents:
                if item.contents[0].find('"domid":"bpmodule-main"') >= 0:
                    view_html = item.contents[0].replace("bigview.view(", "")
                    view_html = view_html[:-1]
                    view_data = json.loads(view_html)
                    html_data = view_data.get("html")
                    view_soup = BeautifulSoup(html_data, 'html.parser')
                    data = view_soup.find_all("a", {"data-spm": "dtitle"})
                    for item in data[0:4]:
                        if item['href'].find("//") == 0:
                            # yield YoukuspiderItem(name=item['title'], view_url=item['href'])
                            vid = item['href'][item['href'].find("id_") + 3:-5]
                            headers = {
                                'Referer': "https://m.youku.com/video/id_" + vid + ".html?source="
                            }
                            s = requests.session()
                            s.cookies.clear()
                            res = s.get(
                                "https://ups.youku.com/ups/get.json?vid="+vid+"&ccode=0501&client_ip=0.0.0.0&client_ts=1537174809&fu=0&vr=0&rst=mp4&dq=mp4&os=ios&bt=phone&bd=&tict=0&d=0&needbf=1&site=1&aw=w&vs=1.0&pver=1&wintype=xplayer_m3u8&utid=W2RgEzXo0B0CASp4Sm1PIsnw&ckey=112%23Zbg4oc4WBHc%2B4sbiF%2Bq%2BTAEPoz8pDk%2BeqMOzqkDpbdfGN4bxCpFZ6mQ%2BfwVxxYn1IcWsmfbwBBYqrpt6k35b4mY2Xqed%2FVGZO2Fhb1f%2F%2Fc%2BAmPmYjJO8%2BmWs5Bmh%2BEFL8vZcTnEnlmIPMWDCzZH4aI9NIMrjGvkv3CwUzeVlnP9SyEOS0Cu3pIDt3vENCvm%2FDW6G1lpXlTHWLoKZTNiVXeEBoFbErJ85uRryyVqnflPQVupCz4VEA5f%2B%2B7E5lDNlrd13fHixiSkIjVjOSJ39S3LSK7vmO90TEwbnPAjy0dXgzAftGn1mcv1FS4ls3NKwNMy%2B%2FoHdC6%2Bpt0I2Z%2FIOLYdei2m23GJ48U7%2F0zq9mqxRobeTWShxo%2BULdsmDpgbUeBrnub1fCyN%2FSowRLiVpHPD43gGujwuPs%2FECHJ3nKk3TrdqAicCW6ASZT4oRXl1xCxuHXXwIljGgdm1KBrmfbg1JNpuQNzk6o0G4H9hLaErK5hVbLQp8J0joWQ0FL5QYd1K2F6eY", headers=headers)
                            s.cookies.clear()
                            res_data = json.loads(res.text)
                            stream_list = res_data.get("data").get("stream")
                            yield YoukuspiderItem(name=item['title'].replace(" ",""), view_json=json.dumps(stream_list))