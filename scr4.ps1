$sourceFolder = "W:\"
$destinationFolder = "C:\Users\LENOVO\Desktop\ft"
$listFile = "C:\Users\LENOVO\Desktop\ft\BS.txt"

# Read codes, trim whitespace, ignore blanks
$partialCodes = Get-Content $listFile | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }

foreach ($code in $partialCodes) {
    # Use -Like instead of -Filter for more control
    $matches = Get-ChildItem -Path $sourceFolder -File | Where-Object { $_.Name -like "$code*" }

    foreach ($file in $matches) {
        $destinationPath = Join-Path $destinationFolder $file.Name
        Copy-Item $file.FullName -Destination $destinationPath -Force
    }
}

Write-Output "All matching files copied successfully!"
