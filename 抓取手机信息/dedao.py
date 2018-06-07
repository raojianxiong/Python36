# coding=utf-8
import requests
import json
from Utils import Utils
import os
import time


class DeDao(object):
    def __init__(self):
        self.row_title = ['来源目录', '标题', '图片', '分享标题', 'mp3地址', '音频时长', '文件大小']
        sheet_name = '逻辑思维音频'

        return_execl = Utils.create_execl(sheet_name, self.row_title)
        self.execl_f = return_execl[0]
        self.sheet_table = return_execl[1]
        self.audio_info = []  # 存放每一条数据中的各元素
        self.count = 0
        self.base_url = 'https://entree.igetget.com/acropolis/v1/audio/listall'
        self.max_id = 0
        self.headers = {
            'Host':	'entree.igetget.com',
            'X-OS':	'iOS',
            'X-NET':	'wifi',
            'Accept':	'*/*',
            'X-Nonce':	'70291808a4530748',
            'Accept-Encoding':	'br, gzip, deflate',
            'X-TARGET':	'main',
            'User-Agent':	'%E5%BE%97%E5%88%B0/4.0.13 CFNetwork/894 Darwin/17.4.0',
            'X-CHIL':	'appstore',
            'Cookie':	'acw_tc=AQAAAPt0EXBorQgA3Tcgb+9WeJpgznSn; aliyungf_tc=AQAAADwDyS2DbAgA3TcgbxkoU3Bb9E7e',
            'X-UID':	'224804667',
            'X-AV':	'4.0.0',
            'X-SEID':	'',
            'X-SCR':	'1242*2208',
            'X-DT':	'phone',
            'X-S':	'1b3579ace486377b',
            'X-Sign':	'ZjQzMzZkNWI2YmJmOTMzNmUyOWJlNGY5NWRhZDYzNzY=',
            'Accept-Language':	'zh-cn',
            'X-D':	'e74fed5a22924a6ab5702a8a5fff9ef8',
            'X-THUMB':	'l',
            'X-T':	'json',
            'X-Timestamp':	'1528304815',
            'X-TS':	'1528304815',
            'X-U':	'224804667',
            'X-App-Key':	'ios-4.0.0',
            'X-OV':	'11.2.6',
            'Connection':	'keep-alive',
            'X-ADV':	'1',
            'Content-Type':	'application/x-www-form-urlencoded',
            'X-V':	'2',
            'X-IS_JAILBREAK':	'NO',
            'X-DV':	'iPhone9,2',
        }

    def request_data(self):
        try:
            data = {
                'max_id': self.max_id,
                'since_id': 0,
                'column_id': 2,
                'count': 20,
                'order': 1,
                'section': 0
            }
            response = requests.post(
                self.base_url, headers=self.headers, data=data)
            print(response.status_code)
            if 200 == response.status_code:
                self.parse_data(response)
        except Exception as e:
            print(e)

    def parse_data(self, response):
        dict_json = json.loads(response.text)
        datas = dict_json['c']['list']
        for data in datas:
            source_name = data['audio_detail']['source_name']
            title = data['audio_detail']['title']
            icon = data['audio_detail']['icon']
            share_title = data['audio_detail']['share_title']
            mp3_url = data['audio_detail']['mp3_play_url']
            duction = str(data['audio_detail']['duration'])+'秒'
            size = data['audio_detail']['size'] / (1000 * 1000)
            size = '%.2fM' % size

            self.download_mp3(mp3_url)

            self.audio_info.append(source_name)
            self.audio_info.append(title)
            self.audio_info.append(icon)
            self.audio_info.append(share_title)
            self.audio_info.append(mp3_url)
            self.audio_info.append(duction)
            self.audio_info.append(size)

            self.count += 1
            Utils.write_execl(self.execl_f, self.sheet_table,
                              self.count, self.audio_info, '逻辑思维.xlsx')
            self.audio_info = []
            print('采集了{}条数据'.format(self.count))

        time.sleep(3)
        max_id = datas[-1]['publish_time_stamp']
        if self.max_id != max_id:
            self.max_id = max_id
            self.request_data()
        else:
            print("数据抓取完毕")

    def download_mp3(self, mp3_url):
        mp3_path = "D:/Photo/mp3/"
        if not os.path.exists(mp3_path):
            os.makedirs(mp3_path)
        with open(mp3_path+mp3_url.split('/')[-1], 'wb') as f:
            f.write(requests.get(mp3_url).content)


if __name__ == '__main__':
    d = DeDao()
    d.request_data()
