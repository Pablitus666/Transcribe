' ============================================================
'   RESTAURAR TECLAS ORIGINALES DE MICROSOFT WORD
'   PROYECTO: TRANSCRIBE V2.0
'   DESARROLLADO POR: Walter Pablo Tellez Ayala
' ============================================================

Option Explicit

Dim shell, fso, word, confirm, wmi, processes, titulo, mensaje, exito

Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' --- SOLICITAR PRIVILEGIOS DE ADMINISTRADOR ---
If Not WScript.Arguments.Named.Exists("elevated") Then
    CreateObject("Shell.Application").ShellExecute "wscript.exe", """" & WScript.ScriptFullName & """ /elevated", "", "runas", 1
    WScript.Quit
End If

' --- DEFINIR CONSTANTES DE TEXTO ---
titulo = "Restauraci" & Chr(243) & "n de Word - Transcribe"
mensaje = "Esta utilidad restaurar" & Chr(225) & " F1 y F2 a sus funciones originales en Word." & vbCrLf & vbCrLf & _
          "Nota: Sus sustituciones y diccionarios NO ser" & Chr(225) & "n afectados." & vbCrLf & vbCrLf & _
          Chr(191) & "Desea restaurar las teclas ahora?"

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

' --- REALIZAR RESTAURACION ---
On Error Resume Next
Set word = CreateObject("Word.Application")

If Err.Number <> 0 Then
    mensaje = "No se pudo conectar con Microsoft Word. Aseg" & Chr(250) & "rese de que est" & Chr(233) & " instalado correctamente."
    MsgBox mensaje, 16, "Error T" & Chr(233) & "cnico"
    WScript.Quit
End If

word.Visible = False
word.CustomizationContext = word.NormalTemplate
word.FindKey(word.BuildKeyCode(112)).Clear ' Restaurar F1
word.FindKey(word.BuildKeyCode(113)).Clear ' Restaurar F2
word.NormalTemplate.Save
word.Quit

If Err.Number = 0 Then
    exito = Chr(201) & "xito"
    mensaje = exito & ": " & Chr(161) & "Restauraci" & Chr(243) & "n completada!" & vbCrLf & vbCrLf & "F1 y F2 vuelven a sus funciones originales."
    MsgBox mensaje, 64, "Restauraci" & Chr(243) & "n"
Else
    mensaje = "Hubo un problema al intentar restaurar la configuraci" & Chr(243) & "n de Word." & vbCrLf & "Detalles: " & Err.Description
    MsgBox mensaje, 16, "Error de Aplicaci" & Chr(243) & "n"
End If

Set word = Nothing
