import StringIO


def index():
   return import_manual()

def import_manual():
   form = FORM(OL(LI("Cargar archivo CSV.", INPUT(_type='file', _name='data', value="Seleccionar archivo")), LI("Restaurar base de datos.", INPUT(_type='submit', _onClick="return confirm('Esta acción borrara la base de datos actual. ¿Estas seguro?')"))))
   form.element(_type='submit')['_class']="btn form_submit"
   form.element(_type='submit')['_value']="Restaurar"
   if form.process().accepted:
      try:
         db.export_to_csv_file(open('temp.csv', 'wb'))
         for tabla in db.tables():
            db[tabla].truncate()
         db.import_from_csv_file(form.vars.data.file)
         response.flash = T('Archivo CSV importado exitosamente.')
      except Exception, e:
         response.flash = "Error: " + str(e)
         db.import_from_csv_file(open('temp.csv', 'rb'))

   return dict(form=form)

def export_manual():
    s = StringIO.StringIO()
    db.export_to_csv_file(s)
    response.headers['Content-Type'] = 'text/csv'
    return s.getvalue()
