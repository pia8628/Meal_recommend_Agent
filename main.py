"""CLI 主程式入口 - 使用 Google ADK"""
import asyncio
from typing import Optional

from google.genai import types

from agents.root_agent import root_agent
from agents.tools import (
    add_preferences_to_memory,
    preferences_available,
    reset_preferences,
)
from config import setup_adk
from google.adk.runners import InMemoryRunner


def _collect_agent_response(events) -> Optional[str]:
    """從事件串流中擷取最後的文字回應。"""

    response_text: Optional[str] = None
    for event in events:
        if event.author == "user":
            continue
        if not event.content or not event.content.parts:
            continue
        parts = [part.text for part in event.content.parts if getattr(part, "text", None)]
        if parts:
            response_text = "".join(parts)
    return response_text


def main():
    """主程式"""
    # 初始化 ADK 設定
    try:
        setup_adk()
    except ValueError as e:
        print(f"設定錯誤：{e}")
        return

    # 建立 Runner 與對話會話
    runner = InMemoryRunner(agent=root_agent)
    reset_preferences()

    user_id = "cli_user"
    session = runner.session_service.create_session_sync(
        app_name=runner.app_name,
        user_id=user_id,
    )
    session_id = session.id

    print("=" * 50)
    print("歡迎使用食材建議 Agent！")
    print("我可以幫您管理食材、記錄偏好、推薦餐點。")
    print("輸入 'exit' 或 '離開' 結束對話")
    print("=" * 50)
    print()

    while True:
        try:
            # 取得用戶輸入
            user_input = input("> ").strip()

            if not user_input:
                continue

            # 檢查是否要離開
            if user_input.lower() in ["exit", "quit", "離開", "再見"]:
                print("再見！")
                break

            # 使用 Runner 執行 Agent
            content = types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_input)],
            )

            events = runner.run(
                user_id=user_id,
                session_id=session_id,
                new_message=content,
            )

            result = _collect_agent_response(events)

            # 顯示結果
            if result:
                print(result)
            else:
                print("（目前沒有文字回應）")
            print()

        except KeyboardInterrupt:
            print("\n\n再見！")
            break
        except Exception as e:
            print(f"發生錯誤：{str(e)}")
            print()

    # 對話結束後，將偏好寫入 ADK 記憶體
    try:
        if preferences_available():
            saved = asyncio.run(
                add_preferences_to_memory(
                    runner.memory_service,
                    app_name=runner.app_name,
                    user_id=user_id,
                )
            )
            if saved:
                print("已將本次偏好記錄存入記憶庫。")
    except Exception as err:
        print(f"儲存偏好至記憶庫時發生錯誤：{err}")
    finally:
        reset_preferences()


if __name__ == "__main__":
    main()
