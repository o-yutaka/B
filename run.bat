@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

if "%MODEL%"=="" set MODEL=mistral
if "%OLLAMA_URL%"=="" set OLLAMA_URL=http://localhost:11434/api/generate
if "%AUTO_LOOP%"=="" set AUTO_LOOP=true

echo [BLACK ORIGIN] 起動準備を開始します...

if not exist .venv\Scripts\python.exe (
  echo 仮想環境が未作成です。install.bat を先に実行してください。
  pause
  exit /b 1
)

call .venv\Scripts\activate

where ollama >nul 2>nul
if errorlevel 1 (
  echo Ollama が見つかりません。https://ollama.com からインストールしてください。
  pause
  exit /b 1
)

tasklist | find /I "ollama" >nul
if errorlevel 1 (
  echo Ollama サーバーを起動します...
  start "Ollama" /MIN ollama serve
) else (
  echo Ollama プロセスは起動済みです。
)

echo Ollama 準備待機中...
set /a RETRY=0
:wait_ollama
curl -s http://localhost:11434/api/tags >nul 2>nul
if errorlevel 1 (
  set /a RETRY+=1
  if !RETRY! GEQ 30 (
    echo Ollama の起動確認に失敗しました。ollama serve を手動確認してください。
    pause
    exit /b 1
  )
  timeout /t 2 >nul
  goto wait_ollama
)

echo モデル確認: %MODEL%
ollama list | find /I "%MODEL%" >nul || ollama pull %MODEL%
if errorlevel 1 (
  echo モデル取得に失敗しました。ネットワーク接続またはモデル名を確認してください。
  pause
  exit /b 1
)

echo FastAPI サーバーを起動します...
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
if errorlevel 1 (
  echo アプリ起動に失敗しました。
  pause
  exit /b 1
)
