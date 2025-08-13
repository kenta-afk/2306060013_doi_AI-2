# 🌤️ 天気情報アプリ

## 📖 アプリ概要

このアプリは、ユーザーが都市名を入力すると、その都市の現在の天気情報を取得・表示するStreamlitアプリです。また、検索履歴をCSVファイルに保存するデータベース機能も実装しています。

### 主な機能
- 🔍 都市名による天気情報検索
- 🌡️ 気温、湿度、風速などの詳細情報表示
- 📊 検索履歴の自動保存（CSV形式）
- 📈 過去の検索履歴の表示
- 📥 検索履歴のCSVダウンロード

## 🛠️ 使用API

**Open-Meteo API**
- URL: https://open-meteo.com/
- 特徴: 無料・APIキー不要
- 機能: 
  - 都市名から座標取得（Geocoding API）
  - 座標から天気データ取得（Weather API）

## 🏗️ システム設計図

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │                  │    │                 │
│  Streamlit UI   │◄──►│   Python Logic   │◄──►│  External APIs  │
│   (app.py)      │    │ (weather_logic.py│    │                 │
│                 │    │                  │    │ • Geocoding API │
│ • ユーザー入力   │    │ • WeatherService │    │ • Weather API   │
│ • 結果表示      │    │ • DatabaseService│    │   (Open-Meteo)  │
│ • 履歴表示      │    │                  │    │                 │
│                 │    │                  │    └─────────────────┘
└─────────────────┘    └──────────────────┘
         │                        │
         │                        ▼
         │              ┌─────────────────┐
         │              │                 │
         └─────────────►│   Local CSV     │
                        │   Database      │
                        │                 │
                        │ • search_history │
                        │   .csv          │
                        │ • 検索履歴保存   │
                        └─────────────────┘
```

## 📁 コード説明図

```
assignment/
├── app.py                 # メインアプリケーション
│   ├── main()            # メイン関数
│   ├── UI構築            # Streamlitコンポーネント
│   └── イベントハンドリング# ボタンクリック等の処理
│
├── weather_logic.py       # ビジネスロジック
│   ├── WeatherService    # 天気情報取得クラス
│   │   ├── get_coordinates()    # 都市→座標変換
│   │   ├── get_weather_data()   # 座標→天気データ
│   │   └── get_weather()        # メイン処理
│   │
│   ├── DatabaseService   # データベース操作クラス
│   │   ├── save_search_history()  # 履歴保存
│   │   ├── get_search_history()   # 履歴取得
│   │   └── get_city_statistics()  # 統計データ
│   │
│   └── weather_code_to_description() # ユーティリティ関数
│
├── data/                  # データ保存ディレクトリ
│   └── search_history.csv # 検索履歴データベース
│
└── requirements.txt       # 依存関係定義
```

## 📊 データベース設計

### search_history.csv の構造

| カラム名 | データ型 | 説明 |
|---------|---------|-----|
| search_time | string | 検索実行時刻 (YYYY-MM-DD HH:MM:SS) |
| city | string | 都市名 |
| latitude | float | 緯度 |
| longitude | float | 経度 |
| temperature | float | 気温 (°C) |
| apparent_temperature | float | 体感温度 (°C) |
| humidity | int | 湿度 (%) |
| pressure | float | 気圧 (hPa) |
| cloud_cover | int | 雲量 (%) |
| wind_speed | float | 風速 (km/h) |
| wind_direction | int | 風向 (度) |
| weather_code | int | 天気コード |
| api_time | string | API取得時刻 |

## 🚀 実行方法

### 1. 環境セットアップ
```bash
# 仮想環境の作成・有効化（自動設定済み）
# 依存関係のインストール（自動実行済み）
```

### 2. アプリケーションの起動
```bash
streamlit run app.py
```

### 3. アプリケーションの使用
1. ブラウザで `http://localhost:8501` にアクセス
2. 都市名を入力（例：Tokyo, Osaka, New York）
3. "🌤️ 天気を取得" ボタンをクリック
4. 天気情報と検索履歴を確認

## 📋 ファイル構成

```
/Users/doikentarou/assignment/
├── app.py              # Streamlitアプリケーション本体
├── weather_logic.py    # ビジネスロジック（天気情報取得・DB操作）
├── requirements.txt    # Python依存関係
├── data/              # データベースディレクトリ
│   └── search_history.csv  # 検索履歴（自動生成）
└── README.md          # このファイル
```

## 🎯 技術的特徴

### アーキテクチャ
- **分離されたコンポーネント**: UI層（app.py）とロジック層（weather_logic.py）を分離
- **クラスベース設計**: WeatherServiceとDatabaseServiceで責任を分離
- **エラーハンドリング**: 各API呼び出しで適切な例外処理を実装

### データベース機能（+3点対象）
- CSV形式での永続化
- 検索履歴の自動保存
- 履歴データのダウンロード機能
- 都市別検索統計機能

### ユーザビリティ
- 直感的なWeb UI
- リアルタイムでの結果表示
- 詳細情報の展開表示
- 検索履歴の可視化

## 📈 今後の拡張可能性

- 天気予報（複数日）の表示
- グラフによるデータ可視化
- 都市別の統計ダッシュボード
- ユーザー設定の保存機能
- より詳細な天気情報（降水確率等）

---

**開発者**: doikentarou  
**開発日**: 2025年8月13日  
**課題**: Streamlitを使ったアプリの開発 + 公開  
**提出期限**: 2025年8月15日（金）23:59
