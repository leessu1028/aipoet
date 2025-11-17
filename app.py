from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os

st.title("인공지능 시인")

# 사이드바에 API 키 입력란 추가
with st.sidebar:
    st.header("설정")
    api_key = st.text_input(
        "Google API Key를 입력하세요",
        type="password",
        placeholder="AIza...",
        help="Google AI Studio에서 API 키를 발급받을 수 있습니다. https://makersuite.google.com/app/apikey"
    )

# API 키가 입력되었는지 확인
if not api_key:
    st.warning("⚠️ 왼쪽 사이드바에서 Google API Key를 입력해주세요.")
    st.stop()

# API 키를 환경 변수에 설정
os.environ["GOOGLE_API_KEY"] = api_key

try:
    # Google Gemini 초기화
    llm = init_chat_model("gemini-1.5-flash", model_provider="google_genai")
    
    # 프롬프트 템플릿 생성
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "{input}")
    ])
    
    output_parser = StrOutputParser()
    
    chain = prompt | llm | output_parser
    
    # 메인 화면
    content = st.text_input("시의 주제를 제시해주세요")
    
    # 시 작성 요청하기
    if st.button("시 작성 요청하기"):
        if not content:
            st.warning("시의 주제를 입력해주세요.")
        else:
            with st.spinner("시를 작성하는 중입니다..."):
                result = chain.invoke({"input": content + "에 대한 시를 써줘"})
                st.write(result)
                
except Exception as e:
    st.error(f"오류가 발생했습니다: {str(e)}")
    st.info("API 키가 올바른지 확인해주세요.")
