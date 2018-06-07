# coding:utf-8
import requests
import json
import time


class GZH():
    def __init__(self):
        self.base_url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzA4NTQwNDcyMA==&f=json&offset={}&count=10&is_ok=1&scene=124&uin=MjI3NjA3NTMyNA%3D%3D&key=c98d6c02144b06270885a670c2a286663f9642c3ff72f373a00f06810301c8c7a7f3cc6229ddc696d9bccda804f946faf49bdb9c864015d943c50daa854219b3590115d9427bc059598cedb40e9d4613&pass_ticket=lYcbXQqfbHyz0ho29nS7V4jaOV82KM5wZk3wD53mBIPfs5kdYJSOVhwkuIWc18P9&wxtoken=&appmsg_token=960_DqPqoyT1gBzGPQoYtXXQ7vvGbGfE1hZOfXdaDw~~&x5=0&f=json"
        self.headers = {
            'Host':	'mp.weixin.qq.com',
            'Connection':	'keep-alive',
            'Accept':	'*/*',
            'User-Agent':	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400',
            'X-Requested-With':	'XMLHttpRequest',
            'Referer':	'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA4NTQwNDcyMA==&scene=124&uin=MjI3NjA3NTMyNA%3D%3D&key=80b590d5e3a259312a4b1997f955cf49f1face919a96bf8f306fd5f9319a4cfe97dcce3de77d021ef4c31c24bb796ab3bdca5915daa97fd8450d32a29b328129fc54f66dfa544ea2e003f294d4fb0b32&devicetype=Windows+10&version=6206021b&lang=zh_CN&a8scene=7&pass_ticket=lYcbXQqfbHyz0ho29nS7V4jaOV82KM5wZk3wD53mBIPfs5kdYJSOVhwkuIWc18P9&winzoom=1',
            'Accept-Encoding':	'gzip, deflate',
            'Accept-Language':	'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4',
            'Cookie':	'rewardsn=; wxtokenkey=777; wxuin=2276075324; devicetype=Windows10; version=6206021b; lang=zh_CN; pass_ticket=lYcbXQqfbHyz0ho29nS7V4jaOV82KM5wZk3wD53mBIPfs5kdYJSOVhwkuIWc18P9; wap_sid2=CLzOqL0IElxLNWE4dV9EQURLc3JOdU9WLTBlR2Vaa0lHQ1phc1p5ekNfWlZwVmVkeVdpcFJrZkZjU2hNX3RPd3dDeDg4S2Joa3JTblFVWkZaYW9FX3RQRTZGN1Q0c0FEQUFBfjDrj+XYBTgNQJVO'
        }
        self.offset = 10

    def request_data(self):
        try:
            response = requests.get(self.base_url.format(
                self.offset), headers=self.headers)
            if response.status_code == 200:
                self.parse_data(response.text)
        except Exception as e:
            print(e)


    def parse_data(self, jsonText):
        datas = json.loads(jsonText)
        print(datas['ret'])
        if datas['ret'] == 0:
            self.offset = datas['next_offset']
            msg_list = datas['general_msg_list']
            result = json.loads(msg_list)['list']
            for data in result:
                try:
                    title = data['app_msg_ext_info']['title']
                    digest = data['app_msg_ext_info']['digest']
                    content_url = data['app_msg_ext_info']['digest']
                    cover = data['app_msg_ext_info']['cover']
                    print('title:{} digest:{} content_url:{} cover:{}'.format(
                        title, digest, content_url, cover))
                except Exception as e:
                    print(e)
                    continue
            print('***************************************************')
            time.sleep(2)
            self.request_data()
        else:
            print("数据抓取错误")


if __name__ == '__main__':
    g = GZH()
    g.request_data()