from pyExcelerator import *

from datetime import datetime


def compact_salary_xls(params):
    wb = Workbook()
    ws = wb.add_sheet('compact')

    obican_fnt = Font()
    obican_fnt.height = 200

    obican = XFStyle()
    obican.font = obican_fnt

    bold_fnt = Font()
    bold_fnt.bold = True

    bold = XFStyle()
    bold.font = bold_fnt

    ws.col(0).width = 0x2500
    ws.col(1).width = 0x500
    ws.col(2).width = 0x3500
    ws.col(4).width = 0x1500

    line = 0

    ws.write(line, 0, 'Ime in Priimek', bold)
    ws.write(line, 1, 'St ur', bold)
    ws.write(line, 2, 'Za opravljeno delo', bold)
    ws.write(line, 3, 'Projekt', bold)
    ws.write(line, 4, 'Stroskovno mesto', bold)
    ws.write(line, 5, 'Znesek', bold)
    
    amount = 0
    for i in params:
        line += 1
        ws.write(line, 0, i['mercenary'], obican)
        try:
            ws.write(line, 1, i['hours'], obican)
        except KeyError:
            pass
        ws.write(line, 2, i['description'], obican)
        ws.write(line, 3, 'Kiberpipa', obican)
        ws.write(line, 4, i['cost_center'], obican)
        ws.write(line, 5, float(i['amount']), obican)

        amount += i['amount']
        bureaucrat = i['bureaucrat']

    line += 2
    ws.write(line, 5, amount, bold)

    line +=2 
    ws.write(line, 0,'Nalog Izdal', obican)
    ws.write_merge(line, line, 1, 2, bureaucrat, obican)


    date = datetime.today()
    line += 1
    ws.write(line, 0, 'Datum', obican)
    ws.write_merge(line, line, 1, 2, '%s/%s/%s' % (date.day, date.month, date.year), obican)
    


    return wb.get_biff_data()
    

def salary_xls(params):
    wb = Workbook()

    for i in params:
        ws = wb.add_sheet(i['mercenary'])


        ws.col(1).width = 0x1500
        ws.col(3).width = 0x2500


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

        line = 0

        ws.write_merge(line, line, 0, 6, 'NALOG ZA IZPLACILO PLACE', style)

        line += 2
        ws.write(line, 1, 'ZA DELAVCA:', subtitle_style)

        line += 2
        ws.write(line, 1, 'Ime in priimek:', obican)
        ws.write(line, 3, i['mercenary'], obican)
        
        try:
            line += 2
            ws.write(line, 1, 'Stevilo ur', obican)
            ws.write(line, 3, i['hours'], obican)
        except KeyError:
            pass

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
        ws.write(line, 3, i['cost_center'], obican)

        line += 3
        ws.write(line, 1, 'Nacin placila', obican)
        ws.write(line, 3, i['salary_type'], obican)

        line += 2
        ws.write(line, 1, 'Nalog izdal:', obican)
        ws.write(line, 3, i['bureaucrat'], obican)
        
        date = datetime.today()
        line += 2
        ws.write(line, 1, 'Datum:', obican)
        ws.write(line, 3, '%s/%s/%s' % (date.day, date.month, date.year), obican)

        line += 2
        ws.write(line, 1, 'Podpis:', obican)
        ws.write(line, 3, '', uline)

        line += 2
        ws.write_merge(line, line, 0, 6, '-------------------------------------------------------------------------------------------------------------------------------------------------------------------------', obican)
        ws.write_merge(line +1 , line +1, 0, 6, '-------------------------------------------------------------------------------------------------------------------------------------------------------------------------', obican)

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
