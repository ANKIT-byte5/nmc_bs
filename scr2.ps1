# Set your source and destination folders
$sourceFolder = "W:\"
$destinationFolder = "C:\Users\LENOVO\Desktop\ft"
$listFile = "C:\Users\LENOVO\Desktop\ft\BS.txt"  # Text file containing partial codes like 12345

# Read the partial codes from the text file
$partialCodes = Get-Content $listFile

# Loop through each partial code
foreach ($code in $partialCodes) {
    # Search for matching files in the source folder
    $matches = Get-ChildItem -Path $sourceFolder -Filter "$code*" -File

    # If matches found, copy the first one
    if ($matches.Count -gt 0) {
        $fileToCopy = $matches[0]
        $destinationPath = Join-Path $destinationFolder $fileToCopy.Name
        Copy-Item $fileToCopy.FullName -Destination $destinationPath
    }
}

Write-Output "Matching files copied successfully!"
