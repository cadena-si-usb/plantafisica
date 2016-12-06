from gluon.serializers import json

def plugin_google_chart():
    """used with the .load view to create a google chart
    Because this is used in a view LOAD, parameters are passed back from the browser as vars in the URL
    The complulsory vars include: 'type', a string defining the chart_type
        'data_url', which is a URL of the function which returns the data to be charted

    The use in the view is like this (including an example data URL

    {{ data_url = URL('plugin_google_chart','plugin_return_data.json',user_signature=True)}}
    ...
    {{=LOAD('plugin_google_chart','plugin_google_chart.load',ajax=True,
        user_signature=True,vars={'type':'bar','data_url':data_url})}}
    """
    chart_type = request.vars.type
    data_url = request.vars.data_url
    options_dict = request.vars.options_dict or ''
    if chart_type and data_url:
        return dict(chart_type=chart_type,data_url=data_url,
                    options_dict=options_dict)
    else:
        return dict()

def getData(month,year,area):
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

    if not (month and year and area):
        isNone = True
    data = {}
    for d in realizadas:
        if not isNone:
            yr = d['fecha_realizacion'].year
            mnth = d['fecha_realizacion'].month
            if not ((months[mnth] == month) and (yr == int(year)) and (d['nombre_area'] == area)):
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
            if not ((months[mnth] == month) and (yr == int(year)) and (d['nombre_area'] == area)):
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
            if not ((months[mnth] == month) and (yr == int(year)) and (d['nombre_area'] == area)):
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
            if not ((months[mnth] == month) and (yr == int(year)) and (d['nombre_area'] == area)):
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
            if not ((months[mnth] == month) and (yr == int(year)) and (d['nombre_area'] == area)):
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
            if not ((months[mnth] == month) and (yr == int(year)) and (d['nombre_area'] == area)):
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
            if not ((months[mnth] == month) and (yr == int(year)) and (d['nombre_area'] == area)):
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
            if not ((months[mnth] == month) and (yr == int(year)) and (d['nombre_area'] == area)):
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
            if not ((months[mnth] == month) and (yr == int(year)) and (d['nombre_area'] == area)):
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
            if not ((months[mnth] == month) and (yr == int(year)) and (d['nombre_area'] == area)):
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

def plugin_return_data():
    """ This is an example function to return a JSON-encoded array to the Google chart plugin.
    The URL should have a .json suffix
    This can also use the @auth.requires_signature() decorator
    """

    args = request.vars
    month = args.month
    year = args.year
    area = args.area

    info = getData(month,year,area)
    data = [['Areas','Solicitadas','Solucionadas','Pendientes','Anuladas',
             'Esperando Compra de Materiales por DPF','Esperando aporte de materiales por parte de usuario',
             'Listo','No procede','Orden Asignada','Orden Por Asignar','Realizada por contratista']]

    for key in info:
        d = []
        d.append(key)
        d.append(info[key]['totales'])
        d.append(info[key]['realizadas'])
        d.append(info[key]['pendientes'])
        d.append(info[key]['anuladas'])
        d.append(info[key]['esperando_c'])
        d.append(info[key]['esperando_a'])
        d.append(info[key]['listos'])
        d.append(info[key]['no_proceden'])
        d.append(info[key]['orden_asignadas'])
        d.append(info[key]['orden_por_asignar'])
        d.append(info[key]['realizada_p_c'])
        data.append(d)
        
    return dict(data=data)


def plugin_usage_example():
    return dict()
