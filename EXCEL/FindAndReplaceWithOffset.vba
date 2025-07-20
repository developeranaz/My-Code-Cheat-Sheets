Sub FlexibleFindAndReplaceWithOffset()
    Dim FINDCELL As String
    Dim REPLACECELL As Variant
    Dim ColumnToFind As String
    Dim ColumnToReplace As String
    Dim RowOffset As Long
    Dim lastRow As Long, i As Long
    Dim targetRow As Long
    
    ' === Editable Settings ===
    FINDCELL = "9898"
    REPLACECELL = 1002
    ColumnToFind = "C"
    ColumnToReplace = "F"
    RowOffset = 9  ' Example: B1 => D12 (1+11)
    ' =========================
    
    lastRow = Cells(Rows.Count, ColumnToFind).End(xlUp).Row
    
    For i = 1 To lastRow
        If InStr(Cells(i, ColumnToFind).Value, FINDCELL) > 0 Then
            targetRow = i + RowOffset
            If targetRow <= Rows.Count Then
                Cells(targetRow, Columns(ColumnToReplace).Column).Value = REPLACECELL
            End If
        End If
    Next i
End Sub
