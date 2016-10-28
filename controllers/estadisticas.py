# -*- coding: utf-8 -*-

def index():
    redirect(URL('estadisticas'))
    return locals()

def estadisticas():
    data = request.vars.data
    print "ARGS: ",data
    return locals()
