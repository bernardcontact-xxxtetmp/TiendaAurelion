# Dashboard de Ventas - Analytics Comercial

## Descripción

Dashboard interactivo de visualización de datos comerciales construido con tecnologías web modernas. Proporciona análisis integral del rendimiento de ventas, productos y clientes con visualizaciones interactivas y efectos visuales sofisticados.

## Características

### 🎨 Diseño Visual
- **Estilo editorial sofisticado** inspirado en publicaciones como Kinfolk y The Gentlewoman
- **Paleta de colores** en azul marino y tonos claros con acentos cálidos
- **Tipografía elegante** con Playfair Display para encabezados e Inter para cuerpo de texto
- **Efectos visuales** incluyendo glass morphism, animaciones suaves y transiciones fluidas

### 📊 Visualizaciones
- **6 gráficos interactivos** con Plotly.js:
  - Ventas por categoría (gráfico de barras)
  - Ventas por ciudad (gráfico de barras horizontal)
  - Métodos de pago (gráfico de torta)
  - Tendencia temporal (gráfico de línea)
  - Top 10 productos más vendidos
  - Top 10 clientes más importantes
- **KPIs dinámicos** con animaciones de números
- **Interactividad completa** con hover effects y transiciones

### 🚀 Tecnologías Utilizadas
- **HTML5** - Estructura semántica
- **Tailwind CSS** - Framework de estilos
- **Plotly.js** - Visualizaciones interactivas
- **Anime.js** - Animaciones y efectos
- **JavaScript ES6+** - Lógica del dashboard
- **Google Fonts** - Tipografías premium
- **Font Awesome** - Iconos vectoriales

### 💫 Efectos Especiales
- **Animaciones de entrada** con stagger effects
- **Glass morphism** en elementos flotantes
- **Hover effects** sofisticados en tarjetas y gráficos
- **Transiciones fluidas** entre estados
- **Scroll animations** con Intersection Observer
- **Real-time updates** simuladas

## Estructura del Proyecto

```
/
├── index.html              # Página principal del dashboard
├── dashboard.js           # Lógica JavaScript principal
├── styles.css             # Estilos adicionales y efectos
├── tailwind.config.js     # Configuración de Tailwind CSS
├── datos_dashboard.json   # Datos procesados para visualizaciones
└── README.md              # Documentación
```

## Datos Analizados

El dashboard analiza datos comerciales que incluyen:

- **343 transacciones** de ventas
- **67 clientes únicos**
- **95 productos diferentes**
- **6 ciudades** de operación
- **4 métodos de pago**
- **13 categorías de productos**

Período de análisis: **Enero - Junio 2024**

## Métricas Principales

- **Total de Ventas**: $2,651,417
- **Transacciones Totales**: 343
- **Clientes Únicos**: 67
- **Promedio por Venta**: $7,730

## Instalación y Uso

1. **Requisitos previos**:
   - Navegador web moderno (Chrome, Firefox, Safari, Edge)
   - Servidor web local (opcional pero recomendado)

2. **Instalación**:
   ```bash
   # Clonar o descargar los archivos del proyecto
   cd dashboard-ventas
   
   # Iniciar servidor local
   python -m http.server 8000
   # o
   npx serve .
   ```

3. **Acceso**:
   - Abrir navegador en `http://localhost:8000`

## Personalización

### Colores
Los colores pueden ser personalizados en `dashboard.js`:
```javascript
this.colors = {
    primary: '#1e3a8a',
    secondary: '#3b82f6',
    accent: '#60a5fa',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
    info: '#06b6d4'
};
```

### Datos
Para actualizar los datos:
1. Modificar el archivo CSV en `/upload/datos_powerbi.csv`
2. Ejecutar el script de procesamiento: `python analisis_datos.py`
3. Los datos se actualizarán automáticamente en `datos_dashboard.json`

## Rendimiento

- **Tiempo de carga**: < 2 segundos
- **Optimizado para**: Chrome, Firefox, Safari, Edge
- **Responsive**: Adaptado para dispositivos móviles y tablets
- **Peso total**: < 500KB (sin datos)

## Navegadores Soportados

- **Chrome** 90+
- **Firefox** 88+
- **Safari** 14+
- **Edge** 90+

## Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para detalles.

## Autor

**Analytics Dashboard Team**
- Diseño y desarrollo de visualizaciones interactivas
- Análisis de datos comerciales
- Implementación de efectos visuales

---

**Nota**: Este dashboard fue desarrollado como demostración de capacidades de visualización de datos con énfasis en diseño editorial sofisticado y experiencia de usuario premium.