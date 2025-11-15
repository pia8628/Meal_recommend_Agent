"""工具函數定義 - 供 ADK Agent 使用"""
import json
import os
import uuid
from typing import Dict, List

from google.adk.events.event import Event
from google.adk.sessions.session import Session
from google.genai import types

from config import get_ingredients_file


class _PreferenceStore:
    """使用於對話期間的偏好暫存。"""

    def __init__(self) -> None:
        self.likes: List[str] = []
        self.dislikes: List[str] = []

    def clear(self) -> None:
        self.likes.clear()
        self.dislikes.clear()

    def add(self, food: str, like: bool) -> None:
        key_list = self.likes if like else self.dislikes
        other_list = self.dislikes if like else self.likes

        if food in other_list:
            other_list.remove(food)

        if food not in key_list:
            key_list.append(food)

    def as_dict(self) -> Dict[str, List[str]]:
        return {
            "likes": list(self.likes),
            "dislikes": list(self.dislikes),
        }

    def has_data(self) -> bool:
        return bool(self.likes or self.dislikes)

    def summary_lines(self) -> List[str]:
        lines: List[str] = []
        if self.likes:
            lines.append(f"喜歡的食物：{', '.join(self.likes)}")
        if self.dislikes:
            lines.append(f"不喜歡的食物：{', '.join(self.dislikes)}")
        return lines


_PREFERENCES = _PreferenceStore()

# 食材管理工具函數
def add_ingredient(name: str) -> str:
    """添加食材到清單"""
    ingredients_file = get_ingredients_file()
    os.makedirs(os.path.dirname(ingredients_file), exist_ok=True)
    
    try:
        with open(ingredients_file, 'r', encoding='utf-8') as f:
            ingredients = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        ingredients = []
    
    if name in ingredients:
        return f"「{name}」已經在食材清單中了。"
    
    ingredients.append(name)
    with open(ingredients_file, 'w', encoding='utf-8') as f:
        json.dump(ingredients, f, ensure_ascii=False, indent=2)
    
    return f"已添加「{name}」到食材清單。"

def remove_ingredient(name: str) -> str:
    """從清單移除食材"""
    ingredients_file = get_ingredients_file()
    
    try:
        with open(ingredients_file, 'r', encoding='utf-8') as f:
            ingredients = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return f"「{name}」不在食材清單中。"
    
    if name not in ingredients:
        return f"「{name}」不在食材清單中。"
    
    ingredients.remove(name)
    with open(ingredients_file, 'w', encoding='utf-8') as f:
        json.dump(ingredients, f, ensure_ascii=False, indent=2)
    
    return f"已從食材清單中移除「{name}」。"

def get_ingredients() -> list:
    """取得食材清單"""
    ingredients_file = get_ingredients_file()
    
    try:
        with open(ingredients_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def list_ingredients() -> str:
    """列出食材清單（格式化）"""
    ingredients = get_ingredients()
    if not ingredients:
        return "目前食材清單是空的。"
    return f"目前食材清單：{', '.join(ingredients)}"

# 偏好管理工具函數
def add_preference(food: str, like: bool = True) -> str:
    """添加飲食偏好（儲存在對話期間的暫存中）。"""
    food = food.strip()
    if not food:
        return "請提供有效的食物名稱。"

    _PREFERENCES.add(food, like)
    action = "喜歡" if like else "不喜歡"
    return f"已記錄您{action}「{food}」。"


def get_preferences() -> Dict[str, List[str]]:
    """取得偏好清單。"""
    return _PREFERENCES.as_dict()


def list_preferences() -> str:
    """列出偏好清單（格式化）。"""
    lines = _PREFERENCES.summary_lines()
    if not lines:
        return "目前還沒有記錄任何偏好。"
    return "\n".join(lines)


def reset_preferences() -> None:
    """重設偏好暫存。"""
    _PREFERENCES.clear()


def preferences_available() -> bool:
    """檢查是否有偏好資料。"""
    return _PREFERENCES.has_data()


def build_preferences_summary() -> str:
    """組裝偏好摘要文字。"""
    lines = _PREFERENCES.summary_lines()
    if not lines:
        return ""
    return "用戶偏好紀錄：\n" + "\n".join(lines)


async def add_preferences_to_memory(memory_service, *, app_name: str, user_id: str) -> bool:
    """將目前偏好寫入 Google ADK 記憶服務。"""

    if memory_service is None or not _PREFERENCES.has_data():
        return False

    summary_text = build_preferences_summary()
    if not summary_text:
        return False

    content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=summary_text)],
    )

    event = Event(
        author="user",
        content=content,
        invocation_id=str(uuid.uuid4()),
    )

    session = Session(
        id=str(uuid.uuid4()),
        app_name=app_name,
        user_id=user_id,
        state={"preferences": _PREFERENCES.as_dict()},
        events=[event],
    )

    await memory_service.add_session_to_memory(session)
    return True

