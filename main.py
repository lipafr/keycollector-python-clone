#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from flask import Flask, render_template_string, request, jsonify

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Импортируем наш модуль
from core.keyword_manager import KeywordManager

# Создаем Flask приложение и менеджер ключевых слов
app = Flask(__name__)
keyword_manager = KeywordManager()

# HTML шаблон с интерфейсом для работы с ключевыми словами
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
            margin: 20px; 
            background: #f5f5f5; 
        }
        .container { 
            background: white; 
            padding: 30px; 
            border-radius: 10px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 { color: #333; text-align: center; }
        .section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        .form-group { margin: 10px 0; }
        input, textarea, button { padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #007bff; color: white; cursor: pointer; }
        button:hover { background: #0056b3; }
        .keyword-list { max-height: 300px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; }
        .keyword-item { padding: 5px; border-bottom: 1px solid #eee; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .stat-card { background: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; }
        .stat-number { font-size: 24px; font-weight: bold; color: #007bff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔑 KeyCollector Python Clone</h1>
        
        <!-- Статистика -->
        <div class="section">
            <h3>📊 Статистика</h3>
            <div class="stats" id="stats">
                <div class="stat-card">
                    <div class="stat-number" id="total-keywords">{{ stats.get('total', 0) }}</div>
                    <div>Всего ключевых слов</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="avg-words">{{ "%.1f"|format(stats.get('avg_word_count', 0)) }}</div>
                    <div>Среднее слов в фразе</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="categories">{{ stats.get('categories', 0) }}</div>
                    <div>Категорий</div>
                </div>
            </div>
        </div>

        <!-- Добавление ключевых слов -->
        <div class="section">
            <h3>➕ Добавить ключевые слова</h3>
            <div class="form-group">
                <textarea id="keywords-input" placeholder="Введите ключевые слова (каждое с новой строки)" rows="5" style="width: 100%;"></textarea>
            </div>
            <button onclick="addKeywords()">Добавить ключевые слова</button>
            <button onclick="clearAll()">Очистить все</button>
        </div>

        <!-- Поиск и фильтрация -->
        <div class="section">
            <h3>🔍 Поиск и фильтрация</h3>
            <div class="form-group">
                <input type="text" id="search-input" placeholder="Поиск по ключевым словам" style="width: 300px;">
                <button onclick="searchKeywords()">Найти</button>
                <button onclick="showAll()">Показать все</button>
            </div>
        </div>

        <!-- Список ключевых слов -->
        <div class="section">
            <h3>📝 Ключевые слова ({{ keywords|length }})</h3>
            <div class="keyword-list" id="keyword-list">
                {% for keyword in keywords %}
                <div class="keyword-item">
                    <strong>{{ keyword.text }}</strong> 
                    <small>(слов: {{ keyword.word_count() }}, добавлено: {{ keyword.added_date.strftime('%H:%M') }})</small>
                </div>
                {% endfor %}
            </div>
        </div>

    </div>

    <script>
        // Функция добавления ключевых слов
        function addKeywords() {
            const input = document.getElementById('keywords-input');
            const keywords = input.value.trim().split('\\n').filter(k => k.trim());
            
            if (keywords.length === 0) {
                alert('Введите ключевые слова!');
                return;
            }

            fetch('/api/keywords', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({keywords: keywords})
            })
            .then(response => response.json())
            .then(data => {
                alert(`Добавлено: ${data.added}, Дубликатов: ${data.duplicates}`);
                location.reload();
            });
        }

        // Функция поиска
        function searchKeywords() {
            const query = document.getElementById('search-input').value;
            
            fetch(`/api/search?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                displayKeywords(data.keywords);
            });
        }

        // Показать все ключевые слова
        function showAll() {
            location.reload();
        }

        // Очистить все ключевые слова
        function clearAll() {
            if (confirm('Удалить все ключевые слова?')) {
                fetch('/api/clear', {method: 'DELETE'})
                .then(() => location.reload());
            }
        }

        // Отображение ключевых слов
        function displayKeywords(keywords) {
            const container = document.getElementById('keyword-list');
            container.innerHTML = '';
            
            keywords.forEach(kw => {
                const div = document.createElement('div');
                div.className = 'keyword-item';
                div.innerHTML = `<strong>${kw.text}</strong> <small>(слов: ${kw.word_count})</small>`;
                container.appendChild(div);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Главная страница с интерфейсом управления ключевыми словами"""
    stats = keyword_manager.get_statistics()
    return render_template_string(HTML_TEMPLATE, 
                                keywords=keyword_manager.keywords, 
                                stats=stats)

@app.route('/api/keywords', methods=['POST'])
def add_keywords():
    """API для добавления ключевых слов"""
    data = request.get_json()
    keywords = data.get('keywords', [])
    
    stats = keyword_manager.add_keywords_bulk(keywords)
    return jsonify(stats)

@app.route('/api/search')
def search_keywords():
    """API для поиска ключевых слов"""
    query = request.args.get('q', '')
    found_keywords = keyword_manager.find_keywords(query)
    
    # Преобразуем в словари для JSON
    keywords_data = []
    for kw in found_keywords:
        keywords_data.append({
            'text': kw.text,
            'word_count': kw.word_count(),
            'frequency': kw.frequency,
            'category': kw.category
        })
    
    return jsonify({'keywords': keywords_data})

@app.route('/api/clear', methods=['DELETE'])
def clear_keywords():
    """API для очистки всех ключевых слов"""
    keyword_manager.clear_all()
    return jsonify({'status': 'cleared'})

@app.route('/api/stats')
def get_stats():
    """API для получения статистики"""
    return jsonify(keyword_manager.get_statistics())

@app.route('/api/export')
def export_keywords():
    """API для экспорта ключевых слов"""
    df = keyword_manager.to_dataframe()
    return jsonify({
        'keywords': df.to_dict('records'),
        'total': len(df)
    })

if __name__ == '__main__':
    print("🚀 Запуск KeyCollector Python Clone...")
    print("📁 Рабочая директория:", os.getcwd())
    print("🌐 Веб-интерфейс: http://localhost:5000")
    print("📊 API endpoints:")
    print("   POST /api/keywords - добавить ключевые слова")
    print("   GET  /api/search - поиск ключевых слов") 
    print("   GET  /api/stats - статистика")
    print("   GET  /api/export - экспорт данных")
    print("⏹️  Для остановки нажмите Ctrl+C")
    
    app.run(host='0.0.0.0', port=5000, debug=True)