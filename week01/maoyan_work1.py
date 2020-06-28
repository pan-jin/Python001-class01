#猫眼爬虫 @panjin
import requests
from bs4 import BeautifulSoup

#设置请求信息

url = 'https://maoyan.com/films?showType=3'
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
'Cookie': '__mta=247354299.1593180880151.1593182538528.1593231838432.7; uuid_n_v=v1; uuid=5E4ACCC0B7B711EA842AD7B3BE0152F25B962864519D4E94AE7AADF177D9E9CD; _csrf=7ad862939c48ec376622b17dd224276c0e9a1b353d2a1c577f88aee3f201aeaa; mojo-uuid=2c6011b63d436437c90972dd503dc80f; _lxsdk_cuid=172f0fafcf2c8-001b1100cff20b-31617402-1aeaa0-172f0fafcf2c8; _lxsdk=5E4ACCC0B7B711EA842AD7B3BE0152F25B962864519D4E94AE7AADF177D9E9CD; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593180880,1593180950,1593181515; mojo-session-id={"id":"de3599e0cc163a2fd57a4bc936226d1e","time":1593272648040}; mojo-trace-id=1; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593272648; __mta=247354299.1593180880151.1593231838432.1593272648181.8; _lxsdk_s=172f6732f03-2f5-7b6-52%7C%7C3'
}
response = requests.get(url,headers=headers)

#设置请求信息
bs_info = BeautifulSoup(response.text,"html.parser")

#抓取电影相关信息
div_movies = bs_info.find("div",class_="classic-movies-list")

movie_name = div_movies.find_all("div",class_="title line-ellipsis")
movie_type = div_movies.find_all("div",class_="actors line-ellipsis")
movie_time = div_movies.find_all("div",class_="show-info line-ellipsis")

#写入电影相关信息
with open("movies.csv","w",encoding="utf-8") as fout:
    for line in range(10):

        out_movies = [
            movie_name[line].get_text(),
            movie_type[line].get_text(),
            movie_time[line].get_text()
        ]
        fout.write("\t".join(out_movies)+"\n")
        print(out_movies)
