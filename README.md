# kiskas

Versión: **V1.0.0**

Aplicación de escritorio en Python para analizar muestras de códigos y generar combinaciones con la misma estructura configurable. Incluye interfaz en español e inglés y un ejecutable para Windows.

Las siete muestras originales contienen cuatro bloques de cinco caracteres, separados por guiones. Los caracteres observados son números y letras mayúsculas. Esto permite describir el formato; no permite reconstruir un algoritmo privado ni asegurar que una combinación sea una licencia válida para otro producto.

## Funciones

- Analiza longitudes, bloques, alfabeto observado, posiciones, prefijo común y frecuencias.
- Carga las siete muestras proporcionadas para empezar a explorar el patrón.
- Configura bloques, longitud, alfabeto, prefijo sin guiones y cantidad de 1 a 10 000 códigos.
- Genera códigos únicos dentro de cada lote mediante `secrets`.
- Copia resultados al portapapeles y exporta TXT o CSV.
- Cambia inmediatamente entre español e inglés.
- Incluye el botón «Cómprame una cerveza» con el [enlace de donación](https://www.paypal.com/donate/?hosted_button_id=ZABFRXC2P3JQN).

## Requisitos y dependencias

Windows 10/11 de 64 bits para el `.exe`. Para trabajar con el código: Python 3.12 o posterior con Tk/Tcl (`tkinter`), Git y GitHub CLI si se publican cambios. La instalación oficial de Python para Windows incluye normalmente Tk/Tcl.

No hay dependencias externas en ejecución: `requirements.txt` documenta esta decisión. La compilación utiliza PyInstaller 6.22.2 y dependencias fijadas en `requirements-build.txt`. Fijar paquetes y usar el mismo entorno facilita repetir el build; no promete binarios idénticos byte por byte.

## Instalación desde el código

En PowerShell, desde la carpeta del proyecto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe kiskas.py
```

No necesitas activar el entorno virtual para estos comandos. Para el ejecutable, descarga `kiskas.exe` de una release publicada y ábrelo. `SHA256SUMS.txt` permite comparar su SHA-256 con `Get-FileHash .\kiskas.exe -Algorithm SHA256`.

## Uso

1. Revisa las muestras o pega otros códigos, uno por línea, y ejecuta el análisis.
2. Ajusta el formato y el alfabeto según tus necesidades. El alfabeto observado puede ser incompleto: siete muestras no demuestran todos los caracteres permitidos por el origen.
3. Introduce un prefijo opcional sin guiones y una cantidad entre 1 y 10 000.
4. Genera el lote; después copia o exporta los resultados. La unicidad se comprueba en ese lote y no entre ejecuciones independientes.

Los archivos exportados se guardan en la ruta que el usuario selecciona. La aplicación trabaja localmente; el enlace de donación abre el navegador cuando se pulsa.

## Pruebas y compilación

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/smoke_gui.py
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv\Scripts\python.exe scripts/build.py
.\.venv\Scripts\python.exe scripts/verify_exe.py
```

El build utiliza `Download_26386.ico`, empaqueta en un único archivo sin consola y produce `kiskas.exe` y `SHA256SUMS.txt` en la raíz, junto a `kiskas.py`. Consulta los pasos y comandos de publicación en [docs/COMANDOS.md](docs/COMANDOS.md).

## Versionado y releases

`VERSION`, con contenido `1.0.0`, es la fuente única de versión. `version.py` proporciona su representación `V1.0.0` a la aplicación y al build; README, changelog, tag y release deben corresponder a esa versión. El binario conserva el nombre `kiskas.exe`; sus metadatos y la release identifican la versión.

Cada commit relevante que llegue a `main` debe aumentar la versión antes del push:

```powershell
.\.venv\Scripts\python.exe scripts/bump_version.py patch --message "Describe el cambio"
```

Usa `patch` para correcciones compatibles y cambios relevantes de documentación/automatización, `minor` para funciones compatibles y `major` para cambios incompatibles. El script sincroniza `VERSION`, README y CHANGELOG. El primer commit parte de V1.0.0 y no necesita aumentar la versión.

El workflow [.github/workflows/release.yml](.github/workflows/release.yml) se ejecuta con cada push a `main`: verifica, compila en Windows y crea el tag `Vx.y.z`, la release y sus dos archivos adjuntos. Una revisión nueva no puede reutilizar un tag existente; aumenta la versión para corregir una release ya publicada. Consulta [CHANGELOG.md](CHANGELOG.md).

## Estructura

```text
kiskas.py                 Interfaz de escritorio bilingüe
kiskas_core.py            Análisis, validación y generación
version.py / VERSION      Acceso a la versión / fuente única
scripts/build.py          Ejecutable e integridad SHA-256
scripts/bump_version.py   Incremento sincronizado de versión
tests/                    Pruebas del comportamiento
docs/                     Especificación, plan, tareas y comandos
.agents/skills/           Skills del proyecto
.github/workflows/        Release automática
Download_26386.ico        Icono local
requirements*.txt         Dependencias de ejecución y compilación
```

## Desarrollo, seguridad y licencia

El proyecto sigue Spec Driven Development: [especificación](docs/spec.md), [plan](docs/plan.md) y [tareas](docs/tasks.md). [AGENTS.md](AGENTS.md) define responsabilidades y las skills locales para mantener esos documentos, comentar el código y publicar versiones.

[docs/security.md](docs/security.md) describe las medidas y los límites de la revisión. No se puede garantizar la ausencia total de vulnerabilidades. Se distribuye bajo [Apache License 2.0](LICENSE).

Referencias oficiales: [módulo secrets](https://docs.python.org/3/library/secrets.html), [uso de PyInstaller](https://pyinstaller.org/en/stable/usage.html) y [uso seguro de GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use).
