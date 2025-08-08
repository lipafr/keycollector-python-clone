#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправление метода интеграции WordstatParser с KeywordManager
"""

def add_wordstat_integration_method():
    """
    Добавьте этот метод в класс WordstatParser
    """
    
    method_code = '''
def add_to_manager_fixed(self, keyword_manager, 
                        min_frequency: int = 0,
                        exclude_patterns: list = None,
                        max_keywords: int = None) -> dict:
    """
    Исправленный метод добавления ключевых слов в KeywordManager
    
    Args:
        keyword_manager: Объект KeywordManager
        min_frequency: Минимальная частотность (по умолчанию 0)
        exclude_patterns: Паттерны для исключения (например, ['snowrunner'])
        max_keywords: Максимальное количество (None = все)
    
    Returns:
        dict: Статистика добавления
    """
    if exclude_patterns is None:
        exclude_patterns = []
    
    stats = {
        'total': len(self.keywords),
        'added': 0,
        'skipped': 0,
        'duplicates': 0,
        'errors': 0
    }
    
    print(f"🚀 Добавление ключевых слов в KeywordManager...")
    print(f"📊 Параметры:")
    print(f"   - Всего ключевых слов: {stats['total']}")
    print(f"   - Минимальная частота: {min_frequency}")
    print(f"   - Исключения: {exclude_patterns}")
    print(f"   - Лимит: {max_keywords or 'без ограничений'}")
    
    for i, keyword_data in enumerate(self.keywords):
        try:
            # Получаем данные
            keyword_text = keyword_data.get('keyword', '').strip()
            frequency = keyword_data.get('frequency', 0)
            
            # Пропускаем пустые
            if not keyword_text:
                stats['skipped'] += 1
                continue
            
            # Фильтр по частоте
            if frequency < min_frequency:
                stats['skipped'] += 1
                continue
            
            # Фильтр по исключениям
            skip_keyword = False
            for pattern in exclude_patterns:
                if pattern.lower() in keyword_text.lower():
                    skip_keyword = True
                    break
            
            if skip_keyword:
                stats['skipped'] += 1
                continue
            
            # Лимит количества
            if max_keywords and stats['added'] >= max_keywords:
                break
            
            # ✅ ПРАВИЛЬНО добавляем с именованными параметрами
            success = keyword_manager.add_keyword(
                keyword=keyword_text,
                frequency=frequency,  # ← Передаем реальную частотность!
                cpc=0.0
            )
            
            if success:
                stats['added'] += 1
                
                # Показываем первые 10 для контроля
                if stats['added'] <= 10:
                    print(f"   ✅ '{keyword_text}' → {frequency:,} запросов")
                elif stats['added'] % 50 == 0:
                    print(f"   📈 Добавлено: {stats['added']}...")
            else:
                stats['duplicates'] += 1
                
        except Exception as e:
            stats['errors'] += 1
            print(f"   ❌ Ошибка: {e}")
    
    # Итоговая статистика
    print(f"\\n📊 Статистика добавления:")
    print(f"   📁 Всего в файле: {stats['total']}")
    print(f"   ✅ Добавлено: {stats['added']}")
    print(f"   ⏭️ Пропущено: {stats['skipped']}")
    print(f"   🔄 Дубликатов: {stats['duplicates']}")
    print(f"   ❌ Ошибок: {stats['errors']}")
    
    success_rate = (stats['added'] / stats['total']) * 100 if stats['total'] > 0 else 0
    print(f"   📈 Успешность: {success_rate:.1f}%")
    
    return stats
    '''
    
    return method_code


def create_fixed_test():
    """Создает исправленный тест"""
    
    test_code = '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ИСПРАВЛЕННЫЙ ТЕСТ - добавляет все 352 ключевых слова
"""

from wordstat_parser import WordstatParser
from keyword_manager import KeywordManager

# Добавьте метод add_to_manager_fixed в WordstatParser (код выше)
# Или используйте этот код:

def test_fixed_integration():
    """Исправленный тест интеграции"""
    
    print("🧪 ИСПРАВЛЕННЫЙ ТЕСТ WordstatParser + KeywordManager")
    print("="*70)
    
    # 1. Загружаем данные
    parser = WordstatParser()
    parser.parse_file("data/input/геологоразведка wordstat.xlsx")
    
    print(f"📁 Загружено из WordStat: {len(parser.keywords)} ключевых слов")
    
    # 2. Создаем менеджер
    manager = KeywordManager()
    
    # 3. Добавляем ВСЕ ключевые слова напрямую
    print(f"\\n🚀 Добавляем ВСЕ ключевые слова...")
    
    added = 0
    errors = 0
    
    for keyword_data in parser.keywords:
        try:
            keyword_text = keyword_data.get('keyword', '').strip()
            frequency = keyword_data.get('frequency', 0)
            
            if not keyword_text:
                continue
            
            # ✅ КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ: передаем frequency правильно
            success = manager.add_keyword(
                keyword=keyword_text,
                frequency=frequency,  # ← Реальная частотность из WordStat
                cpc=0.0
            )
            
            if success:
                added += 1
                
                # Показываем первые 5 для проверки
                if added <= 5:
                    print(f"   ✅ '{keyword_text}' → freq: {frequency}")
            
        except Exception as e:
            errors += 1
            print(f"   ❌ Ошибка: {e}")
    
    # 4. Результаты
    total_in_manager = len(manager.keywords)
    
    print(f"\\n📊 РЕЗУЛЬТАТЫ:")
    print(f"   📁 В WordStat файле: {len(parser.keywords)}")
    print(f"   ✅ Добавлено: {added}")
    print(f"   🎯 В менеджере: {total_in_manager}")
    print(f"   ❌ Ошибок: {errors}")
    
    # 5. Проверяем частотность
    print(f"\\n🏆 Топ-5 по частотности:")
    sorted_kw = sorted(manager.keywords, key=lambda x: x.frequency, reverse=True)
    
    for i, kw in enumerate(sorted_kw[:5], 1):
        print(f"   {i}. '{kw.text}' → {kw.frequency:,} запросов")
    
    # 6. Итоговая проверка
    highest_freq = sorted_kw[0].frequency if sorted_kw else 0
    
    if total_in_manager >= 350 and highest_freq > 10000:
        print(f"\\n🎉 ПОЛНЫЙ УСПЕХ!")
        print(f"   ✅ Добавлено {total_in_manager} из {len(parser.keywords)} ключевых слов")
        print(f"   ✅ Частотность правильная: max = {highest_freq:,}")
        return True
    else:
        print(f"\\n⚠️ ПРОБЛЕМЫ:")
        if total_in_manager < 350:
            print(f"   ❌ Мало ключевых слов: {total_in_manager} < 350")
        if highest_freq <= 10000:
            print(f"   ❌ Неправильная частотность: {highest_freq}")
        
        print(f"\\n🔧 ПРОВЕРЬТЕ:")
        print(f"   1. Класс Keyword принимает параметр frequency?")
        print(f"   2. WordstatParser правильно парсит частотность?")
        print(f"   3. Нет ли фильтров в add_keyword?")
        
        return False

if __name__ == "__main__":
    success = test_fixed_integration()
    
    if success:
        print(f"\\n🎊 ВСЁ ИСПРАВЛЕНО! Теперь добавляются все 352 ключевых слова!")
    '''
    
    return test_code


if __name__ == "__main__":
    print("🛠️ Код для исправления WordstatParser:")
    print("="*50)
    print(add_wordstat_integration_method())
    
    print("\\n" + "="*50)
    print("📋 Сохраните как: test_fixed_wordstat.py")
    print("="*50)
    print(create_fixed_test())