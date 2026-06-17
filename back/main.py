from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


LifeStage = Literal["20~30대", "40~50대", "60대 이상"]
RiskTolerance = Literal["공격형", "균형형", "안정형"]
AccountType = Literal["개인연금", "퇴직연금 DC", "IRP"]
IncomePreference = Literal["성장 중심", "배당·분배금 선호", "배당 선호"]
ManagementStyle = Literal["직접 조합형", "자동 관리형"]


class RecommendationRequest(BaseModel):
    life_stage: LifeStage
    risk_tolerance: RiskTolerance
    account_type: AccountType
    income_preference: IncomePreference
    management_style: ManagementStyle


class AllocationItem(BaseModel):
    asset_class: str
    ratio: int
    role: str
    examples: list[str]


class RecommendationResponse(BaseModel):
    profile_title: str
    portfolio_summary: str
    formation_name: str
    guide_basis: str
    risk_asset_ratio: int
    safe_asset_ratio: int
    allocation: list[AllocationItem]
    input_effects: list[str]
    product_types: list[str]
    reasons: list[str]
    account_rules: list[str]
    action_plan: list[str]
    disclaimer: str


app = FastAPI(
    title="PensionFit API",
    description="미래에셋 연금투자 가이드북 기반 교육용 연금 포트폴리오 추천 API",
    version="1.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ROLE_DESCRIPTIONS = {
    "공격수": "포트폴리오의 성장성과 초과수익 가능성을 담당하는 위험자산",
    "미드필더": "대표지수·배당·혼합형 상품으로 성장과 안정의 균형을 잡는 위험자산",
    "수비수+골키퍼": "채권·현금성·금현물·TDF/TIF 등으로 변동성과 인출 리스크를 낮추는 안정자산",
}

COMMON_ACCOUNT_NOTE = (
    "퇴직연금(DC/IRP) 운용 시 주식형 비중 한도(70%) 적용. "
    "초과 주식 비중 원할 시 '채권혼합형 ETF' 적극 활용 필요"
)


def make_case(
    case_id: str,
    life_stage: LifeStage,
    risk_tolerance: RiskTolerance,
    income_preference: str,
    management_style: ManagementStyle,
    portfolio_name: str,
    risk_asset_ratio: int,
    striker_ratio: int,
    midfielder_ratio: int,
    safe_asset_ratio: int,
    product_note: str,
) -> dict:
    return {
        "case_id": case_id,
        "life_stage": life_stage,
        "risk_tolerance": risk_tolerance,
        "income_preference": income_preference,
        "management_style": management_style,
        "portfolio_name": portfolio_name,
        "risk_asset_ratio": risk_asset_ratio,
        "safe_asset_ratio": safe_asset_ratio,
        "allocation": {
            "공격수": striker_ratio,
            "미드필더": midfielder_ratio,
            "수비수+골키퍼": safe_asset_ratio,
        },
        "asset_template": (
            f"위험자산 {risk_asset_ratio}% "
            f"(공격수 {striker_ratio}%, 미드필더 {midfielder_ratio}%) / "
            f"안정자산 {safe_asset_ratio}%"
        ),
        "product_note": product_note,
        "account_note": COMMON_ACCOUNT_NOTE,
    }


PENSION_CASES = [
    make_case("Case 01", "20~30대", "공격형", "성장 중심", "직접 조합형", "연금 성장기 성장형", 65, 40, 25, 35, "[공격수] TIGER 반도체TOP10, 차이나테크TOP10, AI액티브 중심 + [방어] 초단기채권/금현물"),
    make_case("Case 02", "20~30대", "공격형", "성장 중심", "자동 관리형", "연금 성장기 성장형", 65, 40, 25, 35, "미래에셋전략배분적격TDF (2055/2060 등 장기 타겟)"),
    make_case("Case 03", "20~30대", "공격형", "배당 선호", "직접 조합형", "연금 성장기 성장형", 65, 40, 25, 35, "TIGER 미국배당다우존스 + 타겟커버드콜 결합 (격주 배당 세팅)"),
    make_case("Case 04", "20~30대", "공격형", "배당 선호", "자동 관리형", "연금 성장기 성장형", 65, 40, 25, 35, "미래에셋 글로벌멀티에셋TIF + 장기 TDF 혼합"),
    make_case("Case 05", "20~30대", "균형형", "성장 중심", "직접 조합형", "연금 성장기 밸런스형", 60, 30, 30, 40, "[미드필더] 미국S&P500, TIGER 200 분산 + [방어] 채권혼합형, 금현물 비중 확대"),
    make_case("Case 06", "20~30대", "균형형", "성장 중심", "자동 관리형", "연금 성장기 밸런스형", 60, 30, 30, 40, "미래에셋전략배분적격TDF (2055/2060 등 장기 타겟)"),
    make_case("Case 07", "20~30대", "균형형", "배당 선호", "직접 조합형", "연금 성장기 밸런스형", 60, 30, 30, 40, "TIGER 코리아배당다우존스 + 리츠부동산인프라채권혼합 분산"),
    make_case("Case 08", "20~30대", "균형형", "배당 선호", "자동 관리형", "연금 성장기 밸런스형", 60, 30, 30, 40, "미래에셋 글로벌멀티에셋TIF + 장기 TDF 혼합"),
    make_case("Case 09", "20~30대", "안정형", "성장 중심", "직접 조합형", "연금 성장기 안정형 (방어적)", 50, 20, 30, 50, "[안정자산] 국고채30년스트립액티브, 우량회사채 위주 + 미국S&P500 최소 편입"),
    make_case("Case 10", "20~30대", "안정형", "성장 중심", "자동 관리형", "연금 성장기 안정형 (방어적)", 50, 20, 30, 50, "미래에셋전략배분적격TDF (2055/2060 등 장기 타겟)"),
    make_case("Case 11", "20~30대", "안정형", "배당 선호", "직접 조합형", "연금 성장기 안정형 (방어적)", 50, 20, 30, 50, "TIGER 머니마켓액티브, CD금리플러스 중심 + 배당다우존스 소수 편입"),
    make_case("Case 12", "20~30대", "안정형", "배당 선호", "자동 관리형", "연금 성장기 안정형 (방어적)", 50, 20, 30, 50, "미래에셋 글로벌멀티에셋TIF + 장기 TDF 혼합"),
    make_case("Case 13", "40~50대", "공격형", "성장 중심", "직접 조합형", "연금 성숙기 밸런스형", 60, 30, 30, 40, "[공격수] TIGER 반도체TOP10, 차이나테크TOP10, AI액티브 중심 + [방어] 초단기채권/금현물"),
    make_case("Case 14", "40~50대", "공격형", "성장 중심", "자동 관리형", "연금 성숙기 밸런스형", 60, 30, 30, 40, "미래에셋전략배분적격TDF (2035/2040) 또는 밸런스TRF"),
    make_case("Case 15", "40~50대", "공격형", "배당 선호", "직접 조합형", "연금 성숙기 밸런스형", 60, 30, 30, 40, "TIGER 미국배당다우존스 + 타겟커버드콜 결합 (격주 배당 세팅)"),
    make_case("Case 16", "40~50대", "공격형", "배당 선호", "자동 관리형", "연금 성숙기 밸런스형", 60, 30, 30, 40, "미래에셋 평생소득TIF 50% + 단기 TDF 50%"),
    make_case("Case 17", "40~50대", "균형형", "성장 중심", "직접 조합형", "연금 성숙기 밸런스형", 60, 30, 30, 40, "[미드필더] 미국S&P500, TIGER 200 분산 + [방어] 채권혼합형, 금현물 비중 확대"),
    make_case("Case 18", "40~50대", "균형형", "성장 중심", "자동 관리형", "연금 성숙기 밸런스형", 60, 30, 30, 40, "미래에셋전략배분적격TDF (2035/2040) 또는 밸런스TRF"),
    make_case("Case 19", "40~50대", "균형형", "배당 선호", "직접 조합형", "연금 성숙기 밸런스형", 60, 30, 30, 40, "TIGER 코리아배당다우존스 + 리츠부동산인프라채권혼합 분산"),
    make_case("Case 20", "40~50대", "균형형", "배당 선호", "자동 관리형", "연금 성숙기 밸런스형", 60, 30, 30, 40, "미래에셋 평생소득TIF 50% + 단기 TDF 50%"),
    make_case("Case 21", "40~50대", "안정형", "성장 중심", "직접 조합형", "연금 성숙기 안정형", 50, 20, 30, 50, "[안정자산] 국고채30년스트립액티브, 우량회사채 위주 + 미국S&P500 최소 편입"),
    make_case("Case 22", "40~50대", "안정형", "성장 중심", "자동 관리형", "연금 성숙기 안정형", 50, 20, 30, 50, "미래에셋전략배분적격TDF (2035/2040) 또는 밸런스TRF"),
    make_case("Case 23", "40~50대", "안정형", "배당 선호", "직접 조합형", "연금 성숙기 안정형", 50, 20, 30, 50, "TIGER 머니마켓액티브, CD금리플러스 중심 + 배당다우존스 소수 편입"),
    make_case("Case 24", "40~50대", "안정형", "배당 선호", "자동 관리형", "연금 성숙기 안정형", 50, 20, 30, 50, "미래에셋 평생소득TIF 50% + 단기 TDF 50%"),
    make_case("Case 25", "60대 이상", "공격형", "성장 중심", "직접 조합형", "연금 인출기 밸런스형", 60, 25, 35, 40, "[공격수] TIGER 반도체TOP10, 차이나테크TOP10, AI액티브 중심 + [방어] 초단기채권/금현물"),
    make_case("Case 26", "60대 이상", "공격형", "성장 중심", "자동 관리형", "연금 인출기 밸런스형", 60, 25, 35, 40, "미래에셋 밸런스TRF 안정형 또는 M-ROBO 포트폴리오"),
    make_case("Case 27", "60대 이상", "공격형", "배당 선호", "직접 조합형", "연금 인출기 밸런스형", 60, 25, 35, 40, "TIGER 미국배당다우존스 + 타겟커버드콜 결합 (격주 배당 세팅)"),
    make_case("Case 28", "60대 이상", "공격형", "배당 선호", "자동 관리형", "연금 인출기 밸런스형", 60, 25, 35, 40, "미래에셋 평생소득TIF 위주 은퇴 인출 최적화"),
    make_case("Case 29", "60대 이상", "균형형", "성장 중심", "직접 조합형", "연금 인출기 밸런스형", 60, 25, 35, 40, "[미드필더] 미국S&P500, TIGER 200 분산 + [방어] 채권혼합형, 금현물 비중 확대"),
    make_case("Case 30", "60대 이상", "균형형", "성장 중심", "자동 관리형", "연금 인출기 밸런스형", 60, 25, 35, 40, "미래에셋 밸런스TRF 안정형 또는 M-ROBO 포트폴리오"),
    make_case("Case 31", "60대 이상", "균형형", "배당 선호", "직접 조합형", "연금 인출기 밸런스형", 60, 25, 35, 40, "TIGER 코리아배당다우존스 + 리츠부동산인프라채권혼합 분산"),
    make_case("Case 32", "60대 이상", "균형형", "배당 선호", "자동 관리형", "연금 인출기 밸런스형", 60, 25, 35, 40, "미래에셋 평생소득TIF 위주 은퇴 인출 최적화"),
    make_case("Case 33", "60대 이상", "안정형", "성장 중심", "직접 조합형", "연금 인출기 안정형", 50, 20, 30, 50, "[안정자산] 국고채30년스트립액티브, 우량회사채 위주 + 미국S&P500 최소 편입"),
    make_case("Case 34", "60대 이상", "안정형", "성장 중심", "자동 관리형", "연금 인출기 안정형", 50, 20, 30, 50, "미래에셋 밸런스TRF 안정형 또는 M-ROBO 포트폴리오"),
    make_case("Case 35", "60대 이상", "안정형", "배당 선호", "직접 조합형", "연금 인출기 안정형", 50, 20, 30, 50, "TIGER 머니마켓액티브, CD금리플러스 중심 + 배당다우존스 소수 편입"),
    make_case("Case 36", "60대 이상", "안정형", "배당 선호", "자동 관리형", "연금 인출기 안정형", 50, 20, 30, 50, "미래에셋 평생소득TIF 위주 은퇴 인출 최적화"),
]

CASE_DATA = {
    (
        case["life_stage"],
        case["risk_tolerance"],
        case["income_preference"],
        case["management_style"],
    ): case
    for case in PENSION_CASES
}


def normalize_income_preference(value: str) -> str:
    if value in {"배당 선호", "배당·분배금 선호"}:
        return "배당 선호"
    return "성장 중심"


def get_case(request: RecommendationRequest) -> dict:
    key = (
        request.life_stage,
        request.risk_tolerance,
        normalize_income_preference(request.income_preference),
        request.management_style,
    )
    return CASE_DATA[key]


def split_candidates(text: str) -> list[str]:
    normalized = (
        text.replace(" 또는 ", ", ")
        .replace(" + ", ", ")
        .replace(" 중심 + ", ", ")
    )
    candidates = [item.strip(" .") for item in normalized.split(",")]
    return [item for item in candidates if item]


def extract_tagged_candidates(text: str, tag: str) -> list[str]:
    if tag not in text:
        return []

    segment = text.split(tag, 1)[1]
    for next_tag in (" + [공격수]", " + [미드필더]", " + [방어]", " + [안정자산]"):
        if next_tag in segment:
            segment = segment.split(next_tag, 1)[0]
    return split_candidates(segment)


def build_role_examples(case: dict, role: str) -> list[str]:
    product_note = case["product_note"]
    has_tagged_role = any(
        tag in product_note
        for tag in ("[공격수]", "[미드필더]", "[방어]", "[안정자산]")
    )

    if role == "공격수":
        tagged = extract_tagged_candidates(product_note, "[공격수]")
        if tagged:
            return tagged

    if role == "미드필더":
        tagged = extract_tagged_candidates(product_note, "[미드필더]")
        if tagged:
            return tagged

    if role == "수비수+골키퍼":
        for tag in ("[방어]", "[안정자산]"):
            tagged = extract_tagged_candidates(product_note, tag)
            if tagged:
                return tagged

    if has_tagged_role:
        if "미국S&P500 최소 편입" in product_note and role in {"공격수", "미드필더"}:
            return ["미국S&P500 최소 편입"]
        return ["엑셀 매핑표에서 별도 상품 후보를 명시하지 않은 역할로, 목표 비중만 적용"]

    if case["management_style"] == "자동 관리형":
        if role == "미드필더":
            return split_candidates(product_note)
        if role == "공격수":
            return ["자동 관리형 상품 내부에서 성장자산 비중을 목표시점에 맞춰 편입"]
        return ["자동 관리형 상품 내부에서 채권·현금성 자산 비중을 조절"]

    if case["income_preference"] == "배당 선호":
        if role == "미드필더":
            return split_candidates(product_note)
        if role == "공격수":
            return ["배당·분배금 후보를 중심으로 위험자산 비중을 구성"]
        return ["안정자산 비중은 단기채권·금현물·채권혼합형으로 보완"]

    if role == "공격수" and case["risk_tolerance"] == "공격형":
        return split_candidates(product_note)
    if role == "미드필더":
        return split_candidates(product_note)

    return [ROLE_DESCRIPTIONS[role]]


def build_allocation_items(case: dict) -> list[AllocationItem]:
    return [
        AllocationItem(
            asset_class=role,
            ratio=ratio,
            role=ROLE_DESCRIPTIONS[role],
            examples=build_role_examples(case, role),
        )
        for role, ratio in case["allocation"].items()
    ]


def build_profile_title(request: RecommendationRequest, case: dict) -> str:
    style_label = "자동관리형" if request.management_style == "자동 관리형" else "직접조합형"
    return (
        f"{case['portfolio_name']} "
        f"({request.risk_tolerance}, {normalize_income_preference(request.income_preference)}, {style_label})"
    )


def build_product_types(case: dict) -> list[str]:
    return [
        f"{case['case_id']} 추천 상품군: {case['product_note']}",
        f"자산 배분 템플릿: {case['asset_template']}",
        (
            "직접 조합형은 역할별 ETF 후보를 나누어 담고, "
            "자동 관리형은 TDF·TRF·TIF·로보 포트폴리오처럼 운용을 위임하는 상품군을 우선합니다."
        ),
    ]


def build_reasons(request: RecommendationRequest, case: dict) -> list[str]:
    return [
        (
            f"입력 조합이 엑셀 매핑표의 {case['case_id']}와 일치해 "
            f"{case['portfolio_name']}을 적용했습니다."
        ),
        f"엑셀의 자산 배분 템플릿은 {case['asset_template']}입니다.",
        (
            f"인컴 선호도는 '{normalize_income_preference(request.income_preference)}'로 반영되어 "
            f"추천 상품군을 '{case['product_note']}'로 선택했습니다."
        ),
        (
            f"운용 방식은 '{request.management_style}'로 반영되어 "
            "직접 ETF 조합 또는 자동 관리형 상품군이 달라집니다."
        ),
        f"최종 위험자산 비중은 {case['risk_asset_ratio']}%, 안정자산 비중은 {case['safe_asset_ratio']}%입니다.",
    ]


def build_account_rules(
    request: RecommendationRequest, case: dict
) -> list[str]:
    if request.account_type == "개인연금":
        return [
            "개인연금은 DC/IRP의 위험자산 70% 한도를 직접 적용하지 않습니다.",
            "다만 연금계좌 운용상 레버리지·인버스형 상품은 제외하는 보수적 안내를 유지합니다.",
            f"참고: 엑셀 매핑표의 계좌 유의사항은 '{case['account_note']}'입니다.",
        ]

    rules = [
        case["account_note"],
        (
            f"현재 추천 위험자산 비중은 {case['risk_asset_ratio']}%로 "
            f"{request.account_type}의 70% 한도 이내입니다."
        ),
    ]

    if case["risk_asset_ratio"] > 70:
        rules.append("위험자산이 70%를 넘으므로 실제 운용 전 안정자산 비중을 높여야 합니다.")

    return rules


def build_input_effects(
    request: RecommendationRequest, case: dict
) -> list[str]:
    return [
        f"생애주기: {request.life_stage} 선택으로 {case['portfolio_name']} 후보군에 매핑했습니다.",
        (
            f"투자 성향: {request.risk_tolerance} 선택으로 "
            f"공격수 {case['allocation']['공격수']}%, 미드필더 {case['allocation']['미드필더']}%, "
            f"수비수+골키퍼 {case['allocation']['수비수+골키퍼']}% 비중을 적용했습니다."
        ),
        (
            f"인컴 선호도: {normalize_income_preference(request.income_preference)} 선택으로 "
            f"{case['case_id']}의 추천 상품군을 적용했습니다."
        ),
        f"운용 방식: {request.management_style} 선택으로 상품군 후보를 '{case['product_note']}'로 설정했습니다.",
        (
            f"계좌 종류: {request.account_type} 선택으로 "
            "개인연금 또는 DC/IRP 위험자산 한도 안내를 다르게 표시했습니다."
        ),
    ]


def build_action_plan(request: RecommendationRequest, case: dict) -> list[str]:
    action_plan = [
        f"먼저 현재 보유 상품을 엑셀 매핑표의 {case['case_id']} 기준과 비교합니다.",
        f"목표 비중은 {case['asset_template']}로 두고, 분기 1회 정도 실제 비중을 점검합니다.",
        f"상품 후보는 '{case['product_note']}'를 출발점으로 삼되, 보수·변동성·분배 재원을 함께 확인합니다.",
    ]

    if request.account_type in {"퇴직연금 DC", "IRP"}:
        action_plan.append("DC/IRP에서는 위험자산 비중이 70%를 넘지 않는지 주문 전 다시 확인합니다.")

    return action_plan


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "PensionFit API"}


@app.post("/recommend", response_model=RecommendationResponse)
def recommend_portfolio(request: RecommendationRequest) -> RecommendationResponse:
    case = get_case(request)

    return RecommendationResponse(
        profile_title=build_profile_title(request, case),
        portfolio_summary=(
            f"{request.life_stage}·{request.risk_tolerance}·"
            f"{normalize_income_preference(request.income_preference)}·{request.management_style} 조건을 "
            "PensionFit 36가지 맞춤형 포트폴리오 매핑표에 연결한 결과입니다."
        ),
        formation_name=case["portfolio_name"],
        guide_basis=f"PensionFit_36Cases_Mapping.xlsx / 36가지 맞춤형 포트폴리오 / {case['case_id']}",
        risk_asset_ratio=case["risk_asset_ratio"],
        safe_asset_ratio=case["safe_asset_ratio"],
        allocation=build_allocation_items(case),
        input_effects=build_input_effects(request, case),
        product_types=build_product_types(case),
        reasons=build_reasons(request, case),
        account_rules=build_account_rules(request, case),
        action_plan=build_action_plan(request, case),
        disclaimer=(
            "본 서비스는 오픈소스소프트웨어실습 과제용 교육 서비스이며, "
            "실제 투자 권유나 투자자문이 아닙니다."
        ),
    )
