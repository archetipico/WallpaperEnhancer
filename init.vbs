proceed = MsgBox( "Do you want me to create a file in " &_
    "C:\Users\%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup for you?", _
    vbSystemModal + vbYesNo, "Initializer" )

If proceed = vbYes Then
    Set shell = CreateObject( "WScript.Shell" )
    user = shell.ExpandEnvironmentStrings( "%USERPROFILE%" )
    path = shell.CurrentDirectory

    Set file = CreateObject( "Scripting.FileSystemObject" )
    Set writer = file.CreateTextFile( user & "\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\job.vbs", true )
    writer.WriteLine( "Set shell = CreateObject( " & Chr(34) & "WScript.Shell" & Chr(34) & ")" )
    writer.WriteLine( "shell.run " & Chr(34) & "pythonw.exe " & shell.CurrentDirectory & "\enhancer.py" & Chr(34)  )
    writer.Close

    restart = Msgbox( "Do you want to restart your machine so the script can work?", _
        vbSystemModal + vbYesNo, "Restart" )
    If restart = vbYes Then
        shell.Run "C:\WINDOWS\system32\shutdown.exe -r -t 0"
    Else
        WScript.Quit
    End If
Else
    MsgBox "Process aborted. Restart the process or manually set the variables.", vbSystemModal + vbOKOnly, "Aborted"
End If