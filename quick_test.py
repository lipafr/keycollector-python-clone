import sys
import pandas as pd

sys.path.insert(0, 'src/core')
from keyword_manager import KeywordManager

print("🧪 БЫСТРЫЙ ТЕСТ WordStat")
print("="*40)

# Читаем Excel
df = pd.read_excel("data/input/геологоразведка wordstat.xlsx")
print(f"📊 Размер: {df.shape[0]} строк, {df.shape[1]} колонок")

# Создаем менеджер
manager = KeywordManager()

# Добавляем данные
for index, row in df.iterrows():
    keyword = str(row.iloc[0]).strip()
    
    # Пытаемся извлечь частотность из второй колонки
    frequency = 0
    if len(row) > 1:
        try:
            freq_val = str(row.iloc[1]).replace(",", "")
            frequency = int(float(freq_val))
        except:
            frequency = 0
    
    if keyword != "nan":
        manager.add_keyword(keyword=keyword, frequency=frequency, cpc=0.0)

total = len(manager.keywords)
print(f"📊 Добавлено: {total} ключевых слов")

if total >= 300:
    print("🎉 УСПЕХ!")
else:
    print("⚠️ Мало данных")