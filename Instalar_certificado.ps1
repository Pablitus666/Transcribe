# =======================================
# Instalar_certificado.ps1 – Instalación automática del certificado público
# =======================================

# Ruta del certificado (debe estar en la misma carpeta que este script)
$CertFile = Join-Path $PSScriptRoot "Transcribe_CodeSign.cer"

# Verifica que el archivo exista
if (-Not (Test-Path $CertFile)) {
    Write-Host "No se encontró el certificado en la ruta:" -ForegroundColor Red
    Write-Host $CertFile -ForegroundColor Red
    exit
}

# Importa el certificado en el almacén de 'Entidades de certificación raíz de confianza' del usuario actual
Try {
    Import-Certificate -FilePath $CertFile -CertStoreLocation Cert:\CurrentUser\Root | Out-Null
    Write-Host "✅ Certificado instalado correctamente en el almacén de confianza del usuario actual." -ForegroundColor Green
}
Catch {
    Write-Host "❌ Ocurrió un error al instalar el certificado:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

# Verifica la instalación
$Installed = Get-ChildItem Cert:\CurrentUser\Root | Where-Object { $_.Subject -like "*Transcribe*" }
if ($Installed) {
    Write-Host "🎉 Verificación exitosa: el certificado está instalado y reconocido." -ForegroundColor Cyan
}
else {
    Write-Host "⚠️ No se pudo verificar la instalación del certificado." -ForegroundColor Yellow
}
