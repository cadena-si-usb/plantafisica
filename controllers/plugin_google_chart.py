

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

def getData(month,year):
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
            if not ((months[mnth] == month) and (yr == year)):
                continue 
        if d['nombre_area'] not in data.keys():
            data[d['nombre_area']] = {
                'realizadas': d['count(Solicitud.area)'],
                'pendientes': 0,
                'anuladas': 0,
                'totales': d['count(Solicitud.area)'],
            }
    for d in pendientes:
        if not isNone:
            yr = d['fecha_realizacion'].year
            mnth = d['fecha_realizacion'].month
            if not ((months[mnth] == month) and (yr == year)):
                continue 
        if d['nombre_area'] not in data.keys():
            data[d['nombre_area']] = {
                'realizadas': 0,
                'anuladas': 0,
                'pendientes': d['count(Solicitud.area)'],
                'totales': d['count(Solicitud.area)'],
            }
        else:
            data[d['nombre_area']]['totales'] += d['count(Solicitud.area)']
            data[d['nombre_area']]['pendientes'] = d['count(Solicitud.area)']
    for d in anuladas:
        if not isNone:
            yr = d['fecha_realizacion'].year
            mnth = d['fecha_realizacion'].month
            if not ((months[mnth] == month) and (yr == year)):
                continue 
        if d['nombre_area'] not in data.keys():
            data[d['nombre_area']] = {
                'pendientes': 0,
                'realizadas': 0,
                'anuladas': d['count(Solicitud.area)'],
                'totales': d['count(Solicitud.area)'],
            }
        else:
            data[d['nombre_area']]['totales'] += d['count(Solicitud.area)']
            data[d['nombre_area']]['anuladas'] = d['count(Solicitud.area)']

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
    print "*************************************"
    print month,year
    print "*************************************"

    info = getData(month,year)
    data = [['Areas','Solicitadas','Solucionadas','Pendientes','Anuladas']]

    for key in info:
        d = []
        d.append(key)
        d.append(info[key]['totales'])
        d.append(info[key]['realizadas'])
        d.append(info[key]['pendientes'])
        d.append(info[key]['anuladas'])
        data.append(d)
        
    if (month and year):
        redirect(URL('estadisticas','estadisticas', vars=dict(data=data)))
    return dict(data=data)


def plugin_usage_example():
    return dict()
