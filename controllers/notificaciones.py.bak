# -*- coding: utf-8 -*-
### required - do no delete
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
                response.flash = T('Correo enviado exitosamente.')
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
    session.notification=request.post_vars
    return  notifications_load();

def notifications_load():    #Flush de la tabla
    post_args=session.notification
    if post_args:
        myargs=post_args
    else:
        myargs=request.post_vars
    #db.commit()
    GLOBAL_ICONS={'1': "fa fa-bell", '2':"fa fa-envelope-o", '3':"fa fa-exclamation-circle", '4':"fa fa-exclamation-triangle", '5': "fa fa-comments-o", '6': "fa-flag"}
    icons=['1.png','2.png','3.png','4.png','5.png','6.png']
    myNotif={'Departamento de Mantenimiento':[],'Departamento de Proyectos':[],'Departamento de Planificación':[],'Departamento de Administración':[],'Unidad de Atención e Inspección':[], 'Global':[]}
    
    tablaPlant = db(db.Notificacion_plantillas).select(db.Notificacion_plantillas.id, db.Notificacion_plantillas.descripcion)
    dicPlant = {}
    for plant in tablaPlant:
        dicPlant[plant.id] = plant.descripcion
        
    #En busqueda de materiales deficientes
    notificationList = db(db.Notificacion).select(orderby=~db.Notificacion.id)

    if myargs!={}:
        notificationList = filterNotif(myargs['busq'],myargs['fecha'],myargs['words'],myargs['tipo'],notificationList)
        response.flash = T('Por favor llene la forma.')


    if not notificationList:
        return dict(myNotif=myNotif)
    else:
        icons=[]
        templates=db(db.Notificacion_habilitada).select(orderby=db.Notificacion_habilitada.codigo_plantilla)
        for template in templates:
            icons.append(template.icono)

        for notification in notificationList:
            myIcon=GLOBAL_ICONS[icons[0]]
            date=notification.fecha.strftime("%d/%m/%Y")
            ntype_not="("+date+")-"+ dicPlant[notification.codigo_plantilla]
            # link=db(db.Notificacion_Solicitud.id_notif == notification.id).select(db.Notificacion_Solicitud.id_sol).as_list()[0]['id_sol']
            if notification.departamento:
                link=''
                myNotif[notification.departamento].append({'texto':notification.mensaje,'ntype': ntype_not  ,'icon':myIcon,'link':link    })
                myNotif['Global'].append({'texto':notification.mensaje,'ntype': ntype_not  ,'icon':myIcon,'link':link    })
            else:
                link=''
                myNotif['Global'].append({'texto':notification.mensaje,'ntype': ntype_not  ,'icon':myIcon,'link':link    })
    return dict(myNotif=myNotif)

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

def error():
    return dict()

