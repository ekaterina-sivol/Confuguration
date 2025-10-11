@echo off
py "ETAB2.py" --vfs-path C:\vfs --prompt "win_test> " --startup-script "startup.txt"
pause

py "ETAB2.py" --config-file "config.ini"
pause