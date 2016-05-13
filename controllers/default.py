# -*- coding: utf-8 -*-

from usbutils import get_ldap_data, random_key

#from applications.SIAGES.controllers.notificaciones import notifications_load #No funciona

### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires

def fillPlantillas():
    db.Notificacion_plantillas.insert(codigo='MAT_SUF', descripcion="MATERIAL SUFICIENTE: ",
        mensaje="Actualmente posee %cantidad% %unidad% de %nombre%.")
    db.Notificacion_plantillas.insert(codigo='MAT_INSUF', descripcion="MATERIAL INSUFICIENTE: ",
        mensaje="Actualmente posee %cantidad% %unidad% de %nombre%. Las existencias se encuentran en estado crítico.")
    db.Notificacion_plantillas.insert(codigo='NEW_INC', descripcion="INCORPORACIÓN DE PERSONAL: ",
        mensaje="Se informa que %nombre% ahora ejerce como %cargo% en %area%.")
    db.Notificacion_plantillas.insert(codigo='NEW_DES', descripcion="DESINCORPORACIÓN DE PERSONAL: ",
        mensaje="Se informa que %nombre% ha dejado de ejercer como %cargo% en %area%.")
    db.Notificacion_plantillas.insert(codigo='NEW_SOL', descripcion="NUEVA SOLICITUD",
        mensaje="Estimado(a) %nombre%.\nGracias por comunicarse con nosotros a través de nuestro correo electrónico. Cumplimos con informarle que en los actuales momentos estamos procesando su solicitud con el código #%id%,  la cual nos permitirá canalizar a la brevedad posible la situación planteada en el área de mantenimiento correspondiente.\nLe reiteramos nuestro compromiso para servirle mejor.\nDirección de Planta Física\nUnidad De Atención e Inspección\nExt. 3714 / 6114")
    db.Notificacion_plantillas.insert(codigo='SOL_CRE', descripcion='NUEVA SOLICITUD: ',
        mensaje="Se ha creado una nueva solicitud con el código %id%.")
    db.Notificacion_plantillas.insert(codigo='SOL_MOD', descripcion="SOLICITUD MODIFICADA",
        mensaje="Estimado(a) %nombre%. Gracias por comunicarse con nosotros a través de nuestro correo electrónico. Cumplimos con informarle que en los actuales momentos su solicitud con el codigo %id% se encuentra en estado %estado%.\nLe reiteramos nuestro compromiso para servirle mejor.\nDirección de Planta Física\nUnidad De Atención e Inspección\nExt. 3714 / 6114")

def index():
    plant=db(db.Notificacion_plantillas.id == 1).select()
    i = 0
    for p in plant:
        i+=1
    if i == 0:
        fillPlantillas()
    return  index_load();

def index_load():    #Esto deberia importarse desde notificaciones, pero no supe como.
    post_args=session.notification
    if post_args:
        myargs=post_args
    else:
        myargs=request.post_vars
    #db.commit()
    GLOBAL_ICONS={'1': "fa fa-bell", '2':"fa fa-envelope-o", '3':"fa fa-exclamation-circle", '4':"fa fa-exclamation-triangle", '5': "fa fa-comments-o", '6': "fa-flag"}
    icons=['1.png','2.png','3.png','4.png','5.png','6.png']

    tablaPlant = db(db.Notificacion_plantillas).select(db.Notificacion_plantillas.id, db.Notificacion_plantillas.descripcion)
    dicPlant = {}
    for plant in tablaPlant:
        dicPlant[plant.id] = plant.descripcion

    #En busqueda de materiales deficientes
    notificationList = db(db.Notificacion).select(orderby=~db.Notificacion.id)

    myNotif={'Mantenimiento':[],'Proyectos':[],'Planeación':[],'Administración':[],'Atención e Inspección':[], 'Global':[]}

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
            myIcon=GLOBAL_ICONS['1']
            date=notification.fecha.strftime("%d/%m/%Y")

            ntype_not="("+date+")-"+ dicPlant[notification.codigo_plantilla]
            myNotif['Global'].append({'texto':notification.mensaje,'ntype': ntype_not  ,'icon':myIcon    })
        myNotif['Global']=myNotif['Global'][0:15]
    return dict(myNotif=myNotif)

def login_cas():
    usuario = "ORYEBA"
    redirect(URL(c='default',f='index',vars=dict(usuario=usuario)))

    if not request.vars.getfirst('ticket'):
        #redirect(URL('error'))
        pass
    try:
        import urllib2, ssl
        # ssl._create_default_https_context = ssl._create_unverified_context
        url = "https://secure.dst.usb.ve/validate?ticket="+\
              request.vars.getfirst('ticket') +\
              "&service=http%3A%2F%2F127.0.0.1%3A8000%2FSIAGES%2Fdefault%2Flogin_cas"

        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        the_page = response.read()

    except Exception, e:
        print e
        usuario = "PRUEBA"
        redirect(URL(c='default',f='index',vars=dict(usuario=usuario)))
        # redirect(URL('error'))

    if the_page[0:2] == "no":
        redirect(URL('index'))
    else:
        # session.casticket = request.vars.getfirst('ticket')
        data  = the_page.split()
        usbid = data[1]

        usuario = get_ldap_data(usbid) #Se leen los datos del CAS

        usuario_guardado = db(db.Usuario.USBID == usbid) 
        session.usuario = {}
        session.usuario['usbid'] = usbid
        if (usuario_guardado):
            #Admin','UAI'
            if (usuario_guardado.tipo=="Admin"):
                session.usuario['tipo']="A"
            else:
                session.usuario['tipo']="U"
        else:
            session.usuario['tipo']="S"

        redirect(URL(c='default',f='index_logged',vars=dict(usuario=usuario)))


def index_logged():
    session.usuario = {"tipo":"S"}
    session.usuario['usbid'] = "0910502"
    return index()

@auth.requires_login()
def notifications():
    return dict()

@auth.requires_login()
def requests():
    return dict()

@auth.requires_login()
def inventory():
    return dict()

@auth.requires_login()
def sb():
    return dict()

def error():
    return dict()

'''<!--       <div class="collapse navbar-collapse navbar-ex1-collapse">
          <ul class="nav navbar-nav navbar-right">
            {{='auth' in globals() and auth.navbar('Welcome',mode='dropdown') or ''}}
          </ul>
       </div> -->'''