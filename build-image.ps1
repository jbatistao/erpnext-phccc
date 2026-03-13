# Script de build para jbatistao/frappe-2-full:v15
# Ejecutar desde la raiz del proyecto: .\build-image.ps1

$ErrorActionPreference = "Stop"

# 1. Convertir apps.json a base64
Write-Host "Convirtiendo apps.json a base64..." -ForegroundColor Cyan
$appsJsonPath = Join-Path $PSScriptRoot "apps.json"
$APPS_JSON_BASE64 = [Convert]::ToBase64String(
    [System.Text.Encoding]::UTF8.GetBytes((Get-Content -Raw -Path $appsJsonPath))
)
Write-Host "apps.json codificado ($($APPS_JSON_BASE64.Length) chars)" -ForegroundColor Green

# 2. Construir imagen
Write-Host "" 
Write-Host "Construyendo imagen Docker..." -ForegroundColor Cyan
docker build --no-cache `
    --build-arg=FRAPPE_PATH=https://github.com/frappe/frappe `
    --build-arg=FRAPPE_BRANCH=version-15 `
    --build-arg=PYTHON_VERSION=3.12.0 `
    --build-arg=NODE_VERSION=24.0.0 `
    "--build-arg=APPS_JSON_BASE64=$APPS_JSON_BASE64" `
    --tag=jbatistao/frappe-2-full:v15 `
    --file=images/custom/Containerfile2 `
    .

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: El build falló." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Build exitoso!" -ForegroundColor Green

# 3. Push al registro
Write-Host "Pusheando imagen al registro..." -ForegroundColor Cyan
docker push jbatistao/frappe-2-full:v15

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: El push falló. Verifica que estés logueado con 'docker login'" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Imagen publicada exitosamente: jbatistao/frappe-2-full:v15" -ForegroundColor Green
Write-Host "Ahora ve a Coolify y haz un redeploy forzado para usar la nueva imagen." -ForegroundColor Yellow
