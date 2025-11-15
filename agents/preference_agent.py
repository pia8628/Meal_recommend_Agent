"""偏好記憶 Agent - 使用 Google ADK"""
from google.adk import Agent
from google.adk.tools import FunctionTool
from agents.tools import (
    add_preference, get_preferences, list_preferences
)

# 定義工具
preference_tools = [
    FunctionTool(func=add_preference),
    FunctionTool(func=get_preferences),
    FunctionTool(func=list_preferences),
]

# 建立 Agent
preference_agent = Agent(
    name="preference_agent",
    model="gemini-2.0-flash-exp",
    instruction="""你是一個偏好記憶助手。你的職責是：
1. 記錄用戶喜歡的食物
2. 記錄用戶不喜歡的食物
3. 查詢用戶的飲食偏好

當用戶說喜歡某食物時，使用 add_preference 工具，參數 like=True。
當用戶說不喜歡某食物時，使用 add_preference 工具，參數 like=False。
當用戶要求查看偏好時，使用 list_preferences 工具。

請用繁體中文回應。""",
    tools=preference_tools
)
