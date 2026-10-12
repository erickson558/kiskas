# Plan de implementación SDD

## Diseño

1. Mantener el formato inferido separado de la configuración elegida: las muestras describen lo observado y el usuario selecciona el formato a generar.
2. Implementar análisis y validación en `kiskas_core.py` para probarlos sin abrir ventanas. Comprobar capacidad antes de generar y evitar reintentos ilimitados en espacios pequeños.
3. Construir `kiskas.py` con Tkinter, textos centralizados para español/inglés, ejemplos precargados, copia/exportación y manejo de errores locales.
4. Leer `VERSION` a través de `version.py` tanto en código como en ejecutable. Usar `scripts/bump_version.py` para actualizar los documentos sincronizados.
5. Compilar con `scripts/build.py`, dependencias fijadas e icono local. Calcular SHA-256 del archivo final.
6. Automatizar pruebas y release en Windows mediante GitHub Actions. Verificar permisos, cuenta y destino antes de publicar.

## Verificación

Probar el patrón de las siete muestras, entradas inconsistentes, prefijos, límites de cantidad, capacidad agotada y unicidad. Comprobar exportación y errores previsibles. Abrir la GUI para revisar controles, cambio de idioma y versión. Compilar y abrir el ejecutable en Windows; comparar el hash calculado.

La revisión del workflow debe cubrir permisos mínimos necesarios, ausencia de secretos incrustados, referencias de acciones fijadas, versiones coherentes y rechazo de una revisión nueva con tag existente. Registrar resultados efectivos en las tareas; no marcar publicación o pruebas por anticipado.

## Mantenimiento

Para cada cambio relevante: actualizar especificación cuando cambie el comportamiento, implementar, verificar, actualizar comentarios/documentos, incrementar la versión, recompilar y publicar según autorización. Conservar las inferencias prudentes y el alcance local del programa al añadir funciones.
