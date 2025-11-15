"""配置管理模組"""
import os
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

def get_gemini_api_key():
    """取得 Gemini API key"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "請設定 GEMINI_API_KEY 環境變數或建立 .env 檔案。\n"
            "範例：GEMINI_API_KEY=your_api_key_here"
        )
    return api_key

def setup_adk():
    """設定 ADK（如果需要）"""
    # ADK 通常會自動從環境變數讀取 API key
    # 確保環境變數已設定
    api_key = get_gemini_api_key()
    # 如果需要手動設定，可以在這裡設定
    os.environ["GEMINI_API_KEY"] = api_key

def get_data_dir():
    """取得資料目錄路徑"""
    return os.path.join(os.path.dirname(__file__), "data")

def get_ingredients_file():
    """取得食材清單檔案路徑"""
    return os.path.join(get_data_dir(), "ingredients.json")

def get_preferences_file():
    """取得偏好檔案路徑"""
    return os.path.join(get_data_dir(), "preferences.json")

