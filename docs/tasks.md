# Tareas y evidencia SDD

Esta lista es de aceptación; las casillas solo se completan cuando existe evidencia. La disponibilidad de archivos o un plan no acredita ejecución satisfactoria.

- [x] Implementar el análisis estructural y comprobar las siete muestras.
- [x] Implementar generación configurable con `secrets`, unicidad y validación de capacidad.
- [x] Verificar límites, prefijos, configuración inválida y exportaciones con las pruebas del proyecto.
- [x] Revisar GUI española e inglesa y cambio inmediato de idioma.
- [x] Revisar copia, selección de ruta y errores de escritura.
- [x] Confirmar versión consistente en aplicación, `VERSION`, README y changelog.
- [x] Compilar `kiskas.exe` con icono y sin consola; abrir el ejecutable.
- [x] Comparar el hash de `kiskas.exe` con `SHA256SUMS.txt`.
- [x] Revisar dependencias fijadas, exclusiones de Git, permisos y workflow.
- [x] Validar las tres skills y su integración en `AGENTS.md`.
- [x] Crear primer commit en `main` y repositorio público bajo la cuenta autorizada.
- [x] Verificar ejecución del workflow y release V1.0.0 con ejecutable, checksum y entrega completa.

## Registro de evidencia

Completar con comando, resultado y limitaciones después de cada verificación. Las tareas que no puedan ejecutarse deben explicar el motivo y el siguiente paso concreto.

| Verificación | Evidencia |
| --- | --- |
| Pruebas automatizadas | 16 pruebas pasan con `python -m unittest discover -s tests -v`. `python scripts/smoke_gui.py` verifica idiomas, generación, portapapeles, TXT/CSV, datos inválidos y enlace sin abrir el navegador. |
| Revisión visual de GUI | Ventana revisada en Windows 11: tamaño ajustado a pantalla; controles y botones visibles. Captura temporal local, no publicada. |
| Build y apertura del ejecutable | `python scripts/build.py` y `python scripts/verify_exe.py` correctos. Versión V1.0.0 en propiedades Windows; subsistema PE 2 (GUI sin consola). |
| SHA-256 | El hash del archivo compilado coincide con `SHA256SUMS.txt`; cada compilación local o remota tiene su propio hash. |
| Skills | Las tres skills pasan `quick_validate.py` de skill-creator con Python 3.12; `AGENTS.md` enlaza sus archivos locales. |
| GitHub y release | Repositorio público `erickson558/kiskas`, rama main. Commit inicial `4df80f8`; tag V1.0.0 apunta a ese commit. [Actions 38245969794](https://github.com/erickson558/kiskas/actions/runs/38245969794) terminó con éxito y [release V1.0.0](https://github.com/erickson558/kiskas/releases/tag/V1.0.0) publicada con kiskas.exe, SHA256SUMS.txt y ENTREGA.md. |

La siguiente versión patch incorpora esta evidencia y documenta la selección de credencial por cuenta. La publicación inicial fue verificada antes de registrar las casillas completadas; el resultado de cada release posterior se consulta en GitHub Actions.
