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
    elif request.args(0)=='internos':
        filas = db(db.Usuario.tipo=='Interno').select(orderby=db.Usuario.id)
        response.flash = T('Solo se muestran usuarios internos.')
    elif request.args(0)=='externos':
        filas = db(db.Usuario.tipo=='Externos').select(orderby=db.Usuario.id)
        response.flash = T('Solo se muestran usuarios externos.')
    return locals()
