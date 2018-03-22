#coding=utf-8
import xlrd
import xlwt

data = xlrd.open_workbook('execl_demo.xlsx')
table = data.sheets()[0] #通过索引顺序获取table
print(table.nrows)#行数
print(table.ncols)#烈数

for k in range(table.nrows):
    print(table.row_values(k))
for i in range(table.ncols):
    print(table.col_values(i))

print(table.cell(2,2).value)

for a in range(1,table.nrows):
    for b in range(table.ncols):
        print(table.cell(a,b).value)
    print('-------')

f = xlwt.Workbook(encoding='utf-8')#创建workbook,其实是execl
sheet1 = f.add_sheet('个人信息',cell_overwrite_ok=True)
rowTitle = ['编号','姓名','性别','年龄']
rowDatas = [['张一','男','18'],['李二','女','20'],['黄三','男','38'],['刘四','男','28']]

style = xlwt.XFStyle()
pattern = xlwt.Pattern()
pattern.pattern=xlwt.Pattern.SOLID_PATTERN#实型
pattern.pattern_fore_colour = 4
style.pattern = pattern
for i in range(0,len(rowTitle)):
    sheet1.write(0,i,rowTitle[i],style)

for k in range(0,len(rowDatas)):
    rowDatas[k].insert(0,k+1)#插上编号
    for j in range(0,len(rowDatas[k])):
        sheet1.write(k+1,j,rowDatas[k][j])

f.save("info.xlsx")
