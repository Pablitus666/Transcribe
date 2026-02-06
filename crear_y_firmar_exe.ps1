# =======================================
# crear_y_firmar_exe.ps1
# Firma ejecutables para el proyecto Transcribe
# Autor: Walter Pablo Tellez Ayala
# Email: pharmakoz@gmail.com
# =======================================

param(
    [Parameter(Mandatory = $true)]
    [string]$ExecutablePath
)

Write-Host "== Transcribe :: Firma de ejecutable ==" -ForegroundColor Cyan

if (-not (Test-Path $ExecutablePath)) {
    Write-Host "ERROR: El archivo no existe: $ExecutablePath" -ForegroundColor Red
    exit 1
}

# ------------------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------------------
$CertName        = "Walter Pablo Tellez Ayala - Transcribe Dev"
$CertSubject     = "CN=Walter Pablo Tellez Ayala, O=Transcribe, OU=Development, E=pharmakoz@gmail.com"
$CertPasswordRaw = "Condorito123*#*?"   # ⚠️ SOLO DESARROLLO
$TimestampServer = "http://timestamp.digicert.com"

$CertPassword = ConvertTo-SecureString `
    -String $CertPasswordRaw `
    -Force `
    -AsPlainText

$PfxFilePath = Join-Path (Split-Path $ExecutablePath -Parent) "Transcribe_Dev_Cert.pfx"

# ------------------------------------------------------------
# CREAR CERTIFICADO (SI NO EXISTE)
# ------------------------------------------------------------
if (-not (Test-Path $PfxFilePath)) {

    Write-Host "Creando certificado de firma..." -ForegroundColor Green

    $cert = New-SelfSignedCertificate `
        -Subject $CertSubject `
        -CertStoreLocation "Cert:\CurrentUser\My" `
        -Type CodeSigning `
        -KeyUsage DigitalSignature `
        -KeyExportPolicy Exportable `
        -HashAlgorithm SHA256 `
        -NotAfter (Get-Date).AddYears(1)

    Write-Host "Certificado creado: $($cert.Thumbprint)" -ForegroundColor Green

    Export-PfxCertificate `
        -Cert $cert `
        -FilePath $PfxFilePath `
        -Password $CertPassword | Out-Null

    Write-Host "Certificado exportado a: $PfxFilePath" -ForegroundColor Green
}
else {
    Write-Host "Certificado existente encontrado, reutilizando..." -ForegroundColor Yellow
}

# ------------------------------------------------------------
# LOCALIZAR SIGNTOOL
# ------------------------------------------------------------
$SignToolPath = Get-ChildItem `
    "C:\Program Files (x86)\Windows Kits\10\bin" `
    -Recurse -Filter signtool.exe -ErrorAction SilentlyContinue |
    Sort-Object FullName -Descending |
    Select-Object -First 1 -ExpandProperty FullName

if (-not $SignToolPath) {
    Write-Host "ERROR: signtool.exe no encontrado" -ForegroundColor Red
    exit 1
}

Write-Host "Usando signtool: $SignToolPath" -ForegroundColor Green

# ------------------------------------------------------------
# FIRMAR EJECUTABLE
# ------------------------------------------------------------
Write-Host "Firmando ejecutable..." -ForegroundColor Cyan

& "$SignToolPath" sign `
    /fd SHA256 `
    /tr $TimestampServer `
    /td SHA256 `
    /f "$PfxFilePath" `
    /p $CertPasswordRaw `
    "$ExecutablePath"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Falló la firma" -ForegroundColor Red
    exit 1
}

Write-Host "Firma aplicada correctamente." -ForegroundColor Green

# ------------------------------------------------------------
# VERIFICACIÓN
# ------------------------------------------------------------
Write-Host "Verificando firma..." -ForegroundColor Cyan

& "$SignToolPath" verify /pa "$ExecutablePath"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Firma verificada correctamente." -ForegroundColor Green
}
else {
    Write-Host "Advertencia: la verificación no fue exitosa." -ForegroundColor Yellow
}

Write-Host "Proceso finalizado." -ForegroundColor Cyan
Write-Host "NOTA: Certificado solo válido para desarrollo." -ForegroundColor Yellow
