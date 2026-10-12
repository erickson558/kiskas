# Especificación SDD de kiskas

Versión inicial del producto: V1.0.0. Fecha de referencia: 2026-10-12.

## Necesidad y alcance

El usuario necesita una aplicación Python distribuida como `.exe` que analice ejemplos de combinaciones y genere códigos con una estructura semejante. El programa permite configurar esa estructura y revisar las inferencias antes de generar.

Las muestras son:

```text
3N6A2-BX51N-2ZWFY-65DH1
3N7XE-33YAW-44TYW-9UYSC
3N9TZ-TCXPM-TXWPR-VDCTR
3NA8M-7EXTH-1X6PH-FRMJG
3NBT8-G9TXD-61W7B-PR554
553ST-5G8Z7-992M7-D4DTE
59JKZ-SJ6CE-11MZE-5MPCR
```

Patrón común observable: cuatro bloques de cinco caracteres alfanuméricos mayúsculos, separados por `-`; veinte caracteres y tres guiones. No existe un prefijo común no vacío a las siete muestras. Cinco empiezan por `3N`, pero esa coincidencia parcial no demuestra una regla del origen. No se debe inferir una suma de comprobación, un algoritmo privado o validez ante servicios externos.

## Requisitos funcionales y aceptación

| ID | Requisito | Criterio de aceptación |
| --- | --- | --- |
| F01 | Analizar muestras | Informa estructura, alfabeto observado, frecuencias, posiciones y prefijo común; comunica inconsistencias. |
| F02 | Precargar ejemplos | Las siete muestras están disponibles al iniciar y pueden editarse. |
| F03 | Configurar formato | Permite elegir bloques, longitud por bloque, alfabeto y prefijo sin guiones; rechaza parámetros inválidos. |
| F04 | Generar combinaciones | Acepta entre 1 y 10 000, usa `secrets` y entrega exactamente el lote solicitado sin duplicados. |
| F05 | Validar capacidad | Si el prefijo y alfabeto dejan menos combinaciones que las pedidas, informa el problema sin entrar en un bucle infinito. |
| F06 | Copiar y exportar | Copia resultados y guarda TXT o CSV en la ruta elegida; muestra errores de archivos con claridad. |
| F07 | Cambiar idioma | Español e inglés cambian inmediatamente en los controles y mensajes correspondientes. |
| F08 | Donación | El botón abre `https://www.paypal.com/donate/?hosted_button_id=ZABFRXC2P3JQN`. |
| F09 | Mostrar versión | La GUI y el ejecutable reflejan `VERSION` con presentación `Vx.y.z`. |

La unicidad se limita a un lote. El alfabeto observado no se presenta como el alfabeto definitivo del sistema original. Las distribuciones por posición se presentan como observaciones, sin prometer la misma distribución en los códigos nuevos.

## Requisitos técnicos y de entrega

Windows 10/11 de 64 bits; Python 3.12+; Tkinter y biblioteca estándar en ejecución. Separar GUI (`kiskas.py`), motor (`kiskas_core.py`) y versión (`version.py` + `VERSION`). Validar tamaños antes de realizar trabajo costoso y gestionar fallos esperables de portapapeles, escritura y navegador.

Al iniciar, ajustar la ventana al tamaño de pantalla dejando margen para el título y la barra de tareas. Los errores del motor se transportan mediante claves estructuradas y se traducen en la interfaz. Las muestras tienen límite de 1 MB y 10 000 líneas; se permiten entre 1 y 32 bloques, cada uno de 1 a 32 caracteres, con longitud total de hasta 200 sin guiones. Solo se aceptan caracteres ASCII alfanuméricos para evitar conversiones Unicode inesperadas.

La verificación `scripts/smoke_gui.py` cubre controles, copia, ambos idiomas, exportaciones, rechazo de entradas y enlace. `scripts/verify_exe.py` abre el bundle mediante `--self-test RUTA_JSON`, verifica Tcl/Tk, generación y versión y cierra automáticamente. Ese modo es de diagnóstico y escribe únicamente la ruta indicada.

La compilación usa PyInstaller fijado en `requirements-build.txt`, modo onefile, sin consola y `Download_26386.ico`. `scripts/build.py` deja `kiskas.exe` y `SHA256SUMS.txt` en la raíz. La reproducción del proceso exige dependencias fijadas y entorno compatible; no implica identidad binaria absoluta.

Repositorio público solicitado: `erickson558/kiskas`, rama `main`, licencia Apache 2.0. El workflow se activa por cada push a `main`, ejecuta pruebas, compila y publica el tag/release `Vx.y.z` con ambos artefactos. Una revisión nueva no reutiliza un tag existente. No se guardan tokens en archivos.

El tercer adjunto `ENTREGA.md` se genera desde los archivos reales de la versión y contiene los seis apartados de entrega solicitados, incluyendo archivos completos y comandos. El documento se genera junto al ejecutable y se excluye del historial para evitar copias divergentes de los archivos mantenidos.

## Versionado y mantenimiento

`VERSION` almacena exclusivamente SemVer sin prefijo. Cada commit relevante aumenta major, minor o patch con el script correspondiente y actualiza README y changelog. Para el primer commit se usa V1.0.0. Cambios funcionales posteriores actualizan esta especificación, el plan y las tareas; comentarios explican decisiones y bloques significativos en español.

## Límites

El programa genera combinaciones estructurales, sin comprobar licencias de terceros. No almacena un historial global de códigos ni garantiza unicidad entre lotes. Las medidas de seguridad reducen riesgos concretos y no acreditan ausencia total de vulnerabilidades.
