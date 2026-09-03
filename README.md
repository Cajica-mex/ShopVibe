# ShopVibe - Data Engineering (Junior - Sprint 1)

¡Bienvenido a tu primer día en **ShopVibe** como Junior Data Engineer!

---

## 📈 Contexto de Negocio
ShopVibe acaba de cerrar su **primera ronda semilla de inversión** y las ventas diarias se dispararon un **400%**. Hasta ayer, la analítica dependía de scripts manuales en Python que leían volcados desordenados de archivos JSON y CSV exportados directamente del checkout hacia carpetas locales (`data/raw/`).

El sistema actual colapsó:
* Los reportes en hojas de cálculo tardan horas en abrirse.
* Las métricas de ingresos no cuadran por órdenes duplicadas causadas por reintentos de red en la app móvil.
* Los volcados contienen registros corruptos (precios negativos, correos sin formato, esquemas rotos).
* Finanzas y Operaciones no tienen una fuente única de la verdad.

Fuiste contratado como el **primer Data Engineer Junior** para detener el caos operativo: construirás desde cero un almacén analítico local estructurado bajo la **Arquitectura Medallion** utilizando **DuckDB y Parquet**, asegurando trazabilidad, contratos de datos y un modelo dimensional listo para ser explotado.

---

## 🎯 ¿Qué valor aportarás en el Sprint 1?
1. **Desacoplar la analítica de los archivos operativos:** Centralizar los volcados crudos en una capa inmutable y trazable (**Bronze**) en formato columnar Parquet de alta compresión.
2. **Garantizar calidad y confianza en los datos:** Implementar una capa intermedia (**Silver**) donde se eliminan duplicados, se corrigen esquemas y se desvían registros inválidos a cuarentena (Dead-Letter Queue) sin detener el flujo de datos.
3. **Habilitar el autoservicio analítico (Single Source of Truth):** Modelar una capa final (**Gold**) bajo un esquema en estrella (**Star Schema** con hechos y dimensiones) particionado eficientemente por año y mes para habilitar *partition pruning*.
4. **Automatizar la ejecución:** Ensamblar un orquestador E2E reproducible y tolerante a fallos (`src/pipeline.py`).

---

## 🗂️ Estructura del Repositorio
* `data/raw/`: Volcados crudos del checkout (`sales_orders.json`, `products.csv`, `customers.csv`).
* `data/bronze/`: Capa Bronze inmutable en Parquet (`sales/`, `customers/`, `products/`).
* `data/silver/`: Capa Silver limpia y normalizada (`orders/`, `order_items/`, `customers/`, `quarantine/`).
* `data/gold/`: Capa Gold dimensional (`dim_customers/`, `dim_products/`, `fact_sales/`).
* `schema.sql`: Definiciones DDL compatibles con DuckDB para vistas y tablas de Silver y Gold.
* `src/pipeline.py`: Pipeline principal y orquestador ejecutable.
* `scripts/traffic_generator.py`: Generador de compras sintéticas crudas con inyección de anomalías.
* `tests/test_sprint1.py`: Suite de 15 pruebas unitarias globales.
* `tests_sprint_1/`: Tests unitarios independientes por cada ticket individual (`test_sprint_1_ticket_X.py`).

---

## 🛠️ Herramientas y Ejecución
Asegúrate de tener instaladas las dependencias:
```bash
pip install duckdb
```

### Ejecutar Tests
Para comprobar el progreso de un ticket específico:
```bash
python -m unittest tests_sprint_1/test_sprint_1_ticket_1.py
```
O para correr la suite completa del Sprint 1:
```bash
python -m unittest tests/test_sprint1.py
```
