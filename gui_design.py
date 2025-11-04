# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton,
    QTableWidget, QHeaderView, QGroupBox,
    QMessageBox, QSpinBox, QProgressBar, QApplication, QTableWidgetItem, QFrame,
    QScrollArea # <--- Importante para el scroll vertical
)
from PyQt5.QtCore import Qt, QLocale, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QBrush, QLinearGradient

class MarkovGUI(QMainWindow):

    COLOR_PALETTE = {
        "Soleado": {"fuerte": "#FFB300", "claro": "#FFE082", "icon": "☀️"},
        "Nublado": {"fuerte": "#546E7A", "claro": "#CFD8DC", "icon": "☁️"},
        "Lluvioso": {"fuerte": "#1976D2", "claro": "#90CAF9", "icon": "🌧️"}
    }

    def __init__(self, estados):
        super().__init__()
        self.setWindowTitle("Simulador de Cadena de Markov del Clima 🌦️")
        self.estados = estados
        self.setLocale(QLocale(QLocale.Spanish, QLocale.Guatemala))

        # Tamaño inicial y centrado
        self.resize(900, 980)
        self.setObjectName("mainAppWindow")
        self.center_on_screen()

        # Fondo degradado suave
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 1000)
        gradient.setColorAt(0.0, QColor("#E3F2FD"))
        gradient.setColorAt(1.0, QColor("#FFFFFF"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # Estilos base
        self.setStyleSheet(self._get_base_styles())

        # ------------------- IMPLEMENTACIÓN DE SCROLL VERTICAL -------------------
        self.main_scroll_area = QScrollArea()
        self.main_scroll_area.setWidgetResizable(True)
        self.main_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.main_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.main_scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        # Contenedor principal de la interfaz que irá DENTRO del QScrollArea
        scroll_content = QWidget()
        self.main_layout = QVBoxLayout(scroll_content)
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.main_layout.setContentsMargins(18, 18, 18, 18)
        self.main_layout.setSpacing(12)
        
        self.main_scroll_area.setWidget(scroll_content)
        
        # Widget central y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # El layout del central_widget contendrá el QScrollArea
        main_container_layout = QVBoxLayout(central_widget)
        main_container_layout.setContentsMargins(0, 0, 0, 0)
        main_container_layout.addWidget(self.main_scroll_area)
        # ------------------- FIN DE SCROLL VERTICAL -------------------

        # UI sections
        self._setup_header_bar()
        self._setup_daily_weather_panel()
        self._setup_parametros_calculo()
        self._setup_matriz_transicion_box()
        self._setup_botones_generales()
        self._setup_resultados_box()
        self._setup_statistics_and_history_box()

        # Timer para animación diaria
        self.daily_weather_timer = QTimer(self)
        self.daily_weather_timer.timeout.connect(self._update_daily_weather_animation)
        self.current_simulation_day = 0
        self.simulated_history = []
        
    def _get_base_styles(self):
        return """
            QMainWindow {
                background-color: #E3F2FD;
            }
            QGroupBox {
                border: 2px solid #BBDEFB;
                border-radius: 10px;
                margin-top: 12px;
                background-color: #FFFFFF;
                padding: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: #0D47A1;
                font-weight: bold;
            }
            QPushButton {
                border-radius: 8px;
                padding: 7px 12px;
                font-weight: bold;
                color: white;
                min-height: 36px;
            }
            /* Estilos para SpinBox y ComboBox: color de texto siempre negro */
            QSpinBox, QComboBox {
                padding: 5px;
                border: 1px solid #90CAF9;
                border-radius: 5px;
                background-color: #FAFAFA;
                color: black;
            }
            QComboBox QAbstractItemView {
                color: black;
                selection-background-color: #BBDEFB;
            }
            QTableWidget {
                border: 1px solid #B0BEC5;
                border-radius: 6px;
                gridline-color: #ECEFF1;
                background-color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #90CAF9;
                color: #0D47A1;
                padding: 4px;
                border: none;
                font-weight: bold;
            }
            /* Estilos para scrollbars (Scroll Vertical) */
            QScrollBar:vertical {
                border: 1px solid #90CAF9;
                background: #F0F0F0;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #BBDEFB;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """

    def _setup_header_bar(self):
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #1976D2;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 6px;
            }
        """)
        layout = QHBoxLayout(header_frame)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(15, 8, 15, 8)

        icon_label = QLabel("🌦️")
        icon_label.setFont(QFont("Segoe UI Emoji", 36))
        title_label = QLabel("Simulador de Cadena de Markov del Clima")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        self.main_layout.addWidget(header_frame)

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    # ---------------- UI Sections ----------------
    def _setup_daily_weather_panel(self):
        daily_weather_panel = QWidget()
        daily_weather_panel.setObjectName("dailyWeatherPanel")
        daily_layout = QVBoxLayout(daily_weather_panel)
        daily_layout.setAlignment(Qt.AlignCenter)

        daily_weather_panel.setStyleSheet("""
            QWidget#dailyWeatherPanel {
                border: 2px solid #BBDEFB;
                border-radius: 12px;
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #E3F2FD, stop:1 #FFFFFF);
                padding: 12px;
                margin-bottom: 8px;
            }
        """)

        label_title = QLabel("<b>Clima del Día (Simulación)</b>")
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setFont(QFont("Arial", 12, QFont.Bold))
        daily_layout.addWidget(label_title)

        self.label_sim_icon = QLabel("☀️")
        self.label_sim_icon.setFont(QFont("Segoe UI Emoji", 72))
        self.label_sim_icon.setAlignment(Qt.AlignCenter)
        daily_layout.addWidget(self.label_sim_icon)

        self.label_sim_status = QLabel("Soleado")
        self.label_sim_status.setFont(QFont("Arial", 26, QFont.Bold))
        self.label_sim_status.setAlignment(Qt.AlignCenter)
        self.label_sim_status.setStyleSheet("color: #FFB300;")
        daily_layout.addWidget(self.label_sim_status)

        self.label_sim_day = QLabel("Día 0 de N", alignment=Qt.AlignCenter)
        self.label_sim_day.setFont(QFont("Arial", 11))
        daily_layout.addWidget(self.label_sim_day)

        self.main_layout.addWidget(daily_weather_panel)

    def _setup_parametros_calculo(self):
        param_group = QGroupBox("Parámetros de Simulación")
        param_layout = QVBoxLayout(param_group)
        param_layout.setContentsMargins(10, 10, 10, 10)
        param_layout.setSpacing(8)

        estado_inicial_layout = QHBoxLayout()
        estado_inicial_layout.addWidget(QLabel("<b>Estado Inicial ($q_0$):</b>"))
        self.combo_estado_inicial = QComboBox()
        self.combo_estado_inicial.addItems(self.estados)
        estado_inicial_layout.addWidget(self.combo_estado_inicial)
        param_layout.addLayout(estado_inicial_layout)

        n_dias_layout = QHBoxLayout()
        n_dias_layout.addWidget(QLabel("<b>Número de Pasos (días) $n$:</b>"))
        self.spin_n_dias = QSpinBox()
        self.spin_n_dias.setRange(1, 100)
        self.spin_n_dias.setValue(7)
        n_dias_layout.addWidget(self.spin_n_dias)
        param_layout.addLayout(n_dias_layout)

        self.main_layout.addWidget(param_group)

    def _setup_matriz_transicion_box(self):
        matriz_box = QGroupBox("Matriz de Transición (P) y Alfabeto ($\\Sigma$)")
        layout = QVBoxLayout(matriz_box)
        layout.setSpacing(8)

        btn_layout = QHBoxLayout()
        self.btn_importar = QPushButton("📄 Importar Matriz")
        self.btn_importar.setStyleSheet("background-color: #546E7A;")
        self.btn_guia = QPushButton("ℹ️ Guía de Importación")
        self.btn_guia.setStyleSheet("background-color: #7F8C8D;")
        self.btn_grafico = QPushButton("📊 Mostrar Autómata")
        self.btn_grafico.setStyleSheet("background-color: #43A047;")
        btn_layout.addWidget(self.btn_importar)
        btn_layout.addWidget(self.btn_guia)
        btn_layout.addWidget(self.btn_grafico)
        layout.addLayout(btn_layout)

        self.table_matriz = QTableWidget(3, 3)
        self.table_matriz.setHorizontalHeaderLabels(self.estados)
        self.table_matriz.setVerticalHeaderLabels(self.estados)
        self.table_matriz.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_matriz.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_matriz.setMinimumHeight(160)
        layout.addWidget(self.table_matriz)
        self.main_layout.addWidget(matriz_box)

    def _setup_botones_generales(self):
        action_layout = QHBoxLayout()
        self.btn_calcular = QPushButton("🚀 CALCULAR $P^n$")
        self.btn_calcular.setStyleSheet("background-color: #43A047;")
        self.btn_reiniciar = QPushButton("🔄 Reiniciar Valores")
        self.btn_reiniciar.setStyleSheet("background-color: #E53935;")
        action_layout.addWidget(self.btn_calcular)
        action_layout.addWidget(self.btn_reiniciar)
        self.main_layout.addLayout(action_layout)

    def _setup_resultados_box(self):
        self.resultados_box = QGroupBox("Resultados de la Simulación")
        self.resultados_box.setVisible(False)
        layout = QVBoxLayout(self.resultados_box)
        layout.setSpacing(8)

        self.label_n_final = QLabel("<b>Probabilidades después de N días:</b>")
        layout.addWidget(self.label_n_final)

        self.table_pn = QTableWidget(3, 3)
        self.table_pn.setHorizontalHeaderLabels(self.estados)
        self.table_pn.setVerticalHeaderLabels(self.estados)
        self.table_pn.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_pn.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_pn.setMinimumHeight(160)
        layout.addWidget(self.table_pn)

        self.prob_labels = {}
        for estado in self.estados:
            label = QLabel(f"Prob. de ser <b>{estado}</b>: 0.0000%")
            label.setFont(QFont("Arial", 10))
            layout.addWidget(label)
            self.prob_labels[estado] = label

        self.label_clima_dia_n = QLabel("Clima más probable en el día <b>N</b>: Pendiente")
        self.label_clima_dia_n.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(self.label_clima_dia_n)

        self.main_layout.addWidget(self.resultados_box)

    def _setup_statistics_and_history_box(self):
        stats_history_box = QGroupBox("Estadísticas e Historial")
        stats_history_box.setVisible(False)
        sh_layout = QVBoxLayout(stats_history_box)
        sh_layout.setSpacing(8)
        sh_layout.setContentsMargins(8, 8, 8, 8)

        # Estadísticas (labels y progressbars)
        self.stats_labels = {}
        self.stats_progress_bars = {}
        for estado in self.estados:
            stat_layout = QHBoxLayout()
            icon_label = QLabel(self.COLOR_PALETTE[estado]["icon"])
            icon_label.setFont(QFont("Segoe UI Emoji", 18))
            stat_layout.addWidget(icon_label)

            text_label = QLabel(f"<b>{estado}:</b> 0 (0.00%)")
            self.stats_labels[estado] = text_label
            stat_layout.addWidget(text_label)

            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(0)
            progress_bar.setTextVisible(False)
            color_fuerte = self.COLOR_PALETTE[estado]['fuerte']
            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: 1px solid #E0EAF6;
                    border-radius: 5px;
                    text-align: center;
                }}
                QProgressBar::chunk {{
                    background-color: {color_fuerte};
                    margin: 0px;
                }}
            """)
            self.stats_progress_bars[estado] = progress_bar
            stat_layout.addWidget(progress_bar)
            sh_layout.addLayout(stat_layout)

        # Historial visual: sin botones de Guardar/Cargar
        sh_layout.addWidget(QLabel("<b>Historial:</b>"))
        
        history_frame = QFrame()
        self.history_layout = QHBoxLayout(history_frame)
        self.history_layout.setSpacing(2)
        self.history_layout.setAlignment(Qt.AlignLeft)
        self.history_layout.setContentsMargins(0, 0, 0, 0)
        
        # Añadimos placeholders iniciales
        for _ in range(50):
            label = QLabel("▪")
            label.setFont(QFont("Segoe UI Emoji", 10))
            self.history_layout.addWidget(label)
        
        sh_layout.addWidget(history_frame)

        self.main_layout.addWidget(stats_history_box)
        self.stats_history_box = stats_history_box

    # ---------------- Funciones UI existentes ----------------
    def update_initial_display(self, estado_inicial_str):
        self.label_sim_icon.setText(self.COLOR_PALETTE[estado_inicial_str]["icon"])
        self.label_sim_icon.setStyleSheet(f"color: {self.COLOR_PALETTE[estado_inicial_str]['fuerte']};")
        self.label_sim_status.setText(estado_inicial_str)
        self.label_sim_status.setStyleSheet(f"color: {self.COLOR_PALETTE[estado_inicial_str]['fuerte']};")
        self.label_sim_day.setText("Día 0 de N")

    def start_daily_weather_animation(self, historial, n_dias):
        self.simulated_history = historial
        self.current_simulation_day = 0
        self.total_simulation_days = n_dias
        self.daily_weather_timer.start(400)

    def stop_daily_weather_animation(self):
        self.daily_weather_timer.stop()

    def _update_daily_weather_animation(self):
        if self.current_simulation_day < len(self.simulated_history):
            current_weather = self.simulated_history[self.current_simulation_day]
            self.label_sim_icon.setText(self.COLOR_PALETTE[current_weather]["icon"])
            self.label_sim_status.setText(current_weather)
            self.label_sim_day.setText(f"Día {self.current_simulation_day + 1} de {self.total_simulation_days}")

            self.label_sim_icon.setStyleSheet(f"color: {self.COLOR_PALETTE[current_weather]['fuerte']};")
            self.label_sim_status.setStyleSheet(f"color: {self.COLOR_PALETTE[current_weather]['fuerte']};")
            self.current_simulation_day += 1
        else:
            self.stop_daily_weather_animation()
            self.label_sim_day.setText(f"Simulación Finalizada (Día {self.total_simulation_days})")
            last_weather = self.simulated_history[-1] if self.simulated_history else "Soleado"
            self.label_sim_icon.setStyleSheet(f"color: {self.COLOR_PALETTE[last_weather]['fuerte']};")
            self.label_sim_status.setStyleSheet(f"color: {self.COLOR_PALETTE[last_weather]['fuerte']};")

    def update_statistics_and_history(self, historial_completo):
        # El historial_completo ahora tiene N días, lo que corrige el cálculo de porcentajes.
        total_dias = len(historial_completo)
        counts = {estado: historial_completo.count(estado) for estado in self.estados}

        for estado in self.estados:
            count = counts.get(estado, 0)
            percentage = (count / total_dias) * 100 if total_dias > 0 else 0
            self.stats_labels[estado].setText(f"<b>{estado}:</b> {count} ({percentage:.2f}%)")
            self.stats_progress_bars[estado].setValue(int(percentage))

        # Limpiar history layout
        for i in reversed(range(self.history_layout.count())):
            widget = self.history_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Muestra hasta 50 iconos, pero solo los simulados
        ultimos_50_dias = historial_completo[-50:]
        for clima in ultimos_50_dias:
            label = QLabel(self.COLOR_PALETTE[clima]["icon"])
            label.setFont(QFont("Segoe UI Emoji", 18))
            label.setStyleSheet(f"color: {self.COLOR_PALETTE[clima]['fuerte']};")
            self.history_layout.addWidget(label)

        # Rellena con espacios si el historial es menor a 50
        for _ in range(50 - len(ultimos_50_dias)):
            label = QLabel(" ")
            self.history_layout.addWidget(label)

        self.stats_history_box.setVisible(True)

    def mostrar_guia(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Guía de Importación")
        msg.setText(" Formato de Archivo CSV/TXT\n\nEl archivo debe ser una matriz de 3 filas por 3 columnas.\n\nLas columnas deben estar separadas por comas (,) o punto y coma (;).\n\n¡Importante! Cada fila debe sumar 1.\n\nEjemplo:\n0.70,0.20,0.10\n0.30,0.40,0.30\n0.20,0.40,0.40")
        msg.setStyleSheet("QMessageBox { background-color: #E3F2FD; } QLabel { color: #0D47A1; }")
        msg.exec_()

    def mostrar_mensaje(self, titulo, mensaje, icono=QMessageBox.Information):
        msg = QMessageBox(self)
        msg.setIcon(icono)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.setStyleSheet("QMessageBox { background-color: #E3F2FD; } QLabel { color: #000000; }")
        msg.exec_()