#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from flask import Flask, render_template_string

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Создаем Flask приложение
app = Flask(__name__)

# Простая HTML страница
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KeyCollector Python Clone</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 50px; 
            background: #f5f5f5; 
        }
        .container { 
            background: white; 
            padding: 30px; 
            border-radius: 10px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
        }
        h1 { color: #333; }
        .status { color: #28a745; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>KeyCollector Python Clone</h1>
        <p class="status">Приложение запущено успешно!</p>
        <p><strong>Версия:</strong> 0.1.0</p>
        <p><strong>Статус:</strong> Готов к разработке</p>
        <p><strong>Docker:</strong> Работает</p>
        <hr>
        <h3>Следующие шаги:</h3>
        <ul>
            <li>Настройка GitHub</li>
            <li>Создание модулей</li>
            <li>Разработка функционала</li>
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/status')
def status():
    return {
        "status": "OK",
        "version": "0.1.0",
        "message": "KeyCollector Python Clone работает!"
    }

if __name__ == '__main__':
    print("Запуск KeyCollector Python Clone...")
    print("Рабочая директория:", os.getcwd())
    print("Веб-интерфейс: http://localhost:5000")
    print("API статус: http://localhost:5000/status")
    print("Для остановки нажмите Ctrl+C")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )