Sheet1

    Sub Worksheet_Activate()
    '
    '
    '
    Dim r As Range
    For Each r In Range("d1:d150")
        If r.Value2 <> "" Then
            If r = 0# Then r.EntireRow.Hidden = True
        End If
        Next
    End Sub

ThisWOrkbook

    Private Sub Workbook_BeforeSave(ByVal SaveAsUI As Boolean, Cancel As Boolean)
        Call Sheet4.autohiddenrow
        Call Sheet2.Worksheet_Activate
    End Sub

    Private Sub Workbook_Open()
        Call Sheet4.autohiddenrow
        Call Sheet2.Worksheet_Activate
    End Sub

数据透视图
    
    选择数据透视表中的单元格，按F11 或者 Alt+F1


