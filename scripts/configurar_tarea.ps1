$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c c:\Ideas\radar-alertas\run_diario.bat" -WorkingDirectory "c:\Ideas\radar-alertas"
$t1 = New-ScheduledTaskTrigger -Daily -At 9:00AM
$t2 = New-ScheduledTaskTrigger -Daily -At 2:00PM
$t3 = New-ScheduledTaskTrigger -Daily -At 6:30PM
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Set-ScheduledTask -TaskName "RadarAlertasDiario" -Trigger @($t1, $t2, $t3) -Action $action -Settings $settings
Write-Output "Tarea programada actualizada con éxito a 09:00, 14:00 y 18:30."
