from reportlab.lib.pagesizes import letter
from reportlab.lib import colors, styles
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer,Image, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode import qr
from reportlab.graphics import renderPDF

import subprocess
import os 
import qrcode
import tempfile
from datetime import datetime
class GenerarPDF:
    def __init__(self):
        # Inicializa los atributos de la clase con valores predeterminados
        self.formato = ""
        self.trabajador = ""
        self.codigo = ""
        self.dependencia = ""
        self.ambiente = ""
        self.trabajador_destino = ""
        self.codigo_destino = ""
        self.dependencia_destino = ""
        self.ambiente_destino = ""
        self.tabla = None  # Aquí puedes inicializarlo con el valor apropiado

    def set_datos(self, formato, trabajador, codigo, dependencia, ambiente, trabajador_destino, codigo_destino, dependencia_destino, ambiente_destino, tabla):
        # Establece los atributos de la clase con los datos proporcionados
        self.formato = formato
        self.trabajador = trabajador
        self.codigo = codigo
        self.dependencia = dependencia
        self.ambiente = ambiente
        self.trabajador_destino = trabajador_destino
        self.codigo_destino = codigo_destino
        self.dependencia_destino = dependencia_destino
        self.ambiente_destino = ambiente_destino
        self.tabla = tabla

    def enviar_datos(self):
        formato = self.formato
        trabajador = self.trabajador
        codigo = self.codigo
        dependencia = self.dependencia
        ambiente = self.ambiente
        trabajador_destino = self.trabajador_destino
        codigo_destino = self.codigo_destino
        dependencia_destino = self.dependencia_destino
        ambiente_destino = self.ambiente_destino
        tabla = self.tabla
        # Agregar el código QR
        datos = f"formato: {formato} \n Datos de origen: \n  \ttrabajador: {trabajador} \n \tdependencia: {dependencia} \n \tambiente: {ambiente} \n Datos del destino:\n \ttrabajador: {trabajador_destino} \n \tdependencia: {dependencia_destino} \n \tambiente: {ambiente_destino}"
        return datos
    def header(self,canvas, doc):
        # Agregar el logo
        img_path = "./image/logo.png"
        img = ImageReader(img_path)
        canvas.drawImage(img, 40, 750, width=100, height=30, mask='auto')  # Ajusta las coordenadas según tu preferencia
        datos=self.enviar_datos()
        codigo_qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=0,
        )

        codigo_qr.add_data(datos)
        codigo_qr.make(fit=True)
        imagen_codigo_qr = codigo_qr.make_image(fill_color="black", back_color="white")
        qr_temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        imagen_codigo_qr.save(qr_temp_file.name, "PNG")
        qr_image = Image(qr_temp_file.name, width=60, height=60)
        x_qr = 40  # Ajusta la coordenada X del código QR
        y_qr = 690  # Ajusta la coordenada Y del código QR
        qr_image.drawOn(canvas, x_qr, y_qr)

        # Agregar el texto "Formulario único patrimonial" centrado
        estilo_titulo = getSampleStyleSheet()['Title']
        estilo_titulo.alignment = 1  # Alinea el texto al centro
        estilo_titulo.fontName = 'Helvetica-Bold'  # Cambia 'MiFuente' por el nombre de tu fuente personalizada
        estilo_titulo.fontSize = 10
        titulo_texto = "FORMULARIO UNICO PATRIMONIAL"
        titulo_paragraph = Paragraph(titulo_texto, estilo_titulo)
        x_titulo = 200  # Ajusta la coordenada X del título
        y_titulo = 690  # Ajusta la coordenada Y del título
        titulo_paragraph.wrapOn(canvas, 200, 690)
        titulo_paragraph.drawOn(canvas, x_titulo, y_titulo)

        # Agregar la fecha en el encabezado
        fecha_actual = datetime.now().strftime("%d/%m/%Y")  # Obtiene la fecha actual en formato dd/mm/yyyy
        estilo_fecha = getSampleStyleSheet()['Normal']
        estilo_fecha.alignment = 1  # Alinea el texto al centro
        estilo_fecha.fontName = 'Helvetica-Bold'  # Cambia 'MiFuente' por el nombre de tu fuente personalizada
        estilo_fecha.fontSize = 8
        fecha_texto = f"Fecha: {fecha_actual}"
        x_fecha = 425  # Ajusta la coordenada X de la fecha
        y_fecha = 700  # Ajusta la coordenada Y de la fecha
        fecha_paragraph = Paragraph(fecha_texto, estilo_fecha)
        fecha_paragraph.wrapOn(canvas, 200, 400)
        fecha_paragraph.drawOn(canvas, x_fecha, y_fecha)

        # Agregar el texto "Número de Papeleta" en la parte izquierda
        estilo_numero_papeleta = getSampleStyleSheet()['Normal']
        estilo_numero_papeleta.alignment = 1  # Alinea el texto al centro
        estilo_numero_papeleta.fontName = 'Helvetica-Bold'  # Cambia 'MiFuente' por el nombre de tu fuente personalizada
        estilo_numero_papeleta.fontSize = 8
        numero_papeleta_texto = "N° de Papeleta \t123456"
        x_numero_papeleta = 425 # Ajusta la coordenada X del número de papeleta
        y_numero_papeleta = 690  # Ajusta la coordenada Y del número de papeleta
        numero_papeleta_paragraph = Paragraph(numero_papeleta_texto, estilo_numero_papeleta)
        numero_papeleta_paragraph.wrapOn(canvas, 200, 400)
        numero_papeleta_paragraph.drawOn(canvas, x_numero_papeleta, y_numero_papeleta)


    def generar_reporte(self):
            formato = self.formato
            trabajador = self.trabajador
            codigo = self.codigo
            dependencia = self.dependencia
            ambiente = self.ambiente
            trabajador_destino = self.trabajador_destino
            codigo_destino = self.codigo_destino
            dependencia_destino = self.dependencia_destino
            ambiente_destino = self.ambiente_destino
            tabla = self.tabla
            contenido =[]
            print("Generando reporte...")
            # Crear un archivo PDF
            estilo_contenido = getSampleStyleSheet()['Normal']
            estilo_contenido.fontSize = 8
            ##########################ESTILOS############################################################
            # Definir un estilo personalizado con negrita
            estilo_negrita = ParagraphStyle('negrita')
            estilo_negrita.fontName = 'Helvetica-Bold'
            estilo_negrita.leading = 12
            estilo_negrita.fontSize = 9
            estilo_negrita.leftIndent = 8

            negrita_center = ParagraphStyle('negrita')
            negrita_center.fontName = 'Helvetica-Bold'
            negrita_center.leading = 12
            negrita_center.fontSize = 7
            negrita_center.alignment = 1
            negrita_center.wordWrap = -2 

            estilo_firma = ParagraphStyle('firma')
            estilo_firma.leading = 12
            estilo_firma.fontSize = 7
            estilo_firma.alignment = 1
            estilo_firma.wordWrap = -2 
    #####################################################################################################
            doc = SimpleDocTemplate("./reporte/reporte.pdf", pagesize=letter, leftMargin=30, rightMargin=30)
            #doc.topMargin = 50   #modifica margenes arriba
            doc.bottomMargin = 45 #modifica margenes abajo
            ##################encabezado

            # Definir una plantilla de página
            encabezado_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)
            encabezado_template = PageTemplate(id='encabezado', frames=[encabezado_frame], onPage=self.header)

            # Agregar la plantilla de página al documento
            doc.addPageTemplates([encabezado_template])
    ##################################################################################################       
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
                            ["Trabajador", Paragraph("{}".format(trabajador), negrita_center), "CÓDIGO (***)", Paragraph("{}".format(codigo), negrita_center)]]
            
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

            tabla_estilo = ParagraphStyle('tabla')
            tabla_estilo.leading = 12
            tabla_estilo.fontSize = 8
            tabla_estilo.leftIndent = 8
            #tabla_estilo.leading = 12
            #tabla_estilo.fontSize = 8
            #tabla_estilo.alignment = 1
            # tabla_estilo.wordWrap = -2 
            # tabla_estilo.topPadding = 0  # Padding superior para centrar verticalmente
            # tabla_estilo.bottomPadding = 5  # Padding inferior para centrar verticalmente


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
            # estilo_celda.alignment = 1 
            # estilo_celda.leading = 8
            # estilo_celda.wordWrap = -2  # Espaciado entre líneas
            
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
                            ["Trabajador", Paragraph("{}".format(trabajador_destino), negrita_center), "CÓDIGO (***)", Paragraph("{}".format(codigo_destino), negrita_center)]]
            
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
    ##FIRMA DE CONFORMIDAD
            firma_texto = "V. FIRMA DE CONFORMIDAD<b/>"
            firma_paragraph = Paragraph(firma_texto, estilo_negrita)
            contenido.append(firma_paragraph)

            datos_firma=[
                ["", "", "", ""],
                [Paragraph("FIRMA DEL TRABAJADOR",estilo_firma), Paragraph("VB DEL JEFE DE LA DEPENDENCIA",estilo_firma),Paragraph("FIRMA DEL TRABAJADOR",estilo_firma), Paragraph("VB DEL AREA DE PATRIMONIO",estilo_firma)]
            ]
            firma_tabla = Table(datos_firma, colWidths=[5.25 * cm, 4 * cm, 5.25 * cm, 4 * cm])
            
            # Aplicar un estilo a la tabla
            firma_tabla.setStyle(TableStyle([
                #('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 50),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            # # Aplicar el estilo a las celdas de la tabla
            # for i in range(len(datos_firma)):
            #     firma_tabla.setStyle([('FONTSIZE', (0, i), (-1, i), estilo_contenido.fontSize)])

            contenido.append(firma_tabla)
            ################## Construir el PDF################################
            doc.build(contenido)

            pdf_file = os.path.abspath("./reporte/reporte.pdf")

            # Verificar si el archivo PDF existe
            if os.path.exists(pdf_file):
                # Abrir el archivo PDF en Windows
                subprocess.Popen(["start", pdf_file], shell=True)
            else:
                print("El archivo PDF no se ha generado correctamente o no se encuentra en la ubicación esperada.")