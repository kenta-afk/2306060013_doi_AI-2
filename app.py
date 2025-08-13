import streamlit as st
import pandas as pd
from datetime import datetime
import os
from weather_logic import WeatherService, DatabaseService

# ページ設定
st.set_page_config(
    page_title="天気情報アプリ",
    page_icon="🌤️",
    layout="wide"
)

def main():
    st.title("🌤️ 天気情報アプリ")
    st.markdown("---")
    
    # サイドバーでアプリの説明
    with st.sidebar:
        st.header("📖 アプリについて")
        st.write("""
        このアプリでは：
        - 都市名を入力して天気情報を取得
        - 検索履歴を自動保存
        - 過去の検索履歴を表示
        """)
        
        st.header("🔍 使用API")
        st.write("Open-Meteo API (無料・APIキー不要)")
    
    # メインコンテンツ
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔍 天気を検索")
        
        # 都市名入力
        city_name = st.text_input(
            "都市名を入力してください",
            placeholder="例: Tokyo, Osaka, New York"
        )
        
        if st.button("🌤️ 天気を取得", type="primary"):
            if city_name:
                with st.spinner(f"{city_name}の天気情報を取得中..."):
                    # 天気サービスのインスタンス作成
                    weather_service = WeatherService()
                    
                    # 天気情報取得
                    weather_data = weather_service.get_weather(city_name)
                    
                    if weather_data:
                        # 結果表示
                        st.success(f"✅ {city_name}の天気情報を取得しました！")
                        
                        # 天気情報の表示
                        st.subheader(f"📍 {weather_data['city']}")
                        
                        col_temp, col_humidity, col_wind = st.columns(3)
                        
                        with col_temp:
                            st.metric(
                                "🌡️ 気温",
                                f"{weather_data['temperature']}°C",
                                delta=f"体感 {weather_data['apparent_temperature']}°C"
                            )
                        
                        with col_humidity:
                            st.metric(
                                "💧 湿度",
                                f"{weather_data['humidity']}%"
                            )
                        
                        with col_wind:
                            st.metric(
                                "💨 風速",
                                f"{weather_data['wind_speed']} km/h"
                            )
                        
                        # 詳細情報
                        with st.expander("📊 詳細情報"):
                            detail_col1, detail_col2 = st.columns(2)
                            
                            with detail_col1:
                                st.write(f"**天気コード:** {weather_data['weather_code']}")
                                st.write(f"**気圧:** {weather_data['pressure']} hPa")
                                st.write(f"**雲量:** {weather_data['cloud_cover']}%")
                            
                            with detail_col2:
                                st.write(f"**風向:** {weather_data['wind_direction']}°")
                                st.write(f"**取得時刻:** {weather_data['time']}")
                                st.write(f"**座標:** {weather_data['latitude']}, {weather_data['longitude']}")
                        
                        # データベースに保存
                        db_service = DatabaseService()
                        db_service.save_search_history(city_name, weather_data)
                        
                    else:
                        st.error("❌ 天気情報の取得に失敗しました。都市名を確認してください。")
            else:
                st.warning("⚠️ 都市名を入力してください。")
    
    with col2:
        st.header("📈 検索履歴")
        
        # データベースサービス
        db_service = DatabaseService()
        history = db_service.get_search_history()
        
        if not history.empty:
            # 最新5件を表示
            recent_history = history.head(5)
            
            for _, row in recent_history.iterrows():
                with st.container():
                    st.write(f"**{row['city']}**")
                    st.write(f"🌡️ {row['temperature']}°C")
                    st.write(f"🕐 {row['search_time']}")
                    st.markdown("---")
            
            # 全履歴表示ボタン
            if st.button("📊 全履歴を表示"):
                st.subheader("🗃️ 全検索履歴")
                st.dataframe(
                    history[['search_time', 'city', 'temperature', 'humidity', 'wind_speed']],
                    use_container_width=True
                )
                
                # CSVダウンロード
                csv = history.to_csv(index=False)
                st.download_button(
                    label="📥 CSVをダウンロード",
                    data=csv,
                    file_name=f"weather_history_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("まだ検索履歴がありません。")

if __name__ == "__main__":
    main()
