# -*- coding: utf-8 -*-

'''
오늘 날짜 또는 특정 날짜의 시가총액으로 정렬된 회사코드를 리턴한다.
'''
import datetime
import requests
import csv
import json

from env import DATA_PATH


class Crawler_KRX:
    def __init__(self):
        pass


    @classmethod
    def make_new_lower_code(cls, start_dd = None, end_dd = None):
        if start_dd is None:
            start_dd = cls.date_str(7)
        if end_dd is None:
            end_dd = cls.date_str()

        param = {'name': 'fileDown',
                 'filetype': 'csv',
                 'url': 'MKD/10/1002/10020401/mkd10020401_01',
                 'ind_tp': 'ALL',
                 'output_tp': 'L',
                 'period_strt_dd': start_dd,
                 'period_end_dd': end_dd,
                 'isu_cd': '001230',
                 'pagePath': '/contents/MKD/10/1002/10020401/MKD10020401.jsp'}
        headers = {'Accept': '*/*',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                   'Connection': 'keep-alive',
                   'Host': 'marketdata.krx.co.kr',
                   'Referer': 'http://marketdata.krx.co.kr/mdi',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest'}
        cookies = {'session_id': 'sorryidontcare'}

        URL = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
        response = requests.get(URL, params=param, headers=headers)
        print_response(response)
        return response.text, response.cookies

    @classmethod
    def download_csv(cls, name, file_name, cookies):
        URL = 'http://file.krx.co.kr/download.jspx'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': str(len(name)),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'file.krx.co.kr',
            'Origin': 'http://marketdata.krx.co.kr',
            'Referer': 'http://marketdata.krx.co.kr/mdi',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
        form_data = {'code': name}
        print('------')

        with requests.Session() as s:
            download = s.post(URL, data=form_data, headers=headers)
            print_response(download)
            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)

            with open(f'{DATA_PATH}/{file_name}', 'w', encoding='UTF-8') as f:
                dict_data = []
                for index in range(len(my_list) - 1):
                    row = my_list[index + 1]
                    print(row)
                    code = row[0]
                    name = row[1]
                    trade_date = row[7]

                    cur_price = row[2].replace(',','')
                    dict_data.append({code: {'cur_price': cur_price, 'name':name, 'index': index + 1, 'date':trade_date}})
                f.writelines(json.dumps(dict_data, ensure_ascii=False))

    @classmethod
    def date_str(cls, delta=None):
        if delta is None:
            dt_date = datetime.date.today()
        else:
            dt_date = datetime.date.today() - datetime.timedelta(days=7)

        return dt_date.strftime('%Y%m%d')

def print_response(response):
    return
    print(response.status_code)
    print(response.text)
    print(response.cookies)

krx = Crawler_KRX()
rep, _ = krx.make_new_lower_code()
krx.download_csv(rep, 'new_low_price.json', None)