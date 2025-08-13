"""
天気情報取得とデータベース操作のロジック部分
"""
import requests
import pandas as pd
import os
from datetime import datetime
from typing import Dict, Optional
import json

class WeatherService:
    """天気情報を取得するサービスクラス"""
    
    def __init__(self):
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_url = "https://api.open-meteo.com/v1/forecast"
    
    def get_coordinates(self, city_name: str) -> Optional[Dict]:
        """都市名から座標を取得"""
        try:
            params = {
                "name": city_name,
                "count": 1,
                "language": "ja",
                "format": "json"
            }
            
            response = requests.get(self.geocoding_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("results"):
                result = data["results"][0]
                return {
                    "name": result.get("name", city_name),
                    "latitude": result.get("latitude"),
                    "longitude": result.get("longitude"),
                    "country": result.get("country", ""),
                    "admin1": result.get("admin1", "")
                }
            return None
            
        except Exception as e:
            print(f"座標取得エラー: {e}")
            return None
    
    def get_weather_data(self, latitude: float, longitude: float) -> Optional[Dict]:
        """座標から天気情報を取得"""
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true",
                "hourly": "temperature_2m,relativehumidity_2m,pressure_msl,cloudcover,windspeed_10m,winddirection_10m"
            }
            
            response = requests.get(self.weather_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            current_weather = data.get("current_weather", {})
            
            return {
                "temperature": current_weather.get("temperature"),
                "wind_speed": current_weather.get("windspeed"),
                "wind_direction": current_weather.get("winddirection"),
                "weather_code": current_weather.get("weathercode"),
                "time": current_weather.get("time"),
                # デモ用のダミーデータ
                "apparent_temperature": current_weather.get("temperature", 0) - 2,
                "humidity": 65,
                "pressure": 1013,
                "cloud_cover": 50
            }
            
        except Exception as e:
            print(f"天気データ取得エラー: {e}")
            return None
    
    def get_weather(self, city_name: str) -> Optional[Dict]:
        """都市名から天気情報を取得（メインメソッド）"""
        # 座標を取得
        coordinates = self.get_coordinates(city_name)
        if not coordinates:
            return None
        
        # 天気データを取得
        weather_data = self.get_weather_data(
            coordinates["latitude"], 
            coordinates["longitude"]
        )
        
        if not weather_data:
            return None
        
        # 結果をまとめる
        result = {
            "city": f"{coordinates['name']}, {coordinates['country']}",
            "latitude": coordinates["latitude"],
            "longitude": coordinates["longitude"],
            "temperature": weather_data["temperature"],
            "apparent_temperature": weather_data["apparent_temperature"],
            "humidity": weather_data["humidity"],
            "pressure": weather_data["pressure"],
            "cloud_cover": weather_data["cloud_cover"],
            "wind_speed": weather_data["wind_speed"],
            "wind_direction": weather_data["wind_direction"],
            "weather_code": weather_data["weather_code"],
            "time": weather_data["time"]
        }
        
        return result


class DatabaseService:
    """検索履歴の保存・取得を行うサービスクラス"""
    
    def __init__(self, db_file: str = "data/search_history.csv"):
        self.db_file = db_file
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """dataディレクトリが存在しない場合は作成"""
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
    
    def save_search_history(self, city_name: str, weather_data: Dict):
        """検索履歴をCSVファイルに保存"""
        try:
            # 新しい履歴データ
            new_record = {
                "search_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "city": weather_data["city"],
                "latitude": weather_data["latitude"],
                "longitude": weather_data["longitude"],
                "temperature": weather_data["temperature"],
                "apparent_temperature": weather_data["apparent_temperature"],
                "humidity": weather_data["humidity"],
                "pressure": weather_data["pressure"],
                "cloud_cover": weather_data["cloud_cover"],
                "wind_speed": weather_data["wind_speed"],
                "wind_direction": weather_data["wind_direction"],
                "weather_code": weather_data["weather_code"],
                "api_time": weather_data["time"]
            }
            
            # 既存のデータを読み込み
            if os.path.exists(self.db_file):
                df = pd.read_csv(self.db_file)
                # 新しいレコードを追加
                df = pd.concat([pd.DataFrame([new_record]), df], ignore_index=True)
            else:
                # 新しいファイルを作成
                df = pd.DataFrame([new_record])
            
            # CSVに保存
            df.to_csv(self.db_file, index=False)
            print(f"検索履歴を保存しました: {city_name}")
            
        except Exception as e:
            print(f"検索履歴保存エラー: {e}")
    
    def get_search_history(self) -> pd.DataFrame:
        """検索履歴をCSVファイルから取得"""
        try:
            if os.path.exists(self.db_file):
                df = pd.read_csv(self.db_file)
                # 検索時刻で降順ソート（最新が上）
                df = df.sort_values("search_time", ascending=False)
                return df
            else:
                # ファイルが存在しない場合は空のDataFrameを返す
                return pd.DataFrame()
                
        except Exception as e:
            print(f"検索履歴取得エラー: {e}")
            return pd.DataFrame()
    
    def get_city_statistics(self) -> pd.DataFrame:
        """都市別の検索回数統計を取得"""
        try:
            df = self.get_search_history()
            if df.empty:
                return pd.DataFrame()
            
            # 都市別に集計
            city_stats = df.groupby("city").agg({
                "search_time": "count",
                "temperature": "mean"
            }).reset_index()
            
            city_stats.columns = ["city", "search_count", "avg_temperature"]
            city_stats = city_stats.sort_values("search_count", ascending=False)
            
            return city_stats
            
        except Exception as e:
            print(f"統計取得エラー: {e}")
            return pd.DataFrame()


def weather_code_to_description(code: int) -> str:
    """天気コードを日本語の説明に変換"""
    weather_codes = {
        0: "快晴",
        1: "ほぼ快晴",
        2: "一部曇り",
        3: "曇り",
        45: "霧",
        48: "霧氷",
        51: "小雨",
        53: "雨",
        55: "大雨",
        56: "小雨（氷点下）",
        57: "雨（氷点下）",
        61: "小雨",
        63: "雨",
        65: "大雨",
        66: "小雨（氷点下）",
        67: "雨（氷点下）",
        71: "小雪",
        73: "雪",
        75: "大雪",
        77: "雪粒",
        80: "にわか雨",
        81: "にわか雨",
        82: "激しいにわか雨",
        85: "にわか雪",
        86: "激しいにわか雪",
        95: "雷雨",
        96: "雷雨（雹）",
        99: "激しい雷雨（雹）"
    }
    
    return weather_codes.get(code, f"不明（コード: {code}）")
