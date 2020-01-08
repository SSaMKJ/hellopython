import requests
import csv
import json

from fiftytwo.fiftyTwo import FiftyTwoWeekRange


def get_post_data():
    param = {'name': 'fileDown',
             'filetype': 'csv',
             'url': 'MKD/04/0404/04040200/mkd04040200_01',
             'market_gubun': 'STK',
             'indx_ind_cd': '1001',
             'sect_tp_cd': 'ALL',
             'schdate': '20200107',
             'pagePath': '%2Fcontents%2FMKD%2F04%2F0404%2F04040200%2FMKD04040200.jsp'}
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
               'Connection': 'keep-alive',
               'Host': 'marketdata.krx.co.kr',
               'Referer': 'http://marketdata.krx.co.kr/contents/MKD/04/0404/04040200/MKD04040200.jsp',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'}
    cookies = {'session_id': 'sorryidontcare'}

    URL = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
    response = requests.get(URL, params=param, headers=headers)
    print_response(response)
    return response.text, response.cookies


def print_response(response):
    print(response.status_code)
    print(response.text)
    print(response.cookies)


def download_csv(code, cookies):
    URL = 'http://file.krx.co.kr/download.jspx'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': str(len(code)),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'file.krx.co.kr',
        'Origin': 'http://marketdata.krx.co.kr',
        'Referer': 'http://marketdata.krx.co.kr/contents/MKD/04/0404/04040200/MKD04040200.jsp',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    form_data = {'code':code}
    print('------')

    with requests.Session() as s:
        download = s.post(URL, data=form_data, headers=headers)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        with open('tmp-market-cap.json', 'w', encoding='UTF-8') as f:
            f.writelines('[\n')
            dict_data = []
            for index in range(len(my_list)-1):
                row = my_list[index+1]
                code = row[1]
                name = row[2]
                dict_data.append({code:{'name':name, 'index':index+1}})
            f.writelines(json.dumps(dict_data, ensure_ascii=False))
            f.writelines('\n]')

data, cookie = get_post_data()
download_csv(data, cookie)



print(FiftyTwoWeekRange('005930'))