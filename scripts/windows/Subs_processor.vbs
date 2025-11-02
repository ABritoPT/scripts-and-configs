Option Explicit

const SUBS_FOLDER = "Subs"
const SUB_EXT = "srt"
const SUB_LANG = "eng"

Dim objFSO
Set objFSO = CreateObject("Scripting.FileSystemObject")

Dim topFolderPath
If WScript.Arguments.Count = 0 Then
    topFolderPath = "."
Else
    topFolderPath = WScript.Arguments(0)
End If

If objFSO.FolderExists(topFolderPath) = False Then
    Wscript.Echo "No valid top folder provided: " & topFolderPath
    ExitScript()
End If

Wscript.Echo "Running on top folder " & topFolderPath
Dim topFolder : topFolder = objFSO.GetFolder(topFolderPath)
Dim subsFolder : subsFolder = objFSO.BuildPath(topFolder, SUBS_FOLDER)

If objFSO.FolderExists(subsFolder) = False Then
    Wscript.Echo "No Subs folder found at " & subsFolder
    ExitScript()
End If

Wscript.Echo "Subs folder found at " & subsFolder
Dim epFolder
For Each epFolder in objFSO.GetFolder(subsFolder).SubFolders
    WScript.Echo epFolder.Name

    Dim selectedSubFile
    Set selectedSubFile = Nothing
    Dim subFile
    For Each subFile in epFolder.Files
        If LCase(objFSO.GetExtensionName(subFile.Name)) = SUB_EXT Then
            If InStr(LCase(subFile.Name), SUB_LANG) Then
                If selectedSubFile Is Nothing Then
                    Set selectedSubFile = subFile
                Elseif selectedSubFile.Size < subFile.Size Then
                    Set selectedSubFile = subFile
                End If
            End If
        End If
    Next
    
    If selectedSubFile Is Nothing Then
        WScript.Echo "!! No " & SUB_LANG & " subtitles found"
    Else
        WScript.Echo selectedSubFile.Name
        Dim destSubFileName : destSubFileName = epFolder.Name & "." & SUB_EXT
        objFSO.CopyFile selectedSubFile, objFSO.BuildPath(topFolder, destSubFileName), True
    End If
Next

Function ExitScript()
    WScript.Echo "Press [ENTER] to finish..."
    WScript.StdIn.ReadLine
    WScript.Quit
End Function