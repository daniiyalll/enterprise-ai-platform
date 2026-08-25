# Convert all bg-*.jpg files under frontend/assets/backgrounds to WebP (lossy quality 80)
# Requirements: ImageMagick (magick) or cwebp (libwebp) installed and on PATH.

$src = Join-Path -Path (Get-Location) -ChildPath "frontend\assets\backgrounds"
Get-ChildItem -Path $src -Filter "bg-*.jpg" | ForEach-Object {
    $jpg = $_.FullName
    $webp = [System.IO.Path]::ChangeExtension($jpg, ".webp")

    if (Get-Command magick -ErrorAction SilentlyContinue) {
        magick "${jpg}" -strip -resize 1600x900^ -gravity center -extent 1600x900 -quality 80 "${webp}"
    }
    elseif (Get-Command cwebp -ErrorAction SilentlyContinue) {
        # Create a temp resized jpg then convert
        $temp = Join-Path $src "tmp_$($_.Name)"
        magick "${jpg}" -resize 1600x900^ -gravity center -extent 1600x900 "${temp}" 2>$null
        cwebp -q 80 "${temp}" -o "${webp}"
        Remove-Item "${temp}"
    }
    else {
        Write-Host "Neither ImageMagick nor cwebp found. Install one to run conversions." -ForegroundColor Yellow
    }
}

Write-Host "Conversion script finished. Check frontend/assets/backgrounds for .webp files." -ForegroundColor Green
