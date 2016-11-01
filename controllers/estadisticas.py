# -*- coding: utf-8 -*-

def index():
    redirect(URL('estadisticas'))
    return locals()

def estadisticas():
  data = {} 
  return dict(data=data)

def setMonthYear():
  vrs = request.vars
  month = vrs.month
  year = vrs.year
  redirect(URL('estadisticas', args=[year, month]))
