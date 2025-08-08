#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Правильный тест с исправленными импортами для добавления всех 352 ключевых слов
"""

# ✅ ПРАВИЛЬНЫЕ ИМПОРТЫ согласно структуре проекта
from src.services.wordstat_parser import WordstatParser
from src.core.keyword_manager import KeywordManager

def test_all_352_keywords_correct():
    """Тест добавления всех 352 ключевых слов с правильными импортами"""
    
    print("🧪 ПРАВИЛЬНЫЙ ТЕСТ: Добавляем ВСЕ 352 ключевых слова")
    print("="*70)
    
    # 1. Создаем парсер
    parser = WordstatParser()
    parser.parse_file("data/input/геологоразведка wordstat.xlsx")
    
    print(f"📁 Загружено из WordStat: {len(parser.keywords)} ключевых слов")
    
    # 2. Показываем структуру данных в парсере
    print(f"\n🔍 Первые 3 ключевых слова в парсере:")
    for i, keyword_data in enumerate(parser.keywords[:3]):
        keyword = keyword_data.get('keyword', '')
        frequency = keyword_data.get('frequency', 0)
        print(f"   {i+1}. '{keyword}' → частота в парсере: {frequency}")
    
    # 3. Создаем чистый менеджер
    manager = KeywordManager()
    
    # 4. Добавляем ВСЕ ключевые слова
    print(f"\n🚀 Добавляем ВСЕ ключевые слова...")
    
    added_count = 0
    duplicate_count = 0
    error_count = 0
    
    for keyword_data in parser.keywords:
        try:
            keyword_text = keyword_data.get('keyword', '').strip()
            frequency = keyword_data.get('frequency', 0)
            
            if not keyword_text:
                continue
            
            # 🔑 ГЛАВНОЕ: передаем frequency правильно
            success = manager.add_keyword(
                keyword=keyword_text,
                frequency=frequency,  # ← Реальная частотность из WordStat
                cpc=0.0
            )
            
            if success:
                added_count += 1
                
                # Показываем первые 10
                if added_count <= 10:
                    print(f"   ✅ '{keyword_text}' → freq: {frequency}")
                elif added_count % 100 == 0:
                    print(f"   📈 Добавлено: {added_count} из {len(parser.keywords)}...")
            else:
                duplicate_count += 1
                
        except Exception as e:
            error_count += 1
            if error_count <= 5:
                print(f"   ❌ Ошибка: {e}")
    
    # 5. Результаты
    total_in_manager = len(manager.keywords)
    
    print(f"\n📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print(f"   📁 В WordStat файле: {len(parser.keywords)}")
    print(f"   ✅ Успешно добавлено: {added_count}")
    print(f"   🔄 Дубликатов: {duplicate_count}")
    print(f"   ❌ Ошибок: {error_count}")
    print(f"   🎯 Всего в менеджере: {total_in_manager}")
    
    # 6. Проверяем частотность в менеджере
    print(f"\n🔍 Частотность в менеджере (первые 5):")
    for i, kw_obj in enumerate(manager.keywords[:5]):
        text = kw_obj.text
        freq = kw_obj.frequency
        print(f"   {i+1}. '{text}' → freq в менеджере: {freq}")
    
    # 7. Топ-10 по частотности
    print(f"\n🏆 Топ-10 по частотности:")
    sorted_keywords = sorted(manager.keywords, key=lambda x: x.frequency, reverse=True)
    
    for i, kw_obj in enumerate(sorted_keywords[:10], 1):
        print(f"   {i:2d}. '{kw_obj.text}' → {kw_obj.frequency:,} запросов")
    
    # 8. Финальная проверка
    max_frequency = sorted_keywords[0].frequency if sorted_keywords else 0
    
    print(f"\n🎯 ПРОВЕРКА КРИТЕРИЕВ:")
    print(f"   ✅ Количество ключевых слов: {total_in_manager} из {len(parser.keywords)}")
    print(f"   ✅ Максимальная частотность: {max_frequency:,}")
    
    # Определяем успешность
    success_criteria = {
        'all_added': total_in_manager == len(parser.keywords),
        'correct_frequency': max_frequency > 10000,
        'few_errors': error_count < 10
    }
    
    if all(success_criteria.values()):
        print(f"\n🎉 ПОЛНЫЙ УСПЕХ! 🎉")
        print(f"   🎊 Все {total_in_manager} ключевых слов добавлены!")
        print(f"   🎊 Частотность сохранена правильно!")
        print(f"   🎊 Максимальная частота: {max_frequency:,} запросов!")
        return True
    else:
        print(f"\n⚠️ НАЙДЕНЫ ПРОБЛЕМЫ:")
        
        if not success_criteria['all_added']:
            print(f"   ❌ Добавлено не все: {total_in_manager} из {len(parser.keywords)}")
            
        if not success_criteria['correct_frequency']:
            print(f"   ❌ Неправильная частотность: {max_frequency} (ожидали >10000)")
            
        if not success_criteria['few_errors']:
            print(f"   ❌ Много ошибок: {error_count}")
        
        return False


def debug_imports():
    """Отладка импортов и создания объектов"""
    
    print("🐛 ОТЛАДКА ИМПОРТОВ:")
    print("="*50)
    
    try:
        from src.services.wordstat_parser import WordstatParser
        print("✅ WordstatParser импортирован успешно")
        
        from src.core.keyword_manager import KeywordManager, Keyword
        print("✅ KeywordManager импортирован успешно")
        print("✅ Keyword импортирован успешно")
        
        # Тест создания объектов
        print(f"\n🧪 Тест создания объектов:")
        
        parser = WordstatParser()
        print(f"✅ WordstatParser создан: {parser}")
        
        manager = KeywordManager()
        print(f"✅ KeywordManager создан: {manager}")
        
        # Тест создания Keyword
        kw = Keyword(text="тест", frequency=1000, cpc=5.0)
        print(f"✅ Keyword создан: {kw}")
        print(f"   Текст: '{kw.text}'")
        print(f"   Частота: {kw.frequency}")
        print(f"   CPC: {kw.cpc}")
        
        # Тест добавления в менеджер
        success = manager.add_keyword(keyword="тест импорта", frequency=2000, cpc=10.0)
        print(f"✅ Добавление в менеджер: {success}")
        
        if manager.keywords:
            added_kw = manager.keywords[0]
            print(f"   Добавлено: '{added_kw.text}' (freq: {added_kw.frequency})")
        
        return True
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    except Exception as e:
        print(f"❌ Другая ошибка: {e}")
        return False


if __name__ == "__main__":
    print("🔧 Запуск правильного теста...")
    print("="*70)
    
    # Сначала проверяем импорты
    if debug_imports():
        print("\n" + "="*70)
        
        # Основной тест
        success = test_all_352_keywords_correct()
        
        if success:
            print(f"\n🎊🎊🎊 ВСЁ ИДЕАЛЬНО! 🎊🎊🎊")
            print(f"Все 352 ключевых слова успешно добавлены с правильной частотностью!")
        else:
            print(f"\n🔧 Есть проблемы, но тест показал детали")
    else:
        print(f"\n❌ Проблемы с импортами. Проверьте структуру проекта.")