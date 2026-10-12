# Comandos repetibles en PowerShell

Ejecutar desde la raíz de `kiskas`. Los bloques documentan el procedimiento; no afirman que ya se haya ejecutado. La publicación inicial está solicitada por el usuario en el encargo; en sesiones futuras comprueba que la publicación correspondiente sigue dentro del alcance autorizado.

## Preparar, probar y compilar

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/smoke_gui.py
.\.venv\Scripts\python.exe kiskas.py
.\.venv\Scripts\python.exe scripts/build.py
.\.venv\Scripts\python.exe scripts/verify_exe.py
Get-FileHash .\kiskas.exe -Algorithm SHA256
Get-Content .\SHA256SUMS.txt
```

El entorno virtual mantiene las herramientas separadas. El comando de la GUI abre una ventana; ciérrala para continuar. El build usa el icono local y genera `kiskas.exe` junto al `.py`, sin consola, más su archivo de integridad. Compara el hash antes de distribuir.

## Primer commit y repositorio público

Inspecciona primero el estado local y la cuenta. No sobrescribas un remoto existente ni crees un segundo repositorio si ya existe.

```powershell
gh auth status
gh auth switch --user erickson558
$env:GH_TOKEN = gh auth token --hostname github.com --user erickson558
gh api user --jq .login
git status
git remote -v
gh repo view erickson558/kiskas
```

La asignación mantiene la credencial únicamente en memoria del proceso de PowerShell y evita que otra credencial de entorno prevalezca sobre la cuenta seleccionada. No imprimas `$env:GH_TOKEN`, no lo guardes en archivos y comprueba que `gh api user` devuelva `erickson558`.

Si aún no hay repositorio Git, inicialízalo. El error de `git status` fuera de un repositorio no es un motivo para borrar archivos:

```powershell
git init -b main
git config user.name "erickson558"
git config user.email "erickson558@users.noreply.github.com"
gh auth setup-git
git add .
git diff --cached --stat
git diff --cached
git commit -m "feat: crear kiskas V1.0.0 con generador bilingüe y releases"
```

Revisa que el área preparada no contenga credenciales ni artefactos excluidos. El primer commit utiliza V1.0.0; no ejecutes un bump solo por inicializarlo.

Si `erickson558/kiskas` no existe y su creación está autorizada:

```powershell
gh repo create erickson558/kiskas --public --source . --remote origin --description "Generador y analizador de patrones de códigos con GUI bilingüe en Python"
git push -u origin main
```

Si la creación responde con timeout, consulta `gh repo view erickson558/kiskas` antes de reintentar: GitHub puede haber creado el repositorio aunque no haya llegado la respuesta. Si ya existe vacío, añade `origin` solo si falta y publica `main`.

Si el repositorio existe y corresponde a este proyecto, añade `origin` solo si no está configurado:

```powershell
git remote add origin https://github.com/erickson558/kiskas.git
git push -u origin main
```

Un rechazo por historia remota exige inspeccionar y reconciliar la historia; no uses `--force` como solución automática. GitHub crea el tag y la release mediante el workflow, después del push.

## Cambios posteriores y SemVer

Antes del commit, actualiza SDD y documentación afectada y ejecuta las pruebas. Elige solo uno de estos incrementos:

```powershell
.\.venv\Scripts\python.exe scripts/bump_version.py patch --message "Corregir validación del prefijo"
.\.venv\Scripts\python.exe scripts/bump_version.py minor --message "Añadir una función compatible"
.\.venv\Scripts\python.exe scripts/bump_version.py major --message "Introducir un cambio incompatible"
```

`patch` cubre correcciones compatibles y cambios relevantes de documentación o automatización; `minor`, funciones nuevas compatibles; `major`, cambios incompatibles. Cada comando sincroniza `VERSION`, README y CHANGELOG. No ejecutes los tres para un mismo cambio.

Después del incremento elegido:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/build.py
git add .
git diff --cached
git commit -m "fix: corregir validación del prefijo"
git push origin main
```

Usa mensajes `feat:`, `fix:`, `docs:`, `build:` o `ci:` según el cambio. Un commit relevante en `main` requiere nueva versión para que no colisione con el tag existente. Preferiblemente agrupa el incremento y su cambio en el mismo commit.

## Verificar Actions, tags y release

```powershell
gh run list --repo erickson558/kiskas --workflow release.yml --limit 5
gh run view --repo erickson558/kiskas --log-failed
git fetch origin --tags
git tag --list "V*"
gh release list --repo erickson558/kiskas
gh release view V1.0.0 --repo erickson558/kiskas
```

`gh run view` puede solicitar seleccionar una ejecución; usa su identificador para revisar una concreta. Cambia `V1.0.0` por la versión publicada. Verifica que la release corresponda al commit correcto y contenga `kiskas.exe` y `SHA256SUMS.txt`.

El flujo habitual no requiere `git tag` ni `gh release create` manuales. Si falla una release porque una nueva revisión reutiliza la versión, incrementa versión y vuelve a verificar. No elimines un tag publicado para ocultar el conflicto.
