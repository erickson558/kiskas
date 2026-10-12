# Agentes y responsabilidades de kiskas

Estas responsabilidades permiten repartir trabajo cuando el usuario lo solicite; no requieren abrir subagentes para cada cambio. Un mismo agente puede asumir varios roles. Lee la especificación y revisa el estado del árbol antes de editar.

| Rol | Archivos principales | Resultado esperado |
| --- | --- | --- |
| Desarrollo e interfaz | `kiskas.py` | GUI accesible, español/inglés coherentes, errores comprensibles y exportación fiable. |
| Análisis y motor | `kiskas_core.py`, `tests/` | Inferencias estructurales explícitas, generación con `secrets`, validaciones y unicidad por lote. |
| Release y seguridad | `version.py`, `VERSION`, `scripts/`, `.github/`, dependencias | Versión alineada, build verificable, credenciales fuera del repositorio y publicación autorizada. |

## Skills del proyecto

- [.agents/skills/kiskas-sdd/SKILL.md](.agents/skills/kiskas-sdd/SKILL.md): aplica a cambios funcionales para mantener especificación, plan y tareas junto al código.
- [.agents/skills/kiskas-release/SKILL.md](.agents/skills/kiskas-release/SKILL.md): prepara y publica versiones de este proyecto con la cuenta `erickson558`, respetando la autorización de la sesión.
- [.agents/skills/kiskas-comentarios/SKILL.md](.agents/skills/kiskas-comentarios/SKILL.md): explica las partes del código con comentarios útiles en español.

## Convenciones

Mantén Python 3.12+, biblioteca estándar en ejecución y Tkinter. No atribuyas validez externa a las combinaciones ni trates los siete ejemplos como prueba de un algoritmo privado. Conserva exactamente el enlace de donación especificado en `docs/spec.md`.

Antes de un commit relevante actualiza SDD, comentarios afectados, changelog y versión con `scripts/bump_version.py`. La versión inicial es V1.0.0. Ejecuta pruebas acordes al cambio y recompila cuando cambie el código entregado. El workflow genera tags y releases en cada push a `main`; evita crear una segunda release manual para el mismo cambio.

No añadas credenciales, binarios de trabajo o entornos virtuales a Git. Describe revisiones de seguridad y sus límites con evidencia; no prometas invulnerabilidad. Publicar un repositorio o release exige autorización presente en la conversación; esta guía no la concede.
