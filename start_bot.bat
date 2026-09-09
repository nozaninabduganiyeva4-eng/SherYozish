@echo off
chcp 65001 > nul
echo ==============================================
echo        Shoir AI Telegram Bot
echo ==============================================
echo.

:: Python buyrug'ini aniqlash
where python >nul 2>nul
if %errorlevel% equ 0 (
    set PY_CMD=python
) else (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        set PY_CMD=py
    ) else if exist "%LocalAppData%\Programs\Python\Python312\python.exe" (
        set PY_CMD="%LocalAppData%\Programs\Python\Python312\python.exe"
    ) else (
        echo [DIQQAT] Kompyuteringizda Python topilmadi!
        echo Iltimos, https://www.python.org saytidan Python-ni yuklab oling
        echo va o'rnatishda "Add Python to PATH" katakchasiga belgi qo'ying.
        echo.
        pause
        exit /b
    )
)

echo 1. Kutubxonalar tekshirilmoqda va o'rnatilmoqda...
%PY_CMD% -m pip install -r requirements_poem.txt
if %errorlevel% neq 0 (
    echo.
    echo [XATOLIK] Kutubxonalarni o'rnatishda xatolik yuz berdi.
    pause
    exit /b
)

echo.
echo 2. Bot ishga tushirilmoqda...
%PY_CMD% poem_bot.py
pause

