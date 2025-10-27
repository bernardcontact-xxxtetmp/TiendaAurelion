#!/usr/bin/env python3
"""
Ejemplos de Uso - Dashboard Analytics
====================================

Este archivo contiene ejemplos prácticos de cómo usar las funcionalidades
del programa de análisis de ventas.

Autor: Analytics Dashboard Team
Fecha: 27/10/2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json

def ejemplo_basico():
    """Ejemplo básico de carga y análisis de datos"""
    print("📊 EJEMPLO BÁSICO DE ANÁLISIS")
    print("=" * 40)
    
    # Crear datos de ejemplo si no se tiene el archivo CSV
    datos_ejemplo = {
        'fecha': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-02-01', '2024-02-02'],
        'id_cliente': [1, 2, 1, 3, 2],
        'nombre_cliente_final': ['Juan Pérez', 'María García', 'Juan Pérez', 'Carlos López', 'María García'],
        'ciudad': ['Madrid', 'Barcelona', 'Madrid', 'Valencia', 'Barcelona'],
        'id_producto': [101, 102, 101, 103, 102],
        'nombre_producto': ['Producto A', 'Producto B', 'Producto A', 'Producto C', 'Producto B'],
        'categoria_redefinida': ['Electrónicos', 'Hogar', 'Electrónicos', 'Juguetes', 'Hogar'],
        'cantidad': [2, 1, 3, 1, 2],
        'importe': [200.50, 150.00, 300.75, 89.99, 300.00],
        'medio_pago': ['tarjeta', 'efectivo', 'tarjeta', 'qr', 'transferencia']
    }
    
    df = pd.DataFrame(datos_ejemplo)
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    print("Datos de ejemplo creados:")
    print(df.head())
    print(f"\nDimensiones: {df.shape}")
    print(f"Columnas: {list(df.columns)}")
    
    # Análisis básico
    print(f"\n📈 ANÁLISIS BÁSICO:")
    print(f"- Total ventas: ${df['importe'].sum():.2f}")
    print(f"- Venta promedio: ${df['importe'].mean():.2f}")
    print(f"- Clientes únicos: {df['id_cliente'].nunique()}")
    print(f"- Productos únicos: {df['id_producto'].nunique()}")
    
    return df

def ejemplo_visualizacion_basica(df):
    """Ejemplo de creación de visualizaciones básicas"""
    print("\n📊 EJEMPLO DE VISUALIZACIONES BÁSICAS")
    print("=" * 40)
    
    # Configurar estilo
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Análisis de Ventas - Ejemplos Básicos', fontsize=16, fontweight='bold')
    
    # 1. Ventas por categoría
    ventas_cat = df.groupby('categoria_redefinida')['importe'].sum().sort_values(ascending=True)
    axes[0,0].barh(range(len(ventas_cat)), ventas_cat.values, color='skyblue', alpha=0.8)
    axes[0,0].set_yticks(range(len(ventas_cat)))
    axes[0,0].set_yticklabels(ventas_cat.index)
    axes[0,0].set_title('Ventas por Categoría')
    axes[0,0].set_xlabel('Ventas (USD)')
    
    # 2. Distribución por método de pago
    pago_counts = df['medio_pago'].value_counts()
    axes[0,1].pie(pago_counts.values, labels=pago_counts.index, autopct='%1.1f%%', startangle=90)
    axes[0,1].set_title('Distribución de Métodos de Pago')
    
    # 3. Ventas por ciudad
    ventas_ciudad = df.groupby('ciudad')['importe'].sum().sort_values(ascending=False)
    axes[1,0].bar(range(len(ventas_ciudad)), ventas_ciudad.values, color='lightcoral', alpha=0.8)
    axes[1,0].set_xticks(range(len(ventas_ciudad)))
    axes[1,0].set_xticklabels(ventas_ciudad.index, rotation=45)
    axes[1,0].set_title('Ventas por Ciudad')
    axes[1,0].set_ylabel('Ventas (USD)')
    
    # 4. Serie temporal
    ventas_fecha = df.groupby('fecha')['importe'].sum()
    axes[1,1].plot(ventas_fecha.index, ventas_fecha.values, marker='o', linewidth=2, markersize=6)
    axes[1,1].set_title('Evolución Temporal de Ventas')
    axes[1,1].set_xlabel('Fecha')
    axes[1,1].set_ylabel('Ventas (USD)')
    axes[1,1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('ejemplo_visualizaciones.png', dpi=150, bbox_inches='tight')
    print("✅ Visualizaciones guardadas en 'ejemplo_visualizaciones.png'")
    
    return fig

def ejemplo_analisis_avanzado(df):
    """Ejemplo de análisis estadístico avanzado"""
    print("\n📈 EJEMPLO DE ANÁLISIS AVANZADO")
    print("=" * 40)
    
    # Análisis de correlaciones
    print("1. ANÁLISIS DE CORRELACIONES:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        print("Matriz de correlaciones:")
        print(corr_matrix.round(3))
    
    # Análisis de outliers
    print(f"\n2. ANÁLISIS DE OUTLIERS:")
    Q1 = df['importe'].quantile(0.25)
    Q3 = df['importe'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df['importe'] < lower_bound) | (df['importe'] > upper_bound)]
    print(f"- Transacciones consideradas outliers: {len(outliers)}")
    if len(outliers) > 0:
        print("- Outliers encontrados:")
        print(outliers[['fecha', 'nombre_cliente_final', 'importe']].to_string())
    
    # Análisis de tendencias
    print(f"\n3. ANÁLISIS DE TENDENCIAS:")
    df_sorted = df.sort_values('fecha')
    df_sorted['ventas_acumuladas'] = df_sorted['importe'].cumsum()
    
    print("- Ventas acumuladas por fecha:")
    for fecha, acumulado in zip(df_sorted['fecha'], df_sorted['ventas_acumuladas']):
        print(f"  {fecha.strftime('%Y-%m-%d')}: ${acumulado:.2f}")
    
    return df_sorted

def ejemplo_procesamiento_datos(df):
    """Ejemplo de técnicas avanzadas de procesamiento"""
    print("\n🔧 EJEMPLO DE PROCESAMIENTO AVANZADO")
    print("=" * 40)
    
    # Crear métricas calculadas
    df['valor_unitario'] = df['importe'] / df['cantidad']
    df['mes'] = df['fecha'].dt.month
    df['dia_semana'] = df['fecha'].dt.day_name()
    df['es_fin_de_semana'] = df['dia_semana'].isin(['Saturday', 'Sunday'])
    
    # Agregaciones complejas
    print("1. MÉTRICAS POR CLIENTE:")
    metricas_cliente = df.groupby('nombre_cliente_final').agg({
        'importe': ['sum', 'mean', 'count'],
        'cantidad': 'sum',
        'valor_unitario': 'mean'
    }).round(2)
    
    metricas_cliente.columns = ['total_comprado', 'promedio_compra', 'num_transacciones', 
                               'total_unidades', 'precio_promedio_unitario']
    print(metricas_cliente)
    
    # Análisis de cohortes temporal
    print(f"\n2. ANÁLISIS TEMPORAL:")
    ventas_mes = df.groupby(['mes', 'categoria_redefinida'])['importe'].sum().unstack(fill_value=0)
    print("Ventas por mes y categoría:")
    print(ventas_mes)
    
    # Análisis de frecuencia
    print(f"\n3. ANÁLISIS DE FRECUENCIA:")
    frecuencia_clientes = df['nombre_cliente_final'].value_counts()
    print("Frecuencia de compras por cliente:")
    print(frecuencia_clientes)
    
    return df

def ejemplo_exportar_resultados(df):
    """Ejemplo de exportación de resultados en diferentes formatos"""
    print("\n💾 EJEMPLO DE EXPORTACIÓN DE RESULTADOS")
    print("=" * 40)
    
    # Exportar a CSV
    df.to_csv('datos_procesados.csv', index=False, encoding='utf-8')
    print("✅ Datos procesados exportados a 'datos_procesados.csv'")
    
    # Exportar a Excel con múltiples hojas
    with pd.ExcelWriter('reporte_completo.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Datos_Completos', index=False)
        
        # Resumen por categoría
        resumen_cat = df.groupby('categoria_redefinida').agg({
            'importe': ['sum', 'mean', 'count'],
            'cantidad': 'sum'
        }).round(2)
        resumen_cat.to_excel(writer, sheet_name='Resumen_Categorias')
        
        # Resumen por ciudad
        resumen_ciudad = df.groupby('ciudad').agg({
            'importe': ['sum', 'mean', 'count'],
            'cantidad': 'sum'
        }).round(2)
        resumen_ciudad.to_excel(writer, sheet_name='Resumen_Ciudades')
    
    print("✅ Reporte completo exportado a 'reporte_completo.xlsx'")
    
    # Exportar estadísticas a JSON
    estadisticas = {
        'fecha_analisis': datetime.now().isoformat(),
        'total_registros': len(df),
        'período': {
            'inicio': df['fecha'].min().isoformat(),
            'fin': df['fecha'].max().isoformat()
        },
        'métricas_generales': {
            'total_ventas': float(df['importe'].sum()),
            'promedio_venta': float(df['importe'].mean()),
            'maxima_venta': float(df['importe'].max()),
            'minima_venta': float(df['importe'].min()),
            'desviacion_estandar': float(df['importe'].std())
        },
        'categorias': df['categoria_redefinida'].unique().tolist(),
        'ciudades': df['ciudad'].unique().tolist(),
        'metodos_pago': df['medio_pago'].unique().tolist()
    }
    
    with open('estadisticas.json', 'w', encoding='utf-8') as f:
        json.dump(estadisticas, f, indent=2, ensure_ascii=False)
    
    print("✅ Estadísticas exportadas a 'estadisticas.json'")

def ejemplo_automatizacion():
    """Ejemplo de automatización de análisis"""
    print("\n🤖 EJEMPLO DE AUTOMATIZACIÓN")
    print("=" * 40)
    
    def analizar_archivo(ruta_archivo):
        """Función para analizar un archivo automáticamente"""
        try:
            df = pd.read_csv(ruta_archivo)
            print(f"✅ Archivo {ruta_archivo} cargado: {df.shape}")
            
            # Análisis rápido
            resumen = {
                'archivo': ruta_archivo,
                'fecha_analisis': datetime.now().isoformat(),
                'registros': len(df),
                'columnas': list(df.columns),
                'total_ventas': float(df['importe'].sum()) if 'importe' in df.columns else None,
                'clientes_unicos': int(df['id_cliente'].nunique()) if 'id_cliente' in df.columns else None
            }
            
            return resumen
        except Exception as e:
            print(f"❌ Error analizando {ruta_archivo}: {e}")
            return None
    
    # Simular análisis de múltiples archivos
    archivos = ['datos_enero.csv', 'datos_febrero.csv', 'datos_marzo.csv']
    resultados = []
    
    print("Analizando múltiples archivos...")
    for archivo in archivos:
        resultado = analizar_archivo(archivo)
        if resultado:
            resultados.append(resultado)
    
    if resultados:
        print(f"\n📊 RESUMEN DE ANÁLISIS MÚLTIPLES:")
        for resultado in resultados:
            print(f"- {resultado['archivo']}: {resultado['registros']} registros")
        
        # Guardar resultados consolidados
        with open('analisis_multiple.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        print("✅ Resultados guardados en 'analisis_multiple.json'")

def main():
    """Función principal que ejecuta todos los ejemplos"""
    print("🎓 EJEMPLOS DE USO - DASHBOARD ANALYTICS")
    print("=" * 50)
    print("Este script demuestra diversas técnicas de análisis de datos")
    print("Fecha: 27/10/2024")
    print("=" * 50)
    
    # Crear datos de ejemplo
    df = ejemplo_basico()
    
    # Ejemplos de visualización
    fig = ejemplo_visualizacion_basica(df)
    
    # Análisis avanzado
    df_analizado = ejemplo_analisis_avanzado(df)
    
    # Procesamiento avanzado
    df_procesado = ejemplo_procesamiento_datos(df_analizado)
    
    # Exportar resultados
    ejemplo_exportar_resultados(df_procesado)
    
    # Automatización
    ejemplo_automatizacion()
    
    print(f"\n🎉 ¡Todos los ejemplos han sido ejecutados!")
    print("📚 Revisa los archivos generados para ver los resultados")
    print("🔧 Usa estos ejemplos como base para tus propios análisis")

if __name__ == "__main__":
    main()