# -*- coding: utf-8 -*-
from notificaciones import appendToDbEmployee

def index():
    redirect(URL('listar'))
    return locals()


def agregar():
    form = SQLFORM(db.Empleado)
    form.element(_id='submit_record__row')['_class'] += " text-center"
    form.element(_type='submit')['_class']="btn form_submit " 
    form.element(_type='submit')['_value']="Agregar" 
    if form.process().accepted:
        session.flash = T('El empleado fue agregado exitosamente!')

        ######################### PARA NOTIFICACIONES ##########################
        area = db(db.Area.id == request.vars.area).select(db.Area.nombre_area).as_list()[0]['nombre_area']
        appendToDbEmployee(request.vars.nombre, request.vars.cargo, area, request.vars.estado)
        #######################################################################

        redirect(URL('listar'))
    elif form.errors:
        response.flash = T('La forma tiene errores, por favor llenela correctamente.')
    else:
        response.flash = T('Por favor llene la forma.')
    return locals()


def listar():
    if request.args(0)==None:
        filas = db(db.Empleado).select(orderby=db.Empleado.id)
    elif request.args(0)=='activos':
        filas = db(db.Empleado.estado=='Activo').select()
        response.flash = T('Solo se muestran empleados activos.')
    elif request.args(0)=='inactivos':
        filas = db(db.Empleado.estado=='Inactivo').select()
        response.flash = T('Solo se muestran empleados inactivos.')
    return locals()


def modificar():
    ###########################################################################
    query= db(db.Empleado.id == request.args(0)).select()[0]
    statAnt= query['estado']
    nomAnt= query['nombre']
    cargoAnt= query['cargo']
    area= db(db.Area.id == query['area']).select(db.Area.nombre_area).as_list()[0]['nombre_area']
    ###########################################################################
    
    record = db.Empleado(request.args(0)) or redirect(URL('agregar'))
    form = SQLFORM(db.Empleado, record)
    form.element(_id='submit_record__row')['_class'] += " text-center"
    form.element(_type='submit')['_class']="btn form_submit " 
    form.element(_type='submit')['_value']="Modificar" 
    if form.process().accepted:
        #######################################################################
        if request.vars.estado != statAnt:
            print(request.vars.nombre, request.vars.estado, statAnt)
            appendToDbEmployee(request.vars.nombre, request.vars.cargo, area, request.vars.estado)
        #######################################################################
        session.flash = T('El empleado fue modificado exitosamente!')
        redirect(URL('listar'))
    else:
        response.flash = T('Por favor llene la forma.')
    return locals()
