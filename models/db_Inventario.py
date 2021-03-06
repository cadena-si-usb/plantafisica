# -*- coding: utf-8 -*-

################################################################################
#                         INICIO DECLARACION BASE DE DATOS                     #
################################################################################

#------------------------------------------------------------------------------#
#                            MODULO DE INVENTARIO                              #
#------------------------------------------------------------------------------#

db.define_table('Material',
    Field('nombre', unique=True,
          requires=[IS_NOT_EMPTY(error_message='Introduzca un nombre.'),
                    IS_UPPER()], label='(*) Nombre' ),
    Field('especificacion', type='text' ),
    Field('status', default='Disponible',
          requires=IS_IN_SET(['Disponible','Critico','No disponible'])),
    Field('unidad_metrica',db.Unidad_metrica,
          requires=IS_IN_DB(db(db.Unidad_metrica.estado=='Activo'), 
                                        db.Unidad_metrica, '%(nombre_unidadMetrica)s',
                                        error_message='Elija una de las unidades.') ),
    Field('area', db.Area,
          requires=IS_IN_DB(db(db.Area.estado=='Activo'), db.Area, '%(nombre_area)s', 
                            error_message='Elija una de las areas.'),
          label='(*) Area' ),
    Field('cantidad', type='integer', requires=[IS_NOT_EMPTY(error_message='Introduzca una cantidad.'),
                                                IS_INT_IN_RANGE(0, None, error_message='Muy pequeño!')],
          label='(*) Cantidad' ),
    Field('cantidad_Minima', type='integer', requires=[IS_NOT_EMPTY(error_message='Introduzca un minimo.'),
                                                       IS_INT_IN_RANGE(0, None, error_message='Muy pequeño!')],
          label='(*) Cantidad Minima' ),
    format='%(nombre)s %(cantidad)s'
   )

db.Material.nombre.requires.append(IS_NOT_IN_DB(db, db.Material.nombre,
                                                error_message='Nombre ya almacenado, introduzca otro o modifique el anterior.'))

#------------------------------------------------------------------------------#

db.define_table('Empleado',
    Field('nombre', requires=IS_NOT_EMPTY(error_message='Introduzca un nombre.'), 
          label='(*) Nombre' ),
    Field('cedula', requires=[IS_MATCH('^[0-9][0-9]*$',
                                       error_message='Introduzca una cedula.'),
                              IS_NOT_IN_DB(db, 'Empleado.cedula',
                                           error_message='Cedula ya almacenada o no introducida.')],
          unique=True, label='(*) Cedula' ),
    Field('USBID', requires=IS_NOT_IN_DB(db, 'Empleado.USBID',
                                         error_message='USBID ya almacenado o no introducido.'),
          type='string', unique=True, label='(*) USBID' ),
    Field('telefono', requires=IS_MATCH('^\d{4}?[\s.-]?\d{7}$',
                                        error_message='No es un numero de telefono valido.'),
          label='(*) Telefono', comment='xxxx-xxxxxxx' ),
    Field('correo', requires=IS_EMPTY_OR(IS_EMAIL(error_message='Introduzca un email valido.')),
          comment='nombre@mail.com'),
    Field('cargo', requires=IS_IN_SET(['Supervisor','Obrero'],
                                      error_message='Elija uno de los cargos.'), 
          label='(*) Cargo' ),
    Field('area', db.Area, requires=IS_IN_DB(db(db.Area.estado=='Activo'), db.Area,'%(nombre_area)s',
                                             error_message='Elija una de las areas.'),
         label='(*) Area' ),
    Field('estado', requires=IS_IN_SET(['Inactivo','Activo'], 
          error_message='Elija uno de las estados.'), label='(*) Estado' ),
    Field('tipo', requires=IS_IN_SET(['Interno','Externo'], error_message='Elija uno de los tipos.')),
    format='%(nombre)s %(area)s'
    )


################################################################################
#                          FIN DECLARACION BASE DE DATOS                       #
################################################################################
