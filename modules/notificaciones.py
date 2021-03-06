# -*- coding: utf-8 -*-
### required - do no delete
# from gluon import *
from gluon.tools import Mail

mail = Mail()
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'cybertechsolts@gmail.com'
mail.settings.login = 'cybertechsolts@gmail.com:perreoperreo'

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires

def index():
    redirect(URL('notifications'))
    return locals()
    
def modificarnotif():
    form = SQLFORM.factory(
        Field('Correo', requires =[ IS_NOT_EMPTY(error_message='Campo Requerido'), IS_EMAIL(error_message='Correo inválido') ]),
        Field('Asunto', requires=IS_NOT_EMPTY(error_message='Campo Requerido')),
        Field('Mensaje', requires=IS_NOT_EMPTY(error_message='Campo Requerido'), type='text'),submit_button='Enviar'
    )

    strings = form.elements(_class='string')

    btn = form.elements(_class='btn btn-primary')
    for b in btn:
        b['_class'] = 'btn form_submit'

    btnc = form.elements(_class='w2p-form-button')
    for b in btnc:
        b['_class'] = 'btn form_cancel'

    if form.process().accepted:
        session.name = form.vars.name
        session.email = form.vars.Correo
        session.subject = form.vars.Asunto
        session.message = form.vars.Mensaje
        if mail:
            if mail.send(to=form.vars.Correo,
                subject=form.vars.Asunto,
                message=form.vars.Mensaje):
                response.flash = 'email sent sucessfully.'
            else:
                response.flash = 'fail to send email sorry!'
        else:
            response.flash = 'Unable to send the email : email parameters not defined'
    elif form.errors:
            response.flash='form has errors.'

    response.flash='you clicked on civilized'

    return dict(form=form)


def filterNotif(iSearch,iDate,iwords,itype,notificationList):
    from datetime import datetime

    if iDate=="":
        pass
    else:
        myDate=datetime.strptime(iDate, '%d/%m/%Y')
    myWords=[x.strip() for x in iwords.split(',')]
    mySearch=[x.strip() for x in iSearch.split()]
    newList=[]

    for row in notificationList:
        if iDate=="":
            dateCheck = True
        else:
            dateCheck = row.fecha==myDate

        if iwords=="":
            wordsCheck=True
        else:
            wordsCheck=any([x in str(row) for x in myWords])

        if iSearch=="":
            searchCheck=True
        else:
            searchCheck=any([x in str(row) for x in mySearch])

        if itype=='0':
            typeCheck=True
        else:
            print row.codigo_plantilla
            print type(row.codigo_plantilla)
            print itype
            typeCheck=int(row.codigo_plantilla)==int(itype)

        if dateCheck and wordsCheck and searchCheck and typeCheck:
            newList.append(row)

    return newList
def notifications():
    print('En notifications:')
    print request.post_vars
    session.notification=request.post_vars
    #redirect(URL('notifications_load', vars=dict(postit=request.post_vars)))
    return  notifications_load();

def notifications_load():    #Flush de la tabla
    print('En el otro:')
    print(request.post_vars)
    post_args=session.notification
    if post_args:
        myargs=post_args
    else:
        myargs=request.post_vars
    #db.commit()
    GLOBAL_ICONS={'1': "fa fa-bell", '2':"fa fa-envelope-o", '3':"fa fa-exclamation-circle", '4':"fa fa-exclamation-triangle", '5': "fa fa-comments-o", '6': "fa-flag"}
    ntype=['MATERIAL SUFICIENTE: ', 'MATERIAL INSUFICIENTE: ','INCORPORACIÓN DE PERSONAL: ', 'DESINCORPORACIÓN DE PERSONAL: ']
    icons=['1.png','2.png','3.png','4.png','5.png','6.png']
    #En busqueda de materiales deficientes
    notificationList = db(db.Notificacion).select(orderby=db.Notificacion.id)
    myNotif={'Mantenimiento':[],'Proyectos':[],'Planeación':[],'Administración':[],'Atención e Inspección':[], 'Global':[]}

    if myargs!={}:
        #print notificationList
        notificationList = filterNotif(myargs['busq'],myargs['fecha'],myargs['words'],myargs['tipo'],notificationList)
        print("falle aca?")
        print(notificationList)
        response.flash = T('Por favor llene la forma.')


    if not notificationList:
        return dict(myNotif=myNotif)
    else:
        icons=[]
        templates=db(db.Notificacion_habilitada).select(orderby=db.Notificacion_habilitada.codigo_plantilla)
        for template in templates:
            icons.append(template.icono)

        for notification in notificationList:
            print "wooot"
            myIcon=GLOBAL_ICONS[icons[int(notification.codigo_plantilla)-1]]
            date=notification.fecha.strftime("%d/%m/%Y")
            ntype_not="("+date+")-"+ntype[int(notification.codigo_plantilla)-1]
            myNotif[notification.departamento].append({'texto':notification.mensaje,'ntype': ntype_not  ,'icon':myIcon    })
            myNotif['Global'].append({'texto':notification.mensaje,'ntype': ntype_not  ,'icon':myIcon    })
    return dict(myNotif=myNotif)

# @auth.requires_login()
def requests():

    return dict()

def show_send_email():

    form = SQLFORM.factory(
        Field('Correo', requires =[ IS_NOT_EMPTY(error_message='Campo Requerido'), IS_EMAIL(error_message='Correo inválido') ]),
        Field('Asunto', requires=IS_NOT_EMPTY(error_message='Campo Requerido')),
        Field('Mensaje', requires=IS_NOT_EMPTY(error_message='Campo Requerido'), type='text'),submit_button='Enviar'
    )

    strings = form.elements(_class='string')
    form.add_button('Regresar', URL('default','notifications'))

    btn = form.elements(_class='btn btn-primary')
    for b in btn:
        b['_class'] = 'btn form_submit'

    btnc = form.elements(_class='w2p-form-button')
    for b in btnc:
        b['_class'] = 'btn form_cancel'

    if form.process().accepted:
        session.name = form.vars.name
        session.email = form.vars.Correo
        session.subject = form.vars.Asunto
        session.message = form.vars.Mensaje
        if mail:
            if mail.send(to=form.vars.Correo,
                subject=form.vars.Asunto,
                message=form.vars.Mensaje):
                response.flash = 'email sent sucessfully.'
            else:
                response.flash = 'fail to send email sorry!'
        else:
            response.flash = 'Unable to send the email : email parameters not defined'
    elif form.errors:
            response.flash='form has errors.'

    response.flash='you clicked on civilized'

    return dict(form=form)

def send_mail(name, code, maile, estado = None, observacion = None):
    from gluon import current
    import re
    db = current.db

    if estado:
        estado = estado['nombre_status']
        mensaje = db(db.Notificacion_plantillas.id == 7).select()[0]
        mensaje = str(mensaje['mensaje'])
        mensaje = mensaje.replace("%nombre%", "<b>"+name+"</b>")
        mensaje = mensaje.replace("%id%", "<b>"+str(code)+"</b>")
        mensaje = mensaje.replace("%estado%", "<b>"+estado+"</b>")
        if observacion == None:
            mensaje = mensaje.replace("mejor.","mejor.<b>Observación: Ninguna</b>") 
        else:
            mensaje = mensaje.replace("mejor.","mejor.<b>Observación: "+observacion+"</b>")

        mail.send(to=[maile],
                  subject='Estado de la Solicitud: #' + str(code),
                  reply_to='cybertechsolts@gmail.com',
                  message=(None,mensaje)
                  )
    else:
        mensaje = db(db.Notificacion_plantillas.id == 5).select()[0]
        mensaje = str(mensaje['mensaje'])
        mensaje = mensaje.replace("%nombre%", name)
        mensaje = mensaje.replace("%id%", str(code))

        mail.send(to=[maile],
                  subject='Solicitud recibida: #' + str(code),
                  reply_to='cybertechsolts@gmail.com',
                  message=mensaje
                  )
    # return dict()

def appendToDbSol(code, dept):
    from gluon import current
    db = current.db


    mensaje = db(db.Notificacion_plantillas.id == 6).select()[0]
    mensaje = str(mensaje['mensaje'])
    mensaje = mensaje.replace("%id%", str(code))

    db.Notificacion.insert(codigo_plantilla=6, mensaje=mensaje, departamento=dept)

def appendToDbEmployee(nombre, cargo, area, estado):
    from gluon import current
    db = current.db

    if (estado == 'Activo'):
        mensaje = db(db.Notificacion_plantillas.id == 3).select()[0]
        mensaje = str(mensaje['mensaje'])
        mensaje = mensaje.replace("%nombre%", nombre)
        mensaje = mensaje.replace("%cargo%", cargo)
        mensaje = mensaje.replace("%area%", area)

        db.Notificacion.insert(codigo_plantilla=3, mensaje=mensaje)
        
    else:
        mensaje = db(db.Notificacion_plantillas.id == 4).select()[0]
        mensaje = str(mensaje['mensaje'])
        mensaje = mensaje.replace("%nombre%", nombre)
        mensaje = mensaje.replace("%cargo%", cargo)
        mensaje = mensaje.replace("%area%", area)

        db.Notificacion.insert(codigo_plantilla=4, mensaje=mensaje)

def appendToDbMaterial(nombre, cant, minimun, unidad, cantAnterior=None):
    from gluon import current
    db=current.db
    
    cant = int(cant)
    minimun = int(minimun)
    if not cantAnterior:
        cantAnterior = 0
    
    # Agregando
    if cantAnterior < cant:
        # Agregue y la cantidad es suficiente
        if cant > minimun:
            mensaje = db(db.Notificacion_plantillas.id == 1).select()[0]
            mensaje = str(mensaje['mensaje'])
            mensaje = mensaje.replace("%cantidad%", str(cant))
            mensaje = mensaje.replace("%unidad%", unidad)
            mensaje = mensaje.replace("%nombre%", nombre)
            
            db.Notificacion.insert(codigo_plantilla=1, mensaje=mensaje)
        # Agregue pero la cantidad es insuficiente
        else:
            mensaje = db(db.Notificacion_plantillas.id == 2).select()[0]
            mensaje = str(mensaje['mensaje'])
            mensaje = mensaje.replace("%cantidad%", str(cant))
            mensaje = mensaje.replace("%unidad%", unidad)
            mensaje = mensaje.replace("%nombre%", nombre)
            
            db.Notificacion.insert(codigo_plantilla=2, mensaje=mensaje)

    else:
        # Quite y la cantidad es suficiente
        if cant > minimun:
            mensaje = db(db.Notificacion_plantillas.id == 1).select()[0]
            mensaje = str(mensaje['mensaje'])
            mensaje = mensaje.replace("%cantidad%", str(cant))
            mensaje = mensaje.replace("%unidad%", unidad)
            mensaje = mensaje.replace("%nombre%", nombre)
            
            db.Notificacion.insert(codigo_plantilla=1, mensaje=mensaje)
        # Quite pero la cantidad es insuficiente
        else:
            mensaje = db(db.Notificacion_plantillas.id == 2).select()[0]
            mensaje = str(mensaje['mensaje'])
            mensaje = mensaje.replace("%cantidad%", str(cant))
            mensaje = mensaje.replace("%unidad%", unidad)
            mensaje = mensaje.replace("%nombre%", nombre)
            
            db.Notificacion.insert(codigo_plantilla=2, mensaje=mensaje)

def error():
    return dict()
