import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QGridLayout, QVBoxLayout, QDialog, QHeaderView, QSpacerItem, QSizePolicy,QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.units import cm

import subprocess
import os 

class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Formulario Unico Patrimonial")
        self.setGeometry(100, 100, 800, 600)

        # # Configura el tamaño y la posición de la ventana
        # self.setWindowState(Qt.WindowFullScreen)

        # Establecer el ícono de la aplicación
        app_icon = QIcon("./image/icon.png")  # Reemplaza con la ruta de tu archivo favicon
        self.setWindowIcon(app_icon)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        central_widget.setLayout(layout)

        # Etiqueta y ComboBox para el Formato
        formato_label = QLabel("I. Formato:")
        # Aumentar el tamaño de la letra de la etiqueta
        formato_label.setStyleSheet("font-size: 16px;")
        self.formato_combo = QComboBox()
        self.formato_combo.addItem("Toma de Inventario")
        self.formato_combo.addItem("Salida por Mantenimiento")
        self.formato_combo.addItem("Cuadro de Asignación")
        self.formato_combo.addItem("Acta de Devolución")
        self.formato_combo.addItem("Desplazamiento")
        self.formato_combo.setStyleSheet("font-size: 16px;")
        layout.addWidget(formato_label, 1, 0)
        layout.addWidget(self.formato_combo, 1, 1)

        # Etiqueta y campos de entrada de Datos del Trabajador
        datos_label = QLabel("II. Datos del Origen:")
        datos_label.setStyleSheet("font-size: 16px;")
        trabajador_label = QLabel("Trabajador:")
        trabajador_label.setStyleSheet("font-size: 16px;")
        self.trabajador_input = QLineEdit()
        dependencia_label = QLabel("Dependencia:")
        dependencia_label.setStyleSheet("font-size: 16px;")
        self.dependencia_input = QLineEdit()
        ambiente_label = QLabel("Ambiente:")
        ambiente_label.setStyleSheet("font-size: 16px;")
        self.ambiente_input = QLineEdit()

        # Aumentar el tamaño de la fuente de los campos de entrada
        self.trabajador_input.setStyleSheet("font-size: 16px;")
        self.dependencia_input.setStyleSheet("font-size: 16px;")
        self.ambiente_input.setStyleSheet("font-size: 16px;")

        layout.addWidget(datos_label, 2, 0)
        layout.addWidget(trabajador_label, 3, 0)
        layout.addWidget(self.trabajador_input, 3, 1)
        layout.addWidget(dependencia_label, 3, 2)
        layout.addWidget(self.dependencia_input, 3, 3)
        layout.addWidget(ambiente_label, 3, 4)
        layout.addWidget(self.ambiente_input, 3, 5)
###################################################################################################################
        # Crear tabla para Datos de los Bienes
        bienes_label = QLabel("III. Datos de los Bienes:")
        bienes_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(bienes_label, 4, 0, 1, 6)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Código", "Equipo", "Serie", "Marca", "Modelo", "Estado"])
        layout.addWidget(self.table, 5, 0, 1, 6)


        self.table.setStyleSheet("QTableWidget QHeaderView::section { background-color: #0078D7; color: black; } QTableWidget { gridline-color: white; font-size: 16px;}")
        

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Botones para Ingresar y Eliminar
        ingresar_button = QPushButton("Ingresar")
        eliminar_button = QPushButton("Eliminar")
        layout.addWidget(ingresar_button, 6, 5)
        layout.addWidget(eliminar_button, 7, 5)

        # Conectar botones a funciones
        ingresar_button.clicked.connect(self.mostrar_modal)
        eliminar_button.clicked.connect(self.eliminar_registro)

        # Establecer estilos
        
        central_widget.setStyleSheet("background-color: #000000; color: white; font-weight: bold; font-size: 16px;")
        ingresar_button.setStyleSheet("background-color: #0078D7; color: white; font-weight: bold; font-size: 16px;")
        eliminar_button.setStyleSheet("background-color: #FF0000; color: white; font-weight: bold; font-size: 16px;")



############################################################################################################################
        # Agregar sección IV. Datos de Destino
        destino_label = QLabel("IV. Datos de Destino:")
        destino_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(destino_label, 8, 0, 1, 6)
        trabajador_destino_label = QLabel("Trabajador:")
        trabajador_destino_label.setStyleSheet("font-size: 16px;")
        self.trabajador_destino_input = QLineEdit()
        self.trabajador_destino_input.setStyleSheet("font-size: 16px;")
        dependencia_destino_label = QLabel("Dependencia:")
        dependencia_destino_label.setStyleSheet("font-size: 16px;")
        self.dependencia_destino_input = QLineEdit()
        self.dependencia_destino_input.setStyleSheet("font-size: 16px;")
        ambiente_destino_label = QLabel("Ambiente:")
        ambiente_destino_label.setStyleSheet("font-size: 16px;")
        self.ambiente_destino_input = QLineEdit()
        self.ambiente_destino_input.setStyleSheet("font-size: 16px;")

        layout.addWidget(trabajador_destino_label, 9, 0)
        layout.addWidget(self.trabajador_destino_input, 9, 1)
        layout.addWidget(dependencia_destino_label, 9, 2)
        layout.addWidget(self.dependencia_destino_input, 9, 3)
        layout.addWidget(ambiente_destino_label, 9, 4)
        layout.addWidget(self.ambiente_destino_input, 9, 5)
############################################################################################################

        # Botón "Generar" de color verde
        generar_button = QPushButton("Imprimir")
        generar_button.setStyleSheet("background-color: #008000; color: white; font-size: 16px;")
        layout.addWidget(generar_button, 10, 5)
        
        generar_button.clicked.connect(self.generar_reporte)

    def generar_reporte(self):
        print("Generando reporte...")
        # Crear un archivo PDF
        doc = SimpleDocTemplate("./reporte/reporte.pdf", pagesize=letter)
        contenido = []

        # Obtener todos los datos ingresados
        formato = self.formato_combo.currentText()
        trabajador = self.trabajador_input.text()
        dependencia = self.dependencia_input.text()
        ambiente = self.ambiente_input.text()
        trabajador_destino = self.trabajador_destino_input.text()
        dependencia_destino = self.dependencia_destino_input.text()
        ambiente_destino = self.ambiente_destino_input.text()

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

        num_filas = self.table.rowCount()
        id_autoincremental = 1

        for row in range(num_filas):
            fila = [str(id_autoincremental)]  # Convertir el ID a cadena y agregarlo a la fila
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item is not None:
                    fila.append(item.text())
                else:
                    fila.append("")
            datos_tabla.append(fila)
            id_autoincremental += 1
        # Crear un estilo para los campos de la tabla
        estilo_celda = getSampleStyleSheet()['Normal']
        estilo_celda.fontSize = 8
        
        
        tabla = Table(datos_tabla, colWidths=[1 * cm, 4 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 1 * cm])
        tabla.setStyle(TableStyle([
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
            tabla.setStyle([('FONTSIZE', (0, i), (-1, i), estilo_celda.fontSize)])

        contenido.append(tabla)

        ################## Construir el PDF################################
        doc.build(contenido)

        pdf_file = os.path.abspath("./reporte/reporte.pdf")

        # Verificar si el archivo PDF existe
        if os.path.exists(pdf_file):
            # Abrir el archivo PDF en Windows
            subprocess.Popen(["start", pdf_file], shell=True)
        else:
            print("El archivo PDF no se ha generado correctamente o no se encuentra en la ubicación esperada.")


    def mostrar_modal(self):
        modal = DatosBienesDialog(self)
        if modal.exec_():
            # Obtener datos ingresados desde el modal
            datos = modal.obtener_datos()
            if datos:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                for col, dato in enumerate(datos):
                    item = QTableWidgetItem(str(dato))
                    self.table.setItem(row_position, col, item)

    def eliminar_registro(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)

class DatosBienesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Ingresar Datos de Bienes")
        self.setModal(True)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Campos de entrada en el modal
        self.codigo_input = QLineEdit()
        self.equipo_input = QLineEdit()
        self.serie_input = QLineEdit()
        self.marca_input = QLineEdit()
        self.modelo_input = QLineEdit()
        self.estado_input = QLineEdit()

        layout.addWidget(QLabel("Código:"))
        layout.addWidget(self.codigo_input)
        layout.addWidget(QLabel("Equipo:"))
        layout.addWidget(self.equipo_input)
        layout.addWidget(QLabel("Serie:"))
        layout.addWidget(self.serie_input)
        layout.addWidget(QLabel("Marca:"))
        layout.addWidget(self.marca_input)
        layout.addWidget(QLabel("Modelo:"))
        layout.addWidget(self.modelo_input)
        layout.addWidget(QLabel("Estado:"))
        layout.addWidget(self.estado_input)

        aceptar_button = QPushButton("Aceptar")
        aceptar_button.clicked.connect(self.accept)
        layout.addWidget(aceptar_button)

    def obtener_datos(self):
        codigo = self.codigo_input.text()
        equipo = self.equipo_input.text()
        serie = self.serie_input.text()
        marca = self.marca_input.text()
        modelo = self.modelo_input.text()
        estado = self.estado_input.text()
        return codigo, equipo, serie, marca, modelo, estado

def main():
    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
