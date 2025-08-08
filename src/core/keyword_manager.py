#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль управления ключевыми словами
Основная логика для работы с семантическим ядром
"""

import re
import pandas as pd
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Keyword:
    """Класс для представления ключевого слова"""
    text: str
    frequency: int = 0
    competition: float = 0.0
    cpc: float = 0.0  # Cost Per Click
    category: str = ""
    source: str = ""
    added_date: datetime = None
    
    def __post_init__(self):
        """Автоматическая настройка после создания объекта"""
        if self.added_date is None:
            self.added_date = datetime.now()
        
        # Очистка ключевого слова
        self.text = self._clean_keyword(self.text)
    
    def _clean_keyword(self, keyword: str) -> str:
        """Очистка ключевого слова от лишних символов"""
        # Убираем лишние пробелы и приводим к нижнему регистру
        cleaned = re.sub(r'\s+', ' ', keyword.strip().lower())
        # Убираем специальные символы (оставляем только буквы, цифры, пробелы, дефисы)
        cleaned = re.sub(r'[^\w\s\-]', '', cleaned)
        return cleaned
    
    def word_count(self) -> int:
        """Количество слов в ключевой фразе"""
        return len(self.text.split())
    
    def __str__(self):
        return f"'{self.text}' (freq: {self.frequency}, cpc: {self.cpc})"


class KeywordManager:
    """Менеджер для управления коллекцией ключевых слов"""
    
    def __init__(self):
        """Инициализация менеджера ключевых слов"""
        self.keywords: List[Keyword] = []
        self._keyword_set: Set[str] = set()  # Для быстрой проверки дубликатов
        
    def add_keyword(self, keyword: str, **kwargs) -> bool:
        """
        Добавить ключевое слово
        
        Args:
            keyword: Текст ключевого слова
            **kwargs: Дополнительные параметры (frequency, cpc, etc.)
            
        Returns:
            bool: True если добавлено, False если дубликат
        """
        # Создаем объект ключевого слова
        kw_obj = Keyword(text=keyword, **kwargs)
        
        # Проверяем на дубликаты
        if kw_obj.text in self._keyword_set:
            print(f"Дубликат найден: '{kw_obj.text}'")
            return False
        
        # Добавляем ключевое слово
        self.keywords.append(kw_obj)
        self._keyword_set.add(kw_obj.text)
        
        print(f"Добавлено: {kw_obj}")
        return True
    
    def add_keywords_bulk(self, keywords: List[str]) -> Dict[str, int]:
        """
        Массовое добавление ключевых слов
        
        Args:
            keywords: Список ключевых слов
            
        Returns:
            Dict с статистикой добавления
        """
        stats = {"added": 0, "duplicates": 0, "errors": 0}
        
        for keyword in keywords:
            try:
                if self.add_keyword(keyword):
                    stats["added"] += 1
                else:
                    stats["duplicates"] += 1
            except Exception as e:
                print(f"Ошибка при добавлении '{keyword}': {e}")
                stats["errors"] += 1
        
        return stats
    
    def remove_keyword(self, keyword: str) -> bool:
        """Удалить ключевое слово"""
        cleaned_keyword = Keyword(text=keyword).text
        
        for i, kw in enumerate(self.keywords):
            if kw.text == cleaned_keyword:
                removed_kw = self.keywords.pop(i)
                self._keyword_set.remove(removed_kw.text)
                print(f"Удалено: {removed_kw}")
                return True
        
        print(f"Ключевое слово '{cleaned_keyword}' не найдено")
        return False
    
    def find_keywords(self, pattern: str) -> List[Keyword]:
        """Найти ключевые слова по паттерну"""
        pattern = pattern.lower()
        found = []
        
        for kw in self.keywords:
            if pattern in kw.text:
                found.append(kw)
        
        return found
    
    def filter_by_word_count(self, min_words: int = 1, max_words: int = 10) -> List[Keyword]:
        """Фильтр по количеству слов"""
        return [kw for kw in self.keywords 
                if min_words <= kw.word_count() <= max_words]
    
    def filter_by_frequency(self, min_freq: int = 0, max_freq: int = 999999) -> List[Keyword]:
        """Фильтр по частотности"""
        return [kw for kw in self.keywords 
                if min_freq <= kw.frequency <= max_freq]
    
    def get_statistics(self) -> Dict:
        """Получить статистику по ключевым словам"""
        if not self.keywords:
            return {
                "total": 0,
                "avg_frequency": 0,
                "max_frequency": 0,
                "min_frequency": 0,
                "avg_word_count": 0,
                "categories": 0
            }
        
        frequencies = [kw.frequency for kw in self.keywords]
        word_counts = [kw.word_count() for kw in self.keywords]
        
        return {
            "total": len(self.keywords),
            "avg_frequency": sum(frequencies) / len(frequencies) if frequencies else 0,
            "max_frequency": max(frequencies) if frequencies else 0,
            "min_frequency": min(frequencies) if frequencies else 0,
            "avg_word_count": sum(word_counts) / len(word_counts) if word_counts else 0,
            "categories": len(set(kw.category for kw in self.keywords if kw.category))
        }
    
    def to_dataframe(self) -> pd.DataFrame:
        """Экспорт в pandas DataFrame"""
        if not self.keywords:
            return pd.DataFrame()
        
        data = []
        for kw in self.keywords:
            data.append({
                'keyword': kw.text,
                'frequency': kw.frequency,
                'competition': kw.competition,
                'cpc': kw.cpc,
                'category': kw.category,
                'source': kw.source,
                'word_count': kw.word_count(),
                'added_date': kw.added_date
            })
        
        return pd.DataFrame(data)
    
    def clear_all(self):
        """Очистить все ключевые слова"""
        count = len(self.keywords)
        self.keywords.clear()
        self._keyword_set.clear()
        print(f"Удалено {count} ключевых слов")
    
    def __len__(self):
        """Количество ключевых слов"""
        return len(self.keywords)
    
    def __str__(self):
        """Строковое представление менеджера"""
        return f"KeywordManager: {len(self.keywords)} ключевых слов"


# Пример использования (для тестирования)
if __name__ == "__main__":
    # Создаем менеджер
    manager = KeywordManager()
    
    # Добавляем ключевые слова
    test_keywords = [
        "seo продвижение",
        "оптимизация сайта",
        "ключевые слова",
        "семантическое ядро",
        "яндекс директ"
    ]
    
    print("=== Тестирование KeywordManager ===")
    
    # Массовое добавление
    stats = manager.add_keywords_bulk(test_keywords)
    print(f"Статистика добавления: {stats}")
    
    # Статистика
    print(f"Общая статистика: {manager.get_statistics()}")
    
    # Поиск
    found = manager.find_keywords("сео")
    print(f"Найдено по 'сео': {len(found)} результатов")
    
    # DataFrame
    df = manager.to_dataframe()
    print(f"DataFrame создан: {df.shape}")