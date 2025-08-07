#!/usr/bin/env python3
"""Тест модуля keyword_manager"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.keyword_manager import KeywordManager, Keyword

def test_keyword_manager():
    """Простой тест модуля"""
    print("🧪 Тестирование KeywordManager...")
    
    # Создаем менеджер
    manager = KeywordManager()
    
    # Тестовые данные
    test_keywords = [
        "купить телефон",
        "iPhone 15 цена",
        "android смартфон",
        "мобильный телефон",
        "смартфон недорого"
    ]
    
    # Добавляем ключевые слова
    stats = manager.add_keywords_bulk(test_keywords)
    print(f"✅ Добавлено: {stats}")
    
    # Статистика
    print(f"📊 Статистика: {manager.get_statistics()}")
    
    # Поиск
    found = manager.find_keywords("телефон")
    print(f"🔍 Найдено по 'телефон': {len(found)} результатов")
    
    # Экспорт в DataFrame
    df = manager.to_dataframe()
    print(f"📄 DataFrame: {df.shape[0]} строк, {df.shape[1]} колонок")
    
    print("✅ Тест завершен успешно!")

if __name__ == "__main__":
    test_keyword_manager()