"""工具函數定義 - 供 ADK Agent 使用"""
import json
import os
from config import get_ingredients_file, get_preferences_file

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
    """添加飲食偏好"""
    preferences_file = get_preferences_file()
    os.makedirs(os.path.dirname(preferences_file), exist_ok=True)
    
    try:
        with open(preferences_file, 'r', encoding='utf-8') as f:
            preferences = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        preferences = {"likes": [], "dislikes": []}
    
    key = "likes" if like else "dislikes"
    other_key = "dislikes" if like else "likes"
    
    # 如果已經在另一個列表中，先移除
    if food in preferences[other_key]:
        preferences[other_key].remove(food)
    
    # 添加到對應列表
    if food not in preferences[key]:
        preferences[key].append(food)
    
    with open(preferences_file, 'w', encoding='utf-8') as f:
        json.dump(preferences, f, ensure_ascii=False, indent=2)
    
    action = "喜歡" if like else "不喜歡"
    return f"已記錄您{action}「{food}」。"

def get_preferences() -> dict:
    """取得偏好清單"""
    preferences_file = get_preferences_file()
    
    try:
        with open(preferences_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"likes": [], "dislikes": []}

def list_preferences() -> str:
    """列出偏好清單（格式化）"""
    preferences = get_preferences()
    likes = preferences.get("likes", [])
    dislikes = preferences.get("dislikes", [])
    
    result = []
    if likes:
        result.append(f"喜歡的食物：{', '.join(likes)}")
    if dislikes:
        result.append(f"不喜歡的食物：{', '.join(dislikes)}")
    
    if not result:
        return "目前還沒有記錄任何偏好。"
    
    return "\n".join(result)

