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
        estilo_contenido = getSampleStyleSheet()['Normal']
        estilo_contenido.fontSize = 8

        doc = SimpleDocTemplate("./reporte/reporte.pdf", pagesize=letter, leftMargin=30)
        contenido = []
        ##########################ESTILOS############################################################
        # Definir un estilo personalizado con negrita
        estilo_negrita = ParagraphStyle('negrita')
        estilo_negrita.fontName = 'Helvetica-Bold'
        estilo_negrita.leading = 12

        negrita_center = ParagraphStyle('negrita')
        negrita_center.fontName = 'Helvetica-Bold'
        negrita_center.leading = 12
        negrita_center.fontSize = 7
        negrita_center.alignment = 1
        negrita_center.wordWrap = -2 

        
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
        datos_origen = [["Dependencia", Paragraph("{}".format(dependencia), negrita_center), "CÓDIGO (*)", ""],
                        ["Detalles del Área", Paragraph("{}".format(ambiente), negrita_center), "CÓDIGO (**)",""],
                        ["Trabajador", Paragraph("{}".format(trabajador), negrita_center), "CÓDIGO (***)", ""]]
        
        origen_tabla = Table(datos_origen, colWidths=[2.5 * cm, 12 * cm, 2 * cm, 2 * cm])
        
        # Aplicar un estilo a la tabla
        origen_tabla.setStyle(TableStyle([
            #('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Aplicar el estilo a las celdas de la tabla
        for i in range(len(datos_origen)):
            origen_tabla.setStyle([('FONTSIZE', (0, i), (-1, i), estilo_contenido.fontSize)])

        contenido.append(origen_tabla)
        
        # Espacio en blanco
        contenido.append(Spacer(1, 12))

#############################################################################################
        bienes_texto = "III. DATOS DE LOS BIENES<b/>"
        bienes_paragraph = Paragraph(bienes_texto, estilo_negrita)
        contenido.append(bienes_paragraph)
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
        Newtabla = Table(datos_tabla, colWidths=[0.5 * cm, 3.5 * cm, 2.5 * cm, 5 * cm, 3 * cm, 3.5 * cm, 0.5 * cm])
        Newtabla.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        # Aplicar el estilo a las celdas de la tabla
        for i in range(len(datos_tabla)):
            Newtabla.setStyle([('FONTSIZE', (0, i), (-1, i), estilo_celda.fontSize)])

        contenido.append(Newtabla)

        contenido.append(Spacer(1, 12))
#############################################################################################
##DATOS DE DESTINO
        destino_texto = "IV. DATOS DEL DESTINO (solo utilizar en caso de Desplazamiento / Salida por mantenimiento / Acta de Devolución)<b/>"
        destino_paragraph = Paragraph(destino_texto, estilo_negrita)
        contenido.append(destino_paragraph)
        
        # Tabla para Datos del origen
        datos_destino = [["Dependencia", Paragraph("{}".format(dependencia_destino), negrita_center), "CÓDIGO (*)", ""],
                        ["Detalles del Área", Paragraph("{}".format(ambiente_destino), negrita_center), "CÓDIGO (**)",""],
                        ["Trabajador", Paragraph("{}".format(trabajador_destino), negrita_center), "CÓDIGO (***)", ""]]
        
        destino_tabla = Table(datos_destino, colWidths=[2.5 * cm, 12 * cm, 2 * cm, 2 * cm])
        
        # Aplicar un estilo a la tabla
        destino_tabla.setStyle(TableStyle([
            #('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Aplicar el estilo a las celdas de la tabla
        for i in range(len(datos_destino)):
            destino_tabla.setStyle([('FONTSIZE', (0, i), (-1, i), estilo_contenido.fontSize)])

        contenido.append(destino_tabla)
        
        # Espacio en blanco
        contenido.append(Spacer(1, 12))

#############################################################################################

        ################## Construir el PDF################################
        doc.build(contenido)

        pdf_file = os.path.abspath("./reporte/reporte.pdf")

        # Verificar si el archivo PDF existe
        if os.path.exists(pdf_file):
            # Abrir el archivo PDF en Windows
            subprocess.Popen(["start", pdf_file], shell=True)
        else:
            print("El archivo PDF no se ha generado correctamente o no se encuentra en la ubicación esperada.")