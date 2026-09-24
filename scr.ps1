# Set your source and destination folders
$sourceFolder = "C:\Users\LENOVO\Desktop\5-no"
$destinationFolder = "C:\Users\LENOVO\Desktop\ASD"
$listFile = "C:\Users\LENOVO\Desktop\ASD\BEW.txt"  # Text file containing the filenames

# Read the file names from the text file
$fileNames = Get-Content $listFile

# Copy the matching files to the destination folder
foreach ($file in $fileNames) {
    $sourcePath = Join-Path $sourceFolder $file
    $destinationPath = Join-Path $destinationFolder $file
    
    if (Test-Path $sourcePath) {
        Copy-Item $sourcePath -Destination $destinationPath
    }
}
Write-Output "Files copied successfully!"
