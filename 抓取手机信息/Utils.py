#coding:utf-8
import xlwt

class Utils():
    @staticmethod
    def create_execl(sheet_name,row_title):
        f = xlwt.Workbook()
        sheet_info = f.add_sheet(sheet_name,cell_overwrite_ok=True)
        for i in range(0,len(row_title)):
            sheet_info.write(0,i,row_title[i])

        return f,sheet_info

    @staticmethod
    def write_execl(execl_file,execl_sheet,count,data,execl_name):
        for j in range(len(data)):
            execl_sheet.write(count,j,data[j])

        execl_file.save(execl_name)