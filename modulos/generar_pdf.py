from reportlab.lib.pagesizes import letter
from reportlab.lib import colors, styles
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.units import cm

import subprocess
import os 

def generar_reporte(formato,trabajador,dependencia,ambiente,trabajador_destino, dependencia_destino, ambiente_destino, tabla):
        print("Generando reporte...")
        # Crear un archivo PDF
        doc = SimpleDocTemplate("./reporte/reporte.pdf", pagesize=letter, leftMargin=30)
        contenido = []
        ##########################ESTILOS############################################################
        # Definir un estilo personalizado con negrita
        estilo_negrita = ParagraphStyle('negrita')
        estilo_negrita.fontName = 'Helvetica-Bold'
        estilo_negrita.leading = 12
        estilo_contenido = getSampleStyleSheet()['Normal']
        estilo_contenido.fontSize = 8
#######################################################################################################################
        # Agregar datos al contenido del PDF
        formato_texto = "I. FORMATO (Marca con un (x) aspa el formulario que va a emplear)<br/><b>{}</b>".format(formato)
        formato_paragraph = Paragraph(formato_texto, estilo_negrita)
        contenido.append(formato_paragraph)

        # Espacio en blanco
        contenido.append(Spacer(1, 12))

#####################################################################################################
        origen_texto = "II. DATOS DEL ORIGEN / <b>{}</b><b/>".format(formato)
        origen_paragraph = Paragraph(origen_texto, estilo_negrita)
        contenido.append(origen_paragraph)
        
        # Tabla para Datos del origen
        datos_origen = [["Dependencia", "{}".format(dependencia), "CÓDIGO (*)", ""],
                        ["Detalles del Área", "{}".format(ambiente), "CÓDIGO (**)",""],
                        ["Trabajador", "{}".format(trabajador), "CÓDIGO (***)", ""]]
        
        origen_tabla = Table(datos_origen, colWidths=[3 * cm, 9 * cm, 3 * cm, 3 * cm])
        
        # Aplicar un estilo a la tabla
        origen_tabla.setStyle(TableStyle([
            #('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        contenido.append(origen_tabla)
        
        # Espacio en blanco
        contenido.append(Spacer(1, 12))

        #############################################################################################
        #datos_tabla son los datos que obtendra de la "tabla" creada en el index
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
        
        #creamos "Newtabla" la tabla donde ingresaremos los datos de la tabla
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