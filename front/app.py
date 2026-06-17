import os

import requests
import streamlit as st


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(
    page_title="PensionFit",
    page_icon="💼",
    layout="wide",
)

# ── 글로벌 CSS ────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* 전체 레이아웃 */
    .main .block-container {
        max-width: 1240px;
        padding-top: 0 !important;
        padding-bottom: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* 헤더 */
    .pf-header {
        background: #0f2645;
        border-bottom: 3px solid #2563eb;
        padding: 1.6rem 2.5rem 1.4rem;
        margin: 0 -2rem 1.75rem -2rem;
    }
    .pf-header-row {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 0.3rem;
    }
    .pf-badge {
        background: #2563eb;
        color: #fff;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        padding: 0.2rem 0.6rem;
        border-radius: 5px;
    }
    .pf-title {
        color: #fff;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .pf-sub {
        color: #7fb3f5;
        font-size: 0.82rem;
        margin-left: calc(0.7rem + 2.2rem); /* badge width 보정 */
    }

    /* 상태 / 공지 행 */
    .top-bar {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.25rem;
    }
    .sbadge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.28rem 0.8rem;
        border-radius: 999px;
        white-space: nowrap;
    }
    .sbadge-ok   { background: #dcfce7; color: #15803d; }
    .sbadge-fail { background: #fee2e2; color: #b91c1c; }
    .notice {
        flex: 1;
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 7px;
        padding: 0.45rem 0.9rem;
        font-size: 0.8rem;
        color: #1d4ed8;
    }

    /* 생애주기 카드 버튼 */
    div[class*="st-key-life_stage_card_"] button {
        height: 124px !important;
        min-height: 124px !important;
        border-radius: 10px !important;
        padding: 0.75rem 0.5rem !important;
        white-space: pre-line !important;
        line-height: 1.45 !important;
    }
    div[class*="st-key-life_stage_card_"] button p {
        white-space: pre-line !important;
        line-height: 1.45 !important;
        margin: 0 !important;
    }
    .lc-card.lc-selected .lc-card-name { color: #1d4ed8; }
    .lc-card.lc-selected .lc-card-desc { color: #3b82f6; }

    /* 섹션 라벨 */
    .field-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #64748b;
        letter-spacing: 0.03em;
        margin: 0.9rem 0 0.35rem;
    }

    /* 입력 패널 구분선 */
    .pf-divider {
        border: none;
        border-top: 1px solid #f1f5f9;
        margin: 0.85rem 0;
    }

    /* 추천 버튼 */
    div[data-testid="stBaseButton-primary"].submit-btn button {
        background: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
        color: #fff !important;
        border-radius: 9px !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        padding: 0.6rem !important;
        letter-spacing: 0.01em;
    }

    /* 결과: 빈 상태 */
    .result-empty {
        padding: 3.5rem 1rem;
        text-align: center;
        color: #94a3b8;
    }
    .result-empty-icon { font-size: 2.2rem; margin-bottom: 0.6rem; }
    .result-empty-msg  { font-size: 0.88rem; line-height: 1.65; }

    /* 프로필 배너 */
    .profile-banner {
        background: #0f2645;
        border-left: 4px solid #3b82f6;
        border-radius: 10px;
        padding: 1.05rem 1.3rem;
        margin-bottom: 1rem;
    }
    .profile-banner-title {
        color: #fff;
        font-size: 1.05rem;
        font-weight: 700;
        margin: 0 0 0.25rem;
    }
    .profile-banner-summary {
        color: #93c5fd;
        font-size: 0.81rem;
        line-height: 1.5;
        margin: 0 0 0.5rem;
    }
    .profile-banner-meta {
        font-size: 0.72rem;
        color: #4b6fa8;
        border-top: 1px solid #1e3a6b;
        padding-top: 0.4rem;
        margin-top: 0.4rem;
    }

    /* 비중 카드 */
    .ratio-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.7rem;
        margin-bottom: 1.1rem;
    }
    .ratio-card {
        border-radius: 9px;
        padding: 0.85rem 1rem;
        text-align: center;
    }
    .ratio-card.risk { background: #fff1f2; border: 1px solid #fecdd3; }
    .ratio-card.safe { background: #f0fdf4; border: 1px solid #bbf7d0; }
    .ratio-card-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    .ratio-card.risk .ratio-card-label { color: #be123c; }
    .ratio-card.safe .ratio-card-label { color: #15803d; }
    .ratio-card-value {
        font-size: 2.1rem;
        font-weight: 800;
        line-height: 1;
        letter-spacing: -0.02em;
    }
    .ratio-card.risk .ratio-card-value { color: #e11d48; }
    .ratio-card.safe .ratio-card-value { color: #16a34a; }
    .ratio-card-sub {
        font-size: 0.7rem;
        color: #94a3b8;
        margin-top: 0.2rem;
    }

    /* 배분 차트 */
    .alloc-title {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.07em;
        color: #94a3b8;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }
    .alloc-item { margin-bottom: 0.65rem; }
    .alloc-meta {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 0.25rem;
    }
    .alloc-name {
        font-size: 0.8rem;
        font-weight: 600;
        color: #334155;
    }
    .alloc-pct {
        font-size: 0.8rem;
        font-weight: 700;
    }
    .alloc-role {
        font-size: 0.71rem;
        color: #94a3b8;
        margin-top: 0.1rem;
        margin-bottom: 0.3rem;
    }
    .alloc-track {
        height: 7px;
        background: #f1f5f9;
        border-radius: 4px;
        overflow: hidden;
    }
    .alloc-fill {
        height: 100%;
        border-radius: 4px;
    }

    /* 탭 콘텐츠 */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 0.75rem !important;
    }

    /* 리스트 */
    .pf-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .pf-list li {
        display: flex;
        gap: 0.55rem;
        padding: 0.5rem 0;
        border-bottom: 1px solid #f8fafc;
        font-size: 0.855rem;
        color: #334155;
        line-height: 1.55;
    }
    .pf-list li .bullet {
        color: #3b82f6;
        font-weight: 700;
        flex-shrink: 0;
        margin-top: 0.05rem;
    }

    /* 체크리스트 */
    .pf-checklist {
        list-style: none;
        padding: 0;
        margin: 0.5rem 0 0;
    }
    .pf-checklist li {
        display: flex;
        gap: 0.55rem;
        padding: 0.45rem 0;
        font-size: 0.855rem;
        color: #334155;
        line-height: 1.55;
    }
    .pf-checklist li .box {
        color: #3b82f6;
        font-weight: 700;
        flex-shrink: 0;
    }

    /* 면책 */
    .disclaimer {
        background: #fefce8;
        border: 1px solid #fde68a;
        border-radius: 7px;
        padding: 0.65rem 0.9rem;
        font-size: 0.78rem;
        color: #92400e;
        line-height: 1.5;
        margin-top: 0.75rem;
    }

    /* selectbox label 크기 */
    div[data-testid="stSelectbox"] label {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── 헬퍼 함수 ─────────────────────────────────────────────

def check_backend() -> bool:
    try:
        resp = requests.get(f"{BACKEND_URL}/health", timeout=3)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def request_recommendation(payload: dict) -> dict:
    resp = requests.post(f"{BACKEND_URL}/recommend", json=payload, timeout=8)
    resp.raise_for_status()
    return resp.json()


BAR_COLORS = ["#2563eb", "#7c3aed", "#0891b2", "#059669", "#d97706", "#dc2626"]


def bar_color(idx: int) -> str:
    return BAR_COLORS[idx % len(BAR_COLORS)]


def render_list(items: list[str], cls: str = "pf-list", bullet: str = "→") -> None:
    html = f"<ul class='{cls}'>" + "".join(
        f"<li><span class='bullet'>{bullet}</span><span>{item}</span></li>"
        for item in items
    ) + "</ul>"
    st.markdown(html, unsafe_allow_html=True)


def render_checklist(items: list[str]) -> None:
    html = "<ul class='pf-checklist'>" + "".join(
        f"<li><span class='box'>☐</span><span>{item}</span></li>"
        for item in items
    ) + "</ul>"
    st.markdown(html, unsafe_allow_html=True)


# ── 세션 초기화 ───────────────────────────────────────────

if "life_stage_radio" not in st.session_state:
    st.session_state["life_stage_radio"] = "20~30대"
if "life_stage" not in st.session_state:
    st.session_state["life_stage"] = st.session_state["life_stage_radio"]


# ── 헤더 ──────────────────────────────────────────────────

backend_ok = check_backend()

st.markdown(
    """
    <div class="pf-header">
        <div class="pf-header-row">
            <span class="pf-badge">PF</span>
            <span class="pf-title">PensionFit</span>
        </div>
        <div class="pf-sub">미래에셋 연금투자 가이드북 기반 &nbsp;·&nbsp; 생애주기별 연금 포트폴리오 추천</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── 상태 / 공지 ───────────────────────────────────────────

if backend_ok:
    badge_html = '<span class="sbadge sbadge-ok">● 서버 연결 정상</span>'
else:
    badge_html = '<span class="sbadge sbadge-fail">● 서버 연결 실패</span>'

st.markdown(
    f"""
    <div class="top-bar">
        {badge_html}
        <div class="notice">⚠ 본 서비스는 과제용 교육 서비스이며 실제 투자 권유나 투자자문이 아닙니다.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── 본문 2컬럼 ────────────────────────────────────────────

input_col, result_col = st.columns([1, 1.4], gap="large")

# ── 좌측: 입력 패널 ──────────────────────────────────────

LIFE_STAGES = {
    "20~30대":   ("🌱", "장기 성장자산 집중\n운용"),
    "40~50대":   ("⚖️", "성장과 방어의\n균형"),
    "60대 이상": ("🏖️", "현금흐름과 안정성\n중심"),
}

PORTFOLIO_OPTIONS = {
    "20~30대": ["성장형", "밸런스형"],
    "40~50대": ["밸런스형", "안정형"],
    "60대 이상": ["밸런스형", "안정형"],
}

with input_col:
    with st.container(border=True):
        st.markdown("#### 사용자 정보 입력")

        # 생애주기
        st.markdown('<div class="field-label">생애주기</div>', unsafe_allow_html=True)

        life_stage = st.radio(
            "생애주기",
            list(LIFE_STAGES.keys()),
            key="life_stage_radio",
            label_visibility="collapsed",
            horizontal=True,
        )
        st.session_state["life_stage"] = life_stage

        def set_life_stage(stage: str) -> None:
            st.session_state["life_stage"] = stage
            st.session_state["life_stage_radio"] = stage

        card_cols = st.columns(3)
        for idx, (stage, (icon, desc)) in enumerate(LIFE_STAGES.items()):
            selected = stage == life_stage
            with card_cols[idx]:
                st.button(
                    f"{icon}\n\n{stage}\n{desc}",
                    key=f"life_stage_card_{idx}",
                    type="primary" if selected else "secondary",
                    use_container_width=True,
                    on_click=set_life_stage,
                    args=(stage,),
                )

        st.markdown('<hr class="pf-divider">', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            portfolio_options = PORTFOLIO_OPTIONS[life_stage]
            if (
                "portfolio_type" not in st.session_state
                or st.session_state["portfolio_type"] not in portfolio_options
            ):
                st.session_state["portfolio_type"] = portfolio_options[0]

            portfolio_type = st.selectbox(
                "투자 유형",
                portfolio_options,
                key="portfolio_type",
                help="가이드북 표에 제시된 포트폴리오 유형만 선택합니다.",
            )
        with col_b:
            account_type = st.selectbox(
                "연금 계좌 종류",
                ["개인연금", "퇴직연금 DC", "IRP"],
                help="계좌 종류에 따라 위험자산 한도와 추천 비중이 달라집니다.",
            )

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        payload = {
            "life_stage": life_stage,
            "portfolio_type": portfolio_type,
            "account_type": account_type,
        }

        submitted = st.button(
            "포트폴리오 추천 받기  →",
            type="primary",
            use_container_width=True,
        )

# ── 우측: 결과 패널 ──────────────────────────────────────

with result_col:
    with st.container(border=True):
        st.markdown("#### 추천 결과")

        if not submitted:
            st.markdown(
                """
                <div class="result-empty">
                    <div class="result-empty-icon">📊</div>
                    <div class="result-empty-msg">
                        생애주기·투자 유형을 선택한 뒤<br>
                        <strong>포트폴리오 추천 받기</strong> 버튼을 눌러주세요.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:
            try:
                result = request_recommendation(payload)
            except requests.RequestException as error:
                st.error("추천 결과를 받아오지 못했습니다. FastAPI 서버 상태를 확인해주세요.")
                st.caption(str(error))
            else:
                # 프로필 배너
                st.markdown(
                    f"""
                    <div class="profile-banner">
                        <div class="profile-banner-title">✦ {result["profile_title"]}</div>
                        <div class="profile-banner-summary">{result["portfolio_summary"]}</div>
                        <div class="profile-banner-meta">
                            {result["guide_basis"]} &nbsp;·&nbsp; 포메이션: {result["formation_name"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # 비중 수치
                st.markdown(
                    f"""
                    <div class="ratio-row">
                        <div class="ratio-card risk">
                            <div class="ratio-card-label">위험자산</div>
                            <div class="ratio-card-value">{result["risk_asset_ratio"]}%</div>
                            <div class="ratio-card-sub">주식·성장형 ETF</div>
                        </div>
                        <div class="ratio-card safe">
                            <div class="ratio-card-label">안정자산</div>
                            <div class="ratio-card-value">{result["safe_asset_ratio"]}%</div>
                            <div class="ratio-card-sub">채권·현금성 자산</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # 자산 배분 바
                st.markdown('<div class="alloc-title">자산 배분 상세</div>', unsafe_allow_html=True)

                alloc_html = ""
                for i, item in enumerate(result["allocation"]):
                    color = bar_color(i)
                    alloc_html += f"""
                    <div class="alloc-item">
                        <div class="alloc-meta">
                            <span class="alloc-name">{item["asset_class"]}</span>
                            <span class="alloc-pct" style="color:{color}">{item["ratio"]}%</span>
                        </div>
                        <div class="alloc-role">{item["role"]}</div>
                        <div class="alloc-track">
                            <div class="alloc-fill" style="width:{item['ratio']}%;background:{color}"></div>
                        </div>
                    </div>
                    """
                st.markdown(alloc_html, unsafe_allow_html=True)

                # 상품군 후보 expander
                for item in result["allocation"]:
                    with st.expander(f"💡 {item['asset_class']} 상품군 후보"):
                        for ex in item["examples"]:
                            st.markdown(f"- {ex}")

                st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

                # 탭
                tab_effect, tab_reason, tab_product, tab_rule, tab_json = st.tabs(
                    ["입력 반영", "추천 이유", "상품 유형", "계좌 규칙", "API 응답"]
                )

                with tab_effect:
                    render_list(result["input_effects"])

                with tab_reason:
                    render_list(result["reasons"])

                with tab_product:
                    render_list(result["product_types"])

                with tab_rule:
                    render_list(result["account_rules"])
                    st.markdown(
                        '<p style="font-size:0.8rem;font-weight:700;color:#1d4ed8;margin:1rem 0 0">실행 체크리스트</p>',
                        unsafe_allow_html=True,
                    )
                    render_checklist(result["action_plan"])
                    st.markdown(
                        f'<div class="disclaimer">⚠ {result["disclaimer"]}</div>',
                        unsafe_allow_html=True,
                    )

                with tab_json:
                    st.json(result)
