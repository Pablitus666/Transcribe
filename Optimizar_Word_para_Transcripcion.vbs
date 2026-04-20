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

'' SIG '' Begin signature block
'' SIG '' MIIc0AYJKoZIhvcNAQcCoIIcwTCCHL0CAQExCzAJBgUr
'' SIG '' DgMCGgUAMGcGCisGAQQBgjcCAQSgWTBXMDIGCisGAQQB
'' SIG '' gjcCAR4wJAIBAQQQTvApFpkntU2P5azhDxfrqwIBAAIB
'' SIG '' AAIBAAIBAAIBADAhMAkGBSsOAwIaBQAEFEBK6ftdFdUY
'' SIG '' La0c4V2Vt5NdaYC1oIIW8jCCA7QwggKcoAMCAQICEB2Y
'' SIG '' wJKY9+6cSyPYIzfuaAswDQYJKoZIhvcNAQELBQAwcjEL
'' SIG '' MAkGA1UEBhMCQk8xIjAgBgkqhkiG9w0BCQEWE3BoYXJt
'' SIG '' YWtvekBnbWFpbC5jb20xGzAZBgNVBAoMElNvZnR3YXJl
'' SIG '' IERldmVsb3BlcjEiMCAGA1UEAwwZV2FsdGVyIFBhYmxv
'' SIG '' IFRlbGxleiBBeWFsYTAeFw0yNjAzMDMxMzA2MTVaFw0y
'' SIG '' NzAzMDMxMzI2MTVaMHIxCzAJBgNVBAYTAkJPMSIwIAYJ
'' SIG '' KoZIhvcNAQkBFhNwaGFybWFrb3pAZ21haWwuY29tMRsw
'' SIG '' GQYDVQQKDBJTb2Z0d2FyZSBEZXZlbG9wZXIxIjAgBgNV
'' SIG '' BAMMGVdhbHRlciBQYWJsbyBUZWxsZXogQXlhbGEwggEi
'' SIG '' MA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCko1kM
'' SIG '' kw2OmI8Zq3T2vjPplEiLuBHr6AqWFep4dCFlqZk/xr1b
'' SIG '' /2CLcn6fzzp2lrHmFW5yiZBxOiR9JEnEUcjaHUkeV/KU
'' SIG '' tP840rO7JCy/kYpvK3XQovBCQBuYzUzlS0R4vMdVbkun
'' SIG '' ZEsimDEl3r7MinCxM2RX3p88viZ8hWmYnU5eehBg4qkH
'' SIG '' UhlisXN8ecObFT/eYNeL2NzGQ257iSKxRIe/9R27hRHe
'' SIG '' ZGx2BTT42YnkxtEpU87FEZZdxfVo2vaHGzAkAzHyUJAT
'' SIG '' iQzW/7NaJVzs/BWFy9tuLibdWjI3LYhB0Z/t4cD+t40X
'' SIG '' ateWuwAtU+eSmLkktqFTABPoQo5tAgMBAAGjRjBEMA4G
'' SIG '' A1UdDwEB/wQEAwIHgDATBgNVHSUEDDAKBggrBgEFBQcD
'' SIG '' AzAdBgNVHQ4EFgQUq1WqXUOJlUZqH0TQ6N1bfKt3yu4w
'' SIG '' DQYJKoZIhvcNAQELBQADggEBABfIPOGORQ8XHG6AFm6x
'' SIG '' S16ugoAg/CpkG4k10KmlWAX35mwa8HGO2GOecrb7NJPS
'' SIG '' 5LPWjlKONqin3B6H/kDw5cf8RY2mFpWTCNAnIM6Nzvky
'' SIG '' LsDVxNsU7jkkGdvX7XzFwxX56Cfib/mFhZyNvYXK4v4A
'' SIG '' w3blXEDohN8wCv9KL7EZms/zoo0ytHAev7StB03eDf+z
'' SIG '' Ba+p0P27pGr+8flAIgc5qg2fsxtSARUloYUOxdbyKaRQ
'' SIG '' xBsaI85WHSQKN7zWI07ctoTM0UwsUc1eQf2uE6JOPp6R
'' SIG '' NXUj1wjJ3asOZq8Vr3AKNGRMZo2Y6etoYo7o8C0K25/g
'' SIG '' MlNR+XbVEkDGWaUwggWNMIIEdaADAgECAhAOmxiO+dAt
'' SIG '' 5+/bUOIIQBhaMA0GCSqGSIb3DQEBDAUAMGUxCzAJBgNV
'' SIG '' BAYTAlVTMRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAX
'' SIG '' BgNVBAsTEHd3dy5kaWdpY2VydC5jb20xJDAiBgNVBAMT
'' SIG '' G0RpZ2lDZXJ0IEFzc3VyZWQgSUQgUm9vdCBDQTAeFw0y
'' SIG '' MjA4MDEwMDAwMDBaFw0zMTExMDkyMzU5NTlaMGIxCzAJ
'' SIG '' BgNVBAYTAlVTMRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMx
'' SIG '' GTAXBgNVBAsTEHd3dy5kaWdpY2VydC5jb20xITAfBgNV
'' SIG '' BAMTGERpZ2lDZXJ0IFRydXN0ZWQgUm9vdCBHNDCCAiIw
'' SIG '' DQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAL/mkHNo
'' SIG '' 3rvkXUo8MCIwaTPswqclLskhPfKK2FnC4SmnPVirdprN
'' SIG '' rnsbhA3EMB/zG6Q4FutWxpdtHauyefLKEdLkX9YFPFIP
'' SIG '' Uh/GnhWlfr6fqVcWWVVyr2iTcMKyunWZanMylNEQRBAu
'' SIG '' 34LzB4TmdDttceItDBvuINXJIB1jKS3O7F5OyJP4IWGb
'' SIG '' NOsFxl7sWxq868nPzaw0QF+xembud8hIqGZXV59UWI4M
'' SIG '' K7dPpzDZVu7Ke13jrclPXuU15zHL2pNe3I6PgNq2kZhA
'' SIG '' kHnDeMe2scS1ahg4AxCN2NQ3pC4FfYj1gj4QkXCrVYJB
'' SIG '' MtfbBHMqbpEBfCFM1LyuGwN1XXhm2ToxRJozQL8I11pJ
'' SIG '' pMLmqaBn3aQnvKFPObURWBf3JFxGj2T3wWmIdph2PVld
'' SIG '' QnaHiZdpekjw4KISG2aadMreSx7nDmOu5tTvkpI6nj3c
'' SIG '' AORFJYm2mkQZK37AlLTSYW3rM9nF30sEAMx9HJXDj/ch
'' SIG '' srIRt7t/8tWMcCxBYKqxYxhElRp2Yn72gLD76GSmM9GJ
'' SIG '' B+G9t+ZDpBi4pncB4Q+UDCEdslQpJYls5Q5SUUd0vias
'' SIG '' tkF13nqsX40/ybzTQRESW+UQUOsxxcpyFiIJ33xMdT9j
'' SIG '' 7CFfxCBRa2+xq4aLT8LWRV+dIPyhHsXAj6KxfgommfXk
'' SIG '' aS+YHS312amyHeUbAgMBAAGjggE6MIIBNjAPBgNVHRMB
'' SIG '' Af8EBTADAQH/MB0GA1UdDgQWBBTs1+OC0nFdZEzfLmc/
'' SIG '' 57qYrhwPTzAfBgNVHSMEGDAWgBRF66Kv9JLLgjEtUYun
'' SIG '' pyGd823IDzAOBgNVHQ8BAf8EBAMCAYYweQYIKwYBBQUH
'' SIG '' AQEEbTBrMCQGCCsGAQUFBzABhhhodHRwOi8vb2NzcC5k
'' SIG '' aWdpY2VydC5jb20wQwYIKwYBBQUHMAKGN2h0dHA6Ly9j
'' SIG '' YWNlcnRzLmRpZ2ljZXJ0LmNvbS9EaWdpQ2VydEFzc3Vy
'' SIG '' ZWRJRFJvb3RDQS5jcnQwRQYDVR0fBD4wPDA6oDigNoY0
'' SIG '' aHR0cDovL2NybDMuZGlnaWNlcnQuY29tL0RpZ2lDZXJ0
'' SIG '' QXNzdXJlZElEUm9vdENBLmNybDARBgNVHSAECjAIMAYG
'' SIG '' BFUdIAAwDQYJKoZIhvcNAQEMBQADggEBAHCgv0NcVec4
'' SIG '' X6CjdBs9thbX979XB72arKGHLOyFXqkauyL4hxppVCLt
'' SIG '' pIh3bb0aFPQTSnovLbc47/T/gLn4offyct4kvFIDyE7Q
'' SIG '' Kt76LVbP+fT3rDB6mouyXtTP0UNEm0Mh65ZyoUi0mcud
'' SIG '' T6cGAxN3J0TU53/oWajwvy8LpunyNDzs9wPHh6jSTEAZ
'' SIG '' NUZqaVSwuKFWjuyk1T3osdz9HNj0d1pcVIxv76FQPfx2
'' SIG '' CWiEn2/K2yCNNWAcAgPLILCsWKAOQGPFmCLBsln1VWvP
'' SIG '' J6tsds5vIy30fnFqI2si/xK4VC0nftg62fC2h5b9W9Fc
'' SIG '' rBjDTZ9ztwGpn1eqXijiuZQwgga0MIIEnKADAgECAhAN
'' SIG '' x6xXBf8hmS5AQyIMOkmGMA0GCSqGSIb3DQEBCwUAMGIx
'' SIG '' CzAJBgNVBAYTAlVTMRUwEwYDVQQKEwxEaWdpQ2VydCBJ
'' SIG '' bmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5jb20xITAf
'' SIG '' BgNVBAMTGERpZ2lDZXJ0IFRydXN0ZWQgUm9vdCBHNDAe
'' SIG '' Fw0yNTA1MDcwMDAwMDBaFw0zODAxMTQyMzU5NTlaMGkx
'' SIG '' CzAJBgNVBAYTAlVTMRcwFQYDVQQKEw5EaWdpQ2VydCwg
'' SIG '' SW5jLjFBMD8GA1UEAxM4RGlnaUNlcnQgVHJ1c3RlZCBH
'' SIG '' NCBUaW1lU3RhbXBpbmcgUlNBNDA5NiBTSEEyNTYgMjAy
'' SIG '' NSBDQTEwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIK
'' SIG '' AoICAQC0eDHTCphBcr48RsAcrHXbo0ZodLRRF51NrY0N
'' SIG '' lLWZloMsVO1DahGPNRcybEKq+RuwOnPhof6pvF4uGjwj
'' SIG '' qNjfEvUi6wuim5bap+0lgloM2zX4kftn5B1IpYzTqpyF
'' SIG '' Q/4Bt0mAxAHeHYNnQxqXmRinvuNgxVBdJkf77S2uPoCj
'' SIG '' 7GH8BLuxBG5AvftBdsOECS1UkxBvMgEdgkFiDNYiOTx4
'' SIG '' OtiFcMSkqTtF2hfQz3zQSku2Ws3IfDReb6e3mmdglTca
'' SIG '' arps0wjUjsZvkgFkriK9tUKJm/s80FiocSk1VYLZlDwF
'' SIG '' t+cVFBURJg6zMUjZa/zbCclF83bRVFLeGkuAhHiGPMvS
'' SIG '' GmhgaTzVyhYn4p0+8y9oHRaQT/aofEnS5xLrfxnGpTXi
'' SIG '' UOeSLsJygoLPp66bkDX1ZlAeSpQl92QOMeRxykvq6gby
'' SIG '' lsXQskBBBnGy3tW/AMOMCZIVNSaz7BX8VtYGqLt9MmeO
'' SIG '' reGPRdtBx3yGOP+rx3rKWDEJlIqLXvJWnY0v5ydPpOjL
'' SIG '' 6s36czwzsucuoKs7Yk/ehb//Wx+5kMqIMRvUBDx6z1ev
'' SIG '' +7psNOdgJMoiwOrUG2ZdSoQbU2rMkpLiQ6bGRinZbI4O
'' SIG '' Lu9BMIFm1UUl9VnePs6BaaeEWvjJSjNm2qA+sdFUeEY0
'' SIG '' qVjPKOWug/G6X5uAiynM7Bu2ayBjUwIDAQABo4IBXTCC
'' SIG '' AVkwEgYDVR0TAQH/BAgwBgEB/wIBADAdBgNVHQ4EFgQU
'' SIG '' 729TSunkBnx6yuKQVvYv1Ensy04wHwYDVR0jBBgwFoAU
'' SIG '' 7NfjgtJxXWRM3y5nP+e6mK4cD08wDgYDVR0PAQH/BAQD
'' SIG '' AgGGMBMGA1UdJQQMMAoGCCsGAQUFBwMIMHcGCCsGAQUF
'' SIG '' BwEBBGswaTAkBggrBgEFBQcwAYYYaHR0cDovL29jc3Au
'' SIG '' ZGlnaWNlcnQuY29tMEEGCCsGAQUFBzAChjVodHRwOi8v
'' SIG '' Y2FjZXJ0cy5kaWdpY2VydC5jb20vRGlnaUNlcnRUcnVz
'' SIG '' dGVkUm9vdEc0LmNydDBDBgNVHR8EPDA6MDigNqA0hjJo
'' SIG '' dHRwOi8vY3JsMy5kaWdpY2VydC5jb20vRGlnaUNlcnRU
'' SIG '' cnVzdGVkUm9vdEc0LmNybDAgBgNVHSAEGTAXMAgGBmeB
'' SIG '' DAEEAjALBglghkgBhv1sBwEwDQYJKoZIhvcNAQELBQAD
'' SIG '' ggIBABfO+xaAHP4HPRF2cTC9vgvItTSmf83Qh8WIGjB/
'' SIG '' T8ObXAZz8OjuhUxjaaFdleMM0lBryPTQM2qEJPe36zwb
'' SIG '' SI/mS83afsl3YTj+IQhQE7jU/kXjjytJgnn0hvrV6hqW
'' SIG '' Gd3rLAUt6vJy9lMDPjTLxLgXf9r5nWMQwr8Myb9rEVKC
'' SIG '' hHyfpzee5kH0F8HABBgr0UdqirZ7bowe9Vj2AIMD8liy
'' SIG '' rukZ2iA/wdG2th9y1IsA0QF8dTXqvcnTmpfeQh35k5zO
'' SIG '' CPmSNq1UH410ANVko43+Cdmu4y81hjajV/gxdEkMx1NK
'' SIG '' U4uHQcKfZxAvBAKqMVuqte69M9J6A47OvgRaPs+2ykgc
'' SIG '' GV00TYr2Lr3ty9qIijanrUR3anzEwlvzZiiyfTPjLbnF
'' SIG '' RsjsYg39OlV8cipDoq7+qNNjqFzeGxcytL5TTLL4ZaoB
'' SIG '' dqbhOhZ3ZRDUphPvSRmMThi0vw9vODRzW6AxnJll38F0
'' SIG '' cuJG7uEBYTptMSbhdhGQDpOXgpIUsWTjd6xpR6oaQf/D
'' SIG '' Jbg3s6KCLPAlZ66RzIg9sC+NJpud/v4+7RWsWCiKi9EO
'' SIG '' LLHfMR2ZyJ/+xhCx9yHbxtl5TPau1j/1MIDpMPx0LckT
'' SIG '' etiSuEtQvLsNz3Qbp7wGWqbIiOWCnb5WqxL3/BAPvIXK
'' SIG '' UjPSxyZsq8WhbaM2tszWkPZPubdcMIIG7TCCBNWgAwIB
'' SIG '' AgIQCoDvGEuN8QWC0cR2p5V0aDANBgkqhkiG9w0BAQsF
'' SIG '' ADBpMQswCQYDVQQGEwJVUzEXMBUGA1UEChMORGlnaUNl
'' SIG '' cnQsIEluYy4xQTA/BgNVBAMTOERpZ2lDZXJ0IFRydXN0
'' SIG '' ZWQgRzQgVGltZVN0YW1waW5nIFJTQTQwOTYgU0hBMjU2
'' SIG '' IDIwMjUgQ0ExMB4XDTI1MDYwNDAwMDAwMFoXDTM2MDkw
'' SIG '' MzIzNTk1OVowYzELMAkGA1UEBhMCVVMxFzAVBgNVBAoT
'' SIG '' DkRpZ2lDZXJ0LCBJbmMuMTswOQYDVQQDEzJEaWdpQ2Vy
'' SIG '' dCBTSEEyNTYgUlNBNDA5NiBUaW1lc3RhbXAgUmVzcG9u
'' SIG '' ZGVyIDIwMjUgMTCCAiIwDQYJKoZIhvcNAQEBBQADggIP
'' SIG '' ADCCAgoCggIBANBGrC0Sxp7Q6q5gVrMrV7pvUf+GcAoB
'' SIG '' 38o3zBlCMGMyqJnfFNZx+wvA69HFTBdwbHwBSOeLpvPn
'' SIG '' Z8ZN+vo8dE2/pPvOx/Vj8TchTySA2R4QKpVD7dvNZh6w
'' SIG '' W2R6kSu9RJt/4QhguSssp3qome7MrxVyfQO9sMx6ZAWj
'' SIG '' FDYOzDi8SOhPUWlLnh00Cll8pjrUcCV3K3E0zz09ldQ/
'' SIG '' /nBZZREr4h/GI6Dxb2UoyrN0ijtUDVHRXdmncOOMA3Co
'' SIG '' B/iUSROUINDT98oksouTMYFOnHoRh6+86Ltc5zjPKHW5
'' SIG '' KqCvpSduSwhwUmotuQhcg9tw2YD3w6ySSSu+3qU8DD+n
'' SIG '' igNJFmt6LAHvH3KSuNLoZLc1Hf2JNMVL4Q1OpbybpMe4
'' SIG '' 6YceNA0LfNsnqcnpJeItK/DhKbPxTTuGoX7wJNdoRORV
'' SIG '' bPR1VVnDuSeHVZlc4seAO+6d2sC26/PQPdP51ho1zBp+
'' SIG '' xUIZkpSFA8vWdoUoHLWnqWU3dCCyFG1roSrgHjSHlq8x
'' SIG '' ymLnjCbSLZ49kPmk8iyyizNDIXj//cOgrY7rlRyTlaCC
'' SIG '' fw7aSUROwnu7zER6EaJ+AliL7ojTdS5PWPsWeupWs7Np
'' SIG '' ChUk555K096V1hE0yZIXe+giAwW00aHzrDchIc2bQhpp
'' SIG '' 0IoKRR7YufAkprxMiXAJQ1XCmnCfgPf8+3mnAgMBAAGj
'' SIG '' ggGVMIIBkTAMBgNVHRMBAf8EAjAAMB0GA1UdDgQWBBTk
'' SIG '' O/zyMe39/dfzkXFjGVBDz2GM6DAfBgNVHSMEGDAWgBTv
'' SIG '' b1NK6eQGfHrK4pBW9i/USezLTjAOBgNVHQ8BAf8EBAMC
'' SIG '' B4AwFgYDVR0lAQH/BAwwCgYIKwYBBQUHAwgwgZUGCCsG
'' SIG '' AQUFBwEBBIGIMIGFMCQGCCsGAQUFBzABhhhodHRwOi8v
'' SIG '' b2NzcC5kaWdpY2VydC5jb20wXQYIKwYBBQUHMAKGUWh0
'' SIG '' dHA6Ly9jYWNlcnRzLmRpZ2ljZXJ0LmNvbS9EaWdpQ2Vy
'' SIG '' dFRydXN0ZWRHNFRpbWVTdGFtcGluZ1JTQTQwOTZTSEEy
'' SIG '' NTYyMDI1Q0ExLmNydDBfBgNVHR8EWDBWMFSgUqBQhk5o
'' SIG '' dHRwOi8vY3JsMy5kaWdpY2VydC5jb20vRGlnaUNlcnRU
'' SIG '' cnVzdGVkRzRUaW1lU3RhbXBpbmdSU0E0MDk2U0hBMjU2
'' SIG '' MjAyNUNBMS5jcmwwIAYDVR0gBBkwFzAIBgZngQwBBAIw
'' SIG '' CwYJYIZIAYb9bAcBMA0GCSqGSIb3DQEBCwUAA4ICAQBl
'' SIG '' Kq3xHCcEua5gQezRCESeY0ByIfjk9iJP2zWLpQq1b4UR
'' SIG '' GnwWBdEZD9gBq9fNaNmFj6Eh8/YmRDfxT7C0k8FUFqNh
'' SIG '' +tshgb4O6Lgjg8K8elC4+oWCqnU/ML9lFfim8/9yJmZS
'' SIG '' e2F8AQ/UdKFOtj7YMTmqPO9mzskgiC3QYIUP2S3HQvHG
'' SIG '' 1FDu+WUqW4daIqToXFE/JQ/EABgfZXLWU0ziTN6R3ygQ
'' SIG '' BHMUBaB5bdrPbF6MRYs03h4obEMnxYOX8VBRKe1uNnzQ
'' SIG '' VTeLni2nHkX/QqvXnNb+YkDFkxUGtMTaiLR9wjxUxu2h
'' SIG '' ECZpqyU1d0IbX6Wq8/gVutDojBIFeRlqAcuEVT0cKsb+
'' SIG '' zJNEsuEB7O7/cuvTQasnM9AWcIQfVjnzrvwiCZ85EE8L
'' SIG '' UkqRhoS3Y50OHgaY7T/lwd6UArb+BOVAkg2oOvol/DJg
'' SIG '' ddJ35XTxfUlQ+8Hggt8l2Yv7roancJIFcbojBcxlRcGG
'' SIG '' 0LIhp6GvReQGgMgYxQbV1S3CrWqZzBt1R9xJgKf47Cdx
'' SIG '' VRd/ndUlQ05oxYy2zRWVFjF7mcr4C34Mj3ocCVccAvlK
'' SIG '' V9jEnstrniLvUxxVZE/rptb7IRE2lskKPIJgbaP5t2nG
'' SIG '' j/ULLi49xTcBZU8atufk+EMF/cWuiC7POGT75qaL6vdC
'' SIG '' vHlshtjdNXOCIUjsarfNZzGCBUowggVGAgEBMIGGMHIx
'' SIG '' CzAJBgNVBAYTAkJPMSIwIAYJKoZIhvcNAQkBFhNwaGFy
'' SIG '' bWFrb3pAZ21haWwuY29tMRswGQYDVQQKDBJTb2Z0d2Fy
'' SIG '' ZSBEZXZlbG9wZXIxIjAgBgNVBAMMGVdhbHRlciBQYWJs
'' SIG '' byBUZWxsZXogQXlhbGECEB2YwJKY9+6cSyPYIzfuaAsw
'' SIG '' CQYFKw4DAhoFAKBwMBAGCisGAQQBgjcCAQwxAjAAMBkG
'' SIG '' CSqGSIb3DQEJAzEMBgorBgEEAYI3AgEEMBwGCisGAQQB
'' SIG '' gjcCAQsxDjAMBgorBgEEAYI3AgEVMCMGCSqGSIb3DQEJ
'' SIG '' BDEWBBSKFlD+r0qCD8b18QngdSHcvT+4ezANBgkqhkiG
'' SIG '' 9w0BAQEFAASCAQCO6tCZ76bJzoq3Oh10GH8Rw0GV013+
'' SIG '' SPv48pICbMJpWKO3J6McWwizxQqNC6E0x5LmQbxtfXTU
'' SIG '' rvhWgWANH16oWwm6udNOw5129boDflXY2YvZE5y1jze9
'' SIG '' Jrxco5Nvt47yIk6f8Q2Aw6Yz1At+gnk4p/CNhwiAoYwI
'' SIG '' +9Ezri0ePoyDiNkb1BGG6nU3muBSkBz5qBsVeQW3yJvc
'' SIG '' 0XW+bg7l6b1OQamHxT6xefIH7WNfh4LPyRHfsTL7uIbd
'' SIG '' XAGW8PXNxmo7Hea7SVh19JNOE4OZ/kIVZicymeN+HJM5
'' SIG '' rPvy9lRmIlRLeciAZFV52OGosWZAyElruzmv+eOmtFJS
'' SIG '' VrRhoYIDJjCCAyIGCSqGSIb3DQEJBjGCAxMwggMPAgEB
'' SIG '' MH0waTELMAkGA1UEBhMCVVMxFzAVBgNVBAoTDkRpZ2lD
'' SIG '' ZXJ0LCBJbmMuMUEwPwYDVQQDEzhEaWdpQ2VydCBUcnVz
'' SIG '' dGVkIEc0IFRpbWVTdGFtcGluZyBSU0E0MDk2IFNIQTI1
'' SIG '' NiAyMDI1IENBMQIQCoDvGEuN8QWC0cR2p5V0aDANBglg
'' SIG '' hkgBZQMEAgEFAKBpMBgGCSqGSIb3DQEJAzELBgkqhkiG
'' SIG '' 9w0BBwEwHAYJKoZIhvcNAQkFMQ8XDTI2MDQyMDE1NDc0
'' SIG '' MFowLwYJKoZIhvcNAQkEMSIEICxT8UHjUYAxDZJbkqHJ
'' SIG '' lZQTQkdzKhdAQ4IhKn69KT0QMA0GCSqGSIb3DQEBAQUA
'' SIG '' BIICAAeQfWl2S/t0BtFCJSm5aProbJBvqMld8AyXP5My
'' SIG '' cYdeDSp67cEbq59JZIYuvEBRSzNUXobtdY/cx81N/MTi
'' SIG '' c1vp4t33Xw4rbU2aehr8XtkfKEchQIySOP2usviCUvu0
'' SIG '' Rhpc3rxLpZeMkOPFLlk6wlP3rOI24e29dYvjh54taApT
'' SIG '' 1QFzjC8n3w3DgM8fVeYYZDxJ903e8YAL6nptnzxVevDe
'' SIG '' rn/0OdikJqS98cECVMn4TSN5h/cQR+i2rgE+ru1U76zI
'' SIG '' fwx2YdjBvM5j6EEJGEnSoN04VtxQ8qny1H9zJ9/OGe0j
'' SIG '' ukkv2QaqH15f5R+s3m9JMwZiTEBZz7SXEYYzWr0O76I5
'' SIG '' uyqm15qpjCaF2o0d3u+27a+z31M2NzUnvY+ZeUctesV5
'' SIG '' dlFs9zQDQrCIIp5T/VQd7fzkHVfmrpCCqb7vJROLMre/
'' SIG '' SVnGE10lGDttx5vOgu5n5XqLOBYJiDQ+3Uol7L50l6C6
'' SIG '' VoeY6NGBahbOfxCM9rGNCRzpmwNKHg36zvtuQ6yNSqia
'' SIG '' hD72l1IhL/nfatXRmype/Jx0Ua3J6W0DGNN61i10I4uT
'' SIG '' HIYZnqCRpr2iZh+TQfh+9R0R7ZpnY+CWp28NlrnwYUdk
'' SIG '' XbNqtUPSb6VgdDihTd9md19MQCCJyrRvt9OxFrSXMQ3H
'' SIG '' SI3CiC0yDBVT9h0CTO34P8UUK8Z0
'' SIG '' End signature block
