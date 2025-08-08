#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправленная интеграция WordStat Parser с KeywordManager
Добавляет ВСЕ ключевые слова без фильтров
"""

import pandas as pd
import re
from typing import List, Dict, Any, Optional
import logging

class FixedWordstatIntegration:
    """Класс для добавления ВСЕХ ключевых слов из WordStat в KeywordManager"""
    
    def __init__(self, wordstat_parser):
        """
        Инициализация с объектом WordstatParser
        
        Args:
            wordstat_parser: Объект WordstatParser с загруженными данными
        """
        self.parser = wordstat_parser
        self.logger = logging.getLogger(__name__)
        
    def add_all_keywords_to_manager(self, keyword_manager, 
                                  min_frequency: int = 0,
                                  exclude_patterns: List[str] = None,
                                  max_keywords: Optional[int] = None):
        """
        Добавляет ВСЕ ключевые слова в KeywordManager
        
        Args:
            keyword_manager: Объект KeywordManager
            min_frequency: Минимальная частотность (по умолчанию 0 - все)
            exclude_patterns: Список паттернов для исключения (например, ['snowrunner'])
            max_keywords: Максимальное количество ключевых слов (None = все)
        
        Returns:
            dict: Статистика добавления
        """
        if not hasattr(self.parser, 'keywords') or not self.parser.keywords:
            raise ValueError("WordstatParser не содержит ключевых слов. Сначала загрузите данные.")
        
        # Параметры по умолчанию
        if exclude_patterns is None:
            exclude_patterns = []
        
        # Счетчики
        added_count = 0
        skipped_count = 0
        duplicate_count = 0
        error_count = 0
        
        print(f"🚀 Начинаем добавление ключевых слов...")
        print(f"📊 Всего ключевых слов для обработки: {len(self.parser.keywords)}")
        print(f"⚙️ Фильтры:")
        print(f"   - Минимальная частотность: {min_frequency}")
        print(f"   - Исключаемые паттерны: {exclude_patterns if exclude_patterns else 'нет'}")
        print(f"   - Максимум ключевых слов: {max_keywords if max_keywords else 'без ограничений'}")
        print()
        
        # Обрабатываем каждое ключевое слово
        for i, keyword_data in enumerate(self.parser.keywords, 1):
            try:
                keyword = keyword_data.get('keyword', '').strip()
                frequency = keyword_data.get('frequency', 0)
                
                # Пропускаем пустые ключевые слова
                if not keyword:
                    skipped_count += 1
                    continue
                
                # Фильтр по частотности
                if frequency < min_frequency:
                    skipped_count += 1
                    continue
                
                # Фильтр по исключаемым паттернам
                should_exclude = False
                for pattern in exclude_patterns:
                    if pattern.lower() in keyword.lower():
                        should_exclude = True
                        break
                
                if should_exclude:
                    skipped_count += 1
                    continue
                
                # Ограничение по количеству
                if max_keywords and added_count >= max_keywords:
                    print(f"⏹️ Достигнуто максимальное количество ключевых слов: {max_keywords}")
                    break
                
                # Добавляем ключевое слово
                try:
                    # Проверяем, есть ли уже такое ключевое слово
                    existing_keyword = keyword_manager.get_keyword(keyword)
                    
                    if existing_keyword:
                        # Обновляем частотность, если она больше
                        if frequency > existing_keyword.get('frequency', 0):
                            keyword_manager.update_keyword_frequency(keyword, frequency)
                            print(f"🔄 Обновлено: '{keyword}' - {frequency} запросов")
                        else:
                            duplicate_count += 1
                    else:
                        # Добавляем новое ключевое слово
                        keyword_manager.add_keyword(
                            keyword=keyword,
                            frequency=frequency,
                            cpc=0.0  # CPC пока не известен
                        )
                        added_count += 1
                        
                        # Показываем прогресс каждые 50 ключевых слов
                        if added_count % 50 == 0:
                            print(f"📈 Добавлено: {added_count} ключевых слов...")
                        
                except Exception as e:
                    error_count += 1
                    self.logger.error(f"Ошибка при добавлении '{keyword}': {e}")
                    
            except Exception as e:
                error_count += 1
                self.logger.error(f"Ошибка при обработке ключевого слова #{i}: {e}")
        
        # Итоговая статистика
        stats = {
            'total_processed': len(self.parser.keywords),
            'added': added_count,
            'skipped': skipped_count,
            'duplicates': duplicate_count,
            'errors': error_count,
            'success_rate': round((added_count / len(self.parser.keywords)) * 100, 1)
        }
        
        print(f"\n✅ Обработка завершена!")
        print(f"📊 Статистика:")
        print(f"   - Всего обработано: {stats['total_processed']}")
        print(f"   - Добавлено новых: {stats['added']}")
        print(f"   - Пропущено: {stats['skipped']}")
        print(f"   - Дубликатов: {stats['duplicates']}")
        print(f"   - Ошибок: {stats['errors']}")
        print(f"   - Процент успеха: {stats['success_rate']}%")
        
        return stats
    
    def add_keywords_by_groups(self, keyword_manager, groups_data):
        """
        Добавляет ключевые слова по группам
        
        Args:
            keyword_manager: Объект KeywordManager
            groups_data: Данные о группах из parser.get_keyword_groups()
        """
        added_count = 0
        
        print(f"📁 Добавление ключевых слов по группам...")
        print(f"🗂️ Найдено групп: {len(groups_data)}")
        
        for group_name, keywords_in_group in groups_data.items():
            print(f"\n📂 Группа: '{group_name}' ({len(keywords_in_group)} ключевых слов)")
            
            for keyword_data in keywords_in_group:
                try:
                    keyword = keyword_data['keyword']
                    frequency = keyword_data['frequency']
                    
                    keyword_manager.add_keyword(
                        keyword=keyword,
                        frequency=frequency,
                        cpc=0.0,
                        group=group_name  # Добавляем информацию о группе
                    )
                    
                    added_count += 1
                    print(f"   ✅ '{keyword}' ({frequency} запросов)")
                    
                except Exception as e:
                    print(f"   ❌ Ошибка при добавлении '{keyword}': {e}")
        
        print(f"\n🎉 Всего добавлено по группам: {added_count} ключевых слов")
        return added_count


def fix_wordstat_integration_test():
    """Тестовая функция для проверки исправленной интеграции"""
    try:
        # Импортируем необходимые модули (замените на ваши пути)
        from wordstat_parser import WordstatParser
        from keyword_manager import KeywordManager
        
        print("🧪 Тестирование исправленной интеграции WordStat...")
        
        # Загружаем данные
        parser = WordstatParser()
        parser.parse_file("data/input/геологоразведка wordstat.xlsx")
        
        # Создаем менеджер ключевых слов
        keyword_manager = KeywordManager()
        
        # Создаем объект исправленной интеграции
        fixed_integration = FixedWordstatIntegration(parser)
        
        # Вариант 1: Добавить ВСЕ ключевые слова без фильтров
        print("\n" + "="*60)
        print("ВАРИАНТ 1: Добавляем ВСЕ 352 ключевых слова")
        print("="*60)
        
        stats1 = fixed_integration.add_all_keywords_to_manager(
            keyword_manager=keyword_manager,
            min_frequency=0,  # Без фильтра по частотности
            exclude_patterns=[],  # Без исключений
            max_keywords=None  # Без ограничений
        )
        
        # Проверяем результат
        total_in_manager = len(keyword_manager.get_all_keywords())
        print(f"\n🎯 ИТОГО в менеджере: {total_in_manager} ключевых слов")
        
        # Вариант 2: Только без игровых запросов
        keyword_manager_filtered = KeywordManager()
        
        print("\n" + "="*60)
        print("ВАРИАНТ 2: Без игровых запросов (snowrunner)")
        print("="*60)
        
        stats2 = fixed_integration.add_all_keywords_to_manager(
            keyword_manager=keyword_manager_filtered,
            min_frequency=0,
            exclude_patterns=['snowrunner'],  # Исключаем игровые запросы
            max_keywords=None
        )
        
        total_filtered = len(keyword_manager_filtered.get_all_keywords())
        print(f"\n🎯 ИТОГО без игровых запросов: {total_filtered} ключевых слов")
        
        return True, stats1, stats2
        
    except Exception as e:
        print(f"❌ Ошибка в тесте: {e}")
        return False, None, None


if __name__ == "__main__":
    # Запуск теста
    success, stats1, stats2 = fix_wordstat_integration_test()
    
    if success:
        print(f"\n🎉 Тест успешно завершен!")
        print(f"📊 Добавлено всех ключевых слов: {stats1['added']}")
        print(f"📊 Добавлено без игровых: {stats2['added']}")
    else:
        print(f"❌ Тест завершился с ошибкой")