# ShopVibe - Data Engineering (Junior - Sprint 1)

¡Bienvenido a tu primer día en **ShopVibe** como Junior Data Engineer!

## Contexto de Negocio
ShopVibe es una plataforma de e-commerce de moda de rápido crecimiento. Actualmente, las transacciones de ventas y el catálogo de productos se generan como archivos semiestructurados dispersos (JSON y CSV). El equipo analítico y de marketing requiere centralizar esta información de forma estructurada en una base de datos analítica local (SQLite) para generar reportes consistentes de facturación y detectar tendencias.

## Tus Objetivos en este Sprint 1
Deberás construir el pipeline inicial de Extracción, Limpieza y Carga (ETL) local para ShopVibe:
1.  **Modelo de Datos (`schema.sql`):** Definir el Star Schema inicial en SQLite (tablas de dimensión `dim_products`, `dim_customers` y la tabla de hechos `fact_sales` vinculada).
2.  **Calidad y Limpieza (`src/clean_data.py`):** Escribir funciones modulares en Python para validar correos, comprobar importes mayores a cero, deduplicar transacciones por ID, aplanar compras anidadas de JSON y normalizar estados/direcciones.
3.  **Parsers Auxiliares (`src/parse_csv.py` y `src/audit.py`):** Resolver el parseo de comas mal formadas en CSVs de proveedores externos y registrar auditorías de descarte en `descartes.log` sin detener el pipeline.
4.  **Carga e Integración (`src/db_loader.py` y `src/parquet_loader.py`):** Programar la inserción incremental (Append-only) validando la unicidad del ID de transacción y cargar datos estructurados desde archivos Parquet de inventario.
5.  **Orquestación (`src/pipeline.py`):** Unificar y encadenar todo el flujo de datos con manejo de excepciones y control transaccional (commit/rollback) ante fallos intermitentes.

---

## Estructura del Repositorio
*   `schema.sql`: DDL de base de datos analítica.
*   `src/`: Carpeta con los módulos de código Python.
    *   `clean_data.py`: Módulo de validación y limpieza de strings/números.
    *   `db_loader.py`: Ingestor relacional incremental.
    *   `parse_csv.py`: Módulo parseador de delimitadores CSV.
    *   `audit.py`: Logger local de registros corruptos descartados.
    *   `parquet_loader.py`: Ingestor de archivos Parquet.
    *   `pipeline.py`: Orquestador principal del ETL.
*   `scripts/`: Utilidades del sistema.
    *   `traffic_generator.py`: Generador de compras sintéticas crudas.
*   `tests/`: Suite de validaciones automáticas.
    *   `test_sprint1.py`: Pruebas de unittest para verificar cumplimiento de los 15 tickets.

---

## Cómo Ejecutar y Probar tu Progreso

1.  **Generar datos de prueba:**
    Para generar archivos de ventas crudos en la carpeta `data/raw/` con anomalías inyectadas, corre:
    ```bash
    python scripts/traffic_generator.py --anomalies-all
    ```
2.  **Ejecutar los Tests de Calidad:**
    Ejecuta el suite de pruebas en cualquier momento para ver tu porcentaje de avance y verificar qué tickets de Sprint 1 has cumplido:
    ```bash
    python -m unittest tests/test_sprint1.py
    ```
