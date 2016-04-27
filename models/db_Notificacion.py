# -*- coding: utf-8 -*-
from gluon import current
current.db = db
################################################################################
#                         INICIO DECLARACION BASE DE DATOS                     #
################################################################################

#------------------------------------------------------------------------------#
#                            MODULO DE NOTIFICACIONES                          #
#------------------------------------------------------------------------------#


db.define_table('Notificacion_plantillas',
    Field('codigo', unique=True,
          requires=[IS_NOT_EMPTY(error_message='Introduzca un código de notificación.'),
                    IS_NOT_IN_DB(db, 'Notificacion_plantillas.codigo', error_message='Codigo ya\
                    esta almacenado, introduzca otro o modifique el anterior.')],comment='(*)' ),
    Field('descripcion', type='text' ),
    Field('mensaje', type='text' )
   )

db.define_table('Notificacion_habilitada',
    Field('codigo_plantilla', db.Notificacion_plantillas,
          requires = IS_IN_DB(db, db.Notificacion_plantillas.id, '%(codigo)s', error_message='Elija una de las plantillas.')),
    Field('descripcion', type='text' ),
    Field('mensaje_correo', type='text' ),
    Field('icono',
          requires=IS_IN_SET(['1','2','3','4','5','6'],zero=T('Seleccione un icono.'),
         error_message='Debe seleccionar un icono.'))
   )

db.define_table('Notificacion',
    Field('fecha',type='datetime', default = request.now, requires = IS_DATE(format=('%d/%m/%Y')), writable=False),
    Field('codigo_plantilla', db.Notificacion_plantillas,
          requires = IS_IN_DB(db, db.Notificacion_plantillas.id, '%(codigo)s', error_message='Elija una de las plantillas.')),
    Field('esta_activa',type='boolean',default=True),
    Field('mensaje', type='text' ),
    Field('departamento',
          requires=IS_IN_SET(['Departamento de Mantenimiento','Departamento de Proyectos','Departamento de Planificación','Departamento de Administración','Unidad de Atención e Inspección'],zero=T('Seleccione un departamento.'),
         error_message='Debe seleccionar un departamento.')) ,
   )
db.Notificacion.id.label=T('Numero de Notificacion')

db.define_table('Notificacion_Solicitud',
	Field('id_sol', type='integer'),
	Field('id_notif', type='integer')
	)
################################################################################
#                          FIN DECLARACION BASE DE DATOS                       #
################################################################################