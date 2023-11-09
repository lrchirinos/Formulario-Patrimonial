import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QGridLayout, QVBoxLayout, QDialog, QHeaderView, QSpacerItem, QSizePolicy,QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from modulos.generar_pdf import GenerarPDF


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
                # Ajustar el ancho del combobox a 100 píxeles
        self.formato_combo.setFixedWidth(100)

        layout.addWidget(formato_label, 1, 0)
        layout.addWidget(self.formato_combo, 1, 1)

        # Etiqueta y campos de entrada de Datos del Trabajador
        datos_label = QLabel("II. Datos del Origen:")
        datos_label.setStyleSheet("font-size: 16px;")
        trabajador_label = QLabel("Trabajador:")
        trabajador_label.setStyleSheet("font-size: 16px;")
        self.trabajador_input = QLineEdit()
        codigo_label = QLabel("Código:")
        codigo_label.setStyleSheet("font-size: 16px;")
        self.codigo_input = QLineEdit()
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
        self.codigo_input.setStyleSheet("font-size: 16px;")

        layout.addWidget(datos_label, 2, 0)
        layout.addWidget(trabajador_label, 3, 0)
        layout.addWidget(self.trabajador_input, 3, 1)
        layout.addWidget(codigo_label, 4, 0)
        layout.addWidget(self.codigo_input, 4, 1)
        layout.addWidget(dependencia_label, 3, 2)
        layout.addWidget(self.dependencia_input, 3, 3)
        layout.addWidget(ambiente_label, 3, 4)
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
        layout.addWidget(ingresar_button, 7, 5)
        layout.addWidget(eliminar_button, 8, 5)

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
        layout.addWidget(destino_label, 9, 0, 1, 6)
        trabajador_destino_label = QLabel("Trabajador:")
        trabajador_destino_label.setStyleSheet("font-size: 16px;")
        self.trabajador_destino_input = QLineEdit()
        self.trabajador_destino_input.setStyleSheet("font-size: 16px;")
        codigo_destino_label = QLabel("Codigo:")
        codigo_destino_label.setStyleSheet("font-size: 16px;")
        self.codigo_destino_input = QLineEdit()
        self.codigo_destino_input.setStyleSheet("font-size: 16px;")
        dependencia_destino_label = QLabel("Dependencia:")
        dependencia_destino_label.setStyleSheet("font-size: 16px;")
        self.dependencia_destino_input = QLineEdit()
        self.dependencia_destino_input.setStyleSheet("font-size: 16px;")
        ambiente_destino_label = QLabel("Ambiente:")
        ambiente_destino_label.setStyleSheet("font-size: 16px;")
        self.ambiente_destino_input = QLineEdit()
        self.ambiente_destino_input.setStyleSheet("font-size: 16px;")

        layout.addWidget(trabajador_destino_label, 10, 0)
        layout.addWidget(self.trabajador_destino_input, 10, 1)
        layout.addWidget(codigo_destino_label, 11, 0)
        layout.addWidget(self.codigo_destino_input, 11, 1)
        layout.addWidget(dependencia_destino_label, 10, 2)
        layout.addWidget(self.dependencia_destino_input, 10, 3)
        layout.addWidget(ambiente_destino_label, 10, 4)
        layout.addWidget(self.ambiente_destino_input, 10, 5)
############################################################################################################

        # Botón "Generar" de color verde
        generar_button = QPushButton("Imprimir")
        generar_button.setStyleSheet("background-color: #008000; color: white; font-size: 16px;")
        layout.addWidget(generar_button, 11, 5)
           
        generar_button.clicked.connect(self.enviar_al_modulo)

    def enviar_al_modulo(self):
        # Obtener todos los datos ingresados
        formato = self.formato_combo.currentText()
        trabajador = self.trabajador_input.text().upper()
        codigo=self.codigo_input.text().upper()
        dependencia = self.dependencia_input.text().upper()
        ambiente = self.ambiente_input.text().upper()
        trabajador_destino = self.trabajador_destino_input.text().upper()
        codigo_destino = self.codigo_destino_input.text().upper()
        dependencia_destino = self.dependencia_destino_input.text().upper()
        ambiente_destino = self.ambiente_destino_input.text().upper()
        
        # Obtener la tabla
        tabla = self.table
        generador = GenerarPDF()
        # Llamar a la función generar_reporte en el módulo generar_pdf
        # Configurar los datos en GenerarPDF
        generador.set_datos(formato, trabajador, codigo, dependencia, ambiente, trabajador_destino, codigo_destino, dependencia_destino, ambiente_destino,tabla)
        generador.generar_reporte()


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
