@echo off
chcp 65001 >nul
cls
echo ================================================================
echo                  OLX PARSER - QUICK START
echo ================================================================
echo.
echo [1] Start parser (continuous mode)
echo [2] Test run (once)
echo [3] Test Telegram
echo [4] View statistics
echo [5] Import models from base.xlsx
echo [6] Exit
echo.
set /p choice="Choose action (1-6): "

if "%choice%"=="1" goto start_continuous
if "%choice%"=="2" goto start_once
if "%choice%"=="3" goto test_telegram
if "%choice%"=="4" goto view_stats
if "%choice%"=="5" goto import_base
if "%choice%"=="6" goto end

:start_continuous
cls
echo ================================================================
echo  STARTING PARSER IN CONTINUOUS MODE
echo ================================================================
echo.
echo Parser will check OLX every 5 minutes
echo Good deals (discount 20%% or more) will be sent to Telegram
echo No duplicates - each ad is processed only once
echo.
echo Press Ctrl+C to stop
echo.
pause
python main.py
goto end

:start_once
cls
echo ================================================================
echo  TEST RUN (ONCE)
echo ================================================================
echo.
python main.py --once
echo.
echo ================================================================
echo  Test run completed!
echo ================================================================
echo.
pause
goto end

:test_telegram
cls
echo ================================================================
echo  TELEGRAM TEST
echo ================================================================
echo.
echo IMPORTANT: Send /start to bot @OLXPARSOLX_bot in Telegram first!
echo.
pause
python test_telegram.py
echo.
pause
goto end

:view_stats
cls
echo ================================================================
echo  PARSER STATISTICS
echo ================================================================
echo.
python view_stats.py
echo.
pause
goto end

:import_base
cls
echo ================================================================
echo  IMPORT MODELS FROM base.xlsx
echo ================================================================
echo.
python import_base.py
echo.
pause
goto end

:end
exit
