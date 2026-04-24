# Desafío Técnico - PwC (Low Code Developer)

Este repositorio contiene la solución al desafío técnico de importación y gestión (ABM) de clientes. La API está desarrollada en Python utilizando FastAPI y SQLite como base de datos. Se utilizan Testing para probar la API. Se utilizan Pydantic para validar los datos y SQLAlchemy para la base de datos. Y se utilizan de herramientas Agentes de IA como Antigravity para ayudar al desarrollo y Testing.

## Requisitos Previos
- Python 3.10 o superior instalado.

## Instalación y Ejecución

1. **Clonar el repositorio y entrar al directorio:**
   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd pwc-challenge
   ```
   **Recomendación:** Se puede usar la herramienta Antigravity para clonar el repositorio y ejecutar los tests.

2. **Crear un entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Ejecutar la API:**
   ```bash
   uvicorn app.main:app --reload
   ```
5. **Ejecutar los tests:**
   ```bash
   pytest
   ```

