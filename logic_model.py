# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import random

class MarkovModel:
    
    ESTADOS = ["Soleado", "Nublado", "Lluvioso"]
    
    def __init__(self, P_initial=None):
        if P_initial is None:
            self.P_array = np.array([
                [0.70, 0.20, 0.10],
                [0.30, 0.40, 0.30],
                [0.20, 0.40, 0.40]
            ])
        else:
            self.P_array = P_initial

    def validar_matriz(self, P_df):
        """
        Valida que P_df sea 3x3, valores entre 0 y 1, y cada fila sume 1 (con tolerancia).
        Devuelve (True, numpy_array) o (False, mensaje_error).
        """
        if P_df.shape != (3, 3):
            return False, "La matriz debe ser de 3x3."
        
        P_array = P_df.values.astype(float)
        
        if (P_array < 0).any() or (P_array > 1).any():
            return False, "Todas las probabilidades deben estar en el rango [0, 1]."
            
        for i, row in enumerate(P_array):
            if not np.isclose(np.sum(row), 1.0, atol=1e-4):
                return False, f"La fila '<b>{self.ESTADOS[i]}</b>' no suma 1.0. Suma: {np.sum(row):.4f}"
            
        return True, P_array

    def calcular_pn(self, n):
        """
        Calcula P^n (potencia de la matriz de transición).
        Si n < 1 devuelve la identidad.
        """
        if n < 1:
            return np.identity(len(self.ESTADOS))
        
        return np.linalg.matrix_power(self.P_array, n)

    def obtener_probabilidades_finales(self, Pn_o_P_array, estado_inicial_str):
        """
        Dado P^n (o una matriz P), devuelve un DataFrame con Probabilidades desde estado inicial.
        """
        try:
            estado_idx = self.ESTADOS.index(estado_inicial_str)
        except ValueError:
            raise ValueError(f"Estado inicial '{estado_inicial_str}' no es válido.")
            
        probabilidades = Pn_o_P_array[estado_idx, :]
        return pd.DataFrame({
            'Estado': self.ESTADOS,
            'Probabilidad': probabilidades
        })

    def simular_historial_climatico(self, P_array_actual, n_dias_simulacion, estado_inicial_str):
        """
        Simula n_dias_simulacion a partir de estado_inicial_str usando P_array_actual.
        Devuelve lista de estados (historial).
        """
        if n_dias_simulacion < 1:
            return []

        historial = []
        try:
            estado_actual_idx = self.ESTADOS.index(estado_inicial_str)
        except ValueError:
            raise ValueError(f"Estado inicial '{estado_inicial_str}' no es válido para simulación.")

        for _ in range(n_dias_simulacion):
            historial.append(self.ESTADOS[estado_actual_idx])
            transicion_probs = P_array_actual[estado_actual_idx, :]

            if not np.isclose(np.sum(transicion_probs), 1.0):
                transicion_probs = transicion_probs / np.sum(transicion_probs)

            estado_actual_idx = random.choices(range(len(self.ESTADOS)), weights=transicion_probs, k=1)[0]
            
        return historial

    def obtener_clima_mas_probable_dia_n(self, n_dias, estado_inicial_str):
        """
        Retorna (clima_mas_probable, probabilidad) para el día n.
        """
        if n_dias < 1:
             return estado_inicial_str, 1.0

        Pn_array = self.calcular_pn(n_dias)
        probabilidades_en_n = self.obtener_probabilidades_finales(Pn_array, estado_inicial_str)
        max_prob = probabilidades_en_n['Probabilidad'].max()
        clima_mas_probable = probabilidades_en_n[np.isclose(probabilidades_en_n['Probabilidad'], max_prob)]['Estado'].iloc[0]
        return clima_mas_probable, max_prob