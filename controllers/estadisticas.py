# -*- coding: utf-8 -*-


def index():
    redirect(URL('estadisticas'))
    return locals()

def estadisticas():
    print "hola"
    month = request.vars.month
    year = request.vars.year
    print month, year
    print "chao"
    return locals()
