# -*- coding: utf-8 -*-
from reportlab.platypus import *
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from uuid import uuid4
import os
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.styles import getSampleStyleSheet
import json

def index():
    redirect(URL('estadisticas'))
    return locals()

def estadisticas():
    data = {}
    names = db.executesql("SELECT Area.nombre_area FROM Area;");
    areas = {}
    i = 0
    for a in names:
        areas[i] = a
        i += 1
    areas = json.dumps(areas)
    return dict(data=data,areas=areas)

def setMonthYearArea():
  vrs = request.vars
  month = vrs.month
  year = vrs.year
  area = vrs.area
  redirect(URL('estadisticas', args=[year, month, area]))

def getData(month,year):
    esperando_c = db.executesql("SELECT Area.nombre_area, Solicitud.fecha_realizacion, count(Solicitud.area) FROM Solicitud, Area, Status_solicitud WHERE Solicitud.status = Status_solicitud.id AND Solicitud.area = Area.id AND Status_solicitud.nombre_status = 'Esperando Compra de Materiales por DPF' GROUP BY Solicitud.area;", as_dict = True)
    esperando_a = db.executesql("SELECT Area.nombre_area, Solicitud.fecha_realizacion, count(Solicitud.area) FROM Solicitud, Area, Status_solicitud WHERE Solicitud.status = Status_solicitud.id AND Solicitud.area = Area.id AND Status_solicitud.nombre_status = 'Esperando aporte de materiales por parte de usuario' GROUP BY Solicitud.area;", as_dict = True)
    listos = db.executesql("SELECT Area.nombre_area, Solicitud.fecha_realizacion, count(Solicitud.area) FROM Solicitud, Area, Status_solicitud WHERE Solicitud.status = Status_solicitud.id AND Solicitud.area = Area.id AND Status_solicitud.nombre_status = 'Listo' GROUP BY Solicitud.area;", as_dict = True)
    no_proceden = db.executesql("SELECT Area.nombre_area, Solicitud.fecha_realizacion, count(Solicitud.area) FROM Solicitud, Area, Status_solicitud WHERE Solicitud.status = Status_solicitud.id AND Solicitud.area = Area.id AND Status_solicitud.nombre_status = 'No procede' GROUP BY Solicitud.area;", as_dict = True)
    orden_asignadas = db.executesql("SELECT Area.nombre_area, Solicitud.fecha_realizacion, count(Solicitud.area) FROM Solicitud, Area, Status_solicitud WHERE Solicitud.status = Status_solicitud.id AND Solicitud.area = Area.id AND Status_solicitud.nombre_status = 'Orden Asignada' GROUP BY Solicitud.area;", as_dict = True)
    orden_por_asignar = db.executesql("SELECT Area.nombre_area, Solicitud.fecha_realizacion, count(Solicitud.area) FROM Solicitud, Area, Status_solicitud WHERE Solicitud.status = Status_solicitud.id AND Solicitud.area = Area.id AND Status_solicitud.nombre_status = 'Orden Por Asignar' GROUP BY Solicitud.area;", as_dict = True)
    realizada_p_c = db.executesql("SELECT Area.nombre_area, Solicitud.fecha_realizacion, count(Solicitud.area) FROM Solicitud, Area, Status_solicitud WHERE Solicitud.status = Status_solicitud.id AND Solicitud.area = Area.id AND Status_solicitud.nombre_status = 'Realizada por contratista' GROUP BY Solicitud.area;", as_dict = True)
    pendientes = db.executesql("SELECT Area.nombre_area, Solicitud.fecha_realizacion, count(Solicitud.area) FROM Solicitud, Area, Status_solicitud WHERE Solicitud.status = Status_solicitud.id AND Solicitud.area = Area.id AND Status_solicitud.nombre_status = 'Pendiente' GROUP BY Solicitud.area;", as_dict = True)
    realizadas = db.executesql("SELECT Area.nombre_area, Solicitud.fecha_realizacion, count(Solicitud.area) FROM Solicitud, Area, Status_solicitud WHERE Solicitud.status = Status_solicitud.id AND Solicitud.area = Area.id AND Status_solicitud.nombre_status = 'Realizada' GROUP BY Solicitud.area;", as_dict = True)
    anuladas = db.executesql("SELECT Area.nombre_area, Solicitud.fecha_realizacion, count(Solicitud.area) FROM Solicitud, Area, Status_solicitud WHERE Solicitud.status = Status_solicitud.id AND Solicitud.area = Area.id AND Status_solicitud.nombre_status = 'Anulada' GROUP BY Solicitud.area;", as_dict = True)

    isNone = False

    months = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }

    if not (month and year):
        isNone = True

    data = {}
    for d in realizadas:
        if not isNone:
            yr = d['fecha_realizacion'].year
            mnth = d['fecha_realizacion'].month
            if not ((months[mnth] == month) and (yr == int(year))):
                continue
        if d['nombre_area'] not in data.keys():
            data[d['nombre_area']] = {
                'realizadas': d['count(Solicitud.area)'],
                'pendientes': 0,
                'anuladas': 0,
                'esperando_c': 0,
                'esperando_a': 0,
                'listos': 0,
                'no_proceden': 0,
                'orden_asignadas': 0,
                'orden_por_asignar': 0,
                'realizada_p_c': 0,
                'totales': d['count(Solicitud.area)'],
            }
    for d in pendientes:
        if not isNone:
            yr = d['fecha_realizacion'].year
            mnth = d['fecha_realizacion'].month
            if not ((months[mnth] == month) and (yr == int(year))):
                continue
        if d['nombre_area'] not in data.keys():
            data[d['nombre_area']] = {
                'realizadas': 0,
                'anuladas': 0,
                'pendientes': d['count(Solicitud.area)'],
                'esperando_c': 0,
                'esperando_a': 0,
                'listos': 0,
                'no_proceden': 0,
                'orden_asignadas': 0,
                'orden_por_asignar': 0,
                'realizada_p_c': 0,
                'totales': d['count(Solicitud.area)'],
            }
        else:
            data[d['nombre_area']]['totales'] += d['count(Solicitud.area)']
            data[d['nombre_area']]['pendientes'] = d['count(Solicitud.area)']
    for d in anuladas:
        if not isNone:
            yr = d['fecha_realizacion'].year
            mnth = d['fecha_realizacion'].month
            if not ((months[mnth] == month) and (yr == int(year))):
                continue
        if d['nombre_area'] not in data.keys():
            data[d['nombre_area']] = {
                'pendientes': 0,
                'realizadas': 0,
                'anuladas': d['count(Solicitud.area)'],
                'esperando_c': 0,
                'esperando_a': 0,
                'listos': 0,
                'no_proceden': 0,
                'orden_asignadas': 0,
                'orden_por_asignar': 0,
                'realizada_p_c': 0,
                'totales': d['count(Solicitud.area)'],
            }
        else:
            data[d['nombre_area']]['totales'] += d['count(Solicitud.area)']
            data[d['nombre_area']]['anuladas'] = d['count(Solicitud.area)']
    for d in esperando_c:
        if not isNone:
            yr = d['fecha_realizacion'].year
            mnth = d['fecha_realizacion'].month
            if not ((months[mnth] == month) and (yr == int(year))):
                continue
        if d['nombre_area'] not in data.keys():
            data[d['nombre_area']] = {
                'pendientes': 0,
                'realizadas': 0,
                'anuladas': 0,
                'esperando_c': d['count(Solicitud.area)'],
                'esperando_a': 0,
                'listos': 0,
                'no_proceden': 0,
                'orden_asignadas': 0,
                'orden_por_asignar': 0,
                'realizada_p_c': 0,
                'totales': d['count(Solicitud.area)'],
            }
        else:
            data[d['nombre_area']]['totales'] += d['count(Solicitud.area)']
            data[d['nombre_area']]['esperando_c'] = d['count(Solicitud.area)']
    for d in esperando_a:
        if not isNone:
            yr = d['fecha_realizacion'].year
            mnth = d['fecha_realizacion'].month
            if not ((months[mnth] == month) and (yr == int(year))):
                continue
        if d['nombre_area'] not in data.keys():
            data[d['nombre_area']] = {
                'pendientes': 0,
                'realizadas': 0,
                'anuladas': 0,
                'esperando_c': 0,
                'esperando_a': d['count(Solicitud.area)'],
                'listos': 0,
                'no_proceden': 0,
                'orden_asignadas': 0,
                'orden_por_asignar': 0,
                'realizada_p_c': 0,
                'totales': d['count(Solicitud.area)'],
            }
        else:
            data[d['nombre_area']]['totales'] += d['count(Solicitud.area)']
            data[d['nombre_area']]['esperando_a'] = d['count(Solicitud.area)']
    for d in listos:
        if not isNone:
            yr = d['fecha_realizacion'].year
            mnth = d['fecha_realizacion'].month
            if not ((months[mnth] == month) and (yr == int(year))):
                continue
        if d['nombre_area'] not in data.keys():
            data[d['nombre_area']] = {
                'pendientes': 0,
                'realizadas': 0,
                'anuladas': 0,
                'esperando_c': 0,
                'esperando_a': 0,
                'listos': d['count(Solicitud.area)'],
                'no_proceden': 0,
                'orden_asignadas': 0,
                'orden_por_asignar': 0,
                'realizada_p_c': 0,
                'totales': d['count(Solicitud.area)'],
            }
        else:
            data[d['nombre_area']]['totales'] += d['count(Solicitud.area)']
            data[d['nombre_area']]['listos'] = d['count(Solicitud.area)']
    for d in no_proceden:
        if not isNone:
            yr = d['fecha_realizacion'].year
            mnth = d['fecha_realizacion'].month
            if not ((months[mnth] == month) and (yr == int(year))):
                continue 
        if d['nombre_area'] not in data.keys():
            data[d['nombre_area']] = {
                'pendientes': 0,
                'realizadas': 0,
                'anuladas': 0,
                'esperando_c': 0,
                'esperando_a': 0,
                'listos': 0,
                'no_proceden': d['count(Solicitud.area)'],
                'orden_asignadas': 0,
                'orden_por_asignar': 0,
                'realizada_p_c': 0,
                'totales': d['count(Solicitud.area)'],
            }
        else:
            data[d['nombre_area']]['totales'] += d['count(Solicitud.area)']
            data[d['nombre_area']]['no_proceden'] = d['count(Solicitud.area)']
    for d in orden_asignadas:
        if not isNone:
            yr = d['fecha_realizacion'].year
            mnth = d['fecha_realizacion'].month
            if not ((months[mnth] == month) and (yr == int(year))):
                continue 
        if d['nombre_area'] not in data.keys():
            data[d['nombre_area']] = {
                'pendientes': 0,
                'realizadas': 0,
                'anuladas': 0,
                'esperando_c': 0,
                'esperando_a': 0,
                'listos': 0,
                'no_proceden': 0,
                'orden_asignadas': d['count(Solicitud.area)'],
                'orden_por_asignar': 0,
                'realizada_p_c': 0,
                'totales': d['count(Solicitud.area)'],
            }
        else:
            data[d['nombre_area']]['totales'] += d['count(Solicitud.area)']
            data[d['nombre_area']]['orden_asignadas'] = d['count(Solicitud.area)']
    for d in orden_por_asignar:
        if not isNone:
            yr = d['fecha_realizacion'].year
            mnth = d['fecha_realizacion'].month
            if not ((months[mnth] == month) and (yr == int(year))):
                continue 
        if d['nombre_area'] not in data.keys():
            data[d['nombre_area']] = {
                'pendientes': 0,
                'realizadas': 0,
                'anuladas': 0,
                'esperando_c': 0,
                'esperando_a': 0,
                'listos': 0,
                'no_proceden': 0,
                'orden_asignadas': 0,
                'orden_por_asignar': d['count(Solicitud.area)'],
                'realizada_p_c': 0,
                'totales': d['count(Solicitud.area)'],
            }
        else:
            data[d['nombre_area']]['totales'] += d['count(Solicitud.area)']
            data[d['nombre_area']]['orden_por_asignar'] = d['count(Solicitud.area)']
    for d in realizada_p_c:
        if not isNone:
            yr = d['fecha_realizacion'].year
            mnth = d['fecha_realizacion'].month
            if not ((months[mnth] == month) and (yr == int(year))):
                continue 
        if d['nombre_area'] not in data.keys():
            data[d['nombre_area']] = {
                'pendientes': 0,
                'realizadas': 0,
                'anuladas': 0,
                'esperando_c': 0,
                'esperando_a': 0,
                'listos': 0,
                'no_proceden': 0,
                'orden_asignadas': 0,
                'orden_por_asignar': 0,
                'realizada_p_c': d['count(Solicitud.area)'],
                'totales': d['count(Solicitud.area)'],
            }
        else:
            data[d['nombre_area']]['totales'] += d['count(Solicitud.area)']
            data[d['nombre_area']]['realizada_p_c'] = d['count(Solicitud.area)']

    for key in data.keys():
        data[key]['efectividad'] = (float(data[key]['realizadas']) / data[key]['totales']) * 100

    return data

def get_pdf():
    tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
    doc = SimpleDocTemplate(tmpfilename, rightMargin=1*inch, leftMargin=1*inch, topMargin=1*cm, bottomMargin=1*inch)
    elements = []
    trabajadores = []


    data = [['Universidad Simon Bolivar'],
            ['Vicerrectorado Administrativo'],
            ['Direccion de Planta Fisica'],
            ['Unidad de Atención e Inspección'],
            ['','Solicitudes atentidas y pendientes'],
            [''],
            ['AREA', 'SOLICITADAS', 'SOLUCIONADAS', 'PENDIENTES', 'ANULADAS',  'EFECTIVIDAD(%)']
           ]


    vrs = request.args
    if len(request.args) == 0 :
        y = None
        m = None
    else:
        y = str(vrs[0])
        m = str(vrs[1])

    table_data = getData(m,y)

    format_data = []
    total_solicitadas = 0
    total_realizadas = 0
    total_pendientes = 0
    total_anuladas = 0

    for key in table_data:
        area = []

        styles = getSampleStyleSheet()
        text = Paragraph(str(key),
              styles['Normal'])
        area.append(text)
        area.append(str(table_data[key]['totales']))
        area.append(str(table_data[key]['realizadas']))
        area.append(str(table_data[key]['pendientes']))
        area.append(str(table_data[key]['anuladas']))
        area.append(str(table_data[key]['efectividad']))

        total_solicitadas += table_data[key]['totales']
        total_realizadas += table_data[key]['realizadas']
        total_pendientes += table_data[key]['pendientes']
        total_anuladas += table_data[key]['anuladas']

        format_data.append(area)

    total_efectividad =  (float(total_realizadas) / total_solicitadas) * 100

    totales = [['TOTALES', str(total_solicitadas), str(total_realizadas), str(total_pendientes), str(total_anuladas),  str(total_efectividad) ]]

    data += format_data
    data += totales
    data += [['Observaciones','']]

    t=Table(data,colWidths=3*cm, rowHeights=1*cm, splitByRow=1,
            repeatRows=0, repeatCols=0)

    t.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (4,3), 10),
        ('FONTSIZE', (1,4), (1,4), 20),
        ('FONTSIZE', (1,4), (1,4), 20),
        ('SPAN', (1,-1), (-1,-1)),
        ('GRID', (0,6), (-1,-1), 0.25, colors.black),
        ('ALIGN',(0,6),(-1,-1),'CENTER'),
        ('VALIGN', (0,6), (-1,-1), 'MIDDLE')
        ]))

    t._rowHeights[4] = 2.5 * cm
    t._rowHeights[0] = 0.5 * cm
    t._rowHeights[1] = 0.5 * cm
    t._rowHeights[2] = 0.5 * cm
    t._rowHeights[3] = 0.5 * cm
    t._rowHeights[-1] = 4 * cm


    drawing = Drawing(400,200)

    categories = []
    data = [[],[],[],[]]
    categories = []
    max_x = 0
    steps = 0.5
    for key in table_data.keys():
        categories.append(key)
        max_x = max(max_x,table_data[key]['totales'])
        data[0].append(table_data[key]['totales'])
        data[1].append(table_data[key]['realizadas'])
        data[2].append(table_data[key]['pendientes'])
        data[3].append(table_data[key]['anuladas'])
        pass

    steps = max_x / 10.0


    bc = VerticalBarChart()
    bc.x = -35
    bc.y = 20
    bc.height = 150
    bc.width = 510
    bc.data = data
    bc.barSpacing = 1
    bc.strokeColor = colors.black
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = max_x*1.1
    bc.valueAxis.valueStep = steps
    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 8
    bc.categoryAxis.labels.dy = -2
    bc.categoryAxis.labels.angle = 15
    bc.categoryAxis.categoryNames = categories


    for i in range(len(data)):
        bc.bars[(0,i)].fillColor = colors.blue
        bc.bars[(1,i)].fillColor = colors.green
        bc.bars[(2,i)].fillColor = colors.red
        bc.bars[(3,i)].fillColor = colors.grey

    drawing.add(bc)


    elements.append(t)
    elements.append(drawing)
    doc.build(elements)

    data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return data
