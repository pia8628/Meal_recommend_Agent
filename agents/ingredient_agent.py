"""食材管理 Agent - 使用 Google ADK"""
from google.adk import Agent
from google.adk.tools import FunctionTool
from agents.tools import (
    add_ingredient, remove_ingredient, get_ingredients, list_ingredients
)

# 定義工具
ingredient_tools = [
    FunctionTool(func=add_ingredient),
    FunctionTool(func=remove_ingredient),
    FunctionTool(func=get_ingredients),
    FunctionTool(func=list_ingredients),
]

# 建立 Agent
ingredient_agent = Agent(
    name="ingredient_agent",
    model="gemini-2.0-flash-exp",
    instruction="""你是一個食材管理助手。你的職責是：
1. 管理用戶的食材清單
2. 添加或移除食材
3. 查詢當前食材清單

當用戶要求添加食材時，使用 add_ingredient 工具。
當用戶要求移除食材時，使用 remove_ingredient 工具。
當用戶要求查看食材清單時，使用 list_ingredients 工具。

請用繁體中文回應。""",
    tools=ingredient_tools
)
