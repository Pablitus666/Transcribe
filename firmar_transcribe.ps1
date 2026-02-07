# ==========================================================
# firmar_transcribe.ps1
# Firma profesional de ejecutables (EXE + Installer)
#
# Proyecto : Transcribe
# Autor    : Walter Pablo Tellez Ayala
# Email    : pharmakoz@gmail.com
# Uso      : Desarrollo / Distribución
#
# NOTA:
# Certificado autofirmado (NO confiable públicamente).
# Flujo idéntico al que se usa con certificados reales OV/EV.
# ==========================================================

param(
    [Parameter(Mandatory = $true)]
    [string[]]$FilesToSign
)

Write-Host "== Transcribe :: Firma profesional ==" -ForegroundColor Cyan

# ----------------------------------------------------------
# CONFIGURACIÓN DEL CERTIFICADO
# ----------------------------------------------------------
$AuthorName  = "Walter Pablo Tellez Ayala"
$ProjectName = "Transcribe"
$AuthorEmail = "pharmakoz@gmail.com"

# Subject REAL del certificado (esto ES lo importante)
$CertSubject = "CN=$AuthorName, O=$ProjectName, E=$AuthorEmail"

$CertPasswordPlain = "Condorito123*#*?"
$CertPassword = ConvertTo-SecureString $CertPasswordPlain -AsPlainText -Force
$TimestampServer = "http://timestamp.digicert.com"

# Usar el PFX existente
$PfxPath = "I:\Proyectos Finales Python\Proyecto Transcribe\Transcribe\installer\Transcribe_Dev_Cert.pfx"

# ----------------------------------------------------------
# BUSCAR CERTIFICADO EXISTENTE (DESHABILITADO PARA USAR PFX DIRECTO)
# ----------------------------------------------------------
# Write-Host "Buscando certificado existente..." -ForegroundColor Yellow

# $cert = Get-ChildItem $CertStore | Where-Object {
#     $_.Subject -eq $CertSubject
# } | Select-Object -First 1

# if (-not $cert) {

#     Write-Host "Certificado no encontrado. Creando uno nuevo..." -ForegroundColor Yellow

#     $cert = New-SelfSignedCertificate `
#         -Subject $CertSubject `
#         -Type CodeSigning `
#         -CertStoreLocation $CertStore `
#         -KeyExportPolicy Exportable `
#         -KeyUsage DigitalSignature `
#         -NotAfter (Get-Date).AddYears(2)

#     Export-PfxCertificate `
#         -Cert $cert `
#         -FilePath $PfxPath `
#         -Password $CertPassword

#     Write-Host "Certificado creado correctamente:" -ForegroundColor Green
#     Write-Host "  Autor      : $AuthorName"
#     Write-Host "  Proyecto   : $ProjectName"
#     Write-Host "  Email      : $AuthorEmail"
#     Write-Host "  Thumbprint : $($cert.Thumbprint)"

# } else {

#     Write-Host "Certificado encontrado:" -ForegroundColor Green
#     Write-Host "  Thumbprint : $($cert.Thumbprint)"

#     if (-not (Test-Path $PfxPath)) {
#         Write-Host "Exportando certificado a PFX..." -ForegroundColor Yellow
#         Export-PfxCertificate `
#             -Cert $cert `
#             -FilePath $PfxPath `
#             -Password $CertPassword
#     }
# }

# ----------------------------------------------------------
# VERIFICACIÓN DE PFX EXISTENTE
# ----------------------------------------------------------
if (-not (Test-Path $PfxPath)) {
    Write-Error "El archivo PFX especificado no se encuentra: $PfxPath"
    exit 1
}

Write-Host "Usando archivo PFX existente:" -ForegroundColor Green
Write-Host "  $PfxPath"

# ----------------------------------------------------------
# BUSCAR SIGNTOOL
# ----------------------------------------------------------
$SignTool = Get-ChildItem `
    "C:\Program Files (x86)\Windows Kits\10\bin\*\x64\signtool.exe" `
    -ErrorAction SilentlyContinue |
    Select-Object -First 1 -ExpandProperty FullName

if (-not $SignTool) {
    Write-Error "signtool.exe no encontrado. Instala Windows SDK."
    exit 1
}

Write-Host "Usando signtool:" -ForegroundColor Cyan
Write-Host "  $SignTool"

# ----------------------------------------------------------
# FIRMAR ARCHIVOS
# ----------------------------------------------------------
foreach ($file in $FilesToSign) {

    if (-not (Test-Path $file)) {
        Write-Host "Archivo no encontrado: $file" -ForegroundColor Red
        continue
    }

    Write-Host "`nFirmando:" -ForegroundColor Cyan
    Write-Host "  $file"

    & "$SignTool" sign `
        /fd SHA256 `
        /tr $TimestampServer `
        /td SHA256 `
        /f $PfxPath `
        /p $CertPasswordPlain `
        "$file"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Firma aplicada correctamente." -ForegroundColor Green
    } else {
        Write-Host "Error al firmar $file" -ForegroundColor Red
    }
}

# ----------------------------------------------------------
# VERIFICACIÓN
# ----------------------------------------------------------
Write-Host "`nVerificando firmas..." -ForegroundColor Cyan
foreach ($file in $FilesToSign) {
    Get-AuthenticodeSignature $file | Format-Table Path, Status
}

Write-Host "`nProceso finalizado." -ForegroundColor Green
Write-Host "Certificado:" -ForegroundColor Yellow
Write-Host "  $CertSubject"
Write-Host "Uso exclusivo para desarrollo." -ForegroundColor Yellow
