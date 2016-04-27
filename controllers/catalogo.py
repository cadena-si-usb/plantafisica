# -*- coding: utf-8 -*-

def catalogue():
    personal = db().select(db.Empleado.ALL, orderby=db.Empleado.nombre)
    edificio = db().select(db.Edificio.ALL, orderby=db.Edificio.nombre_edificio)
    material = db().select(db.Material.ALL, orderby=db.Material.nombre)
    area = db().select(db.Area.ALL, orderby=db.Area.nombre_area)
    supervisor = db(db.Empleado.cargo=='Supervisor').select(db.Empleado.ALL, orderby=db.Empleado.nombre)
    unidad = db().select(db.Unidad.ALL, orderby=db.Unidad.nombre_unidad)
    status_solicitud = db().select(db.Status_solicitud.ALL, orderby=db.Status_solicitud.nombre_status)
    prioridad = db().select(db.Prioridad.ALL, orderby=db.Prioridad.nombre_prioridad)
    lugar = db().select(db.Lugar.ALL, orderby=db.Lugar.edificio)
    unidad_metrica = db().select(db.Unidad_metrica.ALL, orderby=db.Unidad_metrica.nombre_unidadMetrica)
    cod = None

    if request.args(2) == None:
        if request.args(0)!=None:
            cod = request.args(0)

    form_unidadMetrica = SQLFORM(db.Unidad_metrica)
    form_unidadMetrica.element(_type='submit')['_class']="btn form_submit"
    form_unidadMetrica.element(_type='submit')['_value']="Agregar"
    if form_unidadMetrica.accepts(request.vars, session):
        unidad_metrica = db().select(db.Unidad_metrica.ALL, orderby=db.Unidad_metrica.nombre_unidadMetrica)
        response.flash = T('Se ha creado una Unidad Métrica')
        cod = "tabla_unidadMetrica"
    elif form_unidadMetrica.errors:
        response.flash = T('No se ha podido crear una Unidad Métrica')

    form_edificio = SQLFORM(db.Edificio)
    form_edificio.element(_type='submit')['_class']="btn form_submit"
    form_edificio.element(_type='submit')['_value']="Agregar"
    if form_edificio.accepts(request.vars, session):
        edificio = db().select(db.Edificio.ALL, orderby=db.Edificio.nombre_edificio)
        response.flash = T('Se ha creado un Edificio.')
        cod = "tabla_edificio"
    elif form_edificio.errors:
        response.flash = T('No se ha podido crear un Edificio.')

    form_area = SQLFORM(db.Area)
    form_area.element(_type='submit')['_class']="btn form_submit"
    form_area.element(_type='submit')['_value']="Agregar"
    if form_area.accepts(request,session):
        area = db().select(db.Area.ALL, orderby=db.Area.nombre_area)
        response.flash = T('Se ha creado un Área.')
        cod = "tabla_area"
    elif form_area.errors:
        response.flash = T('No se ha podido crear un Área')

    form_unidad = SQLFORM(db.Unidad)
    form_unidad.element(_type='submit')['_class']="btn form_submit"
    form_unidad.element(_type='submit')['_value']="Agregar"
    if form_unidad.accepts(request.vars, session):
        unidad = db().select(db.Unidad.ALL, orderby=db.Unidad.nombre_unidad)
        response.flash = T('Se ha creado una Unidad.')
        cod = "tabla_unidades"
    elif form_unidad.errors:
        response.flash = T('No se ha podido crear una Unidad.')

    form_status = SQLFORM(db.Status_solicitud)
    form_status.element(_type='submit')['_class']="btn form_submit"
    form_status.element(_type='submit')['_value']="Agregar"
    if form_status.accepts(request.vars, session):
        status_solicitud = db().select(db.Status_solicitud.ALL, orderby=db.Status_solicitud.nombre_status)
        response.flash = T('Se ha creado un Estatus de Solicitud.')
        cod = "tabla_statusSolicitud"
    elif form_status.errors:
        response.flash = T('No se ha podido crear un Estatus de Solicitud.')

    form_prioridad = SQLFORM(db.Prioridad)
    form_prioridad.element(_type='submit')['_class']="btn form_submit"
    form_prioridad.element(_type='submit')['_value']="Agregar"
    if form_prioridad.accepts(request.vars, session):
        prioridad = db().select(db.Prioridad.ALL, orderby=db.Prioridad.nombre_prioridad)
        response.flash = T('Se ha creado una Prioridad')
        cod = "tabla_prioridad"
    elif form_prioridad.errors:
        response.flash = T('No se ha podido crear una Prioridad.')

    form_lugar = SQLFORM(db.Lugar)
    form_lugar.element(_type='submit')['_class']="btn form_submit"
    form_lugar.element(_type='submit')['_value']="Agregar"
    if form_lugar.accepts(request.vars, session):
        lugar = db().select(db.Lugar.ALL, orderby=db.Lugar.edificio)
        response.flash = T('Se ha creado un Lugar')
        cod = "tabla_lugar"
    elif form_lugar.errors:
        response.flash = T('No se ha podido crear una Lugar.')

    if request.args(2) != None:
        if (request.args(0)=='area'):
            if (request.args(1)=='nombre_area'):
                area = db().select(db.Area.ALL, orderby=db.Area.nombre_area)
            elif (request.args(1)=='nomenclatura'):
                area = db().select(db.Area.ALL, orderby=db.Area.nomenclatura)
            cod = "tabla_area"

        elif (request.args(0)=='edificio'):
            if (request.args(1)=='nombre_edificio'):
                edificio = db().select(db.Edificio.ALL, orderby=db.Edificio.nombre_edificio)
            elif (request.args(1)=='nomenclatura'):
                edificio = db().select(db.Edificio.ALL, orderby=db.Edificio.nomenclatura)
            cod = "tabla_edificio"

        elif (request.args(0)=='lugar'):
            if (request.args(1)=='edificio'):
                lugar = db().select(db.Lugar.ALL, orderby=db.Lugar.edificio)
            elif (request.args(1)=='espacio'):
                lugar = db().select(db.Lugar.ALL, orderby=db.Lugar.espacio)
            cod = "tabla_lugar"

        elif (request.args(0)=='empleado'):
            if (request.args(1)=='nombre'):
                personal = db().select(db.Empleado.ALL, orderby=db.Empleado.nombre)
            cod = "tabla_empleado"

        elif (request.args(0)=='material'):
            if (request.args(1)=='nombre'):
                material = db().select(db.Material.ALL, orderby=db.Material.nombre)
            elif (request.args(1)=='cantidad'):
                material = db().select(db.Material.ALL, orderby=db.Material.cantidad)
            cod = "tabla_material"

    return dict(personal=personal,edificio=edificio,material=material,area=area,supervisor=supervisor,unidad=unidad,status_solicitud=status_solicitud,prioridad=prioridad,form_edificio = form_edificio,form_area = form_area,form_unidad = form_unidad,form_status = form_status,form_prioridad = form_prioridad,lugar = lugar,form_lugar=form_lugar,unidad_metrica = unidad_metrica,form_unidadMetrica = form_unidadMetrica, cod = cod)

def eliminar():
    if (request.args(1)=='lugar'):
        db(db.Lugar.id==request.args(0)).delete()
        cod = "tabla_lugar"

    elif (request.args(1)=='edificio'):
        db(db.Edificio.id==request.args(0)).delete()
        cod = "tabla_edificio"

    elif (request.args(1)=='area'):
        db(db.Area.id==request.args(0)).delete()
        cod = "tabla_area"

    elif (request.args(1)=='unidad'):
        db(db.Unidad.id==request.args(0)).delete()
        cod = "tabla_unidades"

    elif (request.args(1)=='status'):
        db(db.Status_solicitud.id==request.args(0)).delete()
        cod = "tabla_statusSolicitud"

    elif (request.args(1)=='prioridad'):
        db(db.Prioridad.id==request.args(0)).delete()
        cod = "tabla_prioridad"

    elif (request.args(1)=='unidad_metrica'):
        db(db.Unidad_metrica.id==request.args(0)).delete()
        cod = "tabla_unidadMetrica"

    redirect(URL('catalogue',args=cod))
    return dict(cod = cod)

def mod_catalogo():
    if (request.args(1)=='lugar'):
        record = db.Lugar(request.args(0))
        form = SQLFORM(db.Lugar, record)
        title = "Lugar"
        cod = "tabla_lugar"

    elif (request.args(1)=='edificio'):
        record = db.Edificio(request.args(0))
        form = SQLFORM(db.Edificio, record)
        title = "Edificio"
        cod = "tabla_edificio"

    elif (request.args(1)=='area'):
        record = db.Area(request.args(0))
        form = SQLFORM(db.Area, record)
        title = "Área de Trabajo"
        cod = "tabla_area"

    elif (request.args(1)=='unidad'):
        record = db.Unidad(request.args(0))
        form = SQLFORM(db.Unidad, record)
        title = "Unidad"
        cod = "tabla_unidades"

    elif (request.args(1)=='status'):
        record = db.Status_solicitud(request.args(0))
        form = SQLFORM(db.Status_solicitud, record)
        title = "Estado de la Solicitud"
        cod = "tabla_statusSolicitud"

    elif (request.args(1)=='prioridad'):
        record = db.Prioridad(request.args(0))
        form = SQLFORM(db.Prioridad, record)
        title = "Prioridad"
        cod = "tabla_prioridad"

    elif (request.args(1)=='unidad_metrica'):
        record = db.Unidad_metrica(request.args(0))
        form = SQLFORM(db.Unidad_metrica, record)
        title = "Unidad Métrica"
        cod = "tabla_unidadMetrica"

    form.element(_type='submit')['_class']="btn form_submit"
    form.element(_type='submit')['_value']="Modificar"

    if form.process().accepted:
        response.flash = T('Se ha realizado la modificación exitosamente.')
    elif form.errors:
        response.flash = T('Se ha realizado la modificación.')

    return locals()

def listarCatalogo():
    pass
    return locals()

