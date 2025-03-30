from ai_rag import ask_to_ai_rag

if __name__ == "__main__":
    # ✨ 프롬프트 문자열 직접 구성
    prompt_input = "Emotion: SLEEPY, Time: 22:30, Request: I want to feel cozy and relaxed with warm tones"

    # 🧠 AI에게 질문
    try:
        result = ask_to_ai_rag(prompt_input)

        # 🎨 결과 출력
        print("\n🌈 Recommended Light Setting:")
        print(f"🎨 Color  : {result['color']}")
        print(f"💡 Reason : {result['reason']}")
        print(f"📘 Advice : {result['advice']}")

    except Exception as e:
        print("❌ 테스트 실패:", e)
