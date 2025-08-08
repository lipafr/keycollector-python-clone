#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Рабочий тест с DataParser для обработки WordStat файла
"""

import sys
import os

# Добавляем папки в путь
sys.path.insert(0, 'src/core')

def test_wordstat_with_dataparser():
    """Тест обработки WordStat файла через DataParser"""
    
    print("🧪 ТЕСТ: DataParser + WordStat файл")
    print("="*50)
    
    try:
        # Импортируем классы
        from data_parser import DataParser
        from keyword_manager import KeywordManager
        
        print("✅ Импорты успешны!")
        
        # Создаем объекты
        parser = DataParser()
        manager = KeywordManager()
        
        print("✅ Объекты созданы!")
        
        # Парсим WordStat файл как Excel
        print(f"\n📁 Парсим WordStat Excel файл...")
        
        result = parser.parse_excel(
            file_path="data/input/геологоразведка wordstat.xlsx",
            sheet_name=0,      # Первый лист
            keyword_column=0,  # Первая колонка (ключевые слова)
            has_header=True    # Есть заголовки
        )
        
        print(f"📊 Результат парсинга:")
        print(f"   - Найдено ключевых слов: {len(result.keywords)}")
        print(f"   - Ошибок: {len(result.errors)}")
        print(f"   - Источник: {result.source_type}")
        
        if result.errors:
            print(f"⚠️ Ошибки:")
            for error in result.errors:
                print(f"   - {error}")
        
        # Показываем первые 5 ключевых слов из результата
        print(f"\n🔍 Первые 5 ключевых слов из парсера:")
        for i, keyword in enumerate(result.keywords[:5], 1):
            print(f"   {i}. '{keyword}'")
        
        if not result.keywords:
            print("❌ Ключевые слова не найдены!")
            print(f"📋 Метаданные: {result.metadata}")
            return False
        
        # Добавляем ключевые слова в менеджер
        print(f"\n🚀 Добавляем ключевые слова в менеджер...")
        
        added = 0
        for keyword in result.keywords:
            if keyword.strip():  # Только непустые
                success = manager.add_keyword(
                    keyword=keyword,
                    frequency=0,  # DataParser не извлекает частотность
                    cpc=0.0
                )
                if success:
                    added += 1
        
        total = len(manager.keywords)
        
        print(f"\n📊 РЕЗУЛЬТАТЫ:")
        print(f"   📁 Извлечено парсером: {len(result.keywords)}")
        print(f"   ✅ Добавлено в менеджер: {added}")
        print(f"   🎯 Всего в менеджере: {total}")
        
        # Показываем результат в менеджере
        print(f"\n🔍 Первые 5 в менеджере:")
        for i, kw in enumerate(manager.keywords[:5]):
            print(f"   {i+1}. '{kw.text}' (freq: {kw.frequency})")
        
        # Оценка успешности
        if total >= 300:  # Должно быть около 352
            print(f"\n🎉 УСПЕХ! Добавлено {total} ключевых слов!")
            return True
        elif total >= 100:
            print(f"\n✅ ЧАСТИЧНЫЙ УСПЕХ! Добавлено {total} ключевых слов")
            print("⚠️ Но частотность не извлечена (DataParser не поддерживает)")
            return True
        else:
            print(f"\n⚠️ МАЛО ДАННЫХ! Только {total} ключевых слов")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_excel_structure():
    """Анализируем структуру Excel файла"""
    
    print("\n" + "="*50)
    print("🔍 АНАЛИЗ СТРУКТУРЫ EXCEL ФАЙЛА")
    print("="*50)
    
    try:
        import pandas as pd
        
        # Читаем Excel файл
        df = pd.read_excel("data/input/геологоразведка wordstat.xlsx")
        
        print(f"📊 Структура файла:")
        print(f"   - Размер: {df.shape[0]} строк, {df.shape[1]} колонок")
        print(f"   - Колонки: {list(df.columns)}")
        
        # Показываем первые 5 строк
        print(f"\n📋 Первые 5 строк:")
        for i in range(min(5, len(df))):
            row = df.iloc[i]
            print(f"   Строка {i+1}:")
            for j, (col_name, value) in enumerate(row.items()):
                print(f"     {j}: {col_name} = '{value}'")
            print()
        
        # Ищем колонку с частотностью
        print(f"🔍 Поиск колонки с частотностью:")
        for col in df.columns:
            if any(word in str(col).lower() for word in ['частот', 'запрос', 'frequency', 'count']):
                print(f"   ✅ Возможная колонка частотности: '{col}'")
                # Показываем несколько значений
                values = df[col].head()
                print(f"      Первые значения: {list(values)}")
        
        return df
        
    except Exception as e:
        print(f"❌ Ошибка анализа Excel: {e}")
        return None


def create_custom_wordstat_parser(df):
    """Создаем кастомный парсер для WordStat на основе анализа"""
    
    print("\n" + "="*50)
    print("🛠️ СОЗДАНИЕ КАСТОМНОГО WORDSTAT ПАРСЕРА")
    print("="*50)
    
    try:
        from keyword_manager import KeywordManager
        
        manager = KeywordManager()
        
        # Определяем колонки
        keyword_col = None
        frequency_col = None
        
        # Ищем колонку ключевых слов (обычно первая)
        for i, col in enumerate(df.columns):
            if i == 0 or any(word in str(col).lower() for word in ['ключ', 'слов', 'фраз', 'запрос']):
                keyword_col = col
                print(f"✅ Колонка ключевых слов: '{col}'")
                break
        
        # Ищем колонку частотности
        for col in df.columns:
            if any(word in str(col).lower() for word in ['частот', 'запрос', 'frequency', 'count']):
                frequency_col = col
                print(f"✅ Колонка частотности: '{col}'")
                break
        
        if not keyword_col:
            print("❌ Не найдена колонка ключевых слов")
            return False
        
        # Обрабатываем данные
        print(f"\n🚀 Обработка данных...")
        
        added = 0
        for index, row in df.iterrows():
            try:
                keyword = str(row[keyword_col]).strip()
                frequency = 0
                
                if frequency_col and pd.notna(row[frequency_col]):
                    try:
                        frequency = int(float(str(row[frequency_col]).replace(',', '').replace(' ', '')))
                    except:
                        frequency = 0
                
                if keyword and keyword.lower() not in ['nan', 'none', '']:
                    success = manager.add_keyword(
                        keyword=keyword,
                        frequency=frequency,
                        cpc=0.0
                    )
                    
                    if success:
                        added += 1
                        
                        # Показываем первые 10
                        if added <= 10:
                            print(f"   ✅ '{keyword}' → {frequency}")
                
            except Exception as e:
                if added <= 5:  # Показываем только первые ошибки
                    print(f"   ❌ Ошибка в строке {index}: {e}")
        
        total = len(manager.keywords)
        
        print(f"\n📊 РЕЗУЛЬТАТ КАСТОМНОГО ПАРСЕРА:")
        print(f"   📁 Строк в файле: {len(df)}")
        print(f"   ✅ Добавлено: {added}")
        print(f"   🎯 В менеджере: {total}")
        
        # Топ по частотности
        if total > 0:
            sorted_kw = sorted(manager.keywords, key=lambda x: x.frequency, reverse=True)
            max_freq = sorted_kw[0].frequency
            
            print(f"\n🏆 Топ-5 по частотности:")
            for i, kw in enumerate(sorted_kw[:5], 1):
                print(f"   {i}. '{kw.text}' → {kw.frequency:,}")
            
            if total >= 350 and max_freq > 10000:
                print(f"\n🎉 КАСТОМНЫЙ ПАРСЕР - ПОЛНЫЙ УСПЕХ!")
                print(f"   ✅ Все {total} ключевых слов с частотностью!")
                return True
            elif total >= 300:
                print(f"\n✅ КАСТОМНЫЙ ПАРСЕР - УСПЕХ!")
                print(f"   ✅ {total} ключевых слов добавлено!")
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ Ошибка кастомного парсера: {e}")
        return False


if __name__ == "__main__":
    print("🔧 Запуск полного теста WordStat...")
    print("="*60)
    
    # Тест 1: Стандартный DataParser
    success1 = test_wordstat_with_dataparser()
    
    # Тест 2: Анализ структуры файла
    df = test_excel_structure()
    
    # Тест 3: Кастомный парсер
    success3 = False
    if df is not None:
        success3 = create_custom_wordstat_parser(df)
    
    # Итоговый результат
    print(f"\n" + "="*60)
    print(f"📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print(f"   🔧 DataParser: {'✅' if success1 else '❌'}")
    print(f"   🔍 Анализ файла: {'✅' if df is not None else '❌'}")
    print(f"   🛠️ Кастомный парсер: {'✅' if success3 else '❌'}")
    
    if success3:
        print(f"\n🎊 ПОБЕДА! Кастомный парсер справился с задачей!")
    elif success1:
        print(f"\n✅ DataParser работает, но без частотности")
    else:
        print(f"\n🔧 Нужна дополнительная отладка")