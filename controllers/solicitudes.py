# -*- coding: utf-8 -*-

from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors
from uuid import uuid4
import os
from gluon.tools import Crud, Mail
from notificaciones import send_mail, appendToDbSol

crud = Crud(db)

mail = Mail()
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'cybertechsolts@gmail.com'
mail.settings.login = 'cybertechsolts@gmail.com:perreoperreo'

def index():
    redirect(URL('listar'))
    return locals()

def cantidadBuena(form):
  material = db(db.Material.id == form.vars.material).select()[0]
  if form.vars.cantidad > material.cantidad:
    form.errors.cantidad = "No puedes exceder la cantidad de material disponible."

def show():
    solicitud = db(db.Solicitud.id == request.args[0]).select()[0]
    materiales = db(db.Solicitud_Material.solicitud == solicitud.id).select()

    form = SQLFORM( db.Solicitud_Material, fields=['material', 'cantidad'])
    form.vars.solicitud = int(request.args[0])
    form.element(_type='submit')['_class']="btn form_submit"
    form.element(_type='submit')['_value']="Agregar"

    if form.process(onvalidation=cantidadBuena).accepted:

      material = db(db.Material.id == request.vars.material).select().first()
      material.update_record(cantidad = material.cantidad - long(request.vars.cantidad))

      response.flash = T('Se ha agregado el material')
    elif form.errors:
      response.flash = T('Formulario tiene errores, por favor verifique todos los campos.')
    else:
      response.flash = T('Por favor llene la forma.')

    return dict(solicitud=solicitud, form=form, materiales=materiales)

def validacionesExtras(form):
  # Validar que fecha de culminacion sea el mismo dia o despues del de inicio
  if form.vars.fecha_inicio > form.vars.fecha_culminacion:
    form.errors.fecha_culminacion = "Fecha de culminacion debe ser despues de fecha de inicio"

  # Validar que el lugar pertenece a ese edificio
  lugar = db(db.Lugar.id == form.vars.espacio).select()[0]
  if form.vars.edificio != lugar.edificio:
    form.errors.espacio = "El Espacio no corresponde al edificio"

def agregar():
    if session.usuario['tipo'] == "S":
      form = SQLFORM( db.Solicitud, fields=['unidad', 'nombre_contacto', 'info_contacto','telefono',
                                            'edificio','ubicacion', 'requerimiento',
                                            'observacion_solicitud'] )
    else :
      form  = SQLFORM( db.Solicitud, fields=['prioridad','area', 'tipo', 'unidad', 'nombre_contacto', 'info_contacto','telefono',
                                            'edificio','espacio', 'ubicacion', 'requerimiento',
                                            'observacion_solicitud','fecha_inicio','fecha_culminacion','trabajador','vision', 'status'] )

    form.vars.USBID = session.usuario['usbid']
    #form.fields[usbid] = session.usuario['usbid']
    form.element(_id='submit_record__row')['_class'] += " text-center"
    form.element(_type='submit')['_class']="btn form_submit"
    form.element(_type='submit')['_value']="Crear"
    form.element('textarea[name=requerimiento]')['_style']='height:50px'
    form.element('textarea[name=observacion_solicitud]')['_style']='height:50px'
    form.element(_name='telefono')['_style']='width:130px'
    if session.usuario['tipo'] !="S":
      form.element(_name='fecha_inicio')['_style']= 'width:130px'
      form.element(_name='fecha_culminacion')['_style']='width:130px'
      form.element(_name='vision')['_style']='width:130px'

    if form.process(onvalidation=validacionesExtras).accepted:
        #######################################################################
        #################### ENVIO DEL CORREO DE SOLICITUD ####################
        idSol = db(db.Solicitud).select(db.Solicitud.ALL).as_list()[-1]['id']
        correo = request.vars.info_contacto
        send_mail(request.vars.nombre_contacto, idSol, correo)
        #######################################################################
        ############ INGRESA LA NOTIFICACION DE LA SOLICITUD ##################
        #######################################################################
        dept = request.vars.tipo
        novo = appendToDbSol(idSol, dept)
        # idNotif = db(db.Notificacion).select(db.Solicitud.id).as_list()[-1]['id']
        idNotif = db(db.Notificacion).select()[-1]['id']
        db.Notificacion_Solicitud.insert(id_sol=idSol, id_notif=idNotif)
        #######################################################################

        session.flash = T('Solicitud creada exitosamente')
        redirect(URL('listar'))
    elif form.errors:
        response.flash = T('Solicitud tiene errores, por favor verifique todos los campos.')
    else:
        response.flash = T('Por favor llene la forma.')
    return locals()

def listar():
    if session.usuario['tipo'] == "S":
      publicas = db(db.Solicitud.vision == "Publica").select(orderby=db.Solicitud.id)
      privadas = db(db.Solicitud.USBID == session.usuario['usbid']).select(orderby=db.Solicitud.id)
      filas = publicas | privadas
    else :
      filas = db(db.Solicitud).select(orderby=db.Solicitud.id)
    return locals()

def modificar():
    ###########################################################################
    query= db(db.Solicitud.id == request.args(0)).select()
    solicitudAntStat = query[0]['status']
    solicitudAntDept = query[0]['tipo']
    ###########################################################################
    record = db.Solicitud(request.args(0))
    if session.usuario['tipo'] == "S":
      form = SQLFORM( db.Solicitud, record = record, fields=['unidad', 'nombre_contacto', 'info_contacto', 'telefono',
                                            'edificio','ubicacion', 'requerimiento',
                                            'observacion_solicitud'] )
    else :
      form  = SQLFORM( db.Solicitud, record = record, fields=['prioridad','area', 'tipo', 'unidad', 'nombre_contacto', 'info_contacto','telefono',
                                            'edificio','espacio', 'ubicacion', 'requerimiento',
                                            'observacion_solicitud','fecha_inicio','fecha_culminacion','trabajador','vision' ,'status'] )
    form.element(_id='submit_record__row')['_class'] += " text-center"
    form.element(_type='submit')['_class']="btn form_submit"
    form.element(_type='submit')['_value']="Modificar"
    form.element('textarea[name=requerimiento]')['_style']='height:50px'
    form.element('textarea[name=observacion_solicitud]')['_style']='height:50px'
    form.element(_name='telefono')['_style']='width:130px'
    if session.usuario['tipo'] !="S":
      form.element(_name='fecha_inicio')['_style']= 'width:130px'
      form.element(_name='fecha_culminacion')['_style']='width:130px'
      form.element(_name='vision')['_style']='width:110px'

    if form.process().accepted:
        session.flash = T('Solicitud modificada exitosamente!')

        #######################################################################
        solicitudAct = db(db.Solicitud.id == request.args(0)).select()[0]
        import datetime
        now = datetime.datetime.now()
        if (solicitudAntDept != solicitudAct['tipo']):
            db(db.Notificacion.id == query[0]['id']).update(fecha=now,
                departamento=solicitudAct['tipo'])
        if (solicitudAntStat != solicitudAct['status']):
            idSol = solicitudAct['id']
            correo = solicitudAct['info_contacto']
            estado = solicitudAct['status']
            observacion = solicitudAct['observacion_solicitud']
            send_mail(request.vars.nombre_contacto, idSol, correo, estado, observacion=observacion)
            db(db.Notificacion.id == query[0]['id']).update(fecha=now)
        #######################################################################

        redirect(URL('listar'))

    else:
        response.flash = T('Por favor llene la forma.')

    return locals()

def get_trabajadores_pdf(trabajadores):
  if(len(trabajadores) == 2):
    return [trabajadores[0].nombre, '', '', trabajadores[1].nombre, '', '']
  elif(len(trabajadores) == 1):
    return [trabajadores[0].nombre, '', '', '', '', '']
  else:
    return ['', '', '', '', '', '']



def get_pdf():
    solicitud = db.Solicitud(request.args(0))
    tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
    doc = SimpleDocTemplate(tmpfilename)
    elements = []
    trabajadores = []
    if solicitud.trabajador == None:
      trabajadores.append('')
      trabajadores.append('')
      trabajadores.append('')
    else:
      trabajadores.append(solicitud.trabajador[0:2])
      trabajadores.append(solicitud.trabajador[2:4])
      trabajadores.append(solicitud.trabajador[4:6])

    styles = getSampleStyleSheet()
    text = Paragraph(solicitud.requerimiento,
              styles['Normal'])
    text2 = Paragraph(solicitud.observacion_solicitud,
              styles['Normal'])

    data = [['UNIVERSIDAD SIMÓN BOLÍVAR\nVICERRECTORADO ADMINISTRATIVO\nDIRECCIÓN DE PLANTA FÍSICA\nUnidad de Atención e Inspección', '' , 'SOLICITUD DE SERVICIO DE LA DIRECCIÓN PLANTA FÍSICA', '', '', ''],
            [''],
            ['Fecha de Solicitud: ' + str(solicitud.fecha_realizacion), '', 'Área de Trabajo: ' + str(solicitud.area.nombre_area), '', 'Nº Codigo UAI: ' + str(solicitud.id), ''],
            [solicitud.tipo, '', '', 'Entregada a: ' + str(solicitud.supervisor), '', ''],
            ['Unidad Solicitante', '', 'Persona Contacto', '', 'Email de Contacto', ''],
            [solicitud.unidad.nombre_unidad, '', solicitud.nombre_contacto, '', solicitud.info_contacto, ''],
            ['Edificio', 'Espacio', 'Telefono', 'Requerimiento', '', ''],
            [solicitud.edificio.nomenclatura, solicitud.espacio.espacio, solicitud.telefono, text, '', ''],
            ['Observaciones', '', '', '', 'Firma y Sello,\nUnidad de Atención e Inspección', ''],
            [text2, '', '', '', '', ''],
            ['Ejecución', '', '', '', '', ''],
            ['Supervisor Responsable', '', 'Fecha de Inicio\n(Obligatorio)', '', 'Fecha de Culminacion\n(Obligatorio)', ''],
            [solicitud.supervisor, '', solicitud.fecha_inicio, '', solicitud.fecha_culminacion, ''],
            ['Trabajadores Asignados', '', '', '', '', ''],
            get_trabajadores_pdf(trabajadores[0]),
            get_trabajadores_pdf(trabajadores[1]),
            get_trabajadores_pdf(trabajadores[2]),
            [''],
            ['Observaciones', '', '', '', 'Trabajo Terminado', ''],
            [solicitud.observacion_ejecucion, '', '', '', '', 'Terminado'],
            ['', '', '', '', '', 'Falta Material'],
            ['', '', '', '', '', 'Por Unidad Solic.'],
            [''],
            ['Cantidad', 'Materiales Requeridos/\nSolicitud de Almacén', '', 'Si/No', 'Material Retirado por:', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            [''],
            ['Observaciones de Usuario', '', 'Fecha', '', 'Firma', ''],
            ['', '', '', '', '', '']
           ]



    t=Table(data, 3*cm)
    t.setStyle(TableStyle([('SPAN', (0,0), (1,0)),
                           ('SPAN', (2,0), (5,0)),
                           ('FONTSIZE', (0,0), (0,0), 9),
                           ('GRID', (0,2), (5,9), 0.25, colors.black),
                           ('SPAN', (0,2), (1,2)),
                           ('SPAN', (2,2), (3,2)),
                           ('SPAN', (4,2), (5,2)),
                           ('SPAN', (0,3), (2,3)),
                           ('SPAN', (3,3), (5,3)),
                           ('SPAN', (0,4), (1,4)),
                           ('SPAN', (2,4), (3,4)),
                           ('SPAN', (4,4), (5,4)),
                           ('SPAN', (0,5), (1,5)),#
                           ('FONTSIZE', (0,5), (1,5), 6),
                           ('SPAN', (2,5), (3,5)),
                           ('SPAN', (4,5), (5,5)),
                           ('SPAN', (3,6), (5,6)),
                           ('SPAN', (3,7), (5,7)),
                           ('SPAN', (0,8), (3,8)),
                           ('SPAN', (4,8), (5,8)),
                           ('SPAN', (0,9), (3,9)),
                           ('SPAN', (4,9), (5,9)),
                           ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                           ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                           ('ALIGN', (3,7), (3,7), 'LEFT'),
                           ('VALIGN', (3,7), (3,7), 'TOP'),
                           ('ALIGN', (0,9), (0,9), 'LEFT'),
                           ('VALIGN', (0,9), (0,9), 'TOP'),
                           ('ALIGN', (3,3), (3,3), 'LEFT'),
                           ('FONTSIZE', (0,4), (3,4), 12),
                           ('FONTSIZE', (0,6), (3,6), 12),
                           ('FONTSIZE', (0,8), (0,8), 14),
                           ('FONTSIZE', (0,10), (0,10), 12),
                           ('GRID', (0,11), (5,12), 0.25, colors.black),
                           ('SPAN', (0,11), (1,11)),
                           ('SPAN', (2,11), (3,11)),
                           ('SPAN', (4,11), (5,11)),
                           ('SPAN', (0,12), (1,12)),
                           ('SPAN', (2,12), (3,12)),
                           ('SPAN', (4,12), (5,12)),
                           ('FONTSIZE', (0,11), (0,11), 12),
                           ('ALIGN', (0,13), (0,13), 'LEFT'),
                           ('ALIGN', (0,10), (0,10), 'LEFT'),
                           ('GRID', (0,14), (5,16), 0.25, colors.black),
                           ('SPAN', (0,14), (2,14)),
                           ('SPAN', (3,14), (5,14)),
                           ('SPAN', (0,15), (2,15)),
                           ('SPAN', (3,15), (5,15)),
                           ('SPAN', (0,16), (2,16)),
                           ('SPAN', (3,16), (5,16)),
                           ('ALIGN', (0,14), (3,16), 'LEFT'),
                           ('GRID', (0,18), (5,21), 0.25, colors.black),
                           ('SPAN', (0,18), (3,18)),
                           ('SPAN', (4,18), (5,18)),
                           ('SPAN', (0,19), (3,21)),
                           ('GRID', (0,23), (5,26), 0.25, colors.black),
                           ('SPAN', (1,23), (2,23)),
                           ('SPAN', (4,23), (5,23)),
                           ('SPAN', (1,24), (2,24)),
                           ('SPAN', (4,24), (5,26)),
                           ('SPAN', (1,25), (2,25)),
                           ('SPAN', (1,26), (2,26)),
                           ('GRID', (0,28), (-1,-1), 0.25, colors.black),
                           ('SPAN', (0,28), (1,28)),
                           ('SPAN', (2,28), (3,28)),
                           ('SPAN', (4,28), (5,28)),
                           ('SPAN', (0,29), (1,29)),
                           ('SPAN', (2,29), (3,29)),
                           ('SPAN', (4,29), (5,29))
                          ]))
    t._rowHeights[7] = 1.5 * cm
    t._rowHeights[9] = 1.5 * cm
    t._rowHeights[-1] = 1.5 * cm
    elements.append(t)
    doc.build(elements)
    data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return data

def historial():
    filas = db(db.Solicitud).select(orderby=db.Solicitud.id)
    return locals()

def buscador():
    solicitud = None;
    if (request.args(0) != None):
        if (db(db.Solicitud.id==request.args(0)).select()):
            solicitud = db(db.Solicitud.id==request.args(0)).select().first()
        else:
            response.flash = T('No se encontro ninguna solicitud con ese ID')
    return locals()
