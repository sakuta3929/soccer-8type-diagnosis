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

#Googleスプレッドシートの設定
SHEET_LOGGING_ENABLED = True

try:
    sheet_url = st.secrets["sheet_url"] if SHEET_LOGGING_ENABLED else ""
except (KeyError, FileNotFoundError):
    sheet_url = ""

# -------------------------------------
# デザイン
# -------------------------------------

st.markdown("""
<style>
:root {
    --orange: #FF6B00;
    --orange-soft: #FFB347;
    --orange-pale: #FFF0D9;
    --cream: #FFFCF5;
    --ink: #603719;
    --muted: #9A7961;
    --line: #FFD0A3;
}

.stApp {
    background:
        radial-gradient(circle at 10% 5%, #FFB52E 0%, transparent 30%),
        linear-gradient(180deg, #FF7A00 0%, #FF8C19 45%, #FFB347 100%);
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
    <div class="hero-icon">⚽ ✦</div>
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
        "name": "感情ダダ漏れ人間",
        "description": [
            "全力で楽しみ、全力で悔しむ。\n\n",
            "好きなものへの熱量が高く、気持ちが表情や行動に出やすいタイプ周りまで巻き込むエネルギーの持ち主！"
        ],
        "strengths": [
            "・情熱があり、行動力も抜群\n\n",
            "・喜びや感謝を素直に表現できる\n\n",
            "・周囲を盛り上げ、チームの士気を高められる"
        ],
        "weeknesses": ["・感情が先走って、冷静さ失いがち\n\n",
        "・悔しいことを引きずりやすい\n\n",
        "・テンションの差が周りを驚かせることも"],
        "compatible": ["「Ｅ・Ｈ」\n\n"
        "Ｅが一緒に盛り上がってくれて、Ｈが程よく力を抜かしてくれる。"
        "熱量を受け止めてもらえる組み合わせ！"],
        "bias": "・ゴールが決まった瞬間知らない人とも喜びを分かち合う。\n\n"
        "・シュートが外れるとなぜか自分まで頭を抱える。\n\n"
        "・試合終了後も興奮が冷めず、帰り道に試合を再現し始める。\n\n"
        "・「今日は静かに観よう。」と言った五分後には叫んでる。",
        "ikon": "🌞",
    },
    "B": {
            "name": "勝手に監督就任",
            "description": "基本的な説明",
            "strengths": ["長所"],
            "weeknesses": ["短所"],
            "compatible": ["相性のいいタイプ"],
            "bias": "偏見・あるある",
            "ikon": "マーク",
    },
    "C": {
            "name": "推しがいれば世界は平和",
            "description": "基本的な説明",
            "strengths": ["長所"],
            "weeknesses": ["短所"],
            "compatible": ["相性のいいタイプ"],
            "bias": "偏見・あるある",
            "ikon": "マーク",
    },
    "D": {
            "name": "気になったら眠れない人",
            "description": "基本的な説明",
            "strengths": ["長所"],
            "weeknesses": ["短所"],
            "compatible": ["相性のいいタイプ"],
            "bias": "偏見・あるある",
            "ikon": "マーク",
    },
    "E": {
            "name": "みんなの笑顔が自分の報酬",
            "description": "基本的な説明",
            "strengths": ["長所"],
            "weeknesses": ["短所"],
            "compatible": ["相性のいいタイプ"],
            "bias": "偏見・あるある",
            "ikon": "マーク",
    },
    "F": {
            "name": "好きなものには財布緩い人",
            "description": "基本的な説明",
            "strengths": ["長所"],
            "weeknesses": ["短所"],
            "compatible": ["相性のいいタイプ"],
            "bias": "偏見・あるある",
            "ikon": "マーク",
    },
    "G": {
            "name": "目的地より道中好きな人",
            "description": "基本的な説明",
            "strengths": ["長所"],
            "weeknesses": ["短所"],
            "compatible": ["相性のいいタイプ"],
            "bias": "偏見・あるある",
            "ikon": "マーク",
    },
    "H": {
            "name": "マイペースの達人",
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
        "question": "【友達と旅行に行くならどのタイプ？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【楽しそうなら細かいことは気にせず全力で楽しむ！】", "scores": {"A": 3, "G": 1}},
            {"label": "【みんなが楽しめるように場を盛り上げる！】", "scores": {"E": 3, "B": 1}},
            {"label": "【事前に口コミや情報を調べて失敗を防ぎたい！】", "scores": {"D": 3, "B": 1}},
            {"label": "【予定になかった場所にも寄り道したい！】", "scores": {"G": 3, "H": 1}},
        ],
    },
    {
        "question": "【何かにハマった時あなたは？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【好きすぎてつい周りにも熱く語ってしまう】", "scores": {"A": 3, "E": 1}},
            {"label": "【もっと詳しくなりたくて仕組みやコツなどを調べる】", "scores": {"B": 3, "D": 1}},
            {"label": "【一つのものを長く深く好きでい続ける】", "scores": {"D": 3, "C": 1}},
            {"label": "【グッズや関連アイテムまで集めたくなる】", "scores": {"F": 3, "C": 1}},
        ],
    },
    {
        "question": "【友達と意見が食い違ったら？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【自分の意見をつい熱く主張してしまう】", "scores": {"A": 3, "B": 1}},
            {"label": "【どちらが合理的か解決策を考える】", "scores": {"B": 3, "E": 1}},
            {"label": "【相手の気持ちを考えてできるだけ丸く収める】", "scores": {"E": 3, "H": 1}},
            {"label": "【「考え方は人それぞれだよね」と思う】", "scores": {"H": 3, "G": 1}},
        ],
    },
    {
        "question": "【初めてのことに挑戦するときは？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【やると決めたら勢いで飛び込む】", "scores": {"A": 3, "G": 1}},
            {"label": "【まずは情報を集めてうまくいく方法を考える】", "scores": {"D": 3, "B": 1}},
            {"label": "【好きになったらとことん極めたい】", "scores": {"C": 3, "F": 1}},
            {"label": "【気楽に始めて楽しめればそれでＯＫ！】", "scores": {"H": 3, "G": 1}},
        ],
    },
    {
        "question": "【楽しみにしていた予定が急になくなったら？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【別の楽しみを探してすぐ気持ちを切り替えられる】", "scores": {"G": 3, "A": 1}},
            {"label": "【代わりの予定を考えて時間を有効活用する】", "scores": {"B": 3, "D": 1}},
            {"label": "【友達を誘って別の楽しいことをする】", "scores": {"E": 3, "F": 1}},
            {"label": "【せっかくだし家でのんびりする】", "scores": {"H": 3, "F": 1}},
        ],
    },
    {
        "question": "【目標を立てるなら？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【決めたからには絶対に達成したい！】", "scores": {"A": 3, "E": 1}},
            {"label": "【達成するための計画をしっかり立てる】", "scores": {"B": 3, "D": 1}},
            {"label": "【好きなことなら時間を忘れて頑張れる】", "scores": {"C": 3, "F": 1}},
            {"label": "【結果だけじゃなく過程も楽しみたい】", "scores": {"E": 3, "H": 1}},
        ],
    },
    {
        "question": "【好きな人や作品ができたら？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【感情が顔や態度に出てしまう】", "scores": {"A": 3, "E": 1}},
            {"label": "【魅力や人気の理由を分析したくなる】", "scores": {"D": 3, "B": 1}},
            {"label": "【グッズや写真など好きの証拠を残したい】", "scores": {"F": 3, "C": 1}},
            {"label": "【詳しさよりも自分が楽しめれば十分】", "scores": {"H": 3, "C": 1}},
        ],
    },
    {
        "question": "【友達から「どうしたらいいと思う？」と相談されたら？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【「こうしたらいいよ！」と全力で応援する】", "scores": {"A": 3, "E": 1}},
            {"label": "【状況を整理して具体的な解決策を考える】", "scores": {"B": 3, "D": 1}},
            {"label": "【まずは相手の気持ちに寄り添う】", "scores": {"E": 3, "C": 1}},
            {"label": "【自分が納得できる方法が一番だよ】", "scores": {"H": 3, "E": 1}},
        ],
    },
    {
        "question": "【欲しいものを見つけたときどうする？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【欲しいと思ったら勢いで買うこともある】", "scores": {"A": 3, "C": 1}},
            {"label": "【口コミや価格を比較して納得してから買う】", "scores": {"D": 3, "B": 1}},
            {"label": "【好きなブランドや推しのものなら財布が緩む】", "scores": {"F": 3, "C": 1}},
            {"label": "【必要かどうかはその時の気分で決める】", "scores": {"H": 3, "G": 1}},
        ],
    },
    {
        "question": "【友達と遊んだ日の帰り道どんな気分？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【楽しかった余韻でまだテンション高い！】", "scores": {"A": 3, "E": 1}},
            {"label": "【今日の出来事を振り返ったり次の予定を考えたりする】", "scores": {"B": 3, "G": 1}},
            {"label": "【写真や思い出を見返す】", "scores": {"F": 3, "C": 1}},
            {"label": "【「楽しかった～！」で満足。あとはのんびり】", "scores": {"H": 3, "E": 1}},
        ],
    },
    {
        "question": "【初対面の人が多い場所では？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【自分から話しかけて場を盛り上げる】", "scores": {"A": 3, "E": 1}},
            {"label": "【周りの様子を見てまずは雰囲気をつかむ】", "scores": {"D": 3, "B": 1}},
            {"label": "【気の合いそうな人と仲良くなる】", "scores": {"C": 3, "F": 1}},
            {"label": "【無理に話さず自分のペースで過ごす】", "scores": {"H": 3, "E": 1}},
        ],
    },
    {
        "question": "【友達が新しい趣味を始めたら？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【「自分もやってみたい！」となる】", "scores": {"A": 3, "G": 1}},
            {"label": "【どんな趣味なのか詳しく調べてみる】", "scores": {"B": 3, "D": 1}},
            {"label": "【自分もハマったらとことん好きになりそう】", "scores": {"C": 3, "E": 1}},
            {"label": "【面白そうなら試すし合わなければ別のことをする】", "scores": {"G": 3, "H": 1}},
        ],
    },
    {
        "question": "【グループの中でどんな役割になりがち？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【率先してみんなを動かす】", "scores": {"A": 3, "B": 1}},
            {"label": "【全体を見て段取りや役割を考える】", "scores": {"B": 3, "D": 1}},
            {"label": "【みんなが楽しめるように気を配る】", "scores": {"E": 3, "F": 1}},
            {"label": "【決まった役割よりその場の流れに任せる】", "scores": {"G": 3, "H": 1}},
        ],
    },
    {
        "question": "【自分の好きなものを否定されたら？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【「良さが分かってない！」と熱くなる】", "scores": {"A": 3, "C": 1}},
            {"label": "【好きな理由を説明して理解してもらいたくなる】", "scores": {"B": 3, "D": 1}},
            {"label": "【気にせず自分の好きなものを好きでい続ける】", "scores": {"C": 3, "F": 1}},
            {"label": "【「好みは人それぞれだし別にいいかな」と思う】", "scores": {"H": 3, "G": 1}},
        ],
    },
    {
        "question": "【みんなで何かを楽しむなら何が一番嬉しい？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【全員で盛り上がって最高の思い出を作る！】", "scores": {"A": 3, "E": 1}},
            {"label": "【みんなが楽しめるようにうまく計画する】", "scores": {"B": 3, "D": 1}},
            {"label": "【好きなものを共有して一緒に楽しむ】", "scores": {"C": 3, "F": 1}},
            {"label": "【それぞれ好きなように楽しめるのが一番】", "scores": {"H": 3, "E": 1}},
        ],
    },
    {
        "question": "【初めてサッカーの試合を観ることになった！一番楽しみなのは？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【ゴールが決まった瞬間の盛り上がり】", "scores": {"A": 3, "E": 1}},
            {"label": "【どんな作戦で試合が進むのかを見ること】", "scores": {"B": 3, "D": 1}},
            {"label": "【気になる選手を見つけて応援すること】", "scores": {"C": 3, "F": 1}},
            {"label": "【スタジアムの雰囲気やご飯も楽しみ！】", "scores": {"G": 3, "H": 1}},
        ],
    },
    {
        "question": "【近くに全力で応援している人がいたら？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【つられて自分も盛り上がる！】", "scores": {"A": 3, "H": 1}},
            {"label": "【応援のやり方が気になる】", "scores": {"B": 3, "G": 1}},
            {"label": "【自分は自分で推しや好きなチームに集中する】", "scores": {"C": 3, "E": 1}},
            {"label": "【みんなで違って面白いし自由！】", "scores": {"H": 3, "E": 1}},
        ],
    },
    {
        "question": "【試合観戦が終わった後どうする？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【勝っても負けてもしばらくソワソワ】", "scores": {"A": 3, "E": 1}},
            {"label": "【試合を振り返る】", "scores": {"B": 3, "D": 1}},
            {"label": "【好きな選手の活躍や表情を思い返す】", "scores": {"C": 3, "F": 1}},
            {"label": "【試合後のご飯や帰り道まで含めて楽しかったと思う】", "scores": {"G": 3, "H": 1}},
        ],
    },
    {
        "question": "【初めてスタジアムに行くなら事前に何をする？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【応援グッズを用意して気分を高める！】", "scores": {"A": 3, "F": 1}},
            {"label": "【座席やアクセス、試合の見どころを調べる】", "scores": {"D": 3, "B": 1}},
            {"label": "【ユニフォームやタオルなど記念になるものを探す】", "scores": {"F": 3, "C": 1}},
            {"label": "【現地で気になったものを楽しめればいい】", "scores": {"G": 3, "H": 1}},
        ],
    },
    {
        "question": "【理想のサッカー観戦はどれ？】あなたにあてはまるのは？",
        "answers": [
            {"label": "【周りと一緒に叫んでゴールの瞬間に大騒ぎ！】", "scores": {"A": 3, "E": 1}},
            {"label": "【試合の流れを読んで次の展開を予想】", "scores": {"B": 3, "D": 1}},
            {"label": "【推し選手を見守り、活躍したら最高に幸せ】", "scores": {"C": 3, "F": 1}},
            {"label": "【勝敗だけにこだわらず自分らしく楽しむ】", "scores": {"H": 3, "G": 1}},
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
        options=answer_labels,
        index=None,
        key=f"answer_{st.session_state.current_question}",
    )
    selected_answer = next(
        (a for a in q["answers"] if a["label"] == selected_label),
        None
    )

    previous_col, next_col = st.columns(2)

    with previous_col:
        if i > 0 and st.button("← 前の質問へ", key=f"previous_{i}"):
            if selected_answer is not None:
                st.session_state.user_answers[i] = selected_answer
            st.session_state.current_question -= 1
            st.rerun()
    with next_col:
        if i < len(questions) - 1:
            if st.button("次の質問へ →", key=f"next_{i}"):
                if selected_answer is None:
                    st.warning("回答を選んでね！")
                else:
                    st.session_state.user_answers[i] = selected_answer
                    st.session_state.current_question += 1
                    st.rerun()
        else:
            if st.button("診断結果を見る ✨", key="finish_button"):
                if selected_answer is None:
                    st.warning("回答を選んでね！")
                else:
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

    # Googleスプレッドシートへの記録
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
            <div class="result-icon">⚽</div>
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
        f'<div class="info-card"><div class="info-heading">🌧️ 短所・気をつけたいところ</div>{ "　・　".join(result["weeknesses"]) }</div>',
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
