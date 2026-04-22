# ReqPrompt

Aplicacion de escritorio para levantar requerimientos con entrevistas guiadas, banco de preguntas y generacion de prompts estructurados listos para usar en cualquier LLM.

## Estado del proyecto

El flujo anterior basado en un instalador separado fue eliminado del proyecto.

La compilacion oficial ahora queda centralizada en un unico script:

```bash
bash build.sh
```

Ese script prepara el entorno, instala `PyInstaller`, limpia artefactos previos y genera la app de escritorio automaticamente.

## Funcionalidades

- Crear y eliminar proyectos
- Responder preguntas por categoria en la entrevista
- Agregar preguntas variables a cada proyecto
- Buscar proyectos y preguntas
- Importar preguntas desde JSON
- Generar y guardar un prompt final en `.txt`
- Guardar toda la informacion localmente en SQLite

## Requisitos

- Python 3.9 o superior
- Dependencias de `requirements.txt`
- En Linux, librerias graficas necesarias para `pywebview`

## Estructura relevante

```text
req_app/
├── main.py
├── api.py
├── reqprompt/
├── assets/
├── requirements.txt
├── setup.sh
├── run.sh
├── build.sh
├── setup.bat
├── run.bat
└── ReqPrompt.spec
```

## Base de datos

Los datos se guardan localmente en:

`~/.req_elicit/data.db`

## Ejecutar en desarrollo

### macOS / Linux

```bash
chmod +x setup.sh run.sh build.sh
bash setup.sh
bash run.sh
```

### Windows

```bat
setup.bat
run.bat
```

## Compilar la app automaticamente

### macOS / Linux

```bash
bash build.sh
```

El script realiza estos pasos:

1. Verifica que `python3` exista.
2. Crea `venv/` si todavia no existe ejecutando `setup.sh`.
3. Activa el entorno virtual.
4. Instala o actualiza `PyInstaller`.
5. Elimina `build/` y `dist/`.
6. En macOS, genera `build/ReqPrompt.icns` a partir de `assets/icono.png`.
7. Compila usando `ReqPrompt.spec`.

### Resultado de compilacion

- macOS: `dist/ReqPrompt.app`
- Linux: `dist/ReqPrompt/`

## Importar preguntas

El archivo JSON debe tener este formato:

```json
[
  { "category": "Funcional", "text": "Pregunta...", "type": "Abierta" }
]
```

Categorias validas:

- Funcional
- No funcional
- Negocio
- Restriccion
- Interfaz

Tipos validos:

- Abierta
- Cerrada
- Seleccion multiple

## Flujo de uso

1. Crear un proyecto.
2. Completar la entrevista con respuestas del cliente.
3. Agregar preguntas extra si hace falta.
4. Generar el prompt final.
5. Exportarlo a un archivo `.txt`.

## Notas

- La app trabaja sin base de datos remota.
- El prompt final se genera a partir de los datos cargados en cada proyecto.
- `build/` y `dist/` son artefactos generados y pueden recrearse con `bash build.sh`.
