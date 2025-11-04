# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

COLOR_PALETTE = {
    "Soleado": {"fuerte": "#FFB300", "claro": "#FFE082"},
    "Nublado": {"fuerte": "#546E7A", "claro": "#CFD8DC"},
    "Lluvioso": {"fuerte": "#1976D2", "claro": "#90CAF9"}
}

class GraphViewer(QMainWindow):

    def __init__(self, P_array, estados, historial=None):
        super().__init__()
        self.P_array = P_array
        self.estados = estados
        self.historial = historial or []
        self.setWindowTitle("Autómata Probabilístico de Clima (Gráfico)")
        self.setGeometry(100, 100, 720, 720)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        layout.addWidget(QLabel(r"<b>Autómata Probabilístico de Clima</b>", alignment=Qt.AlignCenter))
        self.figure, self.canvas = self._draw_graph(self.historial)
        layout.addWidget(self.canvas)

    def _draw_graph(self, historial=None):
        fig = plt.figure(figsize=(6, 7))
        gs = fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.35)

        ax = fig.add_subplot(gs[0])
        ax.set_title("Diagrama del Autómata Probabilístico", fontsize=14)
        ax.axis('off')

        pos = {
            "Soleado": (0, 1.5),
            "Nublado": (1.2, -0.5),
            "Lluvioso": (-1.2, -0.5)
        }
        
        for estado in self.estados:
            x, y = pos[estado]
            ax.plot(x, y, 'o', markersize=45, color=COLOR_PALETTE[estado]['claro'], alpha=0.95, zorder=1)
            ax.text(x, y, estado, ha='center', va='center', fontsize=10, weight='bold', color=COLOR_PALETTE[estado]['fuerte'], zorder=2)
            
        for i, estado_origen in enumerate(self.estados):
            for j, estado_destino in enumerate(self.estados):
                prob = float(self.P_array[i, j])
                if prob > 0:
                    x1, y1 = pos[estado_origen]
                    x2, y2 = pos[estado_destino]
                    
                    if estado_origen == estado_destino:
                        r = 0.3 
                        ax.annotate("", xy=(x1 - 0.1, y1 + 0.1), xytext=(x1 + 0.1, y1 + 0.1), 
                                    arrowprops=dict(arrowstyle="->", color=COLOR_PALETTE[estado_origen]['fuerte'], linewidth=1.5, 
                                    connectionstyle=f"arc3,rad={r}", shrinkA=10, shrinkB=10), zorder=0)
                        ax.text(x1 - 0.25, y1 + 0.35, f"{prob:.4f}", color=COLOR_PALETTE[estado_origen]['fuerte'], fontsize=9, ha='center', backgroundcolor='white', alpha=0.9)
                    else:
                        mid_x = (x1 + x2) / 2
                        mid_y = (y1 + y2) / 2
                        if i < j:
                            rad = 0.15 
                            text_offset = -0.1 
                        else:
                            rad = 0.15 
                            text_offset = 0.1 

                        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), 
                                    arrowprops=dict(arrowstyle="->", color=COLOR_PALETTE[estado_origen]['fuerte'], linewidth=1.5, 
                                    connectionstyle=f"arc3,rad={rad}", shrinkA=15, shrinkB=15), zorder=0)
                        text_x = mid_x + (y2 - y1) * rad * 3 * text_offset
                        text_y = mid_y + (x1 - x2) * rad * 3 * text_offset
                        ax.text(text_x, text_y, f"{prob:.4f}", color=COLOR_PALETTE[estado_origen]['fuerte'], fontsize=9, ha='center', va='center', zorder=3, backgroundcolor='white', alpha=0.9)

        ax_hist = fig.add_subplot(gs[1])
        ax_hist.set_title("Resumen del Historial (conteo por estado)", fontsize=11)
        ax_hist.set_axis_off()

        if historial:
            counts = {estado: historial.count(estado) for estado in self.estados}
            total = sum(counts.values()) if sum(counts.values()) > 0 else 1
            estados_plot = self.estados
            valores = [counts[e] for e in estados_plot]
            colores = [COLOR_PALETTE[e]['fuerte'] for e in estados_plot]

            left, bottom, width, height = 0.12, 0.08, 0.76, 0.28
            axb = fig.add_axes([left, 0.08, width, 0.18])
            y_pos = np.arange(len(estados_plot))
            axb.barh(y_pos, valores, color=colores, alpha=0.95)
            axb.set_yticks(y_pos)
            axb.set_yticklabels(estados_plot)
            axb.set_xlabel("Días (conteo)")
            for i, v in enumerate(valores):
                axb.text(v + 0.02 * max(1, max(valores)), i, f"{v} ({(v/total*100):.1f}%)", va='center', fontsize=9)
            axb.set_xlim(0, max(max(valores) * 1.15, 1))
        else:
            ax_hist.text(0.5, 0.5, "No hay historial para mostrar", ha='center', va='center', fontsize=10, alpha=0.7)

        fig.tight_layout()
        canvas = FigureCanvas(fig)
        return fig, canvas
