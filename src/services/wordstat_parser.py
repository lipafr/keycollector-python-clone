#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой тест - добавляет в sys.path и импортирует правильно
"""

import sys
import os

# Добавляем папки в путь поиска модулей
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'services'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'core'))

def simple_test():
    """Простой тест добавления всех ключевых слов"""
    
    print("🧪 ПРОСТОЙ ФИНАЛЬНЫЙ ТЕСТ")
    print("="*50)
    
    try:
        # Пробуем импорт
        print("🔍 Попытка импорта...")
        
        # Импортируем напрямую из папок
        from wordstat_parser import WordstatParser
        from keyword_manager import KeywordManager, Keyword
        
        print("✅ Импорты успешны!")
        
        # Создаем объекты
        parser = WordstatParser()
        manager = KeywordManager()
        
        print("✅ Объекты созданы!")
        
        # Загружаем данные
        parser.parse_file("data/input/геологоразведка wordstat.xlsx")
        
        print(f"📁 Загружено: {len(parser.keywords)} ключевых слов")
        
        # Показываем первые 3
        print(f"\n🔍 Первые 3 ключевых слова:")
        for i, kw_data in enumerate(parser.keywords[:3]):
            keyword = kw_data.get('keyword', '')
            frequency = kw_data.get('frequency', 0)
            print(f"   {i+1}. '{keyword}' → {frequency}")
        
        # Добавляем ВСЕ в менеджер
        print(f"\n🚀 Добавляем все ключевые слова...")
        
        added = 0
        for kw_data in parser.keywords:
            keyword_text = kw_data.get('keyword', '').strip()
            frequency = kw_data.get('frequency', 0)
            
            if keyword_text:
                success = manager.add_keyword(
                    keyword=keyword_text,
                    frequency=frequency,
                    cpc=0.0
                )
                if success:
                    added += 1
        
        total = len(manager.keywords)
        
        print(f"\n📊 РЕЗУЛЬТАТЫ:")
        print(f"   📁 В файле: {len(parser.keywords)}")
        print(f"   ✅ Добавлено: {added}")
        print(f"   🎯 В менеджере: {total}")
        
        # Проверяем частотность
        print(f"\n🔍 Частотность первых 5:")
        for i, kw in enumerate(manager.keywords[:5]):
            print(f"   {i+1}. '{kw.text}' → {kw.frequency}")
        
        # Топ по частотности
        sorted_kw = sorted(manager.keywords, key=lambda x: x.frequency, reverse=True)
        max_freq = sorted_kw[0].frequency if sorted_kw else 0
        
        print(f"\n🏆 Топ-3 по частотности:")
        for i, kw in enumerate(sorted_kw[:3], 1):
            print(f"   {i}. '{kw.text}' → {kw.frequency:,}")
        
        # Итог
        if total == len(parser.keywords) and max_freq > 10000:
            print(f"\n🎉 ПОЛНЫЙ УСПЕХ!")
            print(f"   ✅ Все {total} ключевых слов добавлены!")
            print(f"   ✅ Частотность правильная: {max_freq:,}")
            return True
        elif total >= len(parser.keywords) * 0.95:
            print(f"\n✅ ПОЧТИ УСПЕХ!")
            print(f"   ✅ {total} из {len(parser.keywords)} добавлено (95%+)")
            print(f"   ✅ Максимальная частота: {max_freq:,}")
            return True
        else:
            print(f"\n⚠️ ПРОБЛЕМЫ:")
            print(f"   ❌ Добавлено только {total} из {len(parser.keywords)}")
            print(f"   ❌ Максимальная частота: {max_freq}")
            return False
            
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        
        print(f"\n🔧 Попробуем план Б...")
        
        # План Б - прямой импорт
        try:
            sys.path.append('src/services')
            sys.path.append('src/core')
            
            import importlib.util
            
            # Импортируем файлы напрямую
            wordstat_spec = importlib.util.spec_from_file_location(
                "wordstat_parser", 
                "src/services/wordstat_parser.py"
            )
            wordstat_module = importlib.util.module_from_spec(wordstat_spec)
            
            keyword_spec = importlib.util.spec_from_file_location(
                "keyword_manager", 
                "src/core/keyword_manager.py"
            )
            keyword_module = importlib.util.module_from_spec(keyword_spec)
            
            print("✅ Файлы найдены, пробуем загрузить...")
            
            return False  # Остановимся пока на диагностике
            
        except Exception as e:
            print(f"❌ План Б тоже не сработал: {e}")
            
            print(f"\n📋 Проверьте файлы:")
            print(f"   1. src/services/wordstat_parser.py - есть ли класс WordstatParser?")
            print(f"   2. src/core/keyword_manager.py - есть ли класс KeywordManager?")
            print(f"   3. Нет ли циклических импортов в файлах?")
            
            return False
    
    except Exception as e:
        print(f"❌ Другая ошибка: {e}")
        return False


if __name__ == "__main__":
    success = simple_test()
    
    if success:
        print(f"\n🎊 Тест успешен!")
    else:
        print(f"\n🔧 Нужна отладка...")
        
        # Показываем содержимое проблемного файла
        print(f"\n📋 Первые 10 строк wordstat_parser.py:")
        try:
            with open('src/services/wordstat_parser.py', 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f.readlines()[:10], 1):
                    print(f"   {i:2d}: {line.rstrip()}")
        except:
            print("❌ Не удалось прочитать файл")