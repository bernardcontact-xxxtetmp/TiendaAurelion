USO.md — Guía rápida de ejecución
Este documento acompaña el proyecto Tienda Aurelion, brindando instrucciones prácticas para instalar, ejecutar y probar el sistema interactivo de consultas de ventas.

Requisitos
- Python 3.13 instalado (solo si vas a ejecutar el script .py)
- Librería pandas instalada:
pip install pandas
- Carpeta data/ con los siguientes archivos:
- clientes.csv
- productos.csv
- ventas.csv
- detalle_ventas.csv

Ejecución como script
- Abre PowerShell o terminal
- Navega a la carpeta del proyecto:
cd C:\Users\dougl\TiendaAurelion
- Ejecuta el script:
python main.py



Ejecución como .exe
- Asegúrate de tener esta estructura:
dist/
├── TiendaAurelion.exe
├── data/
│   ├── clientes.csv
│   ├── productos.csv
│   ├── ventas.csv
│   └── detalle_ventas.csv


- Abre PowerShell y navega a la carpeta dist:
cd C:\Users\dougl\TiendaAurelion\dist
- Ejecuta el programa:
.\TiendaAurelion.exe
Opciones del menú1. Consultar por cliente
2. Consultar por ciudad
3. Consultar por categoría de producto
4. Mostrar productos por categoría
5. Salir del sistema
Mensaje de cierreEl sistema finaliza con un mensaje personalizado:“Gracias por usar el sistema Tienda Aurelion. Que tus ventas sean abundantes y tus datos limpios.”Puedes editarlo en main.py dentro de la variable mensaje_salida.