@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo [BLACK ORIGIN] インストールを開始します...

where python >nul 2>nul
if errorlevel 1 (
  where py >nul 2>nul
  if errorlevel 1 (
    echo Python が見つかりません。Python 3.11 以上をインストールしてください。
    pause
    exit /b 1
  ) else (
    set "PY_CMD=py -3"
  )
) else (
  set "PY_CMD=python"
)

echo Python 実行コマンド: %PY_CMD%

%PY_CMD% -m ensurepip --upgrade
if errorlevel 1 (
  echo ensurepip に失敗しました。
  pause
  exit /b 1
)

%PY_CMD% -m pip install --upgrade pip
if errorlevel 1 (
  echo pip の更新に失敗しました。
  pause
  exit /b 1
)

if not exist .venv (
  %PY_CMD% -m venv .venv
  if errorlevel 1 (
    echo 仮想環境の作成に失敗しました。
    pause
    exit /b 1
  )
)

call .venv\Scripts\activate
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo 依存関係のインストールに失敗しました。
  pause
  exit /b 1
)

echo インストールが完了しました。run.bat をダブルクリックして起動してください。
pause
