# =======================================
# firmar_exe.ps1 – Firma automática de ejecutables
# Proyecto: Transcribe
# Autor: Walter Pablo Tellez Ayala
# Email: pharmakoz@gmail.com
# =======================================

param(
    [Parameter(Mandatory=$true)]
    [string]$ExecutablePath
)

Write-Host "Iniciando firma de $($ExecutablePath)..." -ForegroundColor Cyan

# THUMBPRINT DEL CERTIFICADO (DEBE COINCIDIR CON EL USADO EN LA UI)
$Thumbprint = "9A307DA02415E7208E883F7B68CB3F00F27E0C75"
$TimestampServer = "http://timestamp.digicert.com"

# --- Obtener certificado ---
$cert = Get-ChildItem Cert:\CurrentUser\My |
        Where-Object { $_.Thumbprint -eq $Thumbprint }

if (-not $cert) {
    Write-Host "Certificado no encontrado en el almacén de usuarios." -ForegroundColor Red
    Write-Host "Asegúrate de que el certificado con Thumbprint '$Thumbprint' está instalado en 'Certificados - Usuario actual -> Personal -> Certificados'." -ForegroundColor Yellow
    exit 1
}

# --- Buscar signtool.exe ---
$SignToolPath = ""
$possibleSignToolPaths = @(
    "C:\Program Files (x86)\Windows Kits\10\bin\*\x64\signtool.exe",
    "C:\Program Files (x86)\Windows Kits\8.1\bin\x64\signtool.exe",
    "C:\Program Files (x86)\Windows Kits\8.0\bin\x64\signtool.exe"
)

foreach ($path in $possibleSignToolPaths) {
    $foundPath = Get-ChildItem -Path $path -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName | Select-Object -First 1
    if ($foundPath) {
        $SignToolPath = $foundPath
        break
    }
}

if (-not (Test-Path $SignToolPath)) {
    Write-Host "ERROR: signtool.exe no encontrado automáticamente." -ForegroundColor Red
    Write-Host "Por favor, instala el Windows SDK (https://developer.microsoft.com/es-es/windows/downloads/windows-sdk/) o proporciona la ruta manualmente." -ForegroundColor Yellow
    Write-Host "Ejemplo de ruta: C:\Program Files (x86)\Windows Kits\10\bin\<VERSION>\x64\signtool.exe" -ForegroundColor Yellow
    exit 1
}

Write-Host "signtool.exe encontrado en: '$SignToolPath'" -ForegroundColor Green

Write-Host "Firmando: $($ExecutablePath)"

# Comando para signtool.exe
# /fd SHA256: Algoritmo de hash de archivo
# /tr: URL del servidor de sellado de tiempo (timestamp)
# /td SHA256: Algoritmo de hash para el sellado de tiempo
# /s My: Certificado en el almacén personal del usuario actual
# /sha1: Hash SHA1 del certificado
$SignCommand = "& `"$SignToolPath`" sign /fd SHA256 /tr `"$TimestampServer`" /td SHA256 /s My /sha1 $($cert.Thumbprint) `"$ExecutablePath`""

try {
    Invoke-Expression $SignCommand
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Firma completada correctamente para $($ExecutablePath)." -ForegroundColor Green
    } else {
        Write-Host "Error al firmar $($ExecutablePath). Código de salida: $LASTEXITCODE" -ForegroundColor Red
        # Podrías añadir más detalles del error si SignTool los proporciona a stderr
        exit 1
    }
} catch {
    Write-Host "Excepción al ejecutar signtool.exe: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Comprobar la firma (opcional)
Write-Host "Verificando la firma..." -ForegroundColor Cyan
try {
    $VerifyCommand = "& `"$SignToolPath`" verify /pa `"$ExecutablePath`""
    Invoke-Expression $VerifyCommand
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Verificación de firma exitosa para $($ExecutablePath)." -ForegroundColor Green
    } else {
        Write-Host "La verificación de firma falló para $($ExecutablePath). Código de salida: $LASTEXITCODE" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Excepción al verificar la firma: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "Proceso de firma finalizado." -ForegroundColor Green
