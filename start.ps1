# OLX Parser - PowerShell версия для быстрого запуска

function Show-Menu {
    Clear-Host
    Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                  OLX PARSER - БЫСТРЫЙ ЗАПУСК                   ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "[1] 🚀 Запуск парсера (постоянная работа)" -ForegroundColor Green
    Write-Host "[2] 🧪 Тестовый запуск (один раз)" -ForegroundColor Yellow
    Write-Host "[3] 📱 Проверка Telegram" -ForegroundColor Magenta
    Write-Host "[4] 📊 Просмотр статистики" -ForegroundColor Blue
    Write-Host "[5] 📦 Импорт базы моделей" -ForegroundColor White
    Write-Host "[6] ❌ Выход" -ForegroundColor Red
    Write-Host ""
}

function Start-Continuous {
    Clear-Host
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host " ЗАПУСК ПАРСЕРА В РЕЖИМЕ ПОСТОЯННОЙ РАБОТЫ" -ForegroundColor Cyan
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚡ Парсер будет проверять OLX каждые 5 минут" -ForegroundColor Green
    Write-Host "💰 Выгодные предложения (скидка ≥20%) будут отправлены в Telegram" -ForegroundColor Green
    Write-Host "🔄 Дубли не отправляются - каждое объявление обрабатывается 1 раз" -ForegroundColor Green
    Write-Host ""
    Write-Host "Для остановки нажмите Ctrl+C" -ForegroundColor Yellow
    Write-Host ""
    pause
    python main.py
}

function Start-Once {
    Clear-Host
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host " ТЕСТОВЫЙ ЗАПУСК (ОДИН РАЗ)" -ForegroundColor Cyan
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    python main.py --once
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host " Тестовый запуск завершен!" -ForegroundColor Green
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    pause
}

function Test-Telegram {
    Clear-Host
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host " ПРОВЕРКА TELEGRAM" -ForegroundColor Cyan
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚠️  ВАЖНО: Перед тестом напишите боту /start в Telegram!" -ForegroundColor Yellow
    Write-Host ""
    pause
    python test_telegram.py
    Write-Host ""
    pause
}

function View-Stats {
    Clear-Host
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host " СТАТИСТИКА ПАРСЕРА" -ForegroundColor Cyan
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    python view_stats.py
    Write-Host ""
    pause
}

function Import-Base {
    Clear-Host
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host " ИМПОРТ БАЗЫ МОДЕЛЕЙ" -ForegroundColor Cyan
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    python import_base.py
    Write-Host ""
    pause
}

# Главный цикл
do {
    Show-Menu
    $choice = Read-Host "Выберите действие (1-6)"
    
    switch ($choice) {
        '1' { Start-Continuous }
        '2' { Start-Once }
        '3' { Test-Telegram }
        '4' { View-Stats }
        '5' { Import-Base }
        '6' { exit }
        default { 
            Write-Host "Неверный выбор. Попробуйте снова." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
} while ($choice -ne '6')
