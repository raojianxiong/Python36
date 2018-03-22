#coding = utf-8
import xlwt
import os
from lxml import etree
from urllib import request,parse
import json


class wzly(object):
    def __init__(self):
        self.gender = 0
        self.stargage = 0
        self.endage = 0
        self.starheight = 0
        self.endheight = 0
        self.marry = 1
        self.salary = 0
        self.eduction = 0
        self.count = 1  # 表示数据条数，去掉标题行
        self.f = None
        self.sheetInfo = None
        self.create_execl()

    def create_execl(self):
        # 创建Execl
        self.f = xlwt.Workbook()
        self.sheetInfo = self.f.add_sheet('我主良缘', cell_overwrite_ok=True)
        rowTitle = ['编号', '昵称', '性别', '年龄', '身高', '籍贯', '学历', '内心独白', '照片']
        # 填充标题
        for i in range(0, len(rowTitle)):
            self.sheetInfo.write(0, i, rowTitle[i])

    def query_data(self):
        # 帅选条件,年龄，身高，教育，期望薪资
        input("请输入你的筛选条件，直接回车可以忽略此次筛选条件:")
        self.query_age()
        self.query_sex()
        self.query_height()
        self.query_money()
        print('您的筛选条件是年龄:{}-{}岁\n性别是:{}\n对方身高是:{}-{}\n对方月薪是:{}'.format(self.stargage,
                                                                       self.endage, self.gender, self.starheight, self.endheight, self.salary))
        self.craw_data()

    def query_age(self):
        try:
            age = int(input('请输入期望对方年龄,如25:'))
        except Exception as e:
            age = 0
        try:
            if 21 <= age <= 30:
                self.stargage = 21
                self.endage = 30
            elif 31 <= age <= 40:
                self.stargage = 31
                self.endage = 40
            elif 41 <= age <= 50:
                self.stargage = 41
                self.endage = 50
            else:
                self.stargage = 0
                self.endage = 0
        except Exception as e:
            self.stargage = 0
            self.endage = 0

    def query_sex(self):
        '''性别筛选'''
        try:
            sex = input('请输入期望对方性别,如:女:')  # 字符串的输入
        except Exception as e:
            sex = '女'

        try:
           if sex == '男':
               self.gender = 1
           else:
               self.gender = 2

        except Exception as e:
           self.gender = 2

    def query_height(self):
        '''身高筛选'''
        try:
            height = input('请输入期望对方身高,如:162:')
        except Exception as e:
            height = 0

            try:
                if 151 <= height <= 160:
                    self.startheight = 151
                    self.endheight = 160
                elif 161 <= height <= 170:
                    self.startheight = 161
                    self.endheight = 170
                elif 171 <= height <= 180:
                    self.startheight = 171
                    self.endheight = 180
                elif 181 <= height <= 190:
                    self.startheight = 181
                    self.endheight = 190
                else:
                    self.startheight = 0
                    self.endheight = 0
            except Exception as e:
                self.startheight = 0
                self.endheight = 0

    def query_money(self):
        '''待遇筛选'''
        try:
            money = input('请输入期望的对方月薪,如:8000:')
        except Exception as e:
            money = 0

        try:
            if 2000 <= money < 5000:
                self.salary = 2
            elif 5000 <= money < 10000:
                self.salary = 3
            elif 10000 <= money <= 20000:
                self.salary = 4
            elif 20000 <= money:
                self.salary = 5
            else:
                self.salary = 0
        except Exception as e:
            self.salary = 0

    def store_info(self, nick, age, height, address, heart, education, img_url):
        if age < 22:
            tag = "22岁以下"
        elif 22 <= age < 32:
            tag = "22-28岁"
        elif 28 <= age < 32:
            tag = '28-32岁'
        elif 32 <= age:
            tag = '32岁以上'
        filename = '{}岁_身高{}_学历{}_{}_{}.jpg'.format(
            age, height, education, address, nick)

        try:
            # 补全文目录
            image_path = 'D:/Photo/{}'.format(tag)

            if not os.path.exists(image_path):
                os.makedirs(image_path)
                print(image_path+"创建成功")
            with open(image_path+'/'+filename, 'wb') as f:
                f.write(request.urlopen(img_url).read())
        except Exception as e:
            print(str(e))

    def store_info_excel(self, nick, age, height, address, heart, education, img_url):
        person = []
        person.append(self.count)
        person.append(nick)
        person.append('女' if self.gender == 2 else '男')
        person.append(age)
        person.append(height)
        person.append(address)
        person.append(education)
        person.append(heart)
        person.append(img_url)

        for j in range(len(person)):
            self.sheetInfo.write(self.count, j, person[j])
        self.f.save('我主良缘.xlsx')
        self.count += 1
        print("插入了{}条数据".format(self.count))

    def parse_data(self, response):
        '''数据解析'''
        persons = json.loads(response).get('data').get('list')
        if persons is None:
            print("数据已经请求完毕")
            return

        for person in persons:
            nick = person.get('username')
            gender = person.get('gender')
            age = 2018-int(person.get('birthdayyear'))
            address = person.get('city')
            heart = person.get('monolog')
            height = person.get('height')
            img_url = person.get('avatar')
            education = person.get('education')
            self.store_info(nick, age, height, address,heart, education, img_url)
            self.store_info_excel(nick, age, height, address, heart, education, img_url)

    def craw_data(self):
        '''数据抓取'''
        headers = {
            'Referer': 'http://www.lovewzly.com/jiaoyu.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'
        }
        page = 1
        while True:
            query_data = {
                'page': page,
                'gender': self.gender,
                'starage': self.stargage,
                'endage': self.endage,
                'starheight': self.starheight,
                'endheight': self.endheight,
                'marry': self.marry,
                'salary': self.salary
            }
            url = 'http://www.lovewzly.com/api/user/pc/list/search?' + parse.urlencode(query_data)
            print(url)
            req = request.Request(url, headers=headers)
            response = request.urlopen(req).read()
            self.parse_data(response)
            page += 1


if __name__ == '__main__':
    wz = wzly()
    wz.query_data()
