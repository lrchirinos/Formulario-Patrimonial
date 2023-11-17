from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer,Image, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

import subprocess
import os 
import qrcode
import tempfile
from datetime import datetime


class GenerarPDF:
    def __init__(self):
        # Inicializa los atributos de la clase con valores predeterminados
        self.formato = ""
        self.numero = ""
        self.trabajador = ""
        self.codigo = ""
        self.dependencia = ""
        self.ambiente = ""
        self.trabajador_destino = ""
        self.codigo_destino = ""
        self.dependencia_destino = ""
        self.ambiente_destino = ""
        self.tabla = None  # Aquí puedes inicializarlo con el valor apropiado
        self.solicitud = ""
        self.diagnostico = ""
        self.conclusion = ""
        self.ingreso = ""
        self.reparacion = ""
    def set_datos(self, formato, numero, trabajador, codigo, dependencia, ambiente, trabajador_destino, codigo_destino, dependencia_destino, ambiente_destino, tabla, solicitud, diagnostico, conclusion, ingreso, reparacion):
        # Establece los atributos de la clase con los datos proporcionados
        self.formato = formato
        self.numero = numero
        self.trabajador = trabajador
        self.codigo = codigo
        self.dependencia = dependencia
        self.ambiente = ambiente
        self.trabajador_destino = trabajador_destino
        self.codigo_destino = codigo_destino
        self.dependencia_destino = dependencia_destino
        self.ambiente_destino = ambiente_destino
        self.tabla = tabla
        self.solicitud = solicitud
        self.diagnostico = diagnostico
        self.conclusion = conclusion
        self.ingreso = ingreso
        self.reparacion = reparacion

    def enviar_datos(self):
        
        trabajador = self.trabajador
        dependencia = self.dependencia
        trabajador_destino = self.trabajador_destino
        dependencia_destino = self.dependencia_destino
        tabla = self.tabla
        # Obtener el número de filas y columnas en la tabla
        num_filas = tabla.rowCount()
        num_columnas = tabla.columnCount()

        # Crear una lista para almacenar los datos de la tabla
        datos_tabla = []

        # Iterar sobre las filas y columnas para obtener los datos
        for fila in range(num_filas):
            fila_datos = []  # Lista para almacenar los datos de la fila actual
            for columna in range(num_columnas):
                item = tabla.item(fila, columna)
                if item is not None:
                    fila_datos.append(item.text())  # Agregar el texto del elemento a la lista
                else:
                    fila_datos.append("")  # Si el elemento es None, agregar una cadena vacía a la lista
            datos_tabla.append(fila_datos)
        # Agregar el código QR
        #datos = f"formato: {formato} \n Datos de origen: \n  \ttrabajador: {trabajador} \n \tdependencia: {dependencia} \n \tambiente: {ambiente} \n Datos del destino:\n \ttrabajador: {trabajador_destino} \n \tdependencia: {dependencia_destino} \n \tambiente: {ambiente_destino}"
        datos = f"trabajador origen: {trabajador} \n dependencia origen: {dependencia} \n trabajador destino: {trabajador_destino} \n dependencia destino: {dependencia_destino} \n dispositivos: {datos_tabla}"
        print(datos_tabla)
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
        numero = self.numero
        estilo_numero_papeleta = getSampleStyleSheet()['Normal']
        estilo_numero_papeleta.alignment = 1  # Alinea el texto al centro
        estilo_numero_papeleta.fontName = 'Helvetica-Bold'  # Cambia 'MiFuente' por el nombre de tu fuente personalizada
        estilo_numero_papeleta.fontSize = 8
        numero_papeleta_texto = f"N° de Papeleta: \t{numero}"
        x_numero_papeleta = 425 # Ajusta la coordenada X del número de papeleta
        y_numero_papeleta = 690  # Ajusta la coordenada Y del número de papeleta
        numero_papeleta_paragraph = Paragraph(numero_papeleta_texto, estilo_numero_papeleta)
        numero_papeleta_paragraph.wrapOn(canvas, 200, 400)
        numero_papeleta_paragraph.drawOn(canvas, x_numero_papeleta, y_numero_papeleta)

    def footer(self,canvas, doc):
        # Agregar el logo
        img_path = "./image/logo.png"
        img = ImageReader(img_path)
        canvas.drawImage(img, 40, 750, width=100, height=30, mask='auto')

        texto_encabezado = '"Año de la lucha contra la corrupción e impunidad"'
        estilo_encabezado = ParagraphStyle('encabezado', fontSize=8, alignment=1, fontName='Helvetica-Oblique')
        estilo_encabezado =Paragraph(texto_encabezado, estilo_encabezado)
        x_anio = 110  # Ajusta la coordenada X del título
        y_anio = 720  # Ajusta la coordenada Y del título
        estilo_encabezado.wrapOn(canvas, 400, 750)
        estilo_encabezado.drawOn(canvas, x_anio, y_anio)

        # Agregar el texto 1
        estilo_primero = getSampleStyleSheet()['Normal']
        estilo_primero.alignment = 1  # Alinea el texto al centro
        estilo_primero.fontName = 'Helvetica-Bold'  # Cambia 'MiFuente' por el nombre de tu fuente personalizada
        estilo_primero.fontSize = 8
        primero_texto = "Jr. Independencia 543 - 547"
        primero_paragraph = Paragraph(primero_texto, estilo_primero)
        x_primero = 321  # Ajusta la coordenada X del título
        y_primero = 40  # Ajusta la coordenada Y del título
        primero_paragraph.wrapOn(canvas, 400, 40)
        primero_paragraph.drawOn(canvas, x_primero, y_primero)

        # Agregar el link
        estilo_primero = getSampleStyleSheet()['Normal']
        estilo_primero.alignment = 1  # Alinea el texto al centro
        estilo_primero.fontName = 'Helvetica-Bold'  # Cambia 'MiFuente' por el nombre de tu fuente personalizada
        estilo_primero.fontSize = 8
        primero_texto = "www.essalud.gob.pe"
        primero_paragraph = Paragraph(primero_texto, estilo_primero)
        x_primero = 200  # Ajusta la coordenada X del título
        y_primero = 25  # Ajusta la coordenada Y del título
        primero_paragraph.wrapOn(canvas, 400, 20)
        primero_paragraph.drawOn(canvas, x_primero, y_primero)

        # Agregar el texto 2
        estilo_segundo = getSampleStyleSheet()['Normal']
        estilo_segundo.alignment = 0  # Alinea el texto al centro
        estilo_segundo.fontName = 'Helvetica'  # Cambia 'MiFuente' por el nombre de tu fuente personalizada
        estilo_segundo.fontSize = 8
        estilo_segundo.leading = 8
        segundo_texto = "Distrito Trujillo <br/> Trujillo-Perú <br/> T: 044-480806 Anexo 1238"
        segundo_paragraph = Paragraph(segundo_texto, estilo_segundo)
        x_segundo = 470  # Ajusta la coordenada X del título
        y_segundo = 20 # Ajusta la coordenada Y del título
        segundo_paragraph.wrapOn(canvas, 470, 20)
        segundo_paragraph.drawOn(canvas, x_segundo, y_segundo)
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

    # Sección de Datos de Destino
            if formato in ["Desplazamiento", "Salida por Mantenimiento", "Acta de Devolución"]:
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
            if formato in ["Desplazamiento", "Salida por Mantenimiento", "Acta de Devolución"]:
                firma_texto = "V. FIRMA DE CONFORMIDAD<b/>"
            else:
                firma_texto = "IV. FIRMA DE CONFORMIDAD<b/>"
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


    def mantenimiento(self):
        trabajador = self.trabajador
        dependencia = self.dependencia
        nota = self.numero
        ingreso = self.ingreso
        reparacion =  self.reparacion
        solicitud = self.solicitud
        diagnostico =  self.diagnostico
        conclusion = self.conclusion
        tabla = self.tabla
        contenido =[]
        # Crear un archivo PDF
        estilo_contenido = getSampleStyleSheet()['Normal']
        estilo_contenido.fontSize = 8
        ##########################ESTILOS############################################################
        # Definir un estilo personalizado con negrita
        estilo_negrita = ParagraphStyle('negrita')
        estilo_negrita.fontName = 'Helvetica-Bold'
        estilo_negrita.fontSize = 7

        estilo_letra = ParagraphStyle('normal')
        estilo_letra.fontSize = 7
        # estilo_letra.leading = 12
        # estilo_letra.alignment = 1
        # estilo_letra.wordWrap = -2 
#####################################################################################################
        
##################################################################################
        doc = SimpleDocTemplate("./reporte/reporte.pdf", pagesize=letter, leftMargin=40, rightMargin=30)
        #doc.bottomMargin = 1
        doc.topMargin = 30

        # Espacio en blanco
        contenido.append(Spacer(1, 24))

        texto_titulo = '<u>SERVICIO DE MANTENIMIENTO</u>'
        estilo_titulo = ParagraphStyle('titulo', fontSize=11, alignment=1, spaceAfter=10, 
                                       fontName='Helvetica-Bold')
        contenido.append(Paragraph(texto_titulo, estilo_titulo))
        contenido.append(Spacer(1, 24))

        # Tabla para Datos
        info = [[Paragraph("DEPENDENCIA", estilo_negrita), Paragraph(": {}".format(dependencia), estilo_letra), Paragraph("HOJA DE SERVICIO",estilo_negrita), Paragraph(": {}".format(nota), estilo_letra)],
                        [Paragraph("RESPONSABLE",estilo_negrita), Paragraph(": {}".format(trabajador), estilo_letra), Paragraph("N° DE INFORME TECNICO",estilo_negrita), Paragraph(": {}".format(nota), estilo_letra)],
                        ["", "", Paragraph("FECHA DE INGRESO",estilo_negrita), Paragraph(": {}".format(ingreso), estilo_letra)],
                        ["", "", Paragraph("FECHA DE REPARACIÓN",estilo_negrita), Paragraph(": {}".format(reparacion), estilo_letra)]]

        datos = Table(info, colWidths=[2.4 * cm, 11 * cm, 3.5 * cm, 2 * cm])

        # Aplicar un estilo a la tabla
        datos.setStyle(TableStyle([
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0.3)
            #('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        contenido.append(datos)
        contenido.append(Spacer(1, 24))
        ###############################tabla dispositivos########################
        #datos_tabla son los datos que obtendra de la "tabla" creada en el index
        datos_tabla = [["CÓDIGO PATRIMONIAL", "EQUIPO", "SERIE", "MARCA", "MODELO"]]

        num_filas = tabla.rowCount()

        tabla_estilo = ParagraphStyle('tabla')
        tabla_estilo.leading = 12
        tabla_estilo.fontSize = 8
        tabla_estilo.leftIndent = 8

        for row in range(num_filas):
            fila = []  # Convertir el ID a cadena y agregarlo a la fila
            for col in range(tabla.columnCount()):
                item = tabla.item(row, col)
                if item is not None:
                    fila.append(item.text())
                else:
                    fila.append("")
            fila=fila[:-1]
            datos_tabla.append(fila)
            
        # Crear un estilo para los campos de la tabla
        estilo_celda = getSampleStyleSheet()['Normal']
        estilo_celda.fontSize = 8
        
        #creamos "Newtabla" la tabla donde ingresaremos los datos de la tabla
        Newtabla = Table(datos_tabla, colWidths=[3.5 * cm, 3 * cm, 5 * cm, 3 * cm, 4 * cm])
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
        contenido.append(Spacer(1, 24))

        #########################################################################
        #informes
        solicitud_texto = "INFORME DE SOLICITUD<b/>"
        contenido.append(Paragraph(solicitud_texto, estilo_negrita))
        contenido.append(Paragraph("{}".format(solicitud), estilo_letra))
        contenido.append(Spacer(1, 12))

        diagnostico_texto = "INFORME DE DIAGNÓSTICO<b/>"
        contenido.append(Paragraph(diagnostico_texto, estilo_negrita))
        contenido.append(Paragraph("{}".format(diagnostico), estilo_letra))
        contenido.append(Spacer(1, 12))

        conclusion_texto = "INFORME DE CONCLUSION<b/>"
        contenido.append(Paragraph(conclusion_texto, estilo_negrita))
        contenido.append(Paragraph("{}".format(conclusion), estilo_letra))

        ######################firma final

        datos_firma=[
                ["", "", ""],
                ["V°B DE LA JEFATURA", "V°B TÉCNICO DE LA OF. DE OSI","RECIBI CONFORME\nDNI:_________\n      NOMBRE:_________________"]
            ]
        firma_tabla = Table(datos_firma, colWidths=[6.5 * cm, 7 * cm, 5 * cm])
        
        # Aplicar un estilo a la tabla
        firma_tabla.setStyle(TableStyle([
            #('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 100),
            #('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold')
        ]))

        contenido.append(firma_tabla)

        ##################encabezado

        footer_frame = Frame(doc.leftMargin, doc.bottomMargin + 20, doc.width, doc.height - 20)

        footer_template = PageTemplate(id='footer', frames=[footer_frame], onPage=self.footer)

        # Agregar la plantilla de página al documento
        doc.addPageTemplates([footer_template])


        #############contruccion del pdf
        doc.build(contenido)
        
        pdf_file = os.path.abspath("./reporte/reporte.pdf")

        # Verificar si el archivo PDF existe
        if os.path.exists(pdf_file):
            # Abrir el archivo PDF en Windows
            subprocess.Popen(["start", pdf_file], shell=True)
        else:
            print("El archivo PDF no se ha generado correctamente o no se encuentra en la ubicación esperada.")

        