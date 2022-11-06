from openpyxl import Workbook

def crearBase():
    book = Workbook()
    
    sheet = book.active
    
    sheet['A1'] = 'Id'
    sheet['B1'] = 'Nombre'
    sheet['C1'] = 'Apellido'
    sheet['D1'] = 'Telefono'
    sheet['E1'] = 'Correo'
    sheet['F1'] = 'Fecha creacion'
    
    book.save('bd_contactos.xlsx')

crearBase()