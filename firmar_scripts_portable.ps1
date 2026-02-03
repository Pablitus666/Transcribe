# =======================================
# firmar_scripts_portable.ps1
# Firma automática con timestamp de los scripts de Transcribe
# Crea el certificado si no existe
# =======================================

# Carpeta donde se encuentra este script
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Datos del certificado
$CertFriendlyName = "Transcribe – Walter Pablo Téllez Ayala"
$CertSubject = "CN=Walter Pablo Téllez Ayala, E=pharmakoz@gmail.com, O=Transcribe Project"
$TimeStampServer = "http://timestamp.digicert.com"

Write-Host "Iniciando firma de scripts Transcribe (portable) con Timestamp..." -ForegroundColor Cyan

# Lista de scripts a firmar
$Scripts = @(
    Join-Path $ProjectDir "Iniciar.vbs"
    Join-Path $ProjectDir "Transcribe.vbs"
    Join-Path $ProjectDir "Instalar_acceso_directo.ps1"
)

# Buscar certificado existente
$Cert = Get-ChildItem Cert:\CurrentUser\My | Where-Object { $_.FriendlyName -eq $CertFriendlyName }

# Si no existe, crear certificado autofirmado
if (-not $Cert) {
    Write-Host "No se encontró el certificado. Creando uno nuevo..." -ForegroundColor Yellow
    $Cert = New-SelfSignedCertificate `
        -Subject $CertSubject `
        -CertStoreLocation Cert:\CurrentUser\My `
        -Type CodeSigning `
        -KeyUsage DigitalSignature `
        -FriendlyName $CertFriendlyName
    Write-Host "Certificado creado: $CertFriendlyName" -ForegroundColor Green
} else {
    Write-Host "Certificado existente encontrado: $CertFriendlyName" -ForegroundColor Green
}

# Firmar cada script
foreach ($Script in $Scripts) {
    if (Test-Path $Script) {
        try {
            Set-AuthenticodeSignature -FilePath $Script -Certificate $Cert -TimestampServer $TimeStampServer
            Write-Host "Firma con Timestamp completada: $Script" -ForegroundColor Green
        } catch {
            Write-Warning "Error al firmar ${Script}: $_"
        }
    } else {
        Write-Warning "No se encontró el archivo para firmar: $Script"
    }
}

Write-Host "Todos los scripts han sido procesados." -ForegroundColor Cyan
