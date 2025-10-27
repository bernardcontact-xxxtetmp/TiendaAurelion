# Programa de Análisis de Ventas - Python

## Descripción

Este programa Python procesa datos de ventas comerciales desde un archivo CSV y genera:
- Análisis estadístico completo
- Visualizaciones con matplotlib
- Reporte detallado en texto
- Datos procesados en formato JSON para dashboards

## Requisitos Previos

### Instalación de Dependencias

Antes de ejecutar el programa, necesitas instalar las siguientes librerías de Python:

```bash
# Instalar pandas para procesamiento de datos
pip install pandas

# Instalar matplotlib para visualizaciones
pip install matplotlib

# Instalar seaborn para estilos de gráficos (opcional)
pip install seaborn

# Instalar numpy para cálculos numéricos
pip install numpy
```

O puedes instalar todas de una vez:
```bash
pip install pandas matplotlib seaborn numpy
```

### Verificar Instalación
```bash
python -c "import pandas; import matplotlib; import numpy; print('✅ Todas las librerías instaladas correctamente')"
```

## Uso del Programa

### 1. Preparar los Datos

Asegúrate de tener tu archivo CSV en la misma carpeta que el programa `main.py`. El archivo debe tener las siguientes columnas:

- `fecha`
- `id_cliente`
- `nombre_cliente_final`
- `ciudad`
- `id_producto`
- `nombre_producto`
- `categoria_redefinida`
- `cantidad`
- `importe`
- `medio_pago`

### 2. Ejecutar el Programa

```bash
# Si el archivo CSV se llama 'datos_powerbi.csv' y está en la misma carpeta
python main.py

# Si el archivo tiene otro nombre o está en otra ubicación
python main.py
# Luego ingresa la ruta cuando el programa la solicite
```

### 3. Seguir las Instrucciones

El programa te guiará a través del proceso:
1. Solicitará la ruta del archivo CSV
2. Validará y procesará los datos
3. Generará visualizaciones
4. Exportará los resultados
5. Preguntará si deseas ver las visualizaciones

## Archivos Generados

Al ejecutar el programa se crearán los siguientes archivos:

### 📊 `dashboard_analytics.png`
- Imagen con todas las visualizaciones generadas
- 9 gráficos diferentes con análisis completo
- Alta resolución (300 DPI)

### 📄 `reporte_analisis.txt`
- Reporte completo en formato texto
- Resumen ejecutivo con métricas clave
- Análisis detallado por categoría, ciudad y método de pago
- Top productos y clientes

### 💾 `datos_dashboard.json`
- Datos procesados en formato JSON
- Listo para usar en aplicaciones web
- Estructura optimizada para visualizaciones

## Ejemplo de Uso

```bash
# Navegar a la carpeta del proyecto
cd C:/Users/dougl/TiendaAurelion

# Ejecutar el programa
python main.py

# Salida esperada:
# 🚀 DASHBOARD ANALYTICS COMERCIAL
# ==================================================
# 📁 Ingrese la ruta del archivo CSV (o presione Enter para usar 'datos_powerbi.csv'): 
# 🔄 Cargando datos...
# ✅ Datos cargados exitosamente: 343 registros, 10 columnas
# 🔍 Validando estructura de datos...
# 📊 Estadísticas básicas:
# ...
# 🎉 ¡Procesamiento completado exitosamente!
```

## Solución de Problemas

### Error: "No se encontró el archivo"
```bash
❌ Error: No se encontró el archivo datos_powerbi.csv
💡 Asegúrate de que el archivo esté en la ruta correcta
```
**Solución:** Verifica que el archivo CSV existe y está en la misma carpeta que `main.py`

### Error: "ModuleNotFoundError"
```bash
❌ ModuleNotFoundError: No module named 'pandas'
```
**Solución:** Instala las dependencias con `pip install pandas matplotlib seaborn numpy`

### Error: "Permission denied"
```bash
❌ PermissionError: [Errno 13] Permission denied
```
**Solución:** Asegúrate de tener permisos de escritura en la carpeta actual

## Características del Programa

### 🔍 Análisis de Datos
- Validación automática de estructura de datos
- Detección de valores nulos y anomalías
- Estadísticas descriptivas completas

### 📈 Visualizaciones
- 9 gráficos diferentes incluyendo:
  - Ventas por categoría (barras verticales)
  - Ventas por ciudad (barras horizontales)
  - Métodos de pago (gráfico de torta)
  - Tendencia temporal (línea con área)
  - Top productos y clientes
  - Análisis temporal por mes y día

### 📋 Reportes
- Resumen ejecutivo con métricas clave
- Análisis detallado por dimensiones
- Identificación de patrones y tendencias
- Exportación en múltiples formatos

### 🎯 Calidad
- Manejo robusto de errores
- Validación exhaustiva de datos
- Generación de archivos consistentes
- Documentación completa

## Personalización

### Modificar Colores de Gráficos
En `main.py`, busca la sección de colores y modifica los valores:
```python
colors = ['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd']  # Cambia estos valores
```

### Ajustar Tamaño de Gráficos
Modifica el parámetro `figsize`:
```python
fig = plt.figure(figsize=(20, 24))  # Ajusta según necesites
```

### Agregar Nuevos Análisis
Extiende la clase `AnalisisVentas` con nuevos métodos:
```python
def mi_nuevo_analisis(self):
    # Tu código de análisis aquí
    pass
```

## Soporte Técnico

Para problemas técnicos o preguntas sobre el código:
1. Verifica que todas las dependencias estén instaladas
2. Asegúrate de que el archivo CSV tenga el formato correcto
3. Comprueba los permisos de escritura en tu sistema
4. Revisa la documentación en `Documentacion_Analytics.md`

## Licencia

Este programa es parte del proyecto Dashboard Analytics Comercial. Uso educativo y comercial permitido.

---
**Versión:** 1.0  
**Última actualización:** 27/10/2024  
**Autor:** Analytics Dashboard Team