# Set the folder path (edit this as needed)
$folderPath = "C:\Users\LENOVO\Desktop\ft\rajat bhai"

# Set the output file path
$outputFile = "C:\Users\LENOVO\Desktop\ft\output.txt"

# Get the list of file names (not folders), and save to a .txt file
Get-ChildItem -Path $folderPath -File | Select-Object -ExpandProperty Name | Out-File -FilePath $outputFile -Encoding UTF8
