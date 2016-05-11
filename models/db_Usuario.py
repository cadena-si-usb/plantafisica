# -*- coding: utf-8 -*-

################################################################################
#                         INICIO DECLARACION BASE DE DATOS                     #
################################################################################

#------------------------------------------------------------------------------#
#                            MODULO DE USUARIO                                 #
#------------------------------------------------------------------------------#

db.define_table('Usuario',
    Field('nombre', requires=IS_NOT_EMPTY(error_message='Introduzca un nombre.'), 
          label='(*) Nombre' ),
    Field('USBID', requires=IS_NOT_IN_DB(db, 'Empleado.USBID',
                                         error_message='USBID ya almacenado o no introducido.'),
          type='string', unique=True, label='(*) USBID' ),
    Field('correo', requires=IS_EMPTY_OR(IS_EMAIL(error_message='Introduzca un email valido.')),
          comment='nombre@mail.com', label='Correo'),
    Field('tipo', requires=IS_IN_SET(['Admin','UAI'], error_message='Elija uno de los tipos de usuario.'), label='(*) Tipo')
    )


################################################################################
#                          FIN DECLARACION BASE DE DATOS                       #
################################################################################
