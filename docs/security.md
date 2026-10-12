# Seguridad y límites de revisión

kiskas procesa texto local y genera combinaciones. No verifica servicios de terceros ni utiliza credenciales de usuarios. El enlace de donación abre el navegador cuando el usuario lo solicita.

## Medidas implementadas

- Generación aleatoria con `secrets` y validación de configuración antes de generar.
- Límite de 10 000 códigos y comprobación de capacidad para evitar solicitudes imposibles y reintentos ilimitados.
- Tratamiento de muestras como datos, sin ejecución de expresiones ni comandos derivados de ellas.
- Gestión de errores de archivos, portapapeles y navegador, con mensajes de la interfaz.
- Dependencias de build fijadas; ejecución con biblioteca estándar.
- SHA-256 del ejecutable para comprobar integridad frente al archivo publicado.
- Tokens fuera del repositorio y autenticación de GitHub CLI mediante sus mecanismos de almacenamiento.
- Workflow con permisos y referencias de acciones revisados para la publicación necesaria.

Revisión del 2026-10-12: `python -m pip_audit -r requirements-build.txt --progress-spinner off` no encontró vulnerabilidades conocidas en las dependencias fijadas. El resultado corresponde a esa consulta y no incluye una garantía sobre vulnerabilidades todavía desconocidas ni sobre todo el sistema operativo. La aplicación no utiliza frameworks web; la skill de revisión no dispone de una referencia específica para Tkinter, por lo que se revisaron las medidas generales de Python y el código del proyecto.

Estas medidas deben contrastarse con el código y la evidencia de [tasks.md](tasks.md). No constituyen una auditoría independiente ni una garantía de ausencia de vulnerabilidades. Un hash detecta cambios respecto del hash esperado; no prueba quién produjo el ejecutable.

## Alcance y riesgos residuales

La revisión abarca validación, consumo acotado de recursos, fallos esperables, dependencias de compilación y configuración de publicación. El sistema operativo, Tk/Tcl, Python, PyInstaller, GitHub y su cadena de suministro pueden incorporar riesgos fuera de este alcance. No se han de presentar pruebas funcionales como una prueba de resistencia frente a todos los ataques.

No pegues datos sensibles en muestras si después vas a compartir exportaciones. Los archivos TXT/CSV son texto sin cifrar. La unicidad y la aleatoriedad no convierten los códigos en licencias auténticas.

## Reportar un problema

Para un error funcional, describe versión, pasos y resultado esperado en el repositorio. Para una posible vulnerabilidad, utiliza la opción de reporte privado de GitHub si está habilitada; evita publicar credenciales o detalles que permitan explotación. Revisa el código y corrige el problema antes de afirmar que está resuelto, registra el alcance y publica una versión nueva.
