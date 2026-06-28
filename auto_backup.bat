@echo off
cd /d "C:\Users\3D_OCT\Documents\Antigravity"
git add .
git commit -m "Backup automatico diario: %date% %time%"
git push
