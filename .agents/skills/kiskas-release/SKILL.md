---
name: kiskas-release
description: Preparar, versionar, compilar y publicar kiskas en erickson558/kiskas con GitHub CLI y el workflow de releases Windows.
---

Lee `docs/COMANDOS.md`, `VERSION`, el changelog y `.github/workflows/release.yml`. Comprueba estado del árbol y remoto antes de cambiarlos. No sobrescribas historias o tags publicados para resolver colisiones.

La cuenta del proyecto es `erickson558`. Comprueba `gh auth status`; selecciona `gh auth switch --user erickson558` y confirma `gh api user --jq .login`. No almacenes tokens ni copie su contenido a documentos, logs o Git. El destino es el repositorio público `erickson558/kiskas` con rama `main`.

`VERSION` es la fuente única. El primer commit usa V1.0.0; para cada commit relevante posterior usa `python scripts/bump_version.py patch|minor|major --message "Descripción"`. Revisa sincronización de README/changelog, pruebas y `python scripts/build.py`. El build produce `kiskas.exe` y `SHA256SUMS.txt` en la raíz.

Antes de crear el repositorio o publicar un push/release, comprueba que la conversación autoriza esa publicación. La autorización previa dentro del mismo alcance sigue vigente; esta skill no concede autorización. Prepara los cambios y su evidencia antes de pedir permiso si falta.

Cada push a `main` activa la release automatizada. Una revisión nueva con tag existente debe fallar y necesita nueva versión; no crees una release manual duplicada. Confirma ejecución, commit, tag `Vx.y.z` y ambos adjuntos antes de informar éxito. Ante rechazo de acceso o conflicto de destino, informa el motivo y conserva el trabajo local.
