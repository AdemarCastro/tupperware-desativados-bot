$exclude = @("venv", "tupperware-desativados-bot.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "tupperware-desativados-bot.zip" -Force