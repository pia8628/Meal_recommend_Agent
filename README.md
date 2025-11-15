# Meal Recommend Agent

一個基於 Google AI Agent Developer Kit (ADK) 的多代理系統，協助使用者管理廚房食材、紀錄飲食偏好並推薦符合需求的餐點。專案預設使用 Gemini 2.0 Flash 模型，由主控代理協調多個具備專業職責的子代理來完成任務，全程以繁體中文互動。

## 功能總覽
- **食材管理**：新增、移除與查詢現有食材清單。
- **偏好記憶**：紀錄喜歡或不喜歡的食物並隨時查詢。
- **餐點推薦**：依據現有食材與偏好推薦 3-5 道餐點，並在必要時提示缺少的食材。
- **營養檢查**：針對指定餐點提供營養均衡評估與建議。

## 架構概述
專案採用階層式代理架構：

1. **Root Agent** (`agents/root_agent.py`)
   - 作為對話入口，理解使用者意圖並分派任務給子代理。
   - 透過 `AgentTool` 對接其他代理，維持自然的中文對話流程。
2. **食材管理代理** (`agents/ingredient_agent.py`)
   - 透過 `FunctionTool` 操作本地 JSON 檔儲存的食材清單。
3. **偏好記憶代理** (`agents/preference_agent.py`)
   - 將喜好與不喜好紀錄至 JSON，並提供格式化查詢結果。
4. **餐點推薦代理** (`agents/recommendation_agent.py`)
   - 與食材、偏好代理協作，組合可行餐點方案。
5. **營養檢查代理** (`agents/nutrition_agent.py`)
   - 單純依賴 LLM 根據既定規則給出營養評估。
6. **工具函式** (`agents/tools.py`)
   - 實作新增/移除/查詢食材與偏好等純函式邏輯，確保代理調用時有一致的資料來源。

主要 CLI 入口 `main.py` 透過 `google.adk.runners.InMemoryRunner` 啟動 Root Agent 與使用者進行對話，而 `config.py` 則負責載入 `.env`、設定 Gemini API Key 以及統一管理資料檔案路徑。

## 安裝與執行
### 1. 建立虛擬環境（建議）
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. 安裝相依套件
```bash
pip install -r requirements.txt
```

### 3. 設定 Gemini API Key
建立 `.env` 檔案或於 shell 中匯出環境變數：
```bash
echo "GEMINI_API_KEY=你的_API_KEY" > .env
```
或
```bash
export GEMINI_API_KEY=你的_API_KEY
```

### 4. 啟動對話式 CLI
```bash
python main.py
```
啟動後即可使用繁體中文與系統互動，輸入 `exit` / `離開` / `quit` 結束對話。

## 互動示例
```
歡迎使用食材建議 Agent！
> 幫我把雞胸肉加進食材清單
已添加「雞胸肉」到食材清單。
> 我喜歡青花菜
已記錄您喜歡「青花菜」。
> 推薦一下今天的晚餐
推薦餐點：
1. 蒜香雞胸義大利麵
   - 所需食材：雞胸肉、義大利麵、蒜頭、青花菜
   - 簡短描述：高蛋白蒜香義大利麵搭配清爽青花菜。
...
```
實際輸出內容會根據模型回應而有所不同。

## 專案結構
```
Meal_recommend_Agent/
├── main.py                 # CLI 進入點，啟動 Root Agent
├── config.py               # API Key 與資料路徑設定
├── agents/
│   ├── root_agent.py       # 負責協調子代理的主控代理
│   ├── ingredient_agent.py # 食材管理代理
│   ├── preference_agent.py # 偏好管理代理
│   ├── recommendation_agent.py # 餐點推薦代理
│   ├── nutrition_agent.py  # 營養評估代理
│   └── tools.py            # 子代理可調用的純函式工具
├── data/
│   ├── ingredients.json    # 食材清單資料
│   └── preferences.json    # 偏好資料
├── requirements.txt        # Python 相依套件
└── README.md
```

## 資料儲存
- 食材與偏好皆以 JSON 檔案儲存在 `data/` 目錄，預設會在第一次寫入時建立。
- `agents/tools.py` 中的函式負責讀寫資料；若檔案不存在或格式錯誤，會回傳空集合並重新建立。

## 開發建議
- 如需新增工具，建議在 `agents/tools.py` 中實作純函式，並透過 `FunctionTool` 暴露給相關代理。
- 若要串接其他資料來源或模型，可在子代理 instruction 中補充規則，或擴充 Root Agent 的工具列表。
- 測試時可搭配虛擬環境與假資料檔案，以避免覆蓋實際使用者紀錄。

## 授權
此專案未附上授權條款，若需發佈請先確認授權需求。
