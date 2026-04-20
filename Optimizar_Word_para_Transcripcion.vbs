' ============================================================
'   OPTIMIZACION DE MICROSOFT WORD PARA TRANSCRIPCION
'   PROYECTO: TRANSCRIBE V2.0
'   DESARROLLADO POR: Walter Pablo Tellez Ayala
' ============================================================

Option Explicit

Dim shell, fso, word, confirm, wmi, processes, titulo, mensaje, exito, ok_msg

Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' --- SOLICITAR PRIVILEGIOS DE ADMINISTRADOR ---
If Not WScript.Arguments.Named.Exists("elevated") Then
    CreateObject("Shell.Application").ShellExecute "wscript.exe", """" & WScript.ScriptFullName & """ /elevated", "", "runas", 1
    WScript.Quit
End If

' --- DEFINIR CONSTANTES DE TEXTO ---
titulo = "Optimizaci" & Chr(243) & "n de Word - Transcribe"
mensaje = "Esta utilidad desactivar" & Chr(225) & " las teclas F1 y F2 en Microsoft Word para evitar conflictos con el programa Transcribe." & vbCrLf & vbCrLf & _
          "IMPORTANTE: Guarde su trabajo y CIERRE Word antes de continuar." & vbCrLf & vbCrLf & _
          Chr(191) & "Desea aplicar esta optimizaci" & Chr(243) & "n ahora?"

' --- VENTANA DE BIENVENIDA ---
confirm = MsgBox(mensaje, 33, titulo)
If confirm <> 1 Then WScript.Quit

' --- VERIFICAR SI WORD ESTA ABIERTO ---
Set wmi = GetObject("winmgmts:\\.\root\cimv2")
Set processes = wmi.ExecQuery("Select * from Win32_Process Where Name = 'winword.exe'")

If processes.Count > 0 Then
    mensaje = "Microsoft Word est" & Chr(225) & " abierto. Por favor, ci" & Chr(233) & "rrelo y vuelva a ejecutar esta herramienta."
    MsgBox mensaje, 48, "Error: Word detectado"
    WScript.Quit
End If

' --- REALIZAR OPTIMIZACION ---
On Error Resume Next
Set word = CreateObject("Word.Application")

If Err.Number <> 0 Then
    mensaje = "No se pudo conectar con Microsoft Word. Aseg" & Chr(250) & "rese de que est" & Chr(233) & " instalado correctamente."
    MsgBox mensaje, 16, "Error T" & Chr(233) & "cnico"
    WScript.Quit
End If

word.Visible = False
word.CustomizationContext = word.NormalTemplate
word.FindKey(word.BuildKeyCode(112)).Disable ' F1
word.FindKey(word.BuildKeyCode(113)).Disable ' F2
word.NormalTemplate.Save
word.Quit

If Err.Number = 0 Then
    exito = Chr(201) & "xito"
    ok_msg = Chr(161) & "Optimizaci" & Chr(243) & "n completada con " & exito & "!" & vbCrLf & vbCrLf & "F1 y F2 han sido desactivados en Word."
    MsgBox ok_msg, 64, exito
Else
    mensaje = "Hubo un problema al intentar guardar los cambios en Word." & vbCrLf & "Detalles: " & Err.Description
    MsgBox mensaje, 16, "Error de Aplicaci" & Chr(243) & "n"
End If

Set word = Nothing
