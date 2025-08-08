# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime 
import utils
import os 
import warnings
warnings.filterwarnings("ignore")
# import Personality.gen_prompt as gen_prompt

st.title("Big Five 성격 검사")
# 설명 텍스트 (줄바꿈 포함)
st.markdown("""
다음은 사람의 **Big-Five 성격 특성**을 측정하기 위한 44가지 질문 세트입니다.  
Big-Five 성격 특성은 다음 다섯 가지 측면을 연속적인 점수로 평가합니다:

- **Openness** (개방성)  
- **Conscientiousness** (성실성)  
- **Extraversion** (외향성)  
- **Agreeableness** (친화성)  
- **Neuroticism** (신경성)  

각 문항에 대해 자신의 성격과 얼마나 잘 일치하는지  
리커트 척도 (매우 그렇지 않다 ~ 매우 그렇다) 를 사용해 응답해주세요.
""")

participant_id = st.number_input("🧑 실험자 번호를 입력하세요:", min_value=1, step=1)


questions = {
    1: ("말을 많이 한다", "BFI_EXT"),
    2: ("다른 사람의 약점을 잘 알아챈다", "BFI_AGR"),
    3: ("일을 신중하고 완전하게 수행한다", "BFI_CON"),
    4: ("슬프고 우울한 편이다", "BFI_NEU"),
    5: ("독창적이며 새로운 아이디어를 잘 떠올린다", "BFI_OPEN"),
    6: ("자신의 생각을 속으로 간직한다", "BFI_EXT"),
    7: ("다른 사람에게 이타적이며 도움이 된다", "BFI_AGR"),
    8: ("약간 덤벙대는 면이 있다", "BFI_CON"),
    9: ("침착하며 스트레스를 잘 다룬다", "BFI_NEU"),
    10: ("다양한 것들에 대해 호기심이 많다", "BFI_OPEN"),
    11: ("에너지가 넘친다", "BFI_EXT"),
    12: ("다른 사람과 자주 다툰다", "BFI_AGR"),
    13: ("성실하고 열심히 일하는 편이다", "BFI_CON"),
    14: ("긴장하고 쉽게 불안해지는 편이다", "BFI_NEU"),
    15: ("영리하고 생각이 많은 편이다", "BFI_OPEN"),
    16: ("분위기를 흥겹게 만든다", "BFI_EXT"),
    17: ("다른 사람을 쉽게 용서한다", "BFI_AGR"),
    18: ("정리가 잘 안 된 편이다", "BFI_CON"),
    19: ("걱정이 많다", "BFI_NEU"),
    20: ("상상력이 풍부하다", "BFI_OPEN"),
    21: ("조용한 편이다", "BFI_EXT"),
    22: ("대체로 사람을 신뢰하는 편이다", "BFI_AGR"),
    23: ("게으른 편이다", "BFI_CON"),
    24: ("쉽게 감정이 동요되지 않으며 안정적이다", "BFI_NEU"),
    25: ("창의적이고 독창적이다", "BFI_OPEN"),
    26: ("자신감 있고 강한 성격을 가졌다", "BFI_EXT"),
    27: ("다른 사람에게 차갑고 거리감이 있다", "BFI_AGR"),
    28: ("일이 끝날 때까지 계속한다", "BFI_CON"),
    29: ("기분 변화가 심한 편이다", "BFI_NEU"),
    30: ("예술적·창의적 경험을 좋아한다", "BFI_OPEN"),
    31: ("약간 수줍은 편이다", "BFI_EXT"),
    32: ("대부분의 사람들에게 친절하고 사려 깊다", "BFI_AGR"),
    33: ("일을 빠르고 신중하게 처리한다", "BFI_CON"),
    34: ("어려운 상황에서도 침착함을 유지한다", "BFI_NEU"),
    35: ("매번 같은 종류의 일을 선호한다", "BFI_OPEN"),
    36: ("사교적이고 사람들과 어울리기 좋아한다", "BFI_EXT"),
    37: ("때때로 다른 사람에게 무례하다", "BFI_AGR"),
    38: ("계획을 세우고 잘 지킨다", "BFI_CON"),
    39: ("쉽게 긴장하고 불안해한다", "BFI_NEU"),
    40: ("생각하고 아이디어를 다루는 걸 좋아한다", "BFI_OPEN"),
    41: ("연극, 음악과 같은 예술적인 것을 좋아하지 않는다", "BFI_OPEN"),
    42: ("협력하고 남과 잘 어울리는 편이다", "BFI_AGR"),
    43: ("주의 집중에 어려움이 있다", "BFI_CON"),
    44: ("예술, 음악, 책에 대해 아는 것이 많다", "BFI_OPEN")
}

# 응답 수집
options = {
    "매우 그렇지 않다": 1,
    "그렇지 않다": 2,
    "보통이다": 3,
    "그렇다": 4,
    "매우 그렇다": 5
}

responses = {}
st.markdown("---")
for q_num, (q_text, _) in questions.items():
    # st.markdown(f"**{q_num}. {q_text}**")
    st.markdown(f"<h4>{q_num}. {q_text}</h4>", unsafe_allow_html=True)

    response = st.radio("", list(options.keys()), key=f"q_{q_num}", index=None, label_visibility="collapsed")
    responses[q_num] = response
    st.markdown("---")

# 제출 버튼
if st.button("제출"):
    # 응답 누락 검사
    if participant_id is None or participant_id == 0:
        st.warning("⚠️ 실험자 번호를 입력해주세요.")
    elif None in responses.values():
        st.warning("⚠️ 모든 문항에 응답해주세요.")
    else:
        # DataFrame 구성
        df = pd.DataFrame([
            {
                "P_Num": participant_id,
                "Q_Num": q,
                "OCEAN": questions[q][1],
                "Score": options[resp]
            }
            for q, resp in responses.items()
        ])
        
      
        st.success("✅ 모든 문항이 제출되었습니다!")
        
        # 전체 응답 CSV 읽기 또는 생성
        if os.path.exists("bfi_responses.csv"):
            df_all = pd.read_csv("bfi_responses.csv")
            df_all = pd.concat([df_all, df], ignore_index=True)
        else:
            df_all = df.copy()

        # # 저장
        df_all.to_csv("bfi_responses.csv", index=False)
        # df_all = pd.read_csv("bfi_responses.csv")
        # 점수 계산 (참가자 번호 전달)
        score = utils.scoring(df_all, participant_id)
        score_df = pd.DataFrame([score])
        score_df.insert(0, "P_Num", participant_id)  # 참가자 번호 추가
        score_df.to_csv(f"final_score.csv", index=False)
        
        st.write("### Big Five 성격 점수")
        st.write(score)

        utils.plot_bfi_radar(score, filename=f"plot/bfi_{participant_id}", id=participant_id)
        st.image(f"plot/bfi_{participant_id}.png", caption="Big Five 성격 차트")
        st.markdown("[(클릭하세요!) Big Five 성격 특성 이론](https://youtu.be/DlGjRsbRmtI?si=Yq4i1ebiYZW0TTNQ&t=146)", unsafe_allow_html=True)


                