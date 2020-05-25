# -*- coding: UTF-8 -*-
import sys
import xlsxwriter
reload(sys)
sys.setdefaultencoding('utf8')

def writeexcl(sample_data, fname):

    STYLE_HEADER = {'font_size': 16, 'border': 1, 'bold': 1, 'bg_color': '#B4C6E7', 'align': 'center', 'valign': 'vcenter'}
    STYLE_TEXT = {'font_size': 14, 'border': 1, 'align':'center'}
    STYLE_NUMBER = {'font_size': 14, 'border': 1, 'align':'center'}
    fname = 'vessel_report' + fname + '.xlsx'
    workbook = xlsxwriter.Workbook(fname)

    style_header = workbook.add_format(STYLE_HEADER)
    style_text = workbook.add_format(STYLE_TEXT)
    style_number = workbook.add_format(STYLE_NUMBER)

    team_sheet = workbook.add_worksheet("船数统计")
    header = ["日期", "经过船只数量", "合计"]
    team_sheet.write_row('A1', header, style_header)

    # 宽度设定
    widths = [20, 20, 15]
    for ind, wid in enumerate(widths):
        team_sheet.set_column(ind, ind, wid)

    for ind, data in enumerate(sample_data):
        team_sheet.write(ind + 1, 0, data[0], style_text)
        team_sheet.write(ind + 1, 1, data[1], style_number)

    # 取得最大行号
    ind += 2
    mergestr = 'C2:C' + str(ind)
    merge_format = workbook.add_format({
        'font_size': 14,
        'bold': True,
        'border': 1,
        'align': 'center',  # 水平居中
        'valign': 'vcenter'  # 垂直居中
        })
    if ind > 2:
        team_sheet.merge_range(mergestr, '=Sum(B2:B'+str(ind)+')', merge_format)
    else:
        team_sheet.write(ind - 1, 2, '=B2', style_number)

    workbook.close()
    #os.system(fname)


if __name__ == '__main__':
    pass