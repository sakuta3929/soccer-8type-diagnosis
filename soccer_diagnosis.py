import streamlit as st
import requests

# -------------------------------------
# 診断ツールの型
# -------------------------------------

st.set_page_config(
    page_title="サッカー観戦タイプ診断",
    page_icon="⚽",
    layout="centered",
)

#後でGoogleスプレッドシートの設定

# -------------------------------------
# デザイン
# -------------------------------------

st.markdown("""
<style>
:root {
    --orange: #F29A55;
    --orange-soft: #F8C99F;
    --orange-pale: #FFF0DF;
    --cream: #FFF9F1;
    --ink: #65452F;
    --muted: #9A7961;
    --line: #F2DCC7;
}

.stApp {
    background:
        radial-gradient(circle at 8% 5%, rgba(255, 207, 157, .55), transparent 25%),
        radial-gradient(circle at 95% 32%, rgba(255, 224, 190, .55), transparent 27%),
        linear-gradient(180deg, #FFE8D0 0%, #FFF8EF 58%, #FFF0DF 100%);
    color: var(--ink);
}

.block-container {
    max-width: 780px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3, p, label, div, button {
    font-family: "Noto Sans JP", "Yu Gothic", sans-serif;
}

h1, h2, h3 {
    color: #89552F !important;
}

.hero {
    text-align: center;
    background: rgba(255, 250, 243, .88);
    border: 1px solid #F3D6B8;
    border-radius: 28px;
    padding: 1.6rem 1rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 8px 24px rgba(143, 87, 40, .08);
}
.hero-icon {
    font-size: 2.6rem;
    line-height: 1.3;
}
.hero-kicker {
    color: #C18450;
    font-size: .76rem;
    font-weight: 800;
    letter-spacing: .2rem;
    margin-top: .45rem;
}
.hero-title {
    color: #89552F;
    font-size: clamp(1.7rem, 5vw, 2.4rem);
    font-weight: 800;
    line-height: 1.45;
    margin: .35rem 0;
}
.hero-subtitle {
    color: #9A7961;
    font-size: .95rem;
    margin-top: .5rem;
}

.stTextInput input {
    background: #FFFEFB;
    border: 1.5px solid #F0D2B4;
    border-radius: 14px;
    color: var(--ink);
    min-height: 2.9rem;
}
.stTextInput input:focus {
    border-color: #E9A36B;
    box-shadow: 0 0 0 2px rgba(242, 154, 85, .16);
}

.stButton > button {
    width: 100%;
    min-height: 2.8rem;
    border: 1px solid #F1BE91;
    border-radius: 999px;
    background: #F8C99F;
    color: #754A2C;
    font-weight: 750;
    transition: all .15s ease;
}
.stButton > button:hover {
    border-color: #E9A36B;
    background: #F3B77F;
    color: #633D24;
    transform: translateY(-1px);
    box-shadow: 0 5px 14px rgba(143, 87, 40, .12);
}
.stButton > button:disabled {
    background: #F3E0CE;
    border-color: #F3E0CE;
    color: #B9A18D;
}

.question-card {
    background: rgba(255, 253, 249, .95);
    border: 1px solid #F1D9C2;
    border-radius: 22px;
    padding: 1.25rem 1.3rem;
    margin: .8rem 0 1rem;
    box-shadow: 0 5px 18px rgba(143, 87, 40, .06);
}
.question-kicker {
    color: #C18450;
    font-size: .8rem;
    font-weight: 800;
    letter-spacing: .1rem;
}
.question-text {
    color: #65452F;
    font-size: 1.2rem;
    font-weight: 750;
    line-height: 1.7;
    margin-top: .55rem;
}

div[data-testid="stRadio"] > div {
    gap: .55rem;
}
div[data-testid="stRadio"] label {
    background: rgba(255, 253, 249, .94);
    border: 1px solid #F1DCC9;
    border-radius: 15px;
    padding: .7rem .85rem;
}
div[data-testid="stRadio"] label:hover {
    border-color: #EFB783;
    background: #FFF8EF;
}

div[data-testid="stProgressBar"] {
    background: #F5DFCA;
    border-radius: 999px;
    overflow: hidden;
}
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #F8C99F, #EEA061);
    border-radius: 999px;
}

.result-card {
    text-align: center;
    background: linear-gradient(145deg, #FFF7EC, #FFFFFF);
    border: 1px solid #F0CDAA;
    border-radius: 26px;
    padding: 1.7rem 1.2rem;
    margin: 1rem 0;
    box-shadow: 0 8px 24px rgba(143, 87, 40, .09);
}
.result-icon {
    font-size: 2.8rem;
}
.result-kicker {
    color: #C18450;
    font-size: .76rem;
    font-weight: 800;
    letter-spacing: .2rem;
    margin: .45rem 0;
}
.result-title {
    color: #89552F;
    font-size: clamp(1.45rem, 4vw, 2rem);
    font-weight: 850;
    line-height: 1.5;
}
.result-description {
    color: #8D705A;
    line-height: 1.8;
    margin-top: .7rem;
}

.info-card {
    background: rgba(255, 253, 249, .92);
    border: 1px solid #F1DCC9;
    border-radius: 18px;
    padding: 1rem 1.1rem;
    margin: .7rem 0;
}
.info-heading {
    color: #A76536;
    font-weight: 800;
    margin-bottom: .45rem;
}
.soft-note {
    color: #9A7961;
    font-size: .82rem;
    text-align: center;
    margin-top: .8rem;
}

@media (max-width: 640px) {
    .block-container { padding: 1rem .75rem 2rem; }
    .hero { padding: 1.25rem .75rem; border-radius: 22px; }
    .question-card { padding: 1.05rem; border-radius: 18px; }
    .question-text { font-size: 1.08rem; }
    .result-card { padding: 1.35rem .9rem; }
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------
# タイトル
# -------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-icon">🍊 ✦</div>
    <div class="hero-kicker">YOUR PERSONALITY CHECK</div>
    <div class="hero-title">タイプ診断</div>
    <div class="hero-subtitle">いくつかの質問から、あなたのタイプを見つけます。</div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------
# タイプ
# -------------------------------------

type_results = {
    "A": {
        "name": "タイプ名",
        "description": "基本的な説明",
        "strengths": ["長所"],
        "weeknesses": ["短所"],
        "compatible": ["相性のいいタイプ"],
        "bias": "偏見・あるある",
        "ikon": "マーク",
    },
    "B": {
            "name": "タイプ名",
            "description": "基本的な説明",
            "strengths": ["長所"],
            "weeknesses": ["短所"],
            "compatible": ["相性のいいタイプ"],
            "bias": "偏見・あるある",
            "ikon": "マーク",
    },
    "C": {
            "name": "タイプ名",
            "description": "基本的な説明",
            "strengths": ["長所"],
            "weeknesses": ["短所"],
            "compatible": ["相性のいいタイプ"],
            "bias": "偏見・あるある",
            "ikon": "マーク",
    },
    "D": {
            "name": "タイプ名",
            "description": "基本的な説明",
            "strengths": ["長所"],
            "weeknesses": ["短所"],
            "compatible": ["相性のいいタイプ"],
            "bias": "偏見・あるある",
            "ikon": "マーク",
    },
    "E": {
            "name": "タイプ名",
            "description": "基本的な説明",
            "strengths": ["長所"],
            "weeknesses": ["短所"],
            "compatible": ["相性のいいタイプ"],
            "bias": "偏見・あるある",
            "ikon": "マーク",
    },
    "F": {
            "name": "タイプ名",
            "description": "基本的な説明",
            "strengths": ["長所"],
            "weeknesses": ["短所"],
            "compatible": ["相性のいいタイプ"],
            "bias": "偏見・あるある",
            "ikon": "マーク",
    },
    "G": {
            "name": "タイプ名",
            "description": "基本的な説明",
            "strengths": ["長所"],
            "weeknesses": ["短所"],
            "compatible": ["相性のいいタイプ"],
            "bias": "偏見・あるある",
            "ikon": "マーク",
    },
    "H": {
            "name": "タイプ名",
            "description": "基本的な説明",
            "strengths": ["長所"],
            "weeknesses": ["短所"],
            "compatible": ["相性のいいタイプ"],
            "bias": "偏見・あるある",
            "ikon": "マーク",
    },
}

# -------------------------------------
# 質問
# -------------------------------------

questions = [
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
    {
        "question": "【質問文】あなたにあてはまるのは？",
        "answers": [
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
            {"label": "【選択肢】", "scores": {"": 3, "": 1}},
        ],
    },
]

# -------------------------------------
# セッション状態の初期化
# -------------------------------------

if "started" not in st.session_state:
    st.session_state.started = False
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = [None] * len(questions)
if "finished" not in st.session_state:
    st.session_state.finished = False
if "sent_to_sheet" not in st.session_state:
    st.session_state.sent_to_sheet = False
if "sent_name" not in st.session_state:
    st.session_state.sent_name = ""

# 名前は必須
name = st.text_input("お名前を入力して下さい。", placeholder="例：ゆうた", key="name_input")

if not name:
    st.info("⚠　診断を始めるには、お名前を入力してください。")

# -------------------------------------
# スタート画面
# -------------------------------------

if not st.session_state.started and not st.session_state.finished:
    if st.button("診断スタート  →", disabled=not name.strip(), key="start_button"):
        st.session_state.started = True
        st.rerun()
    st.markdown(
        '<div class="soft-note">質問にひとつずつ答えてね ✦</div>',
        unsafe_allow_html=True,
    )

# -------------------------------------
# 質問画面
# -------------------------------------

if st.session_state.started and not st.session_state.finished:
    i = st.session_state.current_question
    q = questions[i]

    st.progress((i + 1) / len(questions))
    st.markdown(
        f"""
        <div class="question-card">
            <div class="question-kicker">QUESTION {i + 1:02d}　·　{i + 1}/{len(questions)}</div>
            <div class="question-text">{q["question"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    answer_labels = [a["label"] for a in q["answers"]]
    saved_answer = st.session_state.user_answers[i]
    saved_label = saved_answer["label"] if saved_answer else answer_labels[0]
    default_index = answer_labels.index(saved_label) if saved_label in answer_labels else 0

    selected_label = st.radio(
        "いちばん近いものを選んでね！",
        answer_labels,
        index=default_index,
        key=f"answer_{i}",
    )
    selected_answer = next(a for a in q["answers"] if a["label"] == selected_label)

    previous_col, next_col = st.columns(2)
    with previous_col:
        if i > 0 and st.button("← 前の質問へ", key=f"previous_{i}"):
            st.session_state.user_answers[i] = selected_answer
            st.session_state.current_question -= 1
            st.rerun()
    with next_col:
        if i < len(questions) - 1:
            if st.button("次の質問へ →", key=f"next_{i}"):
                st.session_state.user_answers[i] = selected_answer
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("診断結果を見る ✨", key="finish_button"):
                st.session_state.user_answers[i] = selected_answer
                st.session_state.finished = True
                st.rerun()

# -------------------------------------
# 診断結果
# -------------------------------------

if st.session_state.finished:
    scores = {type_key: 0 for type_key in type_results}

    for answer in st.session_state.user_answers:
        if answer:
            for type_key, points in answer["scores"].items():
                if type_key in scores:
                    scores[type_key] += points

    highest_score = max(scores.values())
    winners = [key for key, score in scores.items() if score == highest_score]
    result_key = winners[0]
    result = type_results[result_key]

    # Googleスプレッドシートへの記録（必要な場合のみ）
    if (
        SHEET_LOGGING_ENABLED
        and sheet_url
        and (not st.session_state.sent_to_sheet or st.session_state.sent_name != name.strip())
    ):
        data = {"name": name.strip(), "result": result["name"], **scores}
        try:
            response = requests.post(sheet_url, data=data, timeout=15)
            response.raise_for_status()
            st.session_state.sent_to_sheet = True
            st.session_state.sent_name = name.strip()
        except requests.RequestException:
            st.warning("結果は表示できましたが、記録の送信に失敗しました。")

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-icon">{result["icon"]}</div>
            <div class="result-kicker">YOUR RESULT</div>
            <div class="result-title">{result["name"]}</div>
            <div class="result-description">{result["description"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="info-card"><div class="info-heading">🌟 長所</div>{ "　・　".join(result["strengths"]) }</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="info-card"><div class="info-heading">🌧️ 短所・気をつけたいところ</div>{ "　・　".join(result["weaknesses"]) }</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="info-card"><div class="info-heading">💞 相性のいいタイプ</div>{ "　・　".join(result["compatible"]) }</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="info-card"><div class="info-heading">👀 ちょっとした偏見・あるある</div>{result["bias"]}</div>',
        unsafe_allow_html=True,
    )

    st.subheader("📊 タイプ別スコア")
    for type_key, score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
        st.write(f"**{type_results[type_key]['name']}**　{score}点")
        st.progress(score / highest_score if highest_score else 0)

    if st.button("↻ もう一度診断する", key="restart_button"):
        st.session_state.started = False
        st.session_state.current_question = 0
        st.session_state.user_answers = [None] * len(questions)
        st.session_state.finished = False
        st.session_state.sent_to_sheet = False
        st.session_state.sent_name = ""
        for key in list(st.session_state.keys()):
            if key.startswith("answer_"):
                del st.session_state[key]
        st.rerun()