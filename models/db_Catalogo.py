# -*- coding: utf-8 -*-
################################################################################
#                         INICIO DECLARACION BASE DE DATOS                     #
################################################################################

#------------------------------------------------------------------------------#
#                               MODULO DE CATALOGO                             #
#------------------------------------------------------------------------------#

db.define_table('Unidad_metrica',
    Field('nombre_unidadMetrica', unique=True, length=20, requires=[IS_NOT_EMPTY(),IS_UPPER()], 
      label='(*)Unidad Métrica'),
    Field('nomenclatura', unique=True, length=10, requires=[IS_NOT_EMPTY(),IS_UPPER()], label='(*)Nomenclatura' ),
    Field('estado', requires=IS_IN_SET(['Inactivo','Activo'], error_message='Elija uno de las estados.'),
          label='(*)Estado', default='Activo'),
    format='%(nombre_unidadMetrica)s %(nomenclatura)s'
               )

db.Unidad_metrica.nombre_unidadMetrica.requires = IS_NOT_IN_DB(db, db.Unidad_metrica.nombre_unidadMetrica)
db.Unidad_metrica.nomenclatura.requires = IS_NOT_IN_DB(db, db.Unidad_metrica.nomenclatura)

#------------------------------------------------------------------------------#

db.define_table('Edificio',
    Field('nombre_edificio', unique=True, length=60, requires=[IS_NOT_EMPTY(),IS_UPPER()], label='(*)Edificio' ),
    Field('nomenclatura', length=5, requires=[IS_NOT_EMPTY(),IS_UPPER()], label='(*)Nomenclatura' ),
    Field('estado', requires=IS_IN_SET(['Inactivo','Activo'], error_message='Elija uno de las estados.'),
          label='(*)Estado', default='Activo'),
    format='%(nombre_edificio)s %(nomenclatura)s'
               )

db.Edificio.nombre_edificio.requires = IS_NOT_IN_DB(db, db.Edificio.nombre_edificio)
db.Edificio.nomenclatura.requires = IS_NOT_IN_DB(db, db.Edificio.nomenclatura)

#------------------------------------------------------------------------------#

db.define_table('Lugar',
    Field('edificio', db.Edificio, requires=IS_IN_DB(db, db.Edificio.nombre_edificio), label='(*)Edificio'),
    Field('espacio', unique=True, length=10, label='(*)Espacio'),
    Field('referencia'),
    Field('extension_tlf', 'integer'),
    Field('estado', requires=IS_IN_SET(['Inactivo','Activo'], error_message='Elija uno de las estados.'),
          label='(*)Estado', default='Activo'),
    format='%(edificio)s %(espacio)s'
               )

db.Lugar.edificio.requires = IS_IN_DB(db, db.Edificio.id, '%(nombre_edificio)s')
db.Lugar.espacio.requires = IS_NOT_IN_DB(db, db.Lugar.espacio)

#------------------------------------------------------------------------------#

db.define_table('Area',
    Field('nombre_area', unique=True, length=60, requires=[IS_NOT_EMPTY(),IS_UPPER()], label='(*)Area' ),
    Field('nomenclatura', unique=True, length=5, requires=[IS_NOT_EMPTY(),IS_UPPER()], label='(*)Nomenclatura' ),
    Field('estado', requires=IS_IN_SET(['Inactivo','Activo'], error_message='Elija uno de las estados.'),
          label='(*)Estado', default='Activo'),
    format='%(nombre_area)s %(nomenclatura)s'
               )

db.Area.nombre_area.requires = IS_NOT_IN_DB(db, db.Area.nombre_area)
db.Area.nomenclatura.requires = IS_NOT_IN_DB(db, db.Area.nomenclatura)

#------------------------------------------------------------------------------#

db.define_table('Unidad',
   Field('nombre_unidad', unique=True, length=60, requires=[IS_NOT_EMPTY(),IS_UPPER()], label='(*)Unidad' ),
   Field('estado', requires=IS_IN_SET(['Inactivo','Activo'], error_message='Elija uno de las estados.'),
          label='(*)Estado', default='Activo'),
   format='%(nombre_unidad)s'
               )

db.Unidad.nombre_unidad.requires = IS_NOT_IN_DB(db, db.Unidad.nombre_unidad)

#------------------------------------------------------------------------------#

db.define_table('Status_solicitud',
   Field('nombre_status', unique=True, length=20, requires=[IS_NOT_EMPTY(),IS_UPPER()], label='(*)Status' ),
   Field('estado', requires=IS_IN_SET(['Inactivo','Activo'], error_message='Elija uno de las estados.'),
          label='(*)Estado', default='Activo'),
   format='%(nombre_status)s'
               )

db.Status_solicitud.nombre_status.requires = IS_NOT_IN_DB(db, db.Status_solicitud.nombre_status)

#------------------------------------------------------------------------------#

db.define_table('Prioridad',
   Field('nombre_prioridad', unique=True, length=20, requires =[IS_NOT_EMPTY(),IS_UPPER()], label='(*)Prioridad' ),
   Field('estado', requires=IS_IN_SET(['Inactivo','Activo'], error_message='Elija uno de las estados.'),
          label='(*)Estado', default='Activo'),
   format='%(nombre_prioridad)s'
               )

db.Prioridad.nombre_prioridad.requires = IS_NOT_IN_DB(db, db.Prioridad.nombre_prioridad)

#------------------------------------------------------------------------------#

db.define_table('Supervisor',
    Field('nombre'),
    Field('cedula'),
    Field('USBID'),
    Field('area'),
    Field('estado'))

################################################################################
#                          FIN DECLARACION BASE DE DATOS                       #
################################################################################
