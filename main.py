#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from flask import Flask, render_template_string, request, jsonify

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Импортируем наш модуль
from core.keyword_manager import KeywordManager
from core.keyword_manager import KeywordManager
from core.data_parser import DataParser

# Создаем Flask приложение и менеджер ключевых слов
app = Flask(__name__)
keyword_manager = KeywordManager()

# Создаем Flask приложение и менеджеры
app = Flask(__name__)
keyword_manager = KeywordManager()
data_parser = DataParser()

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

        <!-- Импорт данных -->
        <div class="section">
            <h3>📥 Импорт данных</h3>
            
            <!-- Загрузка файлов -->
            <div class="form-group">
                <label>📁 Загрузка файлов (CSV, Excel, TXT, JSON):</label>
                <input type="file" id="file-input" accept=".csv,.txt,.xlsx,.xls,.json" style="margin: 10px 0;">
                <br>
                <button onclick="uploadFile()">Загрузить файл</button>
                <div id="upload-status" style="margin-top: 10px; font-style: italic;"></div>
            </div>
            
            <hr>
            
            <!-- Импорт из текста -->
            <div class="form-group">
                <label>📝 Импорт из текста (разные разделители):</label>
                <textarea id="import-text" placeholder="Вставьте данные (каждое ключевое слово с новой строки или через запятую)" rows="4" style="width: 100%;"></textarea>
                <br>
                <label>Разделитель:</label>
                <select id="delimiter">
                    <option value="\n">Новая строка</option>
                    <option value=",">Запятая</option>
                    <option value=";">Точка с запятой</option>
                    <option value="\t">Табуляция</option>
                </select>
                <button onclick="importFromText()">Импортировать из текста</button>
            </div>
            
            <hr>
            
            <!-- Импорт с URL -->
            <div class="form-group">
                <label>🌐 Импорт с веб-страницы:</label>
                <input type="text" id="url-input" placeholder="https://example.com" style="width: 300px;">
                <button onclick="importFromURL()">Импортировать с URL</button>
            </div>
            
            <div class="form-group">
                <small>
                    <strong>Поддерживаемые форматы:</strong>
                    <ul>
                        <li><strong>CSV</strong> - файлы с разделителями (запятая, точка с запятой)</li>
                        <li><strong>Excel</strong> - .xlsx и .xls файлы</li>
                        <li><strong>TXT</strong> - текстовые файлы (каждое ключевое слово с новой строки)</li>
                        <li><strong>JSON</strong> - массивы ключевых слов в JSON формате</li>
                    </ul>
                </small>
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

        // Функция импорта из текста
        function importFromText() {
            const text = document.getElementById('import-text').value.trim();
            const delimiter = document.getElementById('delimiter').value.replace('\\n', '\n').replace('\\t', '\t');
            
            if (!text) {
                alert('Введите текст для импорта!');
                return;
            }

            fetch('/api/import/text', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    text: text,
                    delimiter: delimiter
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.errors && data.errors.length > 0) {
                    alert('Ошибки: ' + data.errors.join(', '));
                } else {
                    alert(`Успешно импортировано: ${data.imported} ключевых слов\\nДубликатов пропущено: ${data.duplicates}`);
                    location.reload();
                }
            })
            .catch(error => {
                alert('Ошибка импорта: ' + error);
            });
        }

        // Функция импорта с URL
        function importFromURL() {
            const url = document.getElementById('url-input').value.trim();
            
            if (!url) {
                alert('Введите URL!');
                return;
            }

            // Показываем индикатор загрузки
            document.getElementById('url-input').disabled = true;
            
            fetch('/api/import/url', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: url})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('url-input').disabled = false;
                
                if (data.errors && data.errors.length > 0) {
                    alert('Ошибки: ' + data.errors.join(', '));
                } else {
                    alert(`Успешно импортировано с ${url}:\\n${data.imported} ключевых слов\\nДубликатов: ${data.duplicates}`);
                    location.reload();
                }
            })
            .catch(error => {
                document.getElementById('url-input').disabled = false;
                alert('Ошибка загрузки: ' + error);
            });
        }

        // Функция загрузки файла
        function uploadFile() {
            const fileInput = document.getElementById('file-input');
            const statusDiv = document.getElementById('upload-status');
            
            if (!fileInput.files || fileInput.files.length === 0) {
                alert('Выберите файл для загрузки!');
                return;
            }
            
            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append('file', file);
            
            // Показываем статус загрузки
            statusDiv.innerHTML = '⏳ Загрузка и обработка файла...';
            statusDiv.style.color = '#007bff';
            
            fetch('/api/import/file', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    statusDiv.innerHTML = `✅ Успешно загружено: ${data.imported} ключевых слов (дубликатов: ${data.duplicates})`;
                    statusDiv.style.color = '#28a745';
                    
                    // Очищаем поле файла
                    fileInput.value = '';
                    
                    // Перезагружаем страницу через 2 секунды
                    setTimeout(() => location.reload(), 2000);
                } else {
                    statusDiv.innerHTML = `❌ Ошибки: ${data.errors.join(', ')}`;
                    statusDiv.style.color = '#dc3545';
                }
            })
            .catch(error => {
                statusDiv.innerHTML = `❌ Ошибка загрузки: ${error}`;
                statusDiv.style.color = '#dc3545';
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

@app.route('/api/import/text', methods=['POST'])
def import_from_text():
    """API для импорта из текста"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        delimiter = data.get('delimiter', '\n')
        
        # Парсим текст
        parse_result = data_parser.parse_text(text, delimiter)
        
        if parse_result.errors:
            return jsonify({
                'success': False,
                'errors': parse_result.errors
            }), 400
        
        # Добавляем ключевые слова
        import_stats = keyword_manager.add_keywords_bulk(parse_result.keywords)
        
        return jsonify({
            'success': True,
            'imported': import_stats['added'],
            'duplicates': import_stats['duplicates'],
            'total_parsed': parse_result.total_processed,
            'metadata': parse_result.metadata
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Ошибка импорта: {str(e)}']
        }), 500

@app.route('/api/import/url', methods=['POST'])
def import_from_url():
    """API для импорта с веб-страницы"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({
                'success': False,
                'errors': ['URL не указан']
            }), 400
        
        # Парсим URL
        parse_result = data_parser.parse_url_content(url)
        
        if parse_result.errors:
            return jsonify({
                'success': False,
                'errors': parse_result.errors
            }), 400
        
        # Добавляем ключевые слова (ограничиваем количество для безопасности)
        limited_keywords = parse_result.keywords[:100]  # Максимум 100 ключевых слов с одного URL
        import_stats = keyword_manager.add_keywords_bulk(limited_keywords)
        
        return jsonify({
            'success': True,
            'imported': import_stats['added'],
            'duplicates': import_stats['duplicates'],
            'total_parsed': len(limited_keywords),
            'url': url,
            'metadata': parse_result.metadata
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Ошибка импорта с URL: {str(e)}']
        }), 500

@app.route('/api/parser/formats')
def get_supported_formats():
    """API для получения поддерживаемых форматов"""
    return jsonify({
        'formats': data_parser.get_supported_formats(),
        'description': {
            '.csv': 'Файлы с разделителями (запятая, точка с запятой)',
            '.txt': 'Текстовые файлы',
            '.xlsx': 'Excel файлы (новый формат)',
            '.xls': 'Excel файлы (старый формат)', 
            '.json': 'JSON файлы с массивами ключевых слов'
        }
    })

@app.route('/api/import/file', methods=['POST'])
def import_from_file():
    """API для импорта из загруженного файла"""
    try:
        # Проверяем наличие файла
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'errors': ['Файл не выбран']
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'errors': ['Имя файла не указано']
            }), 400
        
        # Сохраняем файл временно
        import tempfile
        import os
        
        # Создаем временную папку если её нет
        temp_dir = '/app/data/temp'
        os.makedirs(temp_dir, exist_ok=True)
        
        # Сохраняем файл
        temp_path = os.path.join(temp_dir, file.filename)
        file.save(temp_path)
        
        try:
            # Автоматически определяем формат и парсим
            parse_result = data_parser.auto_detect_format(temp_path)
            
            if parse_result.errors:
                return jsonify({
                    'success': False,
                    'errors': parse_result.errors
                }), 400
            
            # Добавляем ключевые слова
            import_stats = keyword_manager.add_keywords_bulk(parse_result.keywords)
            
            return jsonify({
                'success': True,
                'imported': import_stats['added'],
                'duplicates': import_stats['duplicates'],
                'errors_count': import_stats['errors'],
                'total_parsed': parse_result.total_processed,
                'file_name': file.filename,
                'source_type': parse_result.source_type,
                'metadata': parse_result.metadata
            })
            
        finally:
            # Удаляем временный файл
            try:
                os.remove(temp_path)
            except:
                pass
        
    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Ошибка обработки файла: {str(e)}']
        }), 500

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