# =======================================
# firmar_scripts_timestamp.ps1
# Firma todos los scripts del proyecto Transcribe con certificado de firma de código
# y añade timestamp para que la firma siga siendo válida aunque el certificado expire
# =======================================

# Carpeta donde se encuentra este script
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# FriendlyName del certificado que quieres usar
$CertFriendlyName = "Transcribe – Walter Pablo Téllez Ayala"

# URL de timestamp (oficial Microsoft)
$TimeStampServer = "http://timestamp.digicert.com"

Write-Host "Iniciando firma de scripts Transcribe con Timestamp..." -ForegroundColor Cyan

# Lista de scripts a firmar
$Scripts = @(
    Join-Path $ProjectDir "Iniciar.vbs"
    Join-Path $ProjectDir "Transcribe.vbs"
    Join-Path $ProjectDir "Instalar_acceso_directo.ps1"
)

# Obtener certificado por FriendlyName
$Cert = Get-ChildItem Cert:\CurrentUser\My | Where-Object { $_.FriendlyName -eq $CertFriendlyName }

if (-not $Cert) {
    Write-Error "No se encontró el certificado con FriendlyName: $CertFriendlyName"
    exit 1
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
