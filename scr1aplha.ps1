# Set your source and destination folders
$sourceFolder = "Y:\"
$destinationFolder = "C:\Users\LENOVO\Desktop\ft"
$listFile = "C:\Users\LENOVO\Desktop\ft\BS.txt"  # Text file containing partial codes like 12345

# Read the partial codes from the text file
$partialCodes = Get-Content $listFile

# Loop through each partial code
foreach ($code in $partialCodes) {
    # Search for matching files in the source folder
    $matches = Get-ChildItem -Path $sourceFolder -Filter "$code*" -File

    # If matches found, copy all of them
    if ($matches.Count -gt 0) {
        foreach ($fileToCopy in $matches) {
            $destinationPath = Join-Path $destinationFolder $fileToCopy.Name
            Copy-Item $fileToCopy.FullName -Destination $destinationPath
        }
    }
    else {
        # Output the code that wasn't found
        Write-Output "NOT FOUND"
        Write-Output "$code"
    }
}

Write-Output "All matching files copied successfully!"
