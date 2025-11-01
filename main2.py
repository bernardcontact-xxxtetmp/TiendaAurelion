#!/usr/bin/env python3
# main.py - entry point for Dashboard Analytics (updated to use utils/data_utils)
import argparse
import logging
import sys
from typing import Optional

from utils.data_utils import DataLoadError, ensure_columns, load_csv_safe

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class DashboardAnalytics:
    def __init__(self, ruta_archivo: str, required_columns: Optional[list] = None):
        self.ruta_archivo = ruta_archivo
        self.df = None
        self.required_columns = required_columns or []

    def validar_datos(self) -> bool:
        """Validate basic schema expectations."""
        if self.df is None:
            logger.error("No data loaded yet.")
            return False
        missing = ensure_columns(self.df, self.required_columns)
        if missing:
            logger.error("CSV missing required columns: %s", missing)
            return False
        if self.df.shape[0] == 0:
            logger.error("CSV has zero rows.")
            return False
        logger.info("Validation OK: %d rows, %d columns", self.df.shape[0], self.df.shape[1])
        return True

    def cargar_datos(self) -> bool:
        """Load and validate CSV safely using data_utils."""
        try:
            logger.info("🔄 Cargando datos desde '%s' ...", self.ruta_archivo)
            self.df = load_csv_safe(self.ruta_archivo, encoding="utf-8", low_memory=False)
            logger.info("✅ Datos cargados exitosamente: %d registros, %d columnas", self.df.shape[0], self.df.shape[1])
            if self.required_columns:
                return self.validar_datos()
            return True
        except FileNotFoundError:
            logger.error("❌ Error: No se encontró el archivo %s", self.ruta_archivo)
            logger.info("💡 Asegúrate de que el archivo esté en la ruta correcta")
            return False
        except DataLoadError as e:
            logger.error("❌ Error cargando datos: %s", e)
            return False
        except Exception as e:
            logger.exception("❌ Error inesperado al cargar datos: %s", e)
            return False


def main(argv=None):
    parser = argparse.ArgumentParser(description="Dashboard Analytics - carga de datos")
    parser.add_argument("csv", nargs="?", default="datos_powerbi.csv", help="Ruta al archivo CSV")
    args = parser.parse_args(argv)

    analytics = DashboardAnalytics(args.csv, required_columns=["fecha", "importe", "id_cliente"])
    if not analytics.cargar_datos():
        logger.error("No se pudo cargar o validar el archivo. Saliendo.")
        sys.exit(1)

    logger.info("Continuando con el procesamiento... (placeholder)")
    # Continue with the rest of the program flow...

if __name__ == "__main__":
    main()