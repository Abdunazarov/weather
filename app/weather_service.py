import requests
from datetime import datetime

from settings import API_URL

# Глобальный кеш для хранения данных о погоде
weather_cache = {}

def get_cached_weather(city):
    """Получение погоды из кеша, если она существует и актуальна."""
    cached_data = weather_cache.get(city)
    if not cached_data:
        return None

    # Проверяем, не устарели ли данные
    if (datetime.now() - cached_data['time']).seconds < 600:
        return cached_data['temperature']
    return None

def fetch_weather_from_api(city):
    """Запрос к API для получения текущей погоды по названию города."""
        
    try:
        response = requests.get(API_URL.format(city))
        # Проверка на ошибки HTTP
        response.raise_for_status() 
        data = response.json()
        return data['main']['temp']
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")

def update_weather_cache(city, temperature):
    """Обновление кеша с текущей погодой."""
    weather_cache[city] = {"temperature": temperature, "time": datetime.now()}

def fetch_weather(city):
    """Основная функция для получения погоды, использующая кеш и API."""
    # Сначала пытаемся получить погоду из кеша
    cached_weather = get_cached_weather(city)
    if cached_weather is not None:
        return cached_weather
    
    # Если в кеше нет данных, делаем запрос к API
    temperature = fetch_weather_from_api(city)
    if temperature is not None:
        # Обновляем кеш новыми данными
        update_weather_cache(city, temperature)
        return temperature
    
    # Возвращаем None, если не удалось получить погоду
    return None
