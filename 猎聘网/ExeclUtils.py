# coding=utf-8
"""
@author:SoS
@data:2018/3/19
@version:Python3.6
"""
import xlwt

class ExeclUtils():
    @staticmethod
    def create_execl(sheet_name,row_titles):
        '''
        sheet_name:表格名
        row_titles:行标题
        '''
        f = xlwt.Workbook()
        sheet_info = f.add_sheet(sheet_name,cell_overwrite_ok=True)
        for i in range(0,len(row_titles)):
            sheet_info.write(0,i,row_titles[i])
        return f, sheet_info

    @staticmethod
    def write_execl(execl_file,execl_sheet,count,data,execl_name):
        '''
        execl_file:文件对象
        execl_sheet:表格名
        count:数据插入到哪一行
        data:传入的数据 []类型
        execl_name:execl文件名
        '''
        for j in range(len(data)):
            execl_sheet.write(count,j,data[j])
        execl_file.save(execl_name)