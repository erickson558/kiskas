---
name: kiskas-sdd
description: Mantener la especificación, el plan y las tareas de kiskas junto a cambios funcionales de su generador Python y GUI bilingüe.
---

Lee `docs/spec.md`, `docs/plan.md` y `docs/tasks.md` desde la raíz del proyecto antes de cambiar comportamiento. Actualiza requisitos y criterios afectados; registra evidencia real y limitaciones en las tareas, sin marcar pruebas ni publicación por anticipado.

Preserva la separación entre GUI y motor, Python 3.12+ y ejecución con biblioteca estándar. Los ejemplos permiten inferir estructura y observaciones; no permiten garantizar licencias de terceros. La generación usa `secrets`, valida capacidad y entrega unicidad por lote.

Para textos de interfaz, cubre español e inglés y el cambio inmediato de idioma. Conserva el enlace de donación exacto de la especificación. Cuando cambie el código, revisa sus comentarios y ejecuta las verificaciones pertinentes. Los commits relevantes deben seguir el versionado de `docs/COMANDOS.md`.
