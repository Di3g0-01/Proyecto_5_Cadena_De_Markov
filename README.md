# Simulador de Cadena de Markov del Clima 🌦️

[](https://www.python.org/)
[](https://www.riverbankcomputing.com/software/pyqt/)

## Descripción

Este proyecto es un **simulador educativo de una Cadena de Markov de Primer Orden**, modelando la transición del estado del clima (Soleado, Nublado, Lluvioso) a lo largo de los días. Fue desarrollado como parte de un ejercicio académico para el curso de **Lenguajes Formales y Autómatas** de la Facultad de Ingeniería (Segundo Semestre, Septiembre 2025).

El simulador permite al usuario ingresar una Matriz de Transición (P) y un número de pasos ($n$ días). Realiza tanto el cálculo teórico de las probabilidades después de $n$ pasos ($P^n$) como una simulación práctica de Montecarlo para generar un historial climático día a día.

Este simulador es ideal para entender los conceptos de **Autómatas Probabilísticos** y el comportamiento de los sistemas estocásticos, mostrando la diferencia entre el cálculo determinístico de la matriz de potencia y la variabilidad de una simulación a corto plazo.

-----

## ⚙️ Características Principales

  - **Matriz de Transición (P)**: Interfaz de tabla intuitiva para ingresar las probabilidades de transición entre los 3 estados del clima (Soleado, Nublado, Lluvioso).
  - **Cálculo Determinista ($P^n$)**: Calcula y muestra la matriz de potencia $P^n$ y las probabilidades finales de estar en cada estado después de $N$ días, partiendo de un estado inicial.
  - **Simulación de Montecarlo**: Ejecuta una simulación estocástica paso a paso durante $N$ días, mostrando una animación diaria del clima.
  - **Estadísticas del Historial**: Muestra un conteo y porcentaje exacto de la frecuencia de cada estado dentro de la simulación de $N$ días.
  - **Visualización Gráfica**: Genera un **Autómata Probabilístico (Grafo de Transición)** utilizando Matplotlib, mostrando los estados como nodos y las probabilidades como aristas etiquetadas. Incluye un gráfico de barras que resume el historial simulado para un mejor análisis.
  - **Validación de Matriz**: Valida que las probabilidades estén en el rango $[0, 1]$ y que cada fila de la matriz sume exactamente 1.
  - **Persistencia y Recarga**: Permite importar matrices de transición desde archivos CSV/TXT.
  - **Interfaz Gráfica (GUI)**: Desarrollada con PyQt5 para una experiencia de usuario interactiva y fluida.

-----

## 💻 Requisitos

  - **Python**: Versión 3.6 o superior.
  - **Bibliotecas Estándar de Python**:
      - `json`, `os`, `datetime` (para operaciones auxiliares).
  - **Dependencias de Terceros**:
      - `PyQt5` (para la interfaz gráfica de usuario).
      - `NumPy` y `Pandas` (para el manejo eficiente de la matriz y los cálculos).
      - `Matplotlib` (para la visualización del grafo y las estadísticas).

-----

## 🤝 Contribución

¡Contribuciones para mejorar el simulador son bienvenidas\! Si deseas optimizar los cálculos o mejorar la visualización del autómata:

1.  Fork el repositorio.
2.  Crea una rama: `git checkout -b feature/mejora-grafo`.
3.  Commit cambios: `git commit -m "Mejora el renderizado del autómata"`.
4.  Push a la rama: `git push origin feature/mejora-grafo`.
5.  Abre un Pull Request.

Por favor, mantén el enfoque en la claridad educativa de los conceptos de la Cadena de Markov.

-----

## 📧 Créditos y Contacto

  - **Autor**: Diego Ovalle - Di3g0\_01
  - **Curso**: **Lenguajes Formales y Autómatas**
  - **Fecha**: Octubre 2025.
  - Para dudas o sugerencias: Ovallediego.p@gmail.com o abre un issue en GitHub.

¡Espero que este simulador te sea útil para entender la conexión entre las cadenas de Markov y los Autómatas Probabilísticos\! 🚀
