# reCAPTCHA Solver API

Esta es una aplicación de API que resuelve reCAPTCHAs utilizando Playwright y técnicas de reconocimiento de voz.

## Requisitos

- Python 3.11
- Docker (opcional para contenedorización)
- Docker Compose (opcional para contenedorización)

## Configuración del Entorno Local


### Configuración en Diferentes Sistemas Operativos

#### Windows

1. **Crear y Activar un Entorno Virtual**
   ~~~
   python -m venv venv
   .\\venv\\Scripts\\activate
   ~~~

2. **Instalar las Dependencias**
   ~~~
   pip install -r requirements.txt
   ~~~

3. **Instalar Playwright y sus Dependencias**
   ~~~
   pip install playwright
   playwright install
   playwright install-deps
   ~~~

4. **Ejecutar la Aplicación**
   ~~~
   python main.py
   ~~~

#### macOS/Linux

1. **Crear y Activar un Entorno Virtual**
   ~~~
   python3 -m venv venv
   source venv/bin/activate
   ~~~

2. **Instalar las Dependencias**
   ~~~
   pip install -r requirements.txt
   ~~~

3. **Instalar Playwright y sus Dependencias**
   ~~~
   pip install playwright
   playwright install
   playwright install-deps
   ~~~

4. **Ejecutar la Aplicación**
   ~~~
   python main.py
   ~~~

## Uso de Docker

### 1. Construir la Imagen de Docker
~~~
docker-compose up --build
~~~

### 2. Ejecutar el Contenedor de Docker
~~~
docker-compose up
~~~

La API estará disponible en `http://localhost:8000`.

### 3. Detener el Contenedor de Docker
~~~
docker-compose down
~~~

## Endpoints de la API

### Documentación de la API

La documentación interactiva generada automáticamente por FastAPI está disponible en:

- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

### Ejemplo de Uso

#### Resolver reCAPTCHA
~~~
curl -X POST "http://localhost:8000/solve-recaptcha/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"url\":\"https://www.google.com/recaptcha/api2/demo\"}"
~~~
