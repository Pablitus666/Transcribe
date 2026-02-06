; =====================================================
; Transcribe Installer - Inno Setup Script
; Autor: Walter Pablo Tellez Ayala
; Proyecto: Transcribe
; =====================================================

[Setup]
AppId={{9C9A4E71-4F9A-4C01-A2D1-TRANSCRIBE0001}
AppName=Transcribe
AppVersion=1.0.0
AppPublisher=Walter Pablo Tellez Ayala
AppPublisherURL=https://github.com/Pablitus666

DefaultDirName={autopf}\Transcribe
DefaultGroupName=Transcribe
DisableProgramGroupPage=yes

; El icono se toma DIRECTAMENTE del EXE
SetupIconFile=images\icon.ico
UninstallDisplayIcon={app}\Transcribe.exe

OutputDir=installer
OutputBaseFilename=Transcribe_Setup

Compression=lzma2
SolidCompression=yes
WizardStyle=modern

PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

CloseApplications=yes
RestartApplications=no

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

; =====================================================
; ARCHIVOS
; =====================================================
[Files]
; Ejecutable principal
Source: "dist\Transcribe\Transcribe.exe"; DestDir: "{app}"; Flags: ignoreversion

; Archivos internos PyInstaller
Source: "dist\Transcribe\_internal\*"; DestDir: "{app}\_internal"; Flags: recursesubdirs createallsubdirs

; =====================================================
; ICONOS
; =====================================================
[Icons]
Name: "{group}\Transcribe"; Filename: "{app}\Transcribe.exe"
Name: "{commondesktop}\Transcribe"; Filename: "{app}\Transcribe.exe"; Tasks: desktopicon

; =====================================================
; TAREAS OPCIONALES
; =====================================================
[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; Flags: unchecked
Name: "autorun"; Description: "Ejecutar Transcribe al iniciar Windows"; Flags: unchecked

; =====================================================
; INICIO AUTOMÁTICO
; =====================================================
[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
    ValueType: string; ValueName: "Transcribe"; \
    ValueData: """{app}\Transcribe.exe"""; Tasks: autorun

; =====================================================
; POST-INSTALACIÓN
; =====================================================
[Run]
Filename: "{app}\Transcribe.exe"; \
    Description: "Ejecutar Transcribe ahora"; \
    Flags: nowait postinstall skipifsilent

; =====================================================
; DESINSTALACIÓN LIMPIA
; =====================================================
[UninstallDelete]
Type: filesandordirs; Name: "{app}"
