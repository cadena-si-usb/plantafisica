response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description

response.menu = []

response.admin = [
(T('Índice'),URL('default','index')==URL(),URL('default','index_logged'),[]),
(T('Buscador'),URL('solicitudes','buscador')==URL(),URL('solicitudes','buscador'),[]),
(T('Solicitudes'),URL('solicitudes','listar')==URL(),URL('solicitudes','listar'),[]),
(T('Catálogo'),URL('catalogo','catalogue')==URL(),URL('catalogo','catalogue'),[]),
(T('Inventario'),URL('materiales','index')==URL(),URL('materiales','index'),[]),
(T('Empleados'),URL('empleados','index')==URL(),URL('empleados','index'),[]),
(T('Notificaciones'),URL('notificaciones','notifications')==URL(),URL('notificaciones','notifications'),[]),
(T('Usuarios'),URL('usuarios','listar')==URL(),URL('usuarios','listar'),[])
]

response.uai = [
(T('Índice'),URL('default','index')==URL(),URL('default','index_logged'),[]),
(T('Buscador'),URL('solicitudes','buscador')==URL(),URL('solicitudes','buscador'),[]),
(T('Solicitudes'),URL('solicitudes','listar')==URL(),URL('solicitudes','listar'),[]),
(T('Catálogo'),URL('catalogo','catalogue')==URL(),URL('catalogo','catalogue'),[]),
(T('Inventario'),URL('materiales','index')==URL(),URL('materiales','index'),[]),
(T('Empleados'),URL('empleados','index')==URL(),URL('empleados','index'),[]),
(T('Notificaciones'),URL('notificaciones','notifications')==URL(),URL('notificaciones','notifications'),[])
]

response.otros = [
(T('Índice'),URL('default','index')==URL(),URL('default','index_logged'),[]),
(T('Solicitudes'),URL('solicitudes','listar')==URL(),URL('solicitudes','listar'),[])
]
