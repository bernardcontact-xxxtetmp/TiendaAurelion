#!/usr/bin/env python3
"""
Dashboard Analytics Comercial - Programa Principal
===============================================

Este programa procesa datos de ventas comerciales y genera visualizaciones
interactivas para análisis de negocio.

Autor: Analytics Dashboard Team
Fecha: 27/10/2024
"""

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo para las visualizaciones
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class AnalisisVentas:
    """Clase principal para análisis de datos de ventas"""
    
    def __init__(self, ruta_archivo):
        """
        Inicializa el análisis con el archivo de datos
        
        Args:
            ruta_archivo (str): Ruta al archivo CSV de datos
        """
        self.ruta_archivo = ruta_archivo
        self.df = None
        self.datos_procesados = {}
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga y valida los datos del archivo CSV"""
        try:
            print("🔄 Cargando datos...")
            self.df = pd.read_csv(self.ruta_archivo)
            print(f"✅ Datos cargados exitosamente: {self.df.shape[0]} registros, {self.df.shape[1]} columnas")
            self.validar_datos()
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo {self.ruta_archivo}")
            print("💡 Asegúrate de que el archivo esté en la ruta correcta")
            raise
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
            raise
    
    def validar_datos(self):
        """Valida la estructura y calidad de los datos"""
        print("\n🔍 Validando estructura de datos...")
        
        # Columnas esperadas
        columnas_esperadas = ['fecha', 'id_cliente', 'nombre_cliente_final', 'ciudad', 
                             'id_producto', 'nombre_producto', 'categoria_redefinida', 
                             'cantidad', 'importe', 'medio_pago']
        
        columnas_faltantes = set(columnas_esperadas) - set(self.df.columns)
        if columnas_faltantes:
            print(f"⚠️  Columnas faltantes: {columnas_faltantes}")
        else:
            print("✅ Estructura de columnas correcta")
        
        # Validar tipos de datos
        print(f"📊 Tipos de datos:\n{self.df.dtypes}")
        
        # Verificar valores nulos
        valores_nulos = self.df.isnull().sum()
        if valores_nulos.sum() > 0:
            print(f"⚠️  Valores nulos encontrados:\n{valores_nulos[valores_nulos > 0]}")
        else:
            print("✅ No se encontraron valores nulos")
        
        # Estadísticas básicas
        print(f"\n📈 Estadísticas básicas:")
        print(f"- Período: {self.df['fecha'].min()} a {self.df['fecha'].max()}")
        print(f"- Clientes únicos: {self.df['id_cliente'].nunique()}")
        print(f"- Productos únicos: {self.df['id_producto'].nunique()}")
        print(f"- Ciudades: {self.df['ciudad'].nunique()}")
        print(f"- Categorías: {self.df['categoria_redefinida'].nunique()}")
    
    def procesar_datos(self):
        """Procesa los datos para generar insights"""
        print("\n🔄 Procesando datos...")
        
        # Preparar datos temporales
        self.df['fecha'] = pd.to_datetime(self.df['fecha'])
        self.df['mes'] = self.df['fecha'].dt.month
        self.df['dia_semana'] = self.df['fecha'].dt.day_name()
        self.df['año_mes'] = self.df['fecha'].dt.to_period('M')
        
        # Calcular métricas principales
        resumen = {
            'total_ventas': float(self.df['importe'].sum()),
            'total_cantidad': int(self.df['cantidad'].sum()),
            'total_clientes': int(self.df['id_cliente'].nunique()),
            'total_productos': int(self.df['id_producto'].nunique()),
            'total_transacciones': len(self.df),
            'promedio_venta': float(self.df['importe'].mean()),
            'fecha_inicio': str(self.df['fecha'].min().date()),
            'fecha_fin': str(self.df['fecha'].max().date())
        }
        
        # Ventas por categoría
        ventas_categoria = self.df.groupby('categoria_redefinida').agg({
            'importe': 'sum',
            'cantidad': 'sum'
        }).reset_index().sort_values('importe', ascending=False)
        
        # Ventas por ciudad
        ventas_ciudad = self.df.groupby('ciudad').agg({
            'importe': 'sum',
            'cantidad': 'sum'
        }).reset_index().sort_values('importe', ascending=True)
        
        # Métodos de pago
        ventas_pago = self.df.groupby('medio_pago').agg({
            'importe': 'sum',
            'cantidad': 'sum'
        }).reset_index()
        
        # Serie temporal
        ventas_temporal = self.df.groupby('fecha').agg({
            'importe': 'sum',
            'cantidad': 'sum'
        }).reset_index().sort_values('fecha')
        
        # Top productos
        top_productos = self.df.groupby('nombre_producto').agg({
            'importe': 'sum',
            'cantidad': 'sum'
        }).reset_index().sort_values('importe', ascending=False).head(10)
        
        # Top clientes
        top_clientes = self.df.groupby('nombre_cliente_final').agg({
            'importe': 'sum',
            'cantidad': 'sum'
        }).reset_index().sort_values('importe', ascending=False).head(10)
        
        # Análisis temporal detallado
        ventas_mes = self.df.groupby('mes')['importe'].sum().sort_values(ascending=False)
        ventas_dia_semana = self.df.groupby('dia_semana')['importe'].sum().sort_values(ascending=False)
        
        # Guardar todos los datos procesados
        self.datos_procesados = {
            'resumen': resumen,
            'ventas_categoria': ventas_categoria.to_dict('records'),
            'ventas_ciudad': ventas_ciudad.to_dict('records'),
            'ventas_pago': ventas_pago.to_dict('records'),
            'ventas_temporal': ventas_temporal.to_dict('records'),
            'top_productos': top_productos.to_dict('records'),
            'top_clientes': top_clientes.to_dict('records'),
            'ventas_mes': ventas_mes.to_dict(),
            'ventas_dia_semana': ventas_dia_semana.to_dict()
        }
        
        print("✅ Datos procesados exitosamente")
        self.mostrar_resumen()
    
    def mostrar_resumen(self):
        """Muestra el resumen de métricas principales"""
        resumen = self.datos_procesados['resumen']
        
        print(f"\n📊 RESUMEN EJECUTIVO")
        print(f"{'='*50}")
        print(f"💰 Total de Ventas:    ${resumen['total_ventas']:,.2f}")
        print(f"🛒 Total Transacciones: {resumen['total_transacciones']:,}")
        print(f"👥 Clientes Únicos:     {resumen['total_clientes']:,}")
        print(f"📦 Productos Únicos:    {resumen['total_productos']:,}")
        print(f"💵 Promedio por Venta:  ${resumen['promedio_venta']:,.2f}")
        print(f"📅 Período:            {resumen['fecha_inicio']} a {resumen['fecha_fin']}")
        print(f"{'='*50}")
        
        # Top 5 categorías
        print(f"\n🏆 TOP 5 CATEGORÍAS POR VENTAS:")
        for i, cat in enumerate(self.datos_procesados['ventas_categoria'][:5], 1):
            print(f"{i}. {cat['categoria_redefinida']}: ${cat['importe']:,.2f}")
        
        # Top 3 ciudades
        print(f"\n🌍 TOP 3 CIUDADES POR VENTAS:")
        ciudades = sorted(self.datos_procesados['ventas_ciudad'], 
                         key=lambda x: x['importe'], reverse=True)
        for i, ciudad in enumerate(ciudades[:3], 1):
            print(f"{i}. {ciudad['ciudad']}: ${ciudad['importe']:,.2f}")
        
        # Métodos de pago
        print(f"\n💳 DISTRIBUCIÓN DE PAGOS:")
        for pago in self.datos_procesados['ventas_pago']:
            porcentaje = (pago['importe'] / resumen['total_ventas']) * 100
            print(f"- {pago['medio_pago'].title()}: ${pago['importe']:,.2f} ({porcentaje:.1f}%)")
    
    def generar_visualizaciones(self):
        """Genera visualizaciones básicas con matplotlib"""
        print("\n📊 Generando visualizaciones...")
        
        # Configurar el estilo
        plt.rcParams['figure.facecolor'] = '#f8fafc'
        plt.rcParams['axes.facecolor'] = 'white'
        
        # Crear figura principal con subplots
        fig = plt.figure(figsize=(20, 24))
        fig.suptitle('Dashboard Analytics Comercial - Análisis de Ventas', 
                    fontsize=24, fontweight='bold', y=0.98)
        
        # 1. Ventas por categoría
        ax1 = plt.subplot(3, 3, 1)
        categorias = self.datos_procesados['ventas_categoria']
        cat_names = [cat['categoria_redefinida'] for cat in categorias]
        cat_values = [cat['importe'] for cat in categorias]
        
        bars1 = ax1.bar(range(len(cat_names)), cat_values, 
                       color='#3b82f6', alpha=0.8, edgecolor='white', linewidth=1)
        ax1.set_title('Ventas por Categoría', fontsize=14, fontweight='bold', pad=20)
        ax1.set_ylabel('Ventas (USD)', fontsize=12)
        ax1.set_xticks(range(len(cat_names)))
        ax1.set_xticklabels(cat_names, rotation=45, ha='right', fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Añadir valores en las barras
        for bar, value in zip(bars1, cat_values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'${value:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # 2. Ventas por ciudad
        ax2 = plt.subplot(3, 3, 2)
        ciudades = self.datos_procesados['ventas_ciudad']
        city_names = [city['ciudad'] for city in ciudades]
        city_values = [city['importe'] for city in ciudades]
        
        bars2 = ax2.barh(range(len(city_names)), city_values, 
                        color='#1e3a8a', alpha=0.8, edgecolor='white', linewidth=1)
        ax2.set_title('Ventas por Ciudad', fontsize=14, fontweight='bold', pad=20)
        ax2.set_xlabel('Ventas (USD)', fontsize=12)
        ax2.set_yticks(range(len(city_names)))
        ax2.set_yticklabels(city_names, fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        # Añadir valores en las barras
        for bar, value in zip(bars2, city_values):
            width = bar.get_width()
            ax2.text(width + width*0.01, bar.get_y() + bar.get_height()/2.,
                    f'${value:,.0f}', ha='left', va='center', fontsize=9, fontweight='bold')
        
        # 3. Métodos de pago (gráfico de torta)
        ax3 = plt.subplot(3, 3, 3)
        pagos = self.datos_procesados['ventas_pago']
        pago_labels = [pago['medio_pago'].title() for pago in pagos]
        pago_values = [pago['importe'] for pago in pagos]
        colors = ['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd']
        
        wedges, texts, autotexts = ax3.pie(pago_values, labels=pago_labels, autopct='%1.1f%%',
                                          colors=colors, startangle=90, textprops={'fontsize': 10})
        ax3.set_title('Distribución de Métodos de Pago', fontsize=14, fontweight='bold', pad=20)
        
        # 4. Tendencia temporal
        ax4 = plt.subplot(3, 3, 4)
        temporal = self.datos_procesados['ventas_temporal']
        fechas = [pd.to_datetime(item['fecha']) for item in temporal]
        valores = [item['importe'] for item in temporal]
        
        ax4.plot(fechas, valores, color='#1e3a8a', linewidth=2.5, marker='o', 
                markersize=4, markerfacecolor='#3b82f6', markeredgecolor='white')
        ax4.fill_between(fechas, valores, alpha=0.2, color='#3b82f6')
        ax4.set_title('Tendencia Temporal de Ventas', fontsize=14, fontweight='bold', pad=20)
        ax4.set_ylabel('Ventas Diarias (USD)', fontsize=12)
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3)
        
        # 5. Top 10 productos
        ax5 = plt.subplot(3, 3, 5)
        productos = self.datos_procesados['top_productos']
        prod_names = [prod['nombre_producto'][:20] + '...' if len(prod['nombre_producto']) > 20 
                     else prod['nombre_producto'] for prod in productos]
        prod_values = [prod['importe'] for prod in productos]
        
        bars5 = ax5.barh(range(len(prod_names)), prod_values, 
                        color='#f59e0b', alpha=0.8, edgecolor='white', linewidth=1)
        ax5.set_title('Top 10 Productos Más Vendidos', fontsize=14, fontweight='bold', pad=20)
        ax5.set_xlabel('Ventas (USD)', fontsize=12)
        ax5.set_yticks(range(len(prod_names)))
        ax5.set_yticklabels(prod_names, fontsize=9)
        ax5.grid(True, alpha=0.3)
        
        # 6. Top 10 clientes
        ax6 = plt.subplot(3, 3, 6)
        clientes = self.datos_procesados['top_clientes']
        client_names = [client['nombre_cliente_final'] for client in clientes]
        client_values = [client['importe'] for client in clientes]
        
        bars6 = ax6.barh(range(len(client_names)), client_values, 
                        color='#06b6d4', alpha=0.8, edgecolor='white', linewidth=1)
        ax6.set_title('Top 10 Clientes Más Valiosos', fontsize=14, fontweight='bold', pad=20)
        ax6.set_xlabel('Compras (USD)', fontsize=12)
        ax6.set_yticks(range(len(client_names)))
        ax6.set_yticklabels(client_names, fontsize=9)
        ax6.grid(True, alpha=0.3)
        
        # 7. Ventas por mes
        ax7 = plt.subplot(3, 3, 7)
        ventas_mes = self.datos_procesados['ventas_mes']
        meses = list(ventas_mes.keys())
        valores_mes = list(ventas_mes.values())
        meses_nombres = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
        
        bars7 = ax7.bar(meses, valores_mes, color='#10b981', alpha=0.8, 
                       edgecolor='white', linewidth=1)
        ax7.set_title('Ventas Mensuales', fontsize=14, fontweight='bold', pad=20)
        ax7.set_ylabel('Ventas (USD)', fontsize=12)
        ax7.set_xlabel('Mes', fontsize=12)
        ax7.set_xticklabels(meses_nombres)
        ax7.grid(True, alpha=0.3)
        
        # Añadir valores en las barras
        for bar, value in zip(bars7, valores_mes):
            height = bar.get_height()
            ax7.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'${value:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # 8. Ventas por día de la semana
        ax8 = plt.subplot(3, 3, 8)
        ventas_dia = self.datos_procesados['ventas_dia_semana']
        dias = list(ventas_dia.keys())
        valores_dia = list(ventas_dia.values())
        
        bars8 = ax8.bar(range(len(dias)), valores_dia, color='#8b5cf6', alpha=0.8,
                       edgecolor='white', linewidth=1)
        ax8.set_title('Ventas por Día de la Semana', fontsize=14, fontweight='bold', pad=20)
        ax8.set_ylabel('Ventas (USD)', fontsize=12)
        ax8.set_xticks(range(len(dias)))
        ax8.set_xticklabels(dias, rotation=45, ha='right')
        ax8.grid(True, alpha=0.3)
        
        # 9. Distribución de cantidades
        ax9 = plt.subplot(3, 3, 9)
        cantidades = self.df['cantidad'].value_counts().sort_index()
        ax9.bar(cantidades.index, cantidades.values, color='#ef4444', alpha=0.8,
               edgecolor='white', linewidth=1)
        ax9.set_title('Distribución de Cantidades por Transacción', fontsize=14, fontweight='bold', pad=20)
        ax9.set_xlabel('Cantidad', fontsize=12)
        ax9.set_ylabel('Frecuencia', fontsize=12)
        ax9.grid(True, alpha=0.3)
        
        # Ajustar el layout
        plt.tight_layout()
        plt.subplots_adjust(top=0.95, hspace=0.3, wspace=0.3)
        
        # Guardar la figura
        plt.savefig('dashboard_analytics.png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print("✅ Visualizaciones guardadas en 'dashboard_analytics.png'")
        
        return fig
    
    def exportar_datos_json(self):
        """Exporta los datos procesados a JSON para el dashboard"""
        print("\n💾 Exportando datos a JSON...")
        
        # Asegurar que todos los valores sean serializables
        datos_exportar = {}
        for key, value in self.datos_procesados.items():
            if isinstance(value, dict):
                datos_exportar[key] = {}
                for k, v in value.items():
                    if pd.isna(v):
                        datos_exportar[key][k] = None
                    elif isinstance(v, (np.integer, np.floating)):
                        datos_exportar[key][k] = float(v)
                    else:
                        datos_exportar[key][k] = v
            elif isinstance(value, list):
                datos_exportar[key] = []
                for item in value:
                    if isinstance(item, dict):
                        item_exportar = {}
                        for k, v in item.items():
                            if pd.isna(v):
                                item_exportar[k] = None
                            elif isinstance(v, (np.integer, np.floating)):
                                item_exportar[k] = float(v)
                            else:
                                item_exportar[k] = v
                        datos_exportar[key].append(item_exportar)
                    else:
                        datos_exportar[key].append(item)
            else:
                datos_exportar[key] = value
        
        with open('datos_dashboard.json', 'w', encoding='utf-8') as f:
            json.dump(datos_exportar, f, ensure_ascii=False, indent=2, default=str)
        
        print("✅ Datos exportados a 'datos_dashboard.json'")
    
    def generar_reporte_texto(self):
        """Genera un reporte de análisis en texto plano"""
        print("\n📝 Generando reporte de análisis...")
        
        resumen = self.datos_procesados['resumen']
        
        reporte = f"""
# REPORTE DE ANÁLISIS COMERCIAL
{'='*50}

## RESUMEN EJECUTIVO
- Período de Análisis: {resumen['fecha_inicio']} a {resumen['fecha_fin']}
- Total de Ventas: ${resumen['total_ventas']:,.2f}
- Número de Transacciones: {resumen['total_transacciones']:,}
- Clientes Únicos: {resumen['total_clientes']:,}
- Productos Únicos: {resumen['total_productos']:,}
- Venta Promedio: ${resumen['promedio_venta']:,.2f}

## ANÁLISIS POR CATEGORÍA
{'-'*30}
"""
        
        for i, cat in enumerate(self.datos_procesados['ventas_categoria'], 1):
            porcentaje = (cat['importe'] / resumen['total_ventas']) * 100
            reporte += f"{i}. {cat['categoria_redefinida']}: ${cat['importe']:,.2f} ({porcentaje:.1f}%)\n"
        
        reporte += f"\n## ANÁLISIS GEOGRÁFICO\n{'-'*30}\n"
        ciudades = sorted(self.datos_procesados['ventas_ciudad'], 
                         key=lambda x: x['importe'], reverse=True)
        for i, ciudad in enumerate(ciudades, 1):
            porcentaje = (ciudad['importe'] / resumen['total_ventas']) * 100
            reporte += f"{i}. {ciudad['ciudad']}: ${ciudad['importe']:,.2f} ({porcentaje:.1f}%)\n"
        
        reporte += f"\n## ANÁLISIS DE MÉTODOS DE PAGO\n{'-'*30}\n"
        for pago in self.datos_procesados['ventas_pago']:
            porcentaje = (pago['importe'] / resumen['total_ventas']) * 100
            reporte += f"- {pago['medio_pago'].title()}: ${pago['importe']:,.2f} ({porcentaje:.1f}%)\n"
        
        reporte += f"\n## TOP 5 PRODUCTOS MÁS VENDIDOS\n{'-'*30}\n"
        for i, prod in enumerate(self.datos_procesados['top_productos'][:5], 1):
            reporte += f"{i}. {prod['nombre_producto']}: ${prod['importe']:,.2f}\n"
        
        reporte += f"\n## TOP 5 CLIENTES MÁS VALIOSOS\n{'-'*30}\n"
        for i, client in enumerate(self.datos_procesados['top_clientes'][:5], 1):
            reporte += f"{i}. {client['nombre_cliente_final']}: ${client['importe']:,.2f}\n"
        
        # Análisis temporal
        ventas_mes = self.datos_procesados['ventas_mes']
        mes_max = max(ventas_mes.keys(), key=lambda x: ventas_mes[x])
        meses_nombres = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 
                        4: 'Abril', 5: 'Mayo', 6: 'Junio'}
        
        reporte += f"\n## ANÁLISIS TEMPORAL\n{'-'*30}\n"
        reporte += f"- Mes con mayores ventas: {meses_nombres[int(mes_max)]} (${ventas_mes[mes_max]:,.2f})\n"
        
        ventas_dia = self.datos_procesados['ventas_dia_semana']
        dia_max = max(ventas_dia.keys(), key=lambda x: ventas_dia[x])
        reporte += f"- Día con mayores ventas: {dia_max} (${ventas_dia[dia_max]:,.2f})\n"
        
        reporte += f"\n{'='*50}\n"
        reporte += "Reporte generado automáticamente por Analytics Dashboard\n"
        reporte += f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        with open('reporte_analisis.txt', 'w', encoding='utf-8') as f:
            f.write(reporte)
        
        print("✅ Reporte generado: 'reporte_analisis.txt'")
        return reporte

def main():
    """Función principal del programa"""
    print("🚀 DASHBOARD ANALYTICS COMERCIAL")
    print("="*50)
    print("Procesamiento y análisis de datos de ventas")
    print("Fecha: 27/10/2024")
    print("="*50)
    
    # Solicitar la ruta del archivo
    ruta_archivo = input("\n📁 Ingrese la ruta del archivo CSV (o presione Enter para usar 'datos_powerbi.csv'): ").strip()
    if not ruta_archivo:
        ruta_archivo = 'datos_powerbi.csv'
    
    try:
        # Crear instancia del análisis
        analisis = AnalisisVentas(ruta_archivo)
        
        # Procesar datos
        analisis.procesar_datos()
        
        # Generar visualizaciones
        fig = analisis.generar_visualizaciones()
        
        # Exportar datos JSON
        analisis.exportar_datos_json()
        
        # Generar reporte de texto
        reporte = analisis.generar_reporte_texto()
        
        # Mostrar opciones adicionales
        print(f"\n🎉 ¡Procesamiento completado exitosamente!")
        print(f"📊 Se han generado los siguientes archivos:")
        print(f"   - dashboard_analytics.png (Visualizaciones)")
        print(f"   - datos_dashboard.json (Datos para el dashboard)")
        print(f"   - reporte_analisis.txt (Reporte detallado)")
        
        # Opción de mostrar el gráfico
        mostrar = input("\n¿Desea mostrar las visualizaciones ahora? (s/n): ").lower().strip()
        if mostrar in ['s', 'si', 'yes', 'y']:
            plt.show()
        
        print(f"\n✅ Proceso finalizado. ¡Gracias por usar Analytics Dashboard!")
        
    except Exception as e:
        print(f"\n❌ Error en el procesamiento: {e}")
        print("💡 Por favor, verifique que el archivo CSV existe y tiene el formato correcto.")
        return

if __name__ == "__main__":
    main()