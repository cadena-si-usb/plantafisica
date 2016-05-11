# -*- coding: utf-8 -*-

def index():
    redirect(URL('listar'))
    return locals()

def agregar():
    form = SQLFORM( db.Usuario, fields=['nombre','USBID','correo','tipo'] )
    form.element(_type='submit')['_class']="btn form_submit"
    form.element(_type='submit')['_value']="Agregar"

    if form.process().accepted:
        session.flash = T('El usuario fue agregado exitosamente')
        redirect(URL('listar'))
    elif form.errors:
        response.flash = T('El Usuario tiene errores, por favor verifique todos los campos.')
    else:
        response.flash = T('Por favor llene la forma.')
    return locals()

def listar():
    if request.args(0)==None:
        filas = db(db.Usuario).select(orderby=db.Usuario.id)
    elif request.args(0)=='admin':
        filas = db(db.Usuario.tipo=='Admin').select(orderby=db.Usuario.id)
        response.flash = T('Solo se muestran usuarios administradores.')
    elif request.args(0)=='uai':
        filas = db(db.Usuario.tipo=='UAI').select(orderby=db.Usuario.id)
        response.flash = T('Solo se muestran usuarios UAI.')
    return locals()

def modificar():
    ###########################################################################
    query = db(db.Usuario.id == request.args(0)).select()[0]
    ###########################################################################
    
    record = db.Usuario(request.args(0)) or redirect(URL('agregar'))
    form = SQLFORM(db.Usuario, record)
    form.element(_id='submit_record__row')['_class'] += " text-center"
    form.element(_type='submit')['_class']="btn form_submit " 
    form.element(_type='submit')['_value']="Modificar" 
    if form.process().accepted:
        session.flash = T('El usuario fue modificado exitosamente!')
        redirect(URL('listar'))
    else:
        response.flash = T('Por favor llene la forma.')
    return locals()
