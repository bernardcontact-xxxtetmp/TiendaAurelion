# 🛒 Tienda Aurelion — Sistema de Consulta de Ventas

**Entrega final para Guayerd & IBM SkillsBuild**  
Versión interactiva, funcional y empaquetada como `.exe`  
Base de datos brindada: `clientes.csv`, `productos.csv`, `ventas.csv`, `detalle_ventas.csv`

---

## 1️⃣ Tema, problema y solución

### 🎯 Tema
Desarrollo de un sistema en Python para consultar ventas, productos y clientes desde archivos CSV, vinculado a una base de datos comercial.

### ❗ Problema
Los datos estaban distribuidos en múltiples archivos sin limpieza ni categorización clara, dificultando el análisis por cliente, ciudad o tipo de producto.

### ✅ Solución
Se creó un programa que:
- Limpia y normaliza los datos
- Recategoriza productos automáticamente
- Une las tablas en una vista completa
- Permite consultas interactivas por cliente, ciudad y categoría
- Funciona como script o como `.exe` sin errores

---

## 2️⃣ Fuente, definición, estructura, tipos y escala

### 📌 Fuente
Base de datos brindada por el equipo:  
- `clientes.csv`  
- `productos.csv`  
- `ventas.csv`  
- `detalle_ventas.csv`

### 🧱 Estructura
- `clientes`: ID, nombre, ciudad, fecha de alta  
- `productos`: ID, nombre, categoría original  
- `ventas`: ID, cliente, fecha, medio de pago  
- `detalle_ventas`: ID venta, producto, cantidad, importe

### 🧬 Tipos
- Identificadores numéricos  
- Texto (nombres, ciudades, categorías)  
- Fechas (formato Excel y texto)  
- Valores monetarios

### 📏 Escala
- Datos simulados para cientos de registros  
- Preparado para escalar a miles de ventas y productos

---

## 3️⃣ Pasos, pseudocódigo y diagrama

### 🔄 Pasos
1. Cargar los CSV
2. Limpiar duplicados y nulos
3. Convertir fechas
4. Recategorizar productos por nombre
5. Unir tablas en una vista completa
6. Crear menú interactivo con 5 opciones

### 🧾 Pseudocódigo
INICIO Cargar CSVs desde carpeta /data Limpiar datos y convertir fechas Recategorizar productos Unir tablas por ID Mostrar menú: 1 → Consultar por cliente 2 → Consultar por ciudad 3 → Consultar por categoría 4 → Mostrar productos por categoría 5 → Salir FIN


### 📊 Diagrama lógico
[clientes] ← ventas → [detalle_ventas] ← productos ↓ Consulta interactiva por cliente / ciudad / categoría ↓ Salida en consola con totales y productos


---

## 4️⃣ Sugerencias de Copilot aceptadas y descartadas

### ✅ Aceptadas
- Uso de `os.path.dirname(sys.executable)` para rutas en `.exe`
- Recategorización automática por palabras clave
- Menú interactivo con `input()` y validación
- Mensaje de salida personalizado

### ❌ Descartadas
- Uso de `sys._MEIPASS` (menos confiable en `.exe`)
- Agrupación por categoría original (se redefinió simbólicamente)
- Interfaz gráfica (se priorizó consola por simplicidad)

---

## 5️⃣ Programa en Python interactivo

Archivo: `main.py`  
- Limpieza de datos  
- Recategorización avanzada  
- Uniones entre tablas  
- Menú interactivo con 5 opciones  
- Compatible con `.exe` gracias a rutas absolutas

---

## 6️⃣ Ejecutable funcional

Archivo: `TiendaAurelion.exe`  
- Generado con PyInstaller  
- Funciona sin errores si la carpeta `data/` está junto a él  
- Prueba desde PowerShell:

```bash
cd C:\Users\dougl\EntregaFinal_TiendaAurelion
.\TiendaAurelion.exe

