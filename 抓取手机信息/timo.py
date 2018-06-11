# coding=utf-8
import requests
import json
import time
import random


class TiMo():
    def __init__(self):
        self.baseUrl = "https://api.amemv.com/aweme/v1/aweme/post/?iid=35150003561&device_id=48526500596&os_api=18&app_name=aweme&channel=App%20Store&idfa=D420CB58-25ED-441A-B1E5-FDD8442D0A48&device_platform=iphone&build_number=18504&vid=BDF5B471-35B1-41F0-A6A5-3C85D48DA550&openudid=de110aa76e414c0163cc220e94b9b25c88ede2c1&device_type=iPhone9,2&app_version=1.8.5&version_code=1.8.5&os_version=11.2.6&screen_width=1242&aid=1128&ac=WIFI&count=21&max_cursor=0&min_cursor=0&user_id=58958068057&mas=005ccbf596dd5116e932383c4e6e73aede7fa5761951141f7b6ebe&as=a1b5e5712aaf7b023e8205&ts=1528713978"
        self.video_headers = {
            # ':method':	'GET',
            # ':scheme':	'https',
            # ':path':	'/aweme/v1/aweme/post/?iid=35150003561&device_id=48526500596&os_api=18&app_name=aweme&channel=App%20Store&idfa=D420CB58-25ED-441A-B1E5-FDD8442D0A48&device_platform=iphone&build_number=18504&vid=BDF5B471-35B1-41F0-A6A5-3C85D48DA550&openudid=de110aa76e414c0163cc220e94b9b25c88ede2c1&device_type=iPhone9,2&app_version=1.8.5&version_code=1.8.5&os_version=11.2.6&screen_width=1242&aid=1128&ac=WIFI&count=21&max_cursor=0&min_cursor=0&user_id=58958068057&mas=005ccbf596dd5116e932383c4e6e73aede7fa5761951141f7b6ebe&as=a1b5e5712aaf7b023e8205&ts=1528713978',
            # ':authority':	'api.amemv.com',
            'cookie':	'install_id=35150003561; odin_tt=a004eee5fc56a9e4dc6376f1afccd5e9d8648417ea2e5c8ae45f0cbd8907b0bc618275bc4ba8d98fb9100a19c223a65e; sessionid=8877a21fc511c3805d91de1b5c89498e; sid_guard=8877a21fc511c3805d91de1b5c89498e%7C1528619671%7C2592000%7CTue%2C+10-Jul-2018+08%3A34%3A31+GMT; sid_tt=8877a21fc511c3805d91de1b5c89498e; ttreq=1$2a3dd8106fc952d9f8b84cbeae80d53e1159f929; uid_tt=9633b543f1cba4c3cb7bf185158eb579',
            'accept':	'*/*',
            'user-agent':	'Aweme/1.8.5 (iPhone; iOS 11.2.6; Scale/3.00)',
            'accept-language':	'zh-Hans-CN;q=1',
            'accept-encoding':	'br, gzip, deflate'
        }
        self.comment_headers = {
            'cookie':	'install_id=35150003561; odin_tt=a004eee5fc56a9e4dc6376f1afccd5e9d8648417ea2e5c8ae45f0cbd8907b0bc618275bc4ba8d98fb9100a19c223a65e; sessionid=8877a21fc511c3805d91de1b5c89498e; sid_guard=8877a21fc511c3805d91de1b5c89498e%7C1528619671%7C2592000%7CTue%2C+10-Jul-2018+08%3A34%3A31+GMT; sid_tt=8877a21fc511c3805d91de1b5c89498e; ttreq=1$2a3dd8106fc952d9f8b84cbeae80d53e1159f929; uid_tt=9633b543f1cba4c3cb7bf185158eb579',
            'accept':	'*/*',
            'user-agent':	'Aweme/1.8.5 (iPhone; iOS 11.2.6; Scale/3.00)',
            'accept-language':	'zh-Hans-CN;q=1',
            'accept-encoding':	'br, gzip, deflate'
        }
        self.cursor = 0
        self.unique_id_modify_time = 1528719888
        self._as = 'a155c601d0f1ab2a0e0086'
        self.mas = '0099709b51b018cc14ce29bf6f9f4a3f7b95f5372bb18abf2aaf31'
        self.base_str = 'abcdefghigklmnopqrstuvwxyz0123456789'

    def request_timo_video(self):
        # 提莫名下视频
        response = requests.get(self.baseUrl, headers=self.video_headers)
        if(response.status_code == 200):
            self.__parse_data(response.text)

    def __parse_data(self, text):
        result = json.loads(text)
        datas = result['aweme_list']
        for data in datas:
            download_url = data['video']['download_addr']['url_list']
            duration = data['video']['duration']/(1000*1000)
            duration = '%.2fM' % duration
            play_url = data['video']['play_addr']['url_list']
            nick_name = data['author']['nickname']
            music_title = data['music']['title']
            share_title = data['share_info']['share_title']

            print("作者：%s 标题:%s 视频下载地址:%s 时长:%s 播放地址:%s 音乐:%s " % (
                nick_name, share_title, download_url, duration, play_url, music_title))
            print("************************************************************")

    def request_timo_comment(self):
        # 提莫名下评论
        url = "https://api.amemv.com/aweme/v1/comment/list/?iid=35150003561&device_id=48526500596&os_api=18&app_name=aweme&channel=App%20Store&idfa=D420CB58-25ED-441A-B1E5-FDD8442D0A48&device_platform=iphone&build_number=18504&vid=BDF5B471-35B1-41F0-A6A5-3C85D48DA550&openudid=de110aa76e414c0163cc220e94b9b25c88ede2c1&device_type=iPhone9,2&app_version=1.8.5&version_code=1.8.5&os_version=11.2.6&screen_width=1242&aid=1128&ac=WIFI&aweme_id=6564996818420108547&comment_style=2&count=20&cursor={}&digged_cid=&mas={}&as={}&ts={}"
        response = requests.get(url.format(
            self.cursor, self.mas, self._as, self.unique_id_modify_time), headers=self.comment_headers)
        if response.status_code == 200:
            self.__request_to_get_comment(response.text)

    def __request_to_get_comment(self, text):
        result = json.loads(text)

        try:
            if 1 == result['has_more']:
                for data in result['comments']:
                    comment = data['text']
                    digg_count = data['digg_count']
                    print("共有{}赞  {}".format(digg_count, comment))

                self.cursor = result['cursor']
                self.unique_id_modify_time = result['comments'][-1]['user']['unique_id_modify_time']

                # 以下采用随机替换mas 和 as
                l = list(self.mas)
                l[random.randint(0, len(l)-1)] = random.choice(self.base_str)
                self.mas = "".join(l)
                m = list(self._as)
                m[random.randint(0, len(m)-1)] = random.choice(self.base_str)
                self._as = "".join(m)

                time.sleep(2)
                self.request_timo_comment()

            else:
                print("无数据")
        except Exception as e:
            print(result)
            print(str(e))


if __name__ == '__main__':
    timo = TiMo()
    # 爬取提莫名下所有的短视频
    # timo.request_timo_video()
    # 爬取提模第一个视频的评论及评论的点赞
    timo.request_timo_comment()
