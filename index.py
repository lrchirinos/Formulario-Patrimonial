import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QGridLayout, QVBoxLayout, QDialog, QHeaderView,QDateEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate

from modulos.generar_pdf import GenerarPDF


class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Formulario Unico Patrimonial")
        self.setGeometry(100, 100, 1200, 600)

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

        numero_label = QLabel("N° Papeleta:")
        numero_label.setStyleSheet("font-size: 16px;")
        self.numero_input = QLineEdit()
        layout.addWidget(numero_label, 1, 2)
        layout.addWidget(self.numero_input, 1, 3)

        # Etiqueta y campos de entrada de Datos del Trabajador
        datos_label = QLabel("II. Datos del Origen:")
        datos_label.setStyleSheet("font-size: 16px;")
        trabajador_label = QLabel("Trabajador:")
        trabajador_label.setStyleSheet("font-size: 16px;")
        self.trabajador_input = QLineEdit()
        self.codigo_label = QLabel("Código:")
        self.codigo_label.setStyleSheet("font-size: 16px;")
        self.codigo_input = QLineEdit()
        dependencia_label = QLabel("Dependencia:")
        dependencia_label.setStyleSheet("font-size: 16px;")
        self.dependencia_input = QLineEdit()
        self.ambiente_label = QLabel("Ambiente:")
        self.ambiente_label.setStyleSheet("font-size: 16px;")
        self.ambiente_input = QLineEdit()

        # Aumentar el tamaño de la fuente de los campos de entrada
        self.trabajador_input.setStyleSheet("font-size: 16px;")
        self.dependencia_input.setStyleSheet("font-size: 16px;")
        self.ambiente_input.setStyleSheet("font-size: 16px;")
        self.codigo_input.setStyleSheet("font-size: 16px;")

        layout.addWidget(datos_label, 2, 0)
        layout.addWidget(trabajador_label, 3, 0)
        layout.addWidget(self.trabajador_input, 3, 1)
        layout.addWidget(self.codigo_label, 4, 0)
        layout.addWidget(self.codigo_input, 4, 1)
        layout.addWidget(dependencia_label, 3, 2)
        layout.addWidget(self.dependencia_input, 3, 3)
        layout.addWidget(self.ambiente_label, 3, 4)
        layout.addWidget(self.ambiente_input, 3, 5)
###################################################################################################################
        # Crear tabla para Datos de los Bienes
        bienes_label = QLabel("III. Datos de los Bienes:")
        bienes_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(bienes_label, 5, 0, 1, 6)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Código", "Equipo", "Serie", "Marca", "Modelo", "Estado"])
        layout.addWidget(self.table, 6, 0, 1, 6)


        self.table.setStyleSheet("QTableWidget QHeaderView::section { background-color: #0078D7; color: black; } QTableWidget { gridline-color: white; font-size: 16px;}")
        

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Botones para Ingresar y Eliminar
        ingresar_button = QPushButton("Ingresar")
        eliminar_button = QPushButton("Eliminar")
        layout.addWidget(ingresar_button, 7, 2)
        layout.addWidget(eliminar_button, 7, 3)
        eliminar_button.setFixedWidth(115)

        # Conectar botones a funciones
        ingresar_button.clicked.connect(self.mostrar_modal)
        eliminar_button.clicked.connect(self.eliminar_registro)

        # Establecer estilos
        
        central_widget.setStyleSheet("background-color: #000000; color: white; font-weight: bold; font-size: 16px;")
        ingresar_button.setStyleSheet("background-color: #0078D7; color: white; font-weight: bold; font-size: 16px;")
        eliminar_button.setStyleSheet("background-color: #FF0000; color: white; font-weight: bold; font-size: 16px;")



############################################################################################################################
        
        # Agregar sección IV. Datos de Destino
        self.destino_label = QLabel("IV. Datos de Destino:\t")
        self.destino_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.destino_label, 9, 0, 1, 6)
        
        
        self.trabajador_destino_label = QLabel("Trabajador:")
        self.trabajador_destino_label.setStyleSheet("font-size: 16px;")
        self.trabajador_destino_input = QLineEdit()
        self.trabajador_destino_input.setStyleSheet("font-size: 16px;")
        self.codigo_destino_label = QLabel("Codigo:")
        self.codigo_destino_label.setStyleSheet("font-size: 16px;")
        self.codigo_destino_input = QLineEdit()
        self.codigo_destino_input.setStyleSheet("font-size: 16px;")
        self.dependencia_destino_label = QLabel("Dependencia:")
        self.dependencia_destino_label.setStyleSheet("font-size: 16px;")
        self.dependencia_destino_input = QLineEdit()
        self.dependencia_destino_input.setStyleSheet("font-size: 16px;")
        self.ambiente_destino_label = QLabel("Ambiente:")
        self.ambiente_destino_label.setStyleSheet("font-size: 16px;")
        self.ambiente_destino_input = QLineEdit()
        self.ambiente_destino_input.setStyleSheet("font-size: 16px;")

        layout.addWidget(self.trabajador_destino_label, 10, 0)
        layout.addWidget(self.trabajador_destino_input, 10, 1)
        layout.addWidget(self.codigo_destino_label, 11, 0)
        layout.addWidget(self.codigo_destino_input, 11, 1)
        layout.addWidget(self.dependencia_destino_label, 10, 2)
        layout.addWidget(self.dependencia_destino_input, 10, 3)
        layout.addWidget(self.ambiente_destino_label, 10, 4)
        layout.addWidget(self.ambiente_destino_input, 10, 5)

        #########en el caso que la salidad sea por mantenimiento####################
        self.solicitud_label = QLabel("Informe Solicitud: ")
        self.solicitud_label.setStyleSheet("font-size: 16px;")
        self.solicitud_input = QLineEdit()
        self.solicitud_input.setStyleSheet("font-size: 16px;")
        self.diagnostico_label = QLabel("Informe Diagnóstico: ")
        self.diagnostico_label.setStyleSheet("font-size: 16px;")
        self.diagnostico_input = QLineEdit()
        self.diagnostico_input.setStyleSheet("font-size: 16px;")
        self.conclusion_label = QLabel("Informe Conclusión: ")
        self.conclusion_label.setStyleSheet("font-size: 16px;")
        self.conclusion_input = QLineEdit()
        self.conclusion_input.setStyleSheet("font-size: 16px;")
        self.ingreso_label = QLabel("Ingreso: ")
        self.ingreso_label.setStyleSheet("font-size: 16px;")
        self.ingreso_input = QDateEdit()
        self.reparacion_label = QLabel("Reparación: ")
        self.reparacion_label.setStyleSheet("font-size: 16px;")
        self.reparacion_input = QDateEdit()

        # Configuración adicional para el QDateEdit
        self.ingreso_input.setDisplayFormat("dd/MM/yyyy")
        self.reparacion_input.setDisplayFormat("dd/MM/yyyy")
        fecha_actual = QDate.currentDate()
        self.ingreso_input.setDate(fecha_actual)
        self.reparacion_input.setDate(fecha_actual)

        layout.addWidget(self.solicitud_label, 12, 0)
        layout.addWidget(self.solicitud_input, 12, 1, 1, 5)
        layout.addWidget(self.diagnostico_label, 13, 0)
        layout.addWidget(self.diagnostico_input, 13, 1, 1, 5)
        layout.addWidget(self.conclusion_label, 14, 0)
        layout.addWidget(self.conclusion_input, 14, 1, 1, 5)
        layout.addWidget(self.ingreso_label, 15, 0)
        layout.addWidget(self.ingreso_input, 15, 1)
        layout.addWidget(self.reparacion_label, 15, 2)
        layout.addWidget(self.reparacion_input, 15, 3)

############################################################################################################

        # Botón "Generar" de color verde
        generar_button = QPushButton("Imprimir")
        generar_button.setStyleSheet("background-color: #008000; color: white; font-size: 16px;")
        layout.addWidget(generar_button, 16, 5)
           
        generar_button.clicked.connect(self.enviar_al_modulo)

        # Conectar la señal currentIndexChanged del ComboBox a la función que maneja la visibilidad de los datos de destino
        self.formato_combo.currentIndexChanged.connect(self.actualizar_visibilidad_destino)

        # Inicialmente, ocultar los elementos relacionados con los datos de destino
        self.actualizar_visibilidad_destino()


    def actualizar_visibilidad_destino(self):
        # Obtener el formato seleccionado
        formato_seleccionado = self.formato_combo.currentText()

        # Determinar si mostrar o ocultar los elementos relacionados con los datos de destino
        mostrar_datos_destino = formato_seleccionado in ["Desplazamiento", "Acta de Devolución"]
        mostar_mantenimiento= formato_seleccionado in ["Salida por Mantenimiento"]
        # Establecer la visibilidad de los elementos relacionados con los datos de destino
        self.destino_label.setVisible(mostrar_datos_destino)
        self.trabajador_destino_label.setVisible(mostrar_datos_destino)
        self.trabajador_destino_input.setVisible(mostrar_datos_destino)
        self.codigo_destino_label.setVisible(mostrar_datos_destino)
        self.codigo_destino_input.setVisible(mostrar_datos_destino)
        self.dependencia_destino_label.setVisible(mostrar_datos_destino)
        self.dependencia_destino_input.setVisible(mostrar_datos_destino)
        self.ambiente_destino_label.setVisible(mostrar_datos_destino)
        self.ambiente_destino_input.setVisible(mostrar_datos_destino)
        #####para hacer visible cuando es salida por mantenimiento######
        self.solicitud_label.setVisible(mostar_mantenimiento)
        self.solicitud_input.setVisible(mostar_mantenimiento)
        self.diagnostico_label.setVisible(mostar_mantenimiento)
        self.diagnostico_input.setVisible(mostar_mantenimiento)
        self.conclusion_label.setVisible(mostar_mantenimiento)
        self.conclusion_input.setVisible(mostar_mantenimiento)
        self.ingreso_label.setVisible(mostar_mantenimiento)
        self.ingreso_input.setVisible(mostar_mantenimiento)
        self.reparacion_label.setVisible(mostar_mantenimiento)
        self.reparacion_input.setVisible(mostar_mantenimiento)
        self.codigo_label.setVisible(not mostar_mantenimiento)
        self.codigo_input.setVisible(not mostar_mantenimiento)
        self.ambiente_label.setVisible(not mostar_mantenimiento)
        self.ambiente_input.setVisible(not mostar_mantenimiento)

    def enviar_al_modulo(self):
        # Obtener todos los datos ingresados
        formato = self.formato_combo.currentText()
        numero = self.numero_input.text()
        trabajador = self.trabajador_input.text().upper()
        codigo=self.codigo_input.text().upper()
        dependencia = self.dependencia_input.text().upper()
        ambiente = self.ambiente_input.text().upper()
        trabajador_destino = self.trabajador_destino_input.text().upper()
        codigo_destino = self.codigo_destino_input.text().upper()
        dependencia_destino = self.dependencia_destino_input.text().upper()
        ambiente_destino = self.ambiente_destino_input.text().upper()
        ######caso de mantenimiento##########
        solicitud = self.solicitud_input.text().upper()
        diagnostico = self.diagnostico_input.text().upper()
        conclusion = self.conclusion_input.text().upper()
        ingreso = self.ingreso_input.text().upper()
        reparacion =  self.reparacion_input.text().upper()
         
        # Obtener la tabla
        tabla = self.table
        generador = GenerarPDF()
        # Llamar a la función generar_reporte en el módulo generar_pdf
        # Configurar los datos en GenerarPDF
        generador.set_datos(formato, numero, trabajador, codigo, dependencia, ambiente, trabajador_destino, codigo_destino, dependencia_destino, ambiente_destino,tabla, solicitud, diagnostico, conclusion, ingreso, reparacion)
        print(formato)
        if formato != "Salida por Mantenimiento":
            generador.generar_reporte()
        else:
            generador.mantenimiento()


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
        codigo = self.codigo_input.text().upper()
        equipo = self.equipo_input.text().upper()
        serie = self.serie_input.text().upper()
        marca = self.marca_input.text().upper()
        modelo = self.modelo_input.text().upper()
        estado = self.estado_input.text().upper()
        return codigo, equipo, serie, marca, modelo, estado

def main():
    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
