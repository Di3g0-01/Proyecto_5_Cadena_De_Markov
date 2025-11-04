# -*- coding: utf-8 -*-
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QTimer
from logic_model import MarkovModel
from gui_design import MarkovGUI
from graph_viewer import GraphViewer


class MarkovController:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.graph_viewer = None
        self._initialize_matrix_table()

        # Conexiones
        self.view.btn_calcular.clicked.connect(self.handle_calculate)
        self.view.btn_reiniciar.clicked.connect(self.handle_reset)
        self.view.btn_importar.clicked.connect(self.handle_import_matrix)
        self.view.btn_guia.clicked.connect(self.view.mostrar_guia)
        self.view.btn_grafico.clicked.connect(self.handle_show_graph)
        self.view.combo_estado_inicial.currentIndexChanged.connect(self.handle_initial_state_changed)
        self.handle_initial_state_changed()

    def _initialize_matrix_table(self):
        P_default = self.model.P_array
        for i in range(3):
            for j in range(3):
                item = QTableWidgetItem(f"{P_default[i, j]:.2f}")
                item.setTextAlignment(4)
                self.view.table_matriz.setItem(i, j, item)

    def _get_matrix_from_table(self):
        data = []
        for i in range(3):
            row = []
            for j in range(3):
                item = self.view.table_matriz.item(i, j)
                try:
                    value = float(item.text().replace(',', '.')) if item else 0.0
                except ValueError:
                    self.view.mostrar_mensaje("Error", f"Valor inválido en la celda {i+1},{j+1}", QMessageBox.Warning)
                    return pd.DataFrame()
                row.append(value)
            data.append(row)
        return pd.DataFrame(data, columns=self.model.ESTADOS, index=self.model.ESTADOS)

    def handle_initial_state_changed(self):
        estado_inicial = self.view.combo_estado_inicial.currentText()
        if estado_inicial:
            self.view.update_initial_display(estado_inicial)
        self.view.resultados_box.setVisible(False)
        self.view.stats_history_box.setVisible(False)
        self.view.stop_daily_weather_animation()

    def handle_calculate(self):
        P_df = self._get_matrix_from_table()
        if P_df.empty:
            return

        es_valida, P_array_o_error = self.model.validar_matriz(P_df)
        if not es_valida:
            self.view.mostrar_mensaje("Error de Validación", P_array_o_error, QMessageBox.Critical)
            return

        self.model.P_array = P_array_o_error
        n = self.view.spin_n_dias.value()
        estado_inicial = self.view.combo_estado_inicial.currentText()

        try:
            Pn_array = self.model.calcular_pn(n)
            df_final = self.model.obtener_probabilidades_finales(Pn_array, estado_inicial)

            for i in range(3):
                for j in range(3):
                    item = QTableWidgetItem(f"{Pn_array[i, j]:.4f}")
                    item.setTextAlignment(4)
                    self.view.table_pn.setItem(i, j, item)

            for _, row in df_final.iterrows():
                estado = row['Estado']
                prob = row['Probabilidad']
                self.view.prob_labels[estado].setText(
                    f"Prob. de ser <b>{estado}</b>: {prob * 100:.4f}%"
                )

            clima_mas_probable, prob = self.model.obtener_clima_mas_probable_dia_n(n, estado_inicial)
            self.view.label_clima_dia_n.setText(
                f"Clima más probable en el día <b>{n}</b>: <b>{clima_mas_probable}</b> ({prob*100:.2f}%)"
            )

            # CORRECCIÓN CLAVE: Simular SOLAMENTE 'n' días.
            historial = self.model.simular_historial_climatico(self.model.P_array, n, estado_inicial)
            
            # Las estadísticas se actualizan con el historial correcto de 'n' días.
            self.view.update_statistics_and_history(historial)

            self.view.resultados_box.setVisible(True)
            # self.view.fade_in_results() # LÍNEA ELIMINADA

            # La animación usa el historial completo de 'n' días.
            self.view.start_daily_weather_animation(historial, n)
            QTimer.singleShot(n * 600, lambda: self.view.mostrar_mensaje("Cálculo Exitoso", f"Cálculo de P^{n} completado."))

        except Exception as e:
            self.view.mostrar_mensaje("Error", str(e), QMessageBox.Critical)

    def handle_reset(self):
        self.model = MarkovModel()
        self._initialize_matrix_table()
        self.view.resultados_box.setVisible(False)
        self.view.stats_history_box.setVisible(False)
        self.view.label_clima_dia_n.setText("Clima más probable en el día N: Pendiente")
        self.view.stop_daily_weather_animation()
        self.handle_initial_state_changed()
        self.view.mostrar_mensaje("Reiniciado", "Aplicación restablecida.")

    def handle_import_matrix(self):
        file, _ = QFileDialog.getOpenFileName(self.view, "Importar Matriz", "", "Archivos (*.csv *.txt)")
        if not file:
            return
        try:
            df = pd.read_csv(file, sep='[;,]', header=None, engine='python')
            es_valida, result = self.model.validar_matriz(df)
            if not es_valida:
                raise ValueError(result)
            self.model.P_array = result
            for i in range(3):
                for j in range(3):
                    item = QTableWidgetItem(f"{result[i, j]:.4f}")
                    item.setTextAlignment(4)
                    self.view.table_matriz.setItem(i, j, item)
            self.view.mostrar_mensaje("Importación Exitosa", "Matriz cargada correctamente.")
        except Exception as e:
            self.view.mostrar_mensaje("Error", str(e), QMessageBox.Critical)

    def handle_show_graph(self):
        P_df = self._get_matrix_from_table()
        if P_df.empty:
            return
        es_valida, P_array_o_error = self.model.validar_matriz(P_df)
        if not es_valida:
            self.view.mostrar_mensaje("Error", P_array_o_error, QMessageBox.Critical)
            return
            
        # OBTENER EL HISTORIAL SIMULADO DE LA VISTA
        historial_actual = self.view.simulated_history 
        
        if self.graph_viewer and self.graph_viewer.isVisible():
            self.graph_viewer.close()
            
        # CORRECCIÓN CLAVE: Pasar el historial al GraphViewer
        self.graph_viewer = GraphViewer(P_array_o_error, self.model.ESTADOS, historial=historial_actual)
        self.graph_viewer.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = MarkovModel()
    view = MarkovGUI(model.ESTADOS)
    controller = MarkovController(model, view)
    view.show()
    sys.exit(app.exec_())