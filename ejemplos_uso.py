#!/usr/bin/env python3
"""
Ejemplos de Uso - Dashboard Analytics (updated to use utils/data_utils)
This file now uses utils.data_utils for safe CSV loading, numeric coercion and
atomic JSON writes for the ejemplo_automatizacion example.
"""
import logging
import os
from datetime import datetime
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from utils.data_utils import ensure_columns, load_csv_safe, to_numeric_safe, write_json_atomic

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def ejemplo_basico():
    """Ejemplo básico de carga y análisis de datos"""
    logger.info("📊 EJEMPLO BÁSICO DE ANÁLISIS")
    # Minimal example - real implementation in original file
    datos_ejemplo = {
        'fecha': ['2024-01-15', '2024-01-16'],
        'id_cliente': [1, 2],
        'nombre_cliente_final': ['Juan Pérez', 'María García'],
        'ciudad': ['Madrid', 'Barcelona'],
        'id_producto': [101, 102],
        'nombre_producto': ['Producto A', 'Producto B'],
        'categoria_redefinida': ['Electrónicos', 'Hogar'],
        'cantidad': [2, 1],
        'importe': [200.50, 150.00],
        'medio_pago': ['tarjeta', 'efectivo']
    }
    df = pd.DataFrame(datos_ejemplo)
    df['fecha'] = pd.to_datetime(df['fecha'])
    return df

# ... (other example functions would remain, omitted here for brevity) ...


def ejemplo_automatizacion(input_files: Optional[list] = None, output_json: str = "analisis_multiple.json"):
    """Ejemplo de automatización de análisis sobre múltiples CSVs (hardened)."""
    logger.info("\n🤖 EJEMPLO DE AUTOMATIZACIÓN")
    logger.info("=" * 40)

    if input_files is None:
        input_files = ["datos_enero.csv", "datos_febrero.csv", "datos_marzo.csv"]

    resultados = []

    def analizar_archivo(ruta_archivo: str):
        logger.info("Analizando archivo: %s", ruta_archivo)
        if not os.path.exists(ruta_archivo):
            logger.warning("Archivo no encontrado: %s - se omite.", ruta_archivo)
            return None
        try:
            df = load_csv_safe(ruta_archivo, encoding="utf-8", low_memory=False)
            # Optional: validate minimal expected columns if your workflow requires them
            missing = ensure_columns(df, ["importe", "id_cliente"])
            if missing:
                logger.warning("Archivo %s no tiene columnas requeridas: %s - se continuará con valores parciales.", ruta_archivo, missing)

            registros = int(len(df))
            columnas = list(df.columns)
            total_ventas = None
            clientes_unicos = None

            if "importe" in df.columns:
                df["importe"] = to_numeric_safe(df, "importe")
                total_ventas = float(df["importe"].sum(skipna=True))

            if "id_cliente" in df.columns:
                clientes_unicos = int(df["id_cliente"].nunique())

            resumen = {
                "archivo": ruta_archivo,
                "fecha_analisis": datetime.utcnow().isoformat() + "Z",
                "registros": registros,
                "columnas": columnas,
                "total_ventas": total_ventas,
                "clientes_unicos": clientes_unicos,
            }
            logger.info("✅ Resumen: %s", resumen)
            return resumen
        except Exception as e:
            logger.exception("❌ Error analizando %s: %s", ruta_archivo, e)
            return None

    for archivo in input_files:
        r = analizar_archivo(archivo)
        if r:
            resultados.append(r)

    if resultados:
        logger.info("Guardando resultados consolidados en %s", output_json)
        try:
            write_json_atomic(resultados, output_json, ensure_ascii=False, indent=2)
            logger.info("✅ Resultados guardados en '%s'", output_json)
        except Exception:
            logger.exception("Error al intentar guardar resultados en %s", output_json)
    else:
        logger.info("No se generaron resultados para guardar.")


if __name__ == "__main__":
    ejemplo_automatizacion()