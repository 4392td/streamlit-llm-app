from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

def get_expert_response(input_text, expert_type):
    """
    入力テキストと専門家タイプを受け取り、LLMからの回答を返す関数
    
    Args:
        input_text (str): ユーザーの入力テキスト
        expert_type (str): 選択された専門家のタイプ
    
    Returns:
        str: LLMからの回答
    """
    # 専門家タイプに応じてシステムメッセージを設定
    expert_prompts = {
        "健康アドバイザー": "あなたは健康に関する専門家です。科学的根拠に基づいた安全で実用的な健康アドバイスを提供してください。医療診断や治療に関する内容は避け、一般的な健康維持に関するアドバイスに留めてください。",
        "料理研究家": "あなたは料理の専門家です。美味しく栄養バランスの取れた料理のレシピや調理法、食材の選び方について詳しくアドバイスしてください。初心者にも分かりやすく説明してください。",
        "プログラミング講師": "あなたはプログラミングの専門家です。様々なプログラミング言語やツールについて、初心者から上級者まで理解できるよう丁寧に説明してください。実践的なコード例も含めて回答してください。",
        "旅行コンサルタント": "あなたは旅行の専門家です。世界各地の観光地、文化、交通手段、宿泊施設について詳しい知識を持っています。予算や目的に応じた最適な旅行プランを提案してください。",
        "ビジネスコンサルタント": "あなたはビジネスの専門家です。経営戦略、マーケティング、組織運営、財務管理などについて実践的なアドバイスを提供してください。具体的で実行可能な提案を心がけてください。"
    }
    
    try:
        # ChatOpenAIインスタンスの作成
        llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7,
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        
        # メッセージリストの作成
        messages = [
            SystemMessage(content=expert_prompts[expert_type]),
            HumanMessage(content=input_text)
        ]
        
        # LLMに送信して回答を取得
        result = llm(messages)
        return result.content
        
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

def main():
    st.set_page_config(
        page_title="LangChain専門家チャットアプリ",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 LangChain専門家チャットアプリ")
    
    # アプリの概要説明
    st.markdown("""
    ## 📖 アプリの概要
    このアプリは、LangChainを使用して様々な分野の専門家とチャットできるWebアプリケーションです。
    
    ## 🎯 操作方法
    1. **専門家を選択**: 下のラジオボタンから相談したい専門家を選んでください
    2. **質問を入力**: テキストエリアに質問や相談内容を入力してください
    3. **送信**: 「回答を取得」ボタンをクリックして専門家からの回答を受け取ってください
    
    ## 🔧 技術仕様
    - **フレームワーク**: Streamlit
    - **LLMライブラリ**: LangChain
    - **言語モデル**: OpenAI GPT-4o-mini
    - **Pythonバージョン**: 3.11
    """)
    
    st.divider()
    
    # 専門家タイプの選択
    st.subheader("👨‍⚕️ 専門家を選択してください")
    expert_type = st.radio(
        "どの分野の専門家に相談しますか？",
        ["健康アドバイザー", "料理研究家", "プログラミング講師", "旅行コンサルタント", "ビジネスコンサルタント"],
        horizontal=True
    )
    
    # 選択された専門家の説明
    expert_descriptions = {
        "健康アドバイザー": "💊 健康管理、運動、栄養に関するアドバイスを提供します",
        "料理研究家": "👨‍🍳 レシピ、調理法、食材の選び方について詳しく教えます",
        "プログラミング講師": "💻 プログラミング言語、ツール、開発手法について説明します",
        "旅行コンサルタント": "✈️ 世界各地の観光情報、旅行プランを提案します",
        "ビジネスコンサルタント": "📊 経営戦略、マーケティング、組織運営についてアドバイスします"
    }
    
    st.info(f"**選択中**: {expert_descriptions[expert_type]}")
    
    st.divider()
    
    # 入力フォーム
    st.subheader("💬 質問・相談内容を入力してください")
    user_input = st.text_area(
        "ここに質問や相談内容を入力してください：",
        placeholder=f"{expert_type}に相談したい内容を詳しく書いてください...",
        height=150
    )
    
    # 送信ボタン
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submit_button = st.button("🚀 回答を取得", type="primary", use_container_width=True)
    
    # 回答の表示
    if submit_button:
        if user_input.strip():
            with st.spinner(f"{expert_type}が回答を考えています..."):
                response = get_expert_response(user_input, expert_type)
            
            st.divider()
            st.subheader(f"💡 {expert_type}からの回答")
            st.success(response)
            
            # トークン使用量の表示（参考情報）
            st.caption("※ 回答はAIによって生成されたものです。重要な決定を行う際は、必ず専門家にご相談ください。")
            
        else:
            st.error("質問内容を入力してください。")
    
    # サイドバーに追加情報
    with st.sidebar:
        st.header("📋 使用上の注意")
        st.markdown("""
        - 生成された回答は参考情報です
        - 医療や法律に関する重要な判断は専門家にご相談ください
        - APIキーが必要です（環境変数OPENAI_API_KEYに設定）
        """)
        
        st.header("🔗 関連情報")
        st.markdown("""
        - [LangChain公式ドキュメント](https://python.langchain.com/)
        - [OpenAI API](https://openai.com/api/)
        - [Streamlit公式サイト](https://streamlit.io/)
        """)

if __name__ == "__main__":
    main()