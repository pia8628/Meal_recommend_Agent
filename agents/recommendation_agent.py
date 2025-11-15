"""餐點推薦 Agent - 使用 Google ADK"""
from google.adk import Agent
from google.adk.tools import AgentTool
from agents.ingredient_agent import ingredient_agent
from agents.preference_agent import preference_agent

# 建立 Agent（使用 LLM 推薦餐點）
recommendation_agent = Agent(
    name="recommendation_agent",
    model="gemini-2.0-flash-exp",
    instruction="""你是一個專業的餐點推薦助手。你的職責是：
1. 根據用戶的食材清單推薦適合的餐點
2. 考慮用戶的飲食偏好（喜歡和不喜歡的食物）
3. 考慮用戶的特別要求（例如：想吃雞肉）
4. 確保推薦的餐點符合營養均衡要求

營養均衡要求：
- 建議的餐點應盡量包含蛋白質（肉類、蛋、豆類等）
- 建議的餐點應盡量包含蔬菜
- 建議的餐點應盡量包含碳水化合物（米飯、麵條等）

在推薦餐點前，請先使用 ingredient_agent 取得食材清單，使用 preference_agent 取得用戶偏好。

請用繁體中文回答，格式如下：

推薦餐點：
1. [餐點名稱]
   - 所需食材：[列出需要的食材，僅使用可用食材]
   - 簡短描述：[一句話描述]

2. [餐點名稱]
   - 所需食材：[列出需要的食材]
   - 簡短描述：[一句話描述]

（可以推薦 3-5 個餐點）

如果食材不足，請建議可以搭配的額外食材。""",
    tools=[
        AgentTool(agent=ingredient_agent),
        AgentTool(agent=preference_agent),
    ]
)
