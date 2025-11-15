"""CLI 主程式入口 - 使用 Google ADK"""
from config import setup_adk
from agents.root_agent import root_agent
from google.adk.runners import InMemoryRunner

def main():
    """主程式"""
    # 初始化 ADK 設定
    try:
        setup_adk()
    except ValueError as e:
        print(f"設定錯誤：{e}")
        return
    
    # 建立 Runner
    runner = InMemoryRunner(agent=root_agent)
    
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
            result = runner.run(user_input)
            
            # 顯示結果
            print(result)
            print()
        
        except KeyboardInterrupt:
            print("\n\n再見！")
            break
        except Exception as e:
            print(f"發生錯誤：{str(e)}")
            print()

if __name__ == "__main__":
    main()
