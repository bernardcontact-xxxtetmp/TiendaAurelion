# main.py – Tienda Aurelion – versión robusta
import pandas as pd
import os
import datetime
import argparse
from unidecode import unidecode

# ----------  colores rápidos  ----------
C = {"v": "\033[92m", "a": "\033[93m", "r": "\033[91m", "b": "\033[94m", "x": "\033[0m"}

# ----------  utilidades  ----------
def normalizar(texto: str) -> str:
    """Normaliza texto para comparaciones."""
    return unidecode(str(texto).lower().strip())

def log_consulta(tipo: str, consulta: str) -> None:
    """Guarda registro de consultas."""
    with open("log_consultas.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} | {tipo} | {consulta}\n")

def safe_col(df: pd.DataFrame, col: str, default="NO DEFINIDO"):
    """Devuelve la columna si existe; sino, una Serie constante."""
    return df[col] if col in df.columns else pd.Series([default] * len(df))

# ----------  enriquecimiento caché  ----------
CACHE_PROD = "data/productos_enriquecido.csv"

def cargar_productos() -> pd.DataFrame:
    """Carga productos con categoría enriquecida (cache)."""
    if os.path.exists(CACHE_PROD):
        print(C["v"] + "Usando cache de productos" + C["x"])
        return pd.read_csv(CACHE_PROD)
    print(C["a"] + "Generando cache de productos..." + C["x"])
    prod = pd.read_csv(os.path.join("data", "productos.csv"))
    prod['categoria'] = prod['nombre_producto'].apply(enriquecer_categoria_por_nombre)
    prod.to_csv(CACHE_PROD, index=False)
    return prod

def enriquecer_categoria_por_nombre(nombre: str) -> str:
    """Reglas de categorización."""
    nombre = normalizar(nombre)
    rules = {
        'bebida': 'BEBIDAS', 'jugo': 'BEBIDAS', 'agua': 'BEBIDAS',
        'cerveza': 'BEBIDAS ALCOHÓLICAS', 'vino': 'BEBIDAS ALCOHÓLICAS',
        'whisky': 'BEBIDAS ALCOHÓLICAS', 'ron': 'BEBIDAS ALCOHÓLICAS',
        'fernet': 'BEBIDAS ALCOHÓLICAS', 'vodka': 'BEBIDAS ALCOHÓLICAS',
        'gin': 'BEBIDAS ALCOHÓLICAS', 'sidra': 'BEBIDAS ALCOHÓLICAS',
        'queso': 'LÁCTEOS', 'yogur': 'LÁCTEOS', 'leche': 'LÁCTEOS',
        'gallet': 'SNACKS', 'papas fritas': 'SNACKS', 'chocolate': 'SNACKS',
        'chicle': 'SNACKS', 'turron': 'SNACKS', 'barrita': 'SNACKS',
        'lavandina': 'LIMPIEZA', 'desengrasante': 'LIMPIEZA',
        'limpiavidrios': 'LIMPIEZA', 'detergente': 'LIMPIEZA',
        'shampoo': 'CUIDADO PERSONAL', 'desodorante': 'CUIDADO PERSONAL',
        'crema dental': 'CUIDADO PERSONAL', 'cepillo': 'CUIDADO PERSONAL',
        'hilo dental': 'CUIDADO PERSONAL', 'mascarilla': 'CUIDADO PERSONAL',
        'pizza': 'CONGELADOS', 'hamburguesa': 'CONGELADOS',
        'empanada': 'CONGELADOS', 'verduras congeladas': 'CONGELADOS',
        'helado': 'CONGELADOS',
        'arroz': 'GRANOS Y CEREALES', 'fideos': 'GRANOS Y CEREALES',
        'lenteja': 'GRANOS Y CEREALES', 'garbanzo': 'GRANOS Y CEREALES',
        'poroto': 'GRANOS Y CEREALES', 'avena': 'GRANOS Y CEREALES',
        'granola': 'GRANOS Y CEREALES', 'harina': 'GRANOS Y CEREALES',
        'azucar': 'GRANOS Y CEREALES', 'sal': 'GRANOS Y CEREALES',
        'aceite': 'GRANOS Y CEREALES',
        'aceituna': 'FRUTAS Y VERDURAS', 'mermelada': 'FRUTAS Y VERDURAS',
        'maní': 'FRUTAS Y VERDURAS', 'mix frutos': 'FRUTAS Y VERDURAS',
        'miel': 'FRUTAS Y VERDURAS',
        'pan': 'PANIFICADOS', 'medialuna': 'PANIFICADOS',
        'yerba': 'ALIMENTOS', 'te': 'ALIMENTOS', 'cafe': 'ALIMENTOS',
        'sopa': 'ALIMENTOS', 'caldo': 'ALIMENTOS',
        'toalla húmeda': 'CUIDADO PERSONAL', 'trapo de piso': 'LIMPIEZA',
        'servilleta': 'HOGAR', 'papel higienico': 'HOGAR',
        'suavizante': 'LIMPIEZA', 'jabon': 'LIMPIEZA',
    }
    for key, cat in rules.items():
        if key in nombre:
            return cat
    return 'OTROS'

# ----------  carga de datos  ----------
def cargar_datos() -> dict:
    """Carga todos los CSV y aplica conversiones/caches."""
    base = "data"
    arch = {
        "clientes": "clientes.csv",
        "ventas": "ventas.csv",
        "detalle": "detalle_ventas.csv",
    }
    dfs = {}
    for k, file in arch.items():
        path = os.path.join(base, file)
        if os.path.exists(path):
            dfs[k] = pd.read_csv(path, encoding='utf-8-sig')
            print(C["v"] + f"✅ Cargado: {path} ({len(dfs[k])} filas)" + C["x"])
        else:
            print(C["r"] + f"⚠️ No encontrado: {path}" + C["x"])
            dfs[k] = pd.DataFrame()
    # fechas
    if not dfs["ventas"].empty:
        dfs["ventas"]['fecha'] = pd.to_datetime(dfs["ventas"]['fecha'], format='%m-%d-%y', errors='coerce')
    if not dfs["clientes"].empty:
        dfs["clientes"]['fecha_alta'] = pd.to_datetime(dfs["clientes"]['fecha_alta'], format='%d-%m-%y', errors='coerce')
        fecha_min = dfs["clientes"]['fecha_alta'].min()
        if pd.isna(fecha_min):
            fecha_min = pd.Timestamp('2023-01-01')
        dfs["clientes"]['fecha_alta'] = dfs["clientes"]['fecha_alta'].fillna(fecha_min)
    dfs["productos"] = cargar_productos()
    return dfs

# ----------  merge  ----------
def fusionar_datos(dfs: dict) -> pd.DataFrame:
    """Devuelve DataFrame único con joins y columnas unificadas."""
    det = dfs["detalle"]
    ven = dfs["ventas"]
    pro = dfs["productos"]
    cli = dfs["clientes"]
    if det.empty or ven.empty:
        print(C["r"] + "❌ Falta detalle o ventas" + C["x"])
        return pd.DataFrame()
    df = (det.merge(ven, on="id_venta", how="left", suffixes=("", "_v"))
            .merge(pro, on="id_producto", how="left", suffixes=("", "_p"))
            .merge(cli, on="id_cliente", how="left", suffixes=("", "_c")))
    df['nombre_cliente_final'] = safe_col(df, 'nombre_cliente')
    df = df.loc[:, ~df.columns.duplicated()]
    return df

# ----------  categoría final  ----------
def mapear_categoria(cat: str) -> str:
    return cat.upper()

EMOJI = {
    "ALIMENTOS": "🍽️", "SNACKS": "🍪", "BEBIDAS": "🥤",
    "BEBIDAS ALCOHÓLICAS": "🍷", "LÁCTEOS": "🧀", "LIMPIEZA": "🧼",
    "HOGAR": "🏠", "PANIFICADOS": "🍞", "CARNES Y EMBUTIDOS": "🥩",
    "FRUTAS Y VERDURAS": "🥗", "GRANOS Y CEREALES": "🌾",
    "CUIDADO PERSONAL": "🧴", "MASCOTAS": "🐾", "CONGELADOS": "❄️",
    "OTROS": "📦"
}

# ----------  limpieza  ----------
def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    if 'categoria' in df.columns:
        df['categoria_redefinida'] = df['categoria'].apply(mapear_categoria)
    else:
        df['categoria_redefinida'] = 'OTROS'
    return df

# ----------  consultas  ----------
def consultar_por_cliente(df: pd.DataFrame) -> None:
    nom = input("Nombre o apellido: ").strip()
    log_consulta("CLIENTE", nom)
    mask = df['nombre_cliente_final'].astype(str).apply(normalizar).str.contains(normalizar(nom), na=False)
    out = df[mask].head(50)   # top 50
    print(f"Coincidencias: {len(out)}")
    print(out)
    input("\nENTER para volver...")

def consultar_por_ciudad(df: pd.DataFrame) -> None:
    if 'ciudad' not in df.columns:
        print(C["r"] + "⚠️ Sin datos de ciudad" + C["x"])
        input()
        return
    ciud = sorted(df['ciudad'].dropna().unique())
    for i, c in enumerate(ciud, 1):
        print(f"{i}. {c}")
    try:
        ciu = ciud[int(input("Nº: ")) - 1]
    except:
        print(C["r"] + "❌ Opción inválida" + C["x"])
        input()
        return
    log_consulta("CIUDAD", ciu)
    print(df[df['ciudad'].astype(str).apply(normalizar) == normalizar(ciu)].head(50))
    input("\nENTER...")

def consultar_por_categoria(df: pd.DataFrame) -> None:
    if 'categoria_redefinida' not in df.columns:
        print(C["r"] + "⚠️ Sin categorías" + C["x"])
        input()
        return
    cats = sorted(df['categoria_redefinida'].dropna().unique())
    for i, c in enumerate(cats, 1):
        print(f"{i}. {EMOJI.get(c, '')} {c}")
    try:
        cat = cats[int(input("Nº: ")) - 1]
    except:
        print(C["r"] + "❌ Opción inválida" + C["x"])
        input()
        return
    log_consulta("CATEGORÍA", cat)
    print(df[df['categoria_redefinida'] == cat].head(50))
    input("\nENTER...")

def resumen_por_cliente(df: pd.DataFrame) -> None:
    nom = input("Nombre cliente: ").strip()
    log_consulta("RESUMEN", nom)
    mask = df['nombre_cliente_final'].astype(str).apply(normalizar).str.contains(normalizar(nom), na=False)
    sub = df[mask]
    if sub.empty:
        print(C["r"] + "❌ Sin datos" + C["x"])
        input()
        return
    res = (sub.groupby('nombre_producto')
             .agg(total_cant=('cantidad', 'sum'),
                  total_pesos=('importe', 'sum'))
             .sort_values('total_pesos', ascending=False))
    pd.options.display.float_format = "${:,.0f}".format
    print(res.head(10))
    input("\nENTER...")

# ----------  export  ----------
def exportar_datos_limpios(df: pd.DataFrame, comprimir: bool = False) -> None:
    """Exporta CSV listo para Power-BI (opcionalmente comprimido)."""
    cols = ['fecha', 'id_cliente', 'nombre_cliente_final', 'ciudad',
            'id_producto', 'nombre_producto', 'categoria_redefinida',
            'cantidad', 'importe', 'medio_pago']
    cols = [c for c in cols if c in df.columns]
    archivo = "datos_powerbi.csv" + (".gz" if comprimir else "")
    df[cols].to_csv(archivo, index=False, encoding='utf-8-sig', compression='gzip' if comprimir else None)
    print(C["v"] + f"✅ Exportado: {archivo}" + C["x"])
    input("\nENTER...")

# ----------  menú  ----------
def mostrar_menu() -> None:
    print("\n🛒  TIENDA AURELION – CONSULTAS")
    print("1. Por cliente")
    print("2. Por ciudad")
    print("3. Por categoría")
    print("4. Salir")
    print("5. Exportar CSV")
    print("6. Resumen por cliente")

# ----------  main  ----------
def main() -> None:
    parser = argparse.ArgumentParser(description="Tienda Aurelion – consultas y export")
    parser.add_argument("--export", action="store_true", help="Exporta CSV y sale")
    parser.add_argument("--gzip", action="store_true", help="Comprime el CSV")
    args = parser.parse_args()

    dfs = cargar_datos()
    datos_raw = fusionar_datos(dfs)
    if datos_raw.empty:
        print(C["r"] + "⛔ Sin datos para trabajar" + C["x"])
        exit()
    datos = limpiar_datos(datos_raw)

    if args.export:
        exportar_datos_limpios(datos, comprimir=args.gzip)
        exit()

    while True:
        mostrar_menu()
        try:
            op = int(input("Opción (1-6): ").strip())
        except ValueError:
            print(C["r"] + "❌ Número válido, por favor" + C["x"])
            continue
        if op == 1:
            consultar_por_cliente(datos)
        elif op == 2:
            consultar_por_ciudad(datos)
        elif op == 3:
            consultar_por_categoria(datos)
        elif op == 4:
            print(C["b"] + "👋 Hasta pronto" + C["x"])
            break
        elif op == 5:
            exportar_datos_limpios(datos, comprimir=False)
        elif op == 6:
            resumen_por_cliente(datos)
        else:
            print(C["r"] + "❌ Opción 1-6" + C["x"])

if __name__ == "__main__":
    main()# main.py – Tienda Aurelion – versión robusta
import pandas as pd
import os
import datetime
import argparse
from unidecode import unidecode

# ----------  colores rápidos  ----------
C = {"v": "\033[92m", "a": "\033[93m", "r": "\033[91m", "b": "\033[94m", "x": "\033[0m"}

# ----------  utilidades  ----------
def normalizar(texto: str) -> str:
    """Normaliza texto para comparaciones."""
    return unidecode(str(texto).lower().strip())

def log_consulta(tipo: str, consulta: str) -> None:
    """Guarda registro de consultas."""
    with open("log_consultas.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} | {tipo} | {consulta}\n")

def safe_col(df: pd.DataFrame, col: str, default="NO DEFINIDO"):
    """Devuelve la columna si existe; sino, una Serie constante."""
    return df[col] if col in df.columns else pd.Series([default] * len(df))

# ----------  enriquecimiento caché  ----------
CACHE_PROD = "data/productos_enriquecido.csv"

def cargar_productos() -> pd.DataFrame:
    """Carga productos con categoría enriquecida (cache)."""
    if os.path.exists(CACHE_PROD):
        print(C["v"] + "Usando cache de productos" + C["x"])
        return pd.read_csv(CACHE_PROD)
    print(C["a"] + "Generando cache de productos..." + C["x"])
    prod = pd.read_csv(os.path.join("data", "productos.csv"))
    prod['categoria'] = prod['nombre_producto'].apply(enriquecer_categoria_por_nombre)
    prod.to_csv(CACHE_PROD, index=False)
    return prod

def enriquecer_categoria_por_nombre(nombre: str) -> str:
    """Reglas de categorización."""
    nombre = normalizar(nombre)
    rules = {
        'bebida': 'BEBIDAS', 'jugo': 'BEBIDAS', 'agua': 'BEBIDAS',
        'cerveza': 'BEBIDAS ALCOHÓLICAS', 'vino': 'BEBIDAS ALCOHÓLICAS',
        'whisky': 'BEBIDAS ALCOHÓLICAS', 'ron': 'BEBIDAS ALCOHÓLICAS',
        'fernet': 'BEBIDAS ALCOHÓLICAS', 'vodka': 'BEBIDAS ALCOHÓLICAS',
        'gin': 'BEBIDAS ALCOHÓLICAS', 'sidra': 'BEBIDAS ALCOHÓLICAS',
        'queso': 'LÁCTEOS', 'yogur': 'LÁCTEOS', 'leche': 'LÁCTEOS',
        'gallet': 'SNACKS', 'papas fritas': 'SNACKS', 'chocolate': 'SNACKS',
        'chicle': 'SNACKS', 'turron': 'SNACKS', 'barrita': 'SNACKS',
        'lavandina': 'LIMPIEZA', 'desengrasante': 'LIMPIEZA',
        'limpiavidrios': 'LIMPIEZA', 'detergente': 'LIMPIEZA',
        'shampoo': 'CUIDADO PERSONAL', 'desodorante': 'CUIDADO PERSONAL',
        'crema dental': 'CUIDADO PERSONAL', 'cepillo': 'CUIDADO PERSONAL',
        'hilo dental': 'CUIDADO PERSONAL', 'mascarilla': 'CUIDADO PERSONAL',
        'pizza': 'CONGELADOS', 'hamburguesa': 'CONGELADOS',
        'empanada': 'CONGELADOS', 'verduras congeladas': 'CONGELADOS',
        'helado': 'CONGELADOS',
        'arroz': 'GRANOS Y CEREALES', 'fideos': 'GRANOS Y CEREALES',
        'lenteja': 'GRANOS Y CEREALES', 'garbanzo': 'GRANOS Y CEREALES',
        'poroto': 'GRANOS Y CEREALES', 'avena': 'GRANOS Y CEREALES',
        'granola': 'GRANOS Y CEREALES', 'harina': 'GRANOS Y CEREALES',
        'azucar': 'GRANOS Y CEREALES', 'sal': 'GRANOS Y CEREALES',
        'aceite': 'GRANOS Y CEREALES',
        'aceituna': 'FRUTAS Y VERDURAS', 'mermelada': 'FRUTAS Y VERDURAS',
        'maní': 'FRUTAS Y VERDURAS', 'mix frutos': 'FRUTAS Y VERDURAS',
        'miel': 'FRUTAS Y VERDURAS',
        'pan': 'PANIFICADOS', 'medialuna': 'PANIFICADOS',
        'yerba': 'ALIMENTOS', 'te': 'ALIMENTOS', 'cafe': 'ALIMENTOS',
        'sopa': 'ALIMENTOS', 'caldo': 'ALIMENTOS',
        'toalla húmeda': 'CUIDADO PERSONAL', 'trapo de piso': 'LIMPIEZA',
        'servilleta': 'HOGAR', 'papel higienico': 'HOGAR',
        'suavizante': 'LIMPIEZA', 'jabon': 'LIMPIEZA',
    }
    for key, cat in rules.items():
        if key in nombre:
            return cat
    return 'OTROS'

# ----------  carga de datos  ----------
def cargar_datos() -> dict:
    """Carga todos los CSV y aplica conversiones/caches."""
    base = "data"
    arch = {
        "clientes": "clientes.csv",
        "ventas": "ventas.csv",
        "detalle": "detalle_ventas.csv",
    }
    dfs = {}
    for k, file in arch.items():
        path = os.path.join(base, file)
        if os.path.exists(path):
            dfs[k] = pd.read_csv(path, encoding='utf-8-sig')
            print(C["v"] + f"✅ Cargado: {path} ({len(dfs[k])} filas)" + C["x"])
        else:
            print(C["r"] + f"⚠️ No encontrado: {path}" + C["x"])
            dfs[k] = pd.DataFrame()
    # fechas
    if not dfs["ventas"].empty:
        dfs["ventas"]['fecha'] = pd.to_datetime(dfs["ventas"]['fecha'], format='%m-%d-%y', errors='coerce')
    if not dfs["clientes"].empty:
        dfs["clientes"]['fecha_alta'] = pd.to_datetime(dfs["clientes"]['fecha_alta'], format='%d-%m-%y', errors='coerce')
        fecha_min = dfs["clientes"]['fecha_alta'].min()
        if pd.isna(fecha_min):
            fecha_min = pd.Timestamp('2023-01-01')
        dfs["clientes"]['fecha_alta'] = dfs["clientes"]['fecha_alta'].fillna(fecha_min)
    dfs["productos"] = cargar_productos()
    return dfs

# ----------  merge  ----------
def fusionar_datos(dfs: dict) -> pd.DataFrame:
    """Devuelve DataFrame único con joins y columnas unificadas."""
    det = dfs["detalle"]
    ven = dfs["ventas"]
    pro = dfs["productos"]
    cli = dfs["clientes"]
    if det.empty or ven.empty:
        print(C["r"] + "❌ Falta detalle o ventas" + C["x"])
        return pd.DataFrame()
    df = (det.merge(ven, on="id_venta", how="left", suffixes=("", "_v"))
            .merge(pro, on="id_producto", how="left", suffixes=("", "_p"))
            .merge(cli, on="id_cliente", how="left", suffixes=("", "_c")))
    df['nombre_cliente_final'] = safe_col(df, 'nombre_cliente')
    df = df.loc[:, ~df.columns.duplicated()]
    return df

# ----------  categoría final  ----------
def mapear_categoria(cat: str) -> str:
    return cat.upper()

EMOJI = {
    "ALIMENTOS": "🍽️", "SNACKS": "🍪", "BEBIDAS": "🥤",
    "BEBIDAS ALCOHÓLICAS": "🍷", "LÁCTEOS": "🧀", "LIMPIEZA": "🧼",
    "HOGAR": "🏠", "PANIFICADOS": "🍞", "CARNES Y EMBUTIDOS": "🥩",
    "FRUTAS Y VERDURAS": "🥗", "GRANOS Y CEREALES": "🌾",
    "CUIDADO PERSONAL": "🧴", "MASCOTAS": "🐾", "CONGELADOS": "❄️",
    "OTROS": "📦"
}

# ----------  limpieza  ----------
def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    if 'categoria' in df.columns:
        df['categoria_redefinida'] = df['categoria'].apply(mapear_categoria)
    else:
        df['categoria_redefinida'] = 'OTROS'
    return df

# ----------  consultas  ----------
def consultar_por_cliente(df: pd.DataFrame) -> None:
    nom = input("Nombre o apellido: ").strip()
    log_consulta("CLIENTE", nom)
    mask = df['nombre_cliente_final'].astype(str).apply(normalizar).str.contains(normalizar(nom), na=False)
    out = df[mask].head(50)   # top 50
    print(f"Coincidencias: {len(out)}")
    print(out)
    input("\nENTER para volver...")

def consultar_por_ciudad(df: pd.DataFrame) -> None:
    if 'ciudad' not in df.columns:
        print(C["r"] + "⚠️ Sin datos de ciudad" + C["x"])
        input()
        return
    ciud = sorted(df['ciudad'].dropna().unique())
    for i, c in enumerate(ciud, 1):
        print(f"{i}. {c}")
    try:
        ciu = ciud[int(input("Nº: ")) - 1]
    except:
        print(C["r"] + "❌ Opción inválida" + C["x"])
        input()
        return
    log_consulta("CIUDAD", ciu)
    print(df[df['ciudad'].astype(str).apply(normalizar) == normalizar(ciu)].head(50))
    input("\nENTER...")

def consultar_por_categoria(df: pd.DataFrame) -> None:
    if 'categoria_redefinida' not in df.columns:
        print(C["r"] + "⚠️ Sin categorías" + C["x"])
        input()
        return
    cats = sorted(df['categoria_redefinida'].dropna().unique())
    for i, c in enumerate(cats, 1):
        print(f"{i}. {EMOJI.get(c, '')} {c}")
    try:
        cat = cats[int(input("Nº: ")) - 1]
    except:
        print(C["r"] + "❌ Opción inválida" + C["x"])
        input()
        return
    log_consulta("CATEGORÍA", cat)
    print(df[df['categoria_redefinida'] == cat].head(50))
    input("\nENTER...")

def resumen_por_cliente(df: pd.DataFrame) -> None:
    nom = input("Nombre cliente: ").strip()
    log_consulta("RESUMEN", nom)
    mask = df['nombre_cliente_final'].astype(str).apply(normalizar).str.contains(normalizar(nom), na=False)
    sub = df[mask]
    if sub.empty:
        print(C["r"] + "❌ Sin datos" + C["x"])
        input()
        return
    res = (sub.groupby('nombre_producto')
             .agg(total_cant=('cantidad', 'sum'),
                  total_pesos=('importe', 'sum'))
             .sort_values('total_pesos', ascending=False))
    pd.options.display.float_format = "${:,.0f}".format
    print(res.head(10))
    input("\nENTER...")

# ----------  export  ----------
def exportar_datos_limpios(df: pd.DataFrame, comprimir: bool = False) -> None:
    """Exporta CSV listo para Power-BI (opcionalmente comprimido)."""
    cols = ['fecha', 'id_cliente', 'nombre_cliente_final', 'ciudad',
            'id_producto', 'nombre_producto', 'categoria_redefinida',
            'cantidad', 'importe', 'medio_pago']
    cols = [c for c in cols if c in df.columns]
    archivo = "datos_powerbi.csv" + (".gz" if comprimir else "")
    df[cols].to_csv(archivo, index=False, encoding='utf-8-sig', compression='gzip' if comprimir else None)
    print(C["v"] + f"✅ Exportado: {archivo}" + C["x"])
    input("\nENTER...")

# ----------  menú  ----------
def mostrar_menu() -> None:
    print("\n🛒  TIENDA AURELION – CONSULTAS")
    print("1. Por cliente")
    print("2. Por ciudad")
    print("3. Por categoría")
    print("4. Salir")
    print("5. Exportar CSV")
    print("6. Resumen por cliente")

# ----------  main  ----------
def main() -> None:
    parser = argparse.ArgumentParser(description="Tienda Aurelion – consultas y export")
    parser.add_argument("--export", action="store_true", help="Exporta CSV y sale")
    parser.add_argument("--gzip", action="store_true", help="Comprime el CSV")
    args = parser.parse_args()

    dfs = cargar_datos()
    datos_raw = fusionar_datos(dfs)
    if datos_raw.empty:
        print(C["r"] + "⛔ Sin datos para trabajar" + C["x"])
        exit()
    datos = limpiar_datos(datos_raw)

    if args.export:
        exportar_datos_limpios(datos, comprimir=args.gzip)
        exit()

    while True:
        mostrar_menu()
        try:
            op = int(input("Opción (1-6): ").strip())
        except ValueError:
            print(C["r"] + "❌ Número válido, por favor" + C["x"])
            continue
        if op == 1:
            consultar_por_cliente(datos)
        elif op == 2:
            consultar_por_ciudad(datos)
        elif op == 3:
            consultar_por_categoria(datos)
        elif op == 4:
            print(C["b"] + "👋 Hasta pronto" + C["x"])
            break
        elif op == 5:
            exportar_datos_limpios(datos, comprimir=False)
        elif op == 6:
            resumen_por_cliente(datos)
        else:
            print(C["r"] + "❌ Opción 1-6" + C["x"])

if __name__ == "__main__":
    main()