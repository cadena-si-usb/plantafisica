response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
(T('Índice'),URL('default','index')==URL(),URL('default','index'),[]),
(T('Login'),False,'https://secure.dst.usb.ve/login?service=http%3A%2F%2F127.0.0.1%3A8000%2FSIAGES%2Fdefault%2Flogin_cas',[]),
(T('Buscador'),URL('solicitudes','buscador')==URL(),URL('solicitudes','buscador'),[]),
(T('Solicitudes'),URL('solicitudes','listar')==URL(),URL('solicitudes','listar'),[]),
(T('Catálogo'),URL('catalogo','catalogue')==URL(),URL('catalogo','catalogue'),[]),
(T('Inventario'),URL('materiales','index')==URL(),URL('materiales','index'),[]),
(T('Empleados'),URL('empleados','index')==URL(),URL('empleados','index'),[]),
(T('Notificaciones'),URL('notificaciones','notifications')==URL(),URL('notificaciones','notifications'),[]),
]
