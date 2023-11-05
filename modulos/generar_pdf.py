from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.units import cm

import subprocess
import os 

def generar_reporte(formato,trabajador,dependencia,ambiente,trabajador_destino, dependencia_destino, ambiente_destino, tabla):
        print("Generando reporte...")
        # Crear un archivo PDF
        doc = SimpleDocTemplate("./reporte/reporte.pdf", pagesize=letter)
        contenido = []

        # Agregar datos al contenido del PDF
        contenido.append(Paragraph("I. Formato: <b>{}</b>".format(formato), getSampleStyleSheet()['Normal']))
        contenido.append(Paragraph("II. Datos del Origen:", getSampleStyleSheet()['Heading2']))
        contenido.append(Paragraph("Trabajador: <b>{}</b>".format(trabajador), getSampleStyleSheet()['Normal']))
        contenido.append(Paragraph("Dependencia: <b>{}</b>".format(dependencia), getSampleStyleSheet()['Normal']))
        contenido.append(Paragraph("Ambiente: <b>{}</b>".format(ambiente), getSampleStyleSheet()['Normal']))
        contenido.append(Paragraph("IV. Datos de Destino:", getSampleStyleSheet()['Heading2']))
        contenido.append(Paragraph("Trabajador: <b>{}</b>".format(trabajador_destino), getSampleStyleSheet()['Normal']))
        contenido.append(Paragraph("Dependencia: <b>{}</b>".format(dependencia_destino), getSampleStyleSheet()['Normal']))
        contenido.append(Paragraph("Ambiente: <b>{}</b>".format(ambiente_destino), getSampleStyleSheet()['Normal']))

        ############### Crear una tabla para los datos de los bienes#################################################
        datos_tabla = [["ID","CÓDIGO PATRIMONIAL", "EQUIPO", "SERIE", "MARCA", "MODELO", "E"]]

        num_filas = tabla.rowCount()
        id_autoincremental = 1

        for row in range(num_filas):
            fila = [str(id_autoincremental)]  # Convertir el ID a cadena y agregarlo a la fila
            for col in range(tabla.columnCount()):
                item = tabla.item(row, col)
                if item is not None:
                    fila.append(item.text())
                else:
                    fila.append("")
            datos_tabla.append(fila)
            id_autoincremental += 1
        # Crear un estilo para los campos de la tabla
        estilo_celda = getSampleStyleSheet()['Normal']
        estilo_celda.fontSize = 8
        
        #creamos la tabla donde ingresaremos los datos de la tabla traida desde index
        Newtabla = Table(datos_tabla, colWidths=[1 * cm, 4 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 1 * cm])
        Newtabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        # Aplicar el estilo a las celdas de la tabla
        for i in range(len(datos_tabla)):
            Newtabla.setStyle([('FONTSIZE', (0, i), (-1, i), estilo_celda.fontSize)])

        contenido.append(Newtabla)

        ################## Construir el PDF################################
        doc.build(contenido)

        pdf_file = os.path.abspath("./reporte/reporte.pdf")

        # Verificar si el archivo PDF existe
        if os.path.exists(pdf_file):
            # Abrir el archivo PDF en Windows
            subprocess.Popen(["start", pdf_file], shell=True)
        else:
            print("El archivo PDF no se ha generado correctamente o no se encuentra en la ubicación esperada.")