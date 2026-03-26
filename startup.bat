@echo off
chcp 65001 > nul
setlocal

if not exist .venv\Scripts\python.exe (
  call install.bat
)

call run.bat
