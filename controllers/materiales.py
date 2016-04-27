# -*- coding: utf-8 -*-
from notificaciones import appendToDbMaterial

def index():
    redirect(URL('listar'))
    return locals()


def agregar():
    form = SQLFORM( db.Material, fields=['nombre','area','cantidad',
                                           'unidad_metrica','cantidad_Minima', 'especificacion'] )
    form.element(_id='submit_record__row')['_class'] += " text-center"
    form.element(_type='submit')['_class']="btn form_submit"
    form.element(_type='submit')['_value']="Agregar"
    if form.process().accepted:
        #AUTOUPDATE Material.status
        material = db(db.Material.nombre==form.vars.nombre).select().first()
        if int(form.vars.cantidad) > int(form.vars.cantidad_Minima):
            db.Material(material.id).update_record(status='Disponible')
        elif int(form.vars.cantidad) == int(form.vars.cantidad_Minima):
            db.Material(material.id).update_record(status='Critico')
        else:
            db.Material(material.id).update_record(status='No disponible')
        session.flash = T('El material fue agregado exitosamente!')


        #################### PARA NOTIFICACIONES #############################
        unidad= db(db.Unidad_metrica.id == request.vars.unidad_metrica).select(db.Unidad_metrica.nombre_unidadMetrica).as_list()[0]['nombre_unidadMetrica']
        appendToDbMaterial(request.vars.nombre, request.vars.cantidad, request.vars.cantidad_Minima,
            unidad)
        #######################################################################

        redirect(URL('listar'))
    elif form.errors:
        response.flash = T('La forma tiene errores, por favor llenela correctamente.')
    else:
        response.flash = T('Por favor llene la forma.')
    return locals()


def listar():
    filas = db(db.Material).select(orderby=db.Material.id)
    return locals()


def modificar():
    db.Material.status.writable = False
    cantAnterior = db(db.Material.id == request.args(0)).select(db.Material.cantidad).as_list()[0]['cantidad']
    print('MARICON ', cantAnterior)
    record = db.Material(request.args(0)) or redirect(URL('agregar'))
    form = SQLFORM(db.Material, record)
    form.element(_id='submit_record__row')['_class'] += " text-center"
    form.element(_type='submit')['_class']="btn form_submit"
    form.element(_type='submit')['_value']="Modificar"
    if form.process().accepted:
        #AUTOUPDATE Material.status
        db.Material.status.writable = True
        if int(form.vars.cantidad) > int(form.vars.cantidad_Minima):
            db.Material(form.vars.id).update_record(status='Disponible')
        elif int(form.vars.cantidad) == int(form.vars.cantidad_Minima):
            db.Material(form.vars.id).update_record(status='Critico')
        else:
            db.Material(form.vars.id).update_record(status='No disponible')
        session.flash = T('El material fue modificado exitosamente!')

        ###################### PARA NOTIFICACIONES ##########################
        if request.vars.cantidad != cantAnterior:
            unidad= db(db.Unidad_metrica.id == request.vars.unidad_metrica).select(db.Unidad_metrica.nombre_unidadMetrica).as_list()[0]['nombre_unidadMetrica']
            appendToDbMaterial(request.vars.nombre, request.vars.cantidad, request.vars.cantidad_Minima,
            unidad, cantAnterior)
        #######################################################################

        redirect(URL('listar'))
    else:
        response.flash = T('Por favor llene la forma.')
    return locals()
