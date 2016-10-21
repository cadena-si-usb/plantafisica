# -*- coding: utf-8 -*-


def index():
    redirect(URL('estadisticas'))
    return locals()

def estadisticas():
    return locals()
