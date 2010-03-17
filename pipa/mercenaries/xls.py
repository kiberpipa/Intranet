# -*- coding: utf-8 -*-
from datetime import datetime
from pyExcelerator import *

def salary_xls(compact, bureaucrat, params, year, month):
    title = Font()
    title.name = 'Arial'
    title.bold = True
    title.height = 600


    subtitle  = Font()
    subtitle.height = 260
    subtitle.bold = True
    subtitle.italic = True

    obican_fnt = Font()
    obican_fnt.height = 200

    borders = Borders()
    borders.left = 6
    borders.right = 6
    borders.top = 6
    borders.bottom = 6


    underline = Borders()
    underline.bottom = 2

    al = Alignment()
    al.horz = Alignment.HORZ_CENTER
    al.vert = Alignment.VERT_CENTER

    style = XFStyle()
    style.font = title
    style.borders = borders
    style.alignment = al


    subtitle_style = XFStyle()
    subtitle_style.font = subtitle


    uline = XFStyle()
    uline.borders = underline

    obican = XFStyle()
    obican.font = obican_fnt
    wb = Workbook()

    if compact:
        # sort entries by cost center
        stroskovnomesto_dict = {}
        for i in params:
            a_list = stroskovnomesto_dict.setdefault(i['cost_center'], [])
            a_list.append(i)
            stroskovnomesto_dict[i['cost_center']] = a_list
        
        for mesto, items in stroskovnomesto_dict.iteritems():
            ws = wb.add_sheet(str(mesto))
            ws.col(0).width = 0x1900
            ws.col(1).width = 0x700
            ws.col(2).width = 0x1600
            ws.col(4).width = 0x1700

            line = 0

            ws.write(line, 0, 'Ime in Priimek', subtitle_style)
            ws.write(line, 1, 'St ur', subtitle_style)
            ws.write(line, 2, 'Za opravljeno delo', subtitle_style)
            ws.write(line, 3, 'Projekt', subtitle_style)
            ws.write(line, 4, 'Stroskovno mesto', subtitle_style)
            ws.write(line, 5, 'Znesek', subtitle_style)
            
            amount = 0
            for i in items:
                line += 1
                ws.write(line, 0, i['mercenary'], obican)
                ws.write(line, 1, float(i.get('hours','0')) or '', obican)
                ws.write(line, 2, i['description'], obican)
                ws.write(line, 3, i['cost_center'], obican)
                ws.write(line, 4, u'Plače - 68', obican)
                ws.write(line, 5, float(i['amount']), obican)

                amount += i['amount']

            line += 2
            ws.write(line, 5, str(amount), subtitle_style)

            line +=2 
            ws.write(line, 0,'Nalog Izdal', obican)
            ws.write_merge(line, line, 1, 2, bureaucrat, obican)


            date = datetime.today()
            line += 1
            ws.write(line, 0, 'Datum', obican)
            ws.write_merge(line, line, 1, 2, '%s/%s/%s' % (date.day, date.month, date.year), obican)
    else:
        for i in params:
            ws = wb.add_sheet(i['mercenary'])


            ws.col(1).width = 0x1500
            ws.col(3).width = 0x2500



            line = 0

            ws.write_merge(line, line, 0, 6, 'NALOG ZA IZPLACILO PLACE', style)

            line += 2
            ws.write(line, 1, 'ZA DELAVCA:', subtitle_style)

            line += 2
            ws.write(line, 1, 'Ime in priimek:', obican)
            ws.write(line, 3, i['mercenary'], obican)
            
            line += 2
            ws.write(line, 1, 'Stevilo ur', obican)
            ws.write(line, 3, float(i.get('hours', 0)) or '', obican)

            line += 2
            ws.write(line, 1, 'Znesek', obican)
            ws.write(line, 3, float(i['amount']), obican)

            line += 2
            ws.write(line, 1, 'Za opravljeno delo (opis):', obican)
            ws.write_merge(line, line, 2, 3, '', uline)
            ws.write_merge(line+1, line+1, 1, 3, '', uline)
            ws.write_merge(line+2, line+2, 1, 3, '', uline)

            line += 4
            ws.write_merge(line, line, 1, 2, 'Projekt/sluzba in stroskovno mesto:', obican) 
            ws.write(line, 3, "Kiberpipa %s" % (i['cost_center'],), obican)

            line += 3
            ws.write(line, 1, 'Nacin placila', obican)
            ws.write(line, 3, i['salary_type'], obican)

            line += 2
            ws.write(line, 1, 'Nalog izdal:', obican)
            ws.write(line, 3, bureaucrat, obican)
            
            date = datetime.today()
            line += 2
            ws.write(line, 1, 'Datum:', obican)
            ws.write(line, 3, '%s/%s/%s' % (date.day, date.month, date.year), obican)

            line += 2
            ws.write(line, 1, 'Podpis:', obican)
            ws.write(line, 3, '', uline)

            line += 2
            ws.write_merge(line, line, 0, 6, '--------------------------------------------------------------------------------------------------------------------------------------------------------------------', obican)
            ws.write_merge(line +1 , line +1, 0, 6, '--------------------------------------------------------------------------------------------------------------------------------------------------------------------', obican)

            line += 2
            ws.write(line, 1, 'NALOG PREJEL:', obican)
            ws.write(line, 3, '', uline)

            line += 2
            ws.write(line, 1, 'DATUM:', obican)
            ws.write(line, 3, '', uline)

            line += 2
            ws.write(line, 1, 'PODPIS:', obican)
            ws.write(line, 3, '', uline)


    return wb.get_biff_data()
