import pandas as pd
from datetime import datetime
import os
import sys

# Detectar si se ejecuta como .exe (PyInstaller)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta segura a la carpeta de datos
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Función para convertir fechas desde formato Excel o texto
def convertir_fecha(valor):
    try:
        return datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(valor) - 2)
    except:
        return pd.to_datetime(valor, errors='coerce')

# Cargar los archivos CSV desde la carpeta 'data'
clientes = pd.read_csv(os.path.join(DATA_DIR, 'clientes.csv'), encoding='utf-8')
productos = pd.read_csv(os.path.join(DATA_DIR, 'productos.csv'), encoding='utf-8')
ventas = pd.read_csv(os.path.join(DATA_DIR, 'ventas.csv'), encoding='utf-8')
detalle_ventas = pd.read_csv(os.path.join(DATA_DIR, 'detalle_ventas.csv'), encoding='utf-8')

# Renombrar columnas clave antes de limpiar
clientes.rename(columns={'nombre': 'nombre_cliente'}, inplace=True)
productos.rename(columns={'nombre': 'nombre_producto'}, inplace=True)

# Limpieza de datos
clientes.drop_duplicates(inplace=True)
productos.drop_duplicates(inplace=True)
ventas.drop_duplicates(inplace=True)
detalle_ventas.drop_duplicates(inplace=True)

clientes.dropna(subset=['id_cliente', 'nombre_cliente'], inplace=True)
productos.dropna(subset=['id_producto', 'nombre_producto'], inplace=True)
ventas.dropna(subset=['id_venta', 'id_cliente', 'fecha'], inplace=True)
detalle_ventas.dropna(subset=['id_venta', 'id_producto', 'cantidad', 'importe'], inplace=True)

clientes.reset_index(drop=True, inplace=True)
productos.reset_index(drop=True, inplace=True)
ventas.reset_index(drop=True, inplace=True)
detalle_ventas.reset_index(drop=True, inplace=True)

# Convertir fechas
ventas['fecha'] = ventas['fecha'].apply(convertir_fecha)
clientes['fecha_alta'] = clientes['fecha_alta'].apply(convertir_fecha)

# Recategorizar productos según nombre
def recategorizar_producto(nombre):
    nombre = str(nombre).lower()
    if any(x in nombre for x in ['pan', 'arroz', 'fideos', 'harina', 'azúcar', 'sal', 'lentejas', 'garbanzos', 'porotos']):
        return 'Almacén y secos'
    elif any(x in nombre for x in ['leche', 'yogur', 'queso', 'manteca', 'crema']):
        return 'Lácteos y quesos'
    elif any(x in nombre for x in ['coca', 'pepsi', 'sprite', 'fanta', 'agua', 'energética', 'mate', 'café', 'té']):
        return 'Bebidas'
    elif any(x in nombre for x in ['cerveza', 'vino', 'sidra', 'fernet', 'vodka', 'ron', 'gin', 'whisky', 'licor']):
        return 'Bebidas alcohólicas'
    elif any(x in nombre for x in ['jugo', 'jugo en polvo']):
        return 'Jugos y concentrados'
    elif any(x in nombre for x in ['galletita', 'alfajor', 'papas fritas', 'maní', 'mix', 'chocolate', 'turrón', 'caramelo', 'chicle', 'chupetín']):
        return 'Snacks y golosinas'
    elif any(x in nombre for x in ['shampoo', 'jabón', 'crema dental', 'desodorante', 'cepillo', 'hilo dental', 'mascarilla']):
        return 'Cuidado personal'
    elif any(x in nombre for x in ['detergente', 'lavandina', 'suavizante', 'limpiavidrios', 'desengrasante']):
        return 'Limpieza'
    elif any(x in nombre for x in ['papel higiénico', 'servilleta', 'toalla húmeda', 'esponja', 'trapo']):
        return 'Higiene del hogar'
    elif any(x in nombre for x in ['pizza', 'empanada', 'hamburguesa', 'helado', 'verduras congeladas']):
        return 'Congelados'
    elif any(x in nombre for x in ['aceite', 'vinagre', 'salsa', 'caldo', 'sopa', 'miel', 'stevia', 'granola', 'avena', 'aceituna']):
        return 'Conservas y condimentos'
    else:
        return 'Otros'

# Aplicar recategorización
productos['categoria_redefinida'] = productos['nombre_producto'].apply(recategorizar_producto)

# Unir tablas
ventas_clientes = ventas.merge(clientes, on='id_cliente')
detalle_productos = detalle_ventas.merge(productos, on='id_producto')
datos_completos = detalle_productos.merge(ventas_clientes, on='id_venta')

# Agrupar productos por categoría redefinida
productos_por_categoria = productos.groupby('categoria_redefinida')['nombre_producto'].apply(list).to_dict()

# Función: consultar ventas por ciudad
def consultar_por_ciudad(ciudad):
    filtrado = datos_completos[datos_completos['ciudad'].str.lower() == ciudad.lower()]
    if filtrado.empty:
        print(f"\nNo se encontraron ventas en la ciudad '{ciudad}'.")
    else:
        print(f"\nVentas en {ciudad}:")
        print(filtrado[['nombre_cliente', 'nombre_producto', 'cantidad', 'importe']].head())
        print(f"Total vendido: ₡{filtrado['importe'].sum():,.2f}")

# Función: consultar productos comprados por cliente
def consultar_por_cliente(nombre):
    filtrado = datos_completos[datos_completos['nombre_cliente'].str.lower().str.contains(nombre.lower())]
    if filtrado.empty:
        print(f"\nNo se encontraron compras para el cliente '{nombre}'.")
    else:
        print(f"\nCompras de {nombre}:")
        print(filtrado[['nombre_cliente', 'nombre_producto', 'cantidad', 'importe']].head())
        print(f"Total gastado: ₡{filtrado['importe'].sum():,.2f}")

# Función: consultar ventas por categoría redefinida
def consultar_por_categoria(categoria):
    if 'categoria_redefinida' not in datos_completos.columns:
        print("⚠️ La columna 'categoria_redefinida' no está disponible en los datos.")
        return
    filtrado = datos_completos[datos_completos['categoria_redefinida'].str.lower().str.contains(categoria.lower())]
    if filtrado.empty:
        print(f"\nNo se encontraron ventas en la categoría '{categoria}'.")
    else:
        print(f"\nVentas en la categoría '{categoria}':")
        print(filtrado[['nombre_producto', 'categoria_redefinida', 'cantidad', 'importe']].head())
        print(f"Total vendido en esta categoría: ₡{filtrado['importe'].sum():,.2f}")

# Función: mostrar productos por categoría redefinida
def mostrar_productos_por_categoria():
    print("\n📦 Productos disponibles por categoría:")
    for categoria, lista_productos in productos_por_categoria.items():
        print(f"\n🗂️ {categoria}:")
        for producto in lista_productos:
            print(f"  - {producto}")

# Interfaz principal con bucle y salida personalizada
if __name__ == "__main__":
    mensaje_salida = "Gracias por usar el sistema Tienda Aurelion. Que tus ventas sean abundantes y tus datos limpios."

    while True:
        print("\n🛒 SISTEMA DE CONSULTA DE VENTAS — TIENDA AURELION")
        print("1. Consultar por cliente")
        print("2. Consultar por ciudad")
        print("3. Consultar por categoría de producto")
        print("4. Mostrar productos por categoría")
        print("5. Salir del sistema")
        opcion = input("Seleccione una opción (1, 2, 3, 4 o 5): ")

        if opcion == "1":
            cliente = input("Ingrese el nombre del cliente: ")
            consultar_por_cliente(cliente)
        elif opcion == "2":
            ciudad = input("Ingrese el nombre de la ciudad: ")
            consultar_por_ciudad(ciudad)
        elif opcion == "3":
            categoria = input("Ingrese la categoría del producto: ")
            consultar_por_categoria(categoria)
        elif opcion == "4":
            mostrar_productos_por_categoria()
        elif opcion == "5":
            print(f"\n🧾 {mensaje_salida}")
            break
        else:
            print("Opción no válida. Intente de nuevo.")