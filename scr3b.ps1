# Set your source and destination folders



$sourceFolder = "X:\"
$destinationRoot = "C:\Users\LENOVO\Desktop\ft"
$listFile = "C:\Users\LENOVO\Desktop\ft\Bills.txt"

# Read each line from Bills.txt
$lines = Get-Content $listFile

foreach ($line in $lines) {
    # Split line into bill number + item codes
    $parts = $line.Split(",")
    $billNo = $parts[0].Trim()
    $itemCodes = $parts[1..($parts.Length - 1)]

    # Create folder for this bill
    $billFolder = Join-Path $destinationRoot "Bill_$billNo"
    if (-not (Test-Path $billFolder)) {
        New-Item -ItemType Directory -Path $billFolder | Out-Null
    }

    # Copy all matching files for each item code
    foreach ($code in $itemCodes) {
        $matches = Get-ChildItem -Path $sourceFolder -File | Where-Object { $_.Name -like "$code*" }
        foreach ($file in $matches) {
            $destinationPath = Join-Path $billFolder $file.Name
            Copy-Item $file.FullName -Destination $destinationPath -Force
        }
    }
}

Write-Output "✅ All bills processed: item photos copied into their respective Bill folders!"

