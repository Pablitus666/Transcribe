# =======================================
# firmar_scripts_portable_full.ps1
# Firma automática con timestamp + instalación de certificado en TrustedPublisher
# =======================================

# Carpeta donde se encuentra este script
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Datos del certificado
$CertFriendlyName = "Transcribe – Walter Pablo Téllez Ayala"
$CertSubject = "CN=Walter Pablo Téllez Ayala, E=pharmakoz@gmail.com, O=Transcribe Project"
$TimeStampServer = "http://timestamp.digicert.com"
$ExportCerFile = Join-Path $ProjectDir "Transcribe_CodeSign.cer"

Write-Host "Iniciando firma de scripts Transcribe (completa) con Timestamp..." -ForegroundColor Cyan

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

# Exportar certificado a .cer para TrustedPublisher
if (-not (Test-Path $ExportCerFile)) {
    Export-Certificate -Cert $Cert -FilePath $ExportCerFile | Out-Null
    Write-Host "Certificado exportado a: $ExportCerFile" -ForegroundColor Green
} else {
    Write-Host "Archivo .cer ya existe: $ExportCerFile" -ForegroundColor Yellow
}

# Importar certificado a TrustedPublisher del usuario actual
try {
    Import-Certificate -FilePath $ExportCerFile -CertStoreLocation Cert:\CurrentUser\TrustedPublisher | Out-Null
    Write-Host "Certificado instalado en TrustedPublisher correctamente." -ForegroundColor Green
} catch {
    Write-Warning "Error al instalar el certificado en TrustedPublisher: $_"
}

# Firmar cada script con timestamp
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
