#!/usr/bin/env python3
"""Отладка чтения Excel файла"""

import pandas as pd
import sys
import os

def debug_excel():
    """Отладка чтения Excel файла"""
    print("🔍 Отладка Excel файла...")
    
    file_path = "data/input/геологоразведка wordstat.xlsx"
    
    try:
        # Читаем Excel файл
        df = pd.read_excel(file_path, sheet_name=0)
        
        print(f"📊 Информация о файле:")
        print(f"   Размер: {df.shape[0]} строк, {df.shape[1]} колонок")
        print(f"   Колонки: {list(df.columns)}")
        
        print(f"\n📋 Первые 5 строк:")
        for i in range(min(5, len(df))):
            row = df.iloc[i]
            print(f"   Строка {i}:")
            for j, (col_name, value) in enumerate(zip(df.columns, row)):
                print(f"      Колонка {j} '{col_name}': {repr(value)} (тип: {type(value).__name__})")
            print()
        
        print(f"📈 Анализ колонки с частотностью:")
        
        # Ищем колонку с числами
        for i, col_name in enumerate(df.columns):
            col_data = df.iloc[:, i]
            numeric_count = col_data.apply(lambda x: isinstance(x, (int, float)) and not pd.isna(x)).sum()
            
            print(f"   Колонка {i} '{col_name}':")
            print(f"      Числовых значений: {numeric_count}")
            
            if numeric_count > 0:
                sample_numbers = col_data[col_data.apply(lambda x: isinstance(x, (int, float)) and not pd.isna(x))].head(3)
                print(f"      Примеры чисел: {list(sample_numbers)}")
        
        # Пробуем разные способы чтения
        print(f"\n🔬 Тестируем чтение частотности:")
        
        for i in range(min(10, len(df))):
            row = df.iloc[i]
            keyword = row.iloc[0] if len(row) > 0 else None
            frequency_raw = row.iloc[1] if len(row) > 1 else None
            
            # Пробуем преобразовать в число
            frequency = 0
            if pd.notna(frequency_raw):
                try:
                    if isinstance(frequency_raw, (int, float)):
                        frequency = int(frequency_raw)
                    else:
                        frequency = int(float(str(frequency_raw)))
                except:
                    frequency = 0
            
            print(f"   '{keyword}': частота_raw={repr(frequency_raw)} → frequency={frequency}")
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_excel()