from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


LifeStage = Literal["20~30대", "40~50대", "60대 이상"]
RiskTolerance = Literal["공격형", "균형형", "안정형"]
AccountType = Literal["개인연금", "퇴직연금 DC", "IRP"]
IncomePreference = Literal["성장 중심", "배당·분배금 선호"]
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
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


GUIDE_FORMATIONS = {
    "20~30대": {
        "공격형": {
            "formation": "연금 성장기 성장형",
            "basis": "가이드북 9쪽: 연금 성장기 포트폴리오 성장형 비중",
            "allocation": {"공격수": 40, "미드필더": 25, "수비수+골키퍼": 35},
            "mapping_note": "20~30대 공격형은 가이드북의 성장기 성장형 포메이션을 적용했습니다.",
        },
        "균형형": {
            "formation": "연금 성장기 밸런스형",
            "basis": "가이드북 9쪽: 연금 성장기 포트폴리오 밸런스형 비중",
            "allocation": {"공격수": 30, "미드필더": 30, "수비수+골키퍼": 40},
            "mapping_note": "20~30대 균형형은 가이드북의 성장기 밸런스형 포메이션을 적용했습니다.",
        },
        "안정형": {
            "formation": "연금 성장기 밸런스형",
            "basis": "가이드북 9쪽: 연금 성장기 포트폴리오 밸런스형 비중",
            "allocation": {"공격수": 30, "미드필더": 30, "수비수+골키퍼": 40},
            "mapping_note": "가이드북의 성장기 표에는 안정형 열이 없어 가장 보수적인 성장기 밸런스형을 적용했습니다.",
        },
    },
    "40~50대": {
        "공격형": {
            "formation": "연금 성숙기 밸런스형",
            "basis": "가이드북 11쪽: 연금 성숙기 포트폴리오 밸런스형 비중",
            "allocation": {"공격수": 30, "미드필더": 30, "수비수+골키퍼": 40},
            "mapping_note": "가이드북의 성숙기 표에는 성장형 열이 없어 공격형도 성숙기 밸런스형을 기준으로 삼았습니다.",
        },
        "균형형": {
            "formation": "연금 성숙기 밸런스형",
            "basis": "가이드북 11쪽: 연금 성숙기 포트폴리오 밸런스형 비중",
            "allocation": {"공격수": 30, "미드필더": 30, "수비수+골키퍼": 40},
            "mapping_note": "40~50대 균형형은 가이드북의 성숙기 밸런스형 포메이션을 적용했습니다.",
        },
        "안정형": {
            "formation": "연금 성숙기 안정형",
            "basis": "가이드북 11쪽: 연금 성숙기 포트폴리오 안정형 비중",
            "allocation": {"공격수": 20, "미드필더": 30, "수비수+골키퍼": 50},
            "mapping_note": "40~50대 안정형은 가이드북의 성숙기 안정형 포메이션을 적용했습니다.",
        },
    },
    "60대 이상": {
        "공격형": {
            "formation": "연금 인출기 밸런스형",
            "basis": "가이드북 13쪽: 연금 인출기 포트폴리오 밸런스형 비중",
            "allocation": {"공격수": 25, "미드필더": 35, "수비수+골키퍼": 40},
            "mapping_note": "가이드북의 인출기 표에는 성장형 열이 없어 공격형도 인출기 밸런스형을 기준으로 삼았습니다.",
        },
        "균형형": {
            "formation": "연금 인출기 밸런스형",
            "basis": "가이드북 13쪽: 연금 인출기 포트폴리오 밸런스형 비중",
            "allocation": {"공격수": 25, "미드필더": 35, "수비수+골키퍼": 40},
            "mapping_note": "60대 이상 균형형은 가이드북의 인출기 밸런스형 포메이션을 적용했습니다.",
        },
        "안정형": {
            "formation": "연금 인출기 안정형",
            "basis": "가이드북 13쪽: 연금 인출기 포트폴리오 안정형 비중",
            "allocation": {"공격수": 20, "미드필더": 30, "수비수+골키퍼": 50},
            "mapping_note": "60대 이상 안정형은 가이드북의 인출기 안정형 포메이션을 적용했습니다.",
        },
    },
}


ROLE_DESCRIPTIONS = {
    "공격수": "수익 성장을 담당하는 주식형·테마형 자산",
    "미드필더": "성장과 방어의 균형을 잡는 대표지수·배당·분산형 자산",
    "수비수+골키퍼": "변동성 완충과 계좌 안정성을 담당하는 채권·금현물·TDF/TIF형 자산",
}


ROLE_EXAMPLES = {
    "20~30대": {
        "공격수": [
            "TIGER 반도체TOP10",
            "TIGER 차이나테크TOP10",
            "TIGER 미국필라델피아반도체나스닥",
            "TIGER 글로벌AI액티브",
        ],
        "미드필더": [
            "TIGER 200",
            "TIGER 코스닥150",
            "TIGER 미국S&P500",
        ],
        "수비수+골키퍼": [
            "TIGER KRX금현물",
            "TIGER 미국테크TOP10채권혼합Fn",
            "TIGER 미국나스닥100채권혼합Fn",
            "미래에셋전략배분적격TDF2045",
        ],
    },
    "40~50대": {
        "공격수": [
            "TIGER 미국테크TOP10",
            "TIGER 차이나테크TOP10",
            "TIGER 글로벌AI액티브",
        ],
        "미드필더": [
            "TIGER 200",
            "TIGER 미국S&P500",
            "TIGER 미국배당다우존스",
        ],
        "수비수+골키퍼": [
            "TIGER KRX금현물",
            "TIGER 미국초단기(3개월이하)국채",
            "TIGER 미국테크TOP10채권혼합Fn",
            "TIGER 미국나스닥100채권혼합Fn",
            "미래에셋밸런스TRF안정형",
        ],
    },
    "60대 이상": {
        "공격수": [
            "TIGER 미국S&P500",
            "TIGER 200",
        ],
        "미드필더": [
            "TIGER 코리아배당다우존스",
            "TIGER 미국나스닥100타겟데일리커버드콜",
            "TIGER KRX금현물",
            "TIGER 토탈월드스탁액티브",
        ],
        "수비수+골키퍼": [
            "TIGER 머니마켓액티브",
            "TIGER 미국초단기(3개월이하)국채",
            "TIGER 미국테크TOP10채권혼합Fn",
            "TIGER 미국나스닥100채권혼합Fn",
            "미래에셋평생소득TIF",
        ],
    },
}


def get_formation(request: RecommendationRequest) -> dict:
    return GUIDE_FORMATIONS[request.life_stage][request.risk_tolerance]


def build_allocation_items(
    life_stage: LifeStage, allocation: dict[str, int]
) -> list[AllocationItem]:
    return [
        AllocationItem(
            asset_class=role,
            ratio=ratio,
            role=ROLE_DESCRIPTIONS[role],
            examples=ROLE_EXAMPLES[life_stage][role],
        )
        for role, ratio in allocation.items()
    ]


def build_profile_title(
    request: RecommendationRequest, formation_name: str
) -> str:
    style_label = "자동관리형" if request.management_style == "자동 관리형" else "직접조합형"
    income_label = "인컴 선호" if request.income_preference == "배당·분배금 선호" else "성장 중심"
    return f"{formation_name} 포트폴리오 ({request.risk_tolerance}, {income_label}, {style_label})"


def build_product_types(request: RecommendationRequest) -> list[str]:
    products = [
        "공격수: 장기 수익률을 기대하는 주식형·테마형 ETF 상품군",
        "미드필더: 대표지수, 배당, 분산형 상품처럼 성장과 안정의 균형을 잡는 상품군",
        "수비수+골키퍼: 채권혼합형, 단기국채, 금현물, TDF/TIF처럼 변동성을 낮추는 상품군",
    ]

    if request.income_preference == "배당·분배금 선호":
        products.append(
            "인컴 선호 반영: 비중은 가이드북 포메이션을 유지하고, 미드필더 안에서 배당다우존스·월배당·커버드콜형 예시를 우선 확인하도록 안내합니다."
        )
    else:
        products.append(
            "성장 중심 반영: 비중은 가이드북 포메이션을 유지하고, 공격수와 대표지수형 미드필더를 중심으로 확인하도록 안내합니다."
        )

    if request.management_style == "자동 관리형":
        products.append(
            "자동 관리형 반영: 직접 ETF 조합이 부담스러우면 TDF, TRF, TIF처럼 자산배분을 자동화하는 상품군을 핵심 후보로 둡니다."
        )
    else:
        products.append(
            "직접 조합형 반영: 공격수·미드필더·수비수+골키퍼 비중에 맞춰 ETF 상품군을 나누어 조합합니다."
        )

    return products


def build_reasons(
    request: RecommendationRequest,
    formation: dict,
    risk_asset_ratio: int,
) -> list[str]:
    allocation = formation["allocation"]

    reasons = [
        formation["mapping_note"],
        f"{formation['basis']}을 기준으로 공격수 {allocation['공격수']}%, 미드필더 {allocation['미드필더']}%, 수비수+골키퍼 {allocation['수비수+골키퍼']}%를 적용했습니다.",
    ]

    if request.life_stage == "20~30대":
        reasons.append("연금 성장기는 장기 투자 기간을 활용하되, 가이드북도 수비수+골키퍼를 35~40% 배치해 변동성 관리를 함께 둡니다.")
    elif request.life_stage == "40~50대":
        reasons.append("연금 성숙기는 은퇴가 가까워지는 구간이므로 성장보다 균형과 리스크 관리 비중이 커집니다.")
    else:
        reasons.append("연금 인출기는 꾸준한 현금흐름과 안정적 자산관리가 중요해 수비수+골키퍼 비중을 높게 둡니다.")

    if request.income_preference == "배당·분배금 선호":
        reasons.append("배당·분배금 선호는 포트폴리오 비중을 임의로 바꾸지 않고, 미드필더 상품군 선택 기준에 반영했습니다.")
    else:
        reasons.append("성장 중심 선택은 포트폴리오 비중을 임의로 바꾸지 않고, 공격수와 대표지수형 상품군 선택 기준에 반영했습니다.")

    if request.management_style == "자동 관리형":
        reasons.append("자동 관리형 선택은 TDF, TRF, TIF 등 자동 자산배분형 상품군 안내에 반영했습니다.")
    else:
        reasons.append("직접 조합형 선택은 포메이션별 상품군을 직접 나누어 담는 방식으로 안내했습니다.")

    reasons.append(f"공격수+미드필더 합산 비중은 {risk_asset_ratio}%입니다.")
    return reasons


def build_account_rules(account_type: AccountType, risk_asset_ratio: int) -> list[str]:
    if account_type == "개인연금":
        return [
            "개인연금은 DC/IRP의 위험자산 70% 한도를 직접 적용하지 않습니다.",
            "다만 연금계좌 특성상 레버리지·인버스형 상품은 제외하는 보수적 안내를 적용합니다.",
        ]

    rules = [
        f"{account_type} 계좌는 위험자산 70% 한도를 고려해야 하므로 공격수+미드필더 합산 비중을 점검했습니다.",
    ]

    if risk_asset_ratio <= 70:
        rules.append(
            f"현재 포메이션의 공격수+미드필더 합산 비중은 {risk_asset_ratio}%로 70% 한도 안에 있습니다."
        )
    else:
        rules.append(
            "현재 포메이션이 70%를 초과하므로 실제 운용에서는 수비수+골키퍼 비중을 추가로 높여야 합니다."
        )

    return rules


def build_input_effects(
    request: RecommendationRequest,
    formation: dict,
    risk_asset_ratio: int,
) -> list[str]:
    allocation = formation["allocation"]

    effects = [
        f"생애주기: {request.life_stage}를 선택해 {formation['formation']} 포메이션을 적용했습니다.",
        (
            f"투자 성향: {request.risk_tolerance} 성향을 가이드북 표의 포메이션 열에 매핑해 "
            f"공격수 {allocation['공격수']}%, 미드필더 {allocation['미드필더']}%, "
            f"수비수+골키퍼 {allocation['수비수+골키퍼']}% 비중을 결정했습니다."
        ),
    ]

    if request.account_type == "개인연금":
        effects.append(
            "계좌 종류: 개인연금은 DC/IRP의 위험자산 70% 한도 점검 대상은 아니지만, 레버리지·인버스형 상품 제외 안내를 표시했습니다."
        )
    else:
        effects.append(
            f"계좌 종류: {request.account_type}는 위험자산 70% 한도를 고려해야 하므로 공격수+미드필더 합산 {risk_asset_ratio}%를 점검했습니다."
        )

    if request.income_preference == "배당·분배금 선호":
        effects.append(
            "인컴 선호도: 배당·분배금 선호를 반영해 배당, 월분배, 커버드콜, TIF 등 현금흐름형 상품군 후보를 우선 안내했습니다."
        )
    else:
        effects.append(
            "인컴 선호도: 성장 중심 선택을 반영해 공격수와 대표지수형 미드필더 상품군 후보를 우선 안내했습니다."
        )

    if request.management_style == "자동 관리형":
        effects.append(
            "운용 방식: 자동 관리형 선택을 반영해 TDF, TRF, TIF처럼 자산배분을 자동화하는 상품군 후보를 안내했습니다."
        )
    else:
        effects.append(
            "운용 방식: 직접 조합형 선택을 반영해 공격수·미드필더·수비수+골키퍼 역할별 ETF 상품군 후보를 나누어 안내했습니다."
        )

    return effects


def build_action_plan(request: RecommendationRequest) -> list[str]:
    action_plan = [
        "먼저 보유 상품을 공격수, 미드필더, 수비수+골키퍼 역할로 분류합니다.",
        "가이드북 포메이션 비중과 실제 보유 비중을 비교하고, 분기 1회 정도 리밸런싱합니다.",
    ]

    if request.account_type in {"퇴직연금 DC", "IRP"}:
        action_plan.append("DC/IRP에서는 공격수+미드필더 비중이 70%를 넘지 않는지 확인합니다.")

    if request.income_preference == "배당·분배금 선호":
        action_plan.append("분배형 상품은 분배금 수준뿐 아니라 원금 변동과 분배 재원 구조를 함께 확인합니다.")

    return action_plan


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "PensionFit API"}


@app.post("/recommend", response_model=RecommendationResponse)
def recommend_portfolio(request: RecommendationRequest) -> RecommendationResponse:
    formation = get_formation(request)
    allocation = formation["allocation"]
    risk_asset_ratio = allocation["공격수"] + allocation["미드필더"]
    safe_asset_ratio = allocation["수비수+골키퍼"]

    return RecommendationResponse(
        profile_title=build_profile_title(request, formation["formation"]),
        portfolio_summary=(
            f"{request.life_stage}·{request.risk_tolerance}·{request.account_type} 조건을 "
            "미래에셋 연금투자 가이드북의 연금 포메이션 표에 매핑한 결과입니다."
        ),
        formation_name=formation["formation"],
        guide_basis=formation["basis"],
        risk_asset_ratio=risk_asset_ratio,
        safe_asset_ratio=safe_asset_ratio,
        allocation=build_allocation_items(request.life_stage, allocation),
        input_effects=build_input_effects(request, formation, risk_asset_ratio),
        product_types=build_product_types(request),
        reasons=build_reasons(request, formation, risk_asset_ratio),
        account_rules=build_account_rules(request.account_type, risk_asset_ratio),
        action_plan=build_action_plan(request),
        disclaimer=(
            "본 서비스는 오픈소스소프트웨어실습 과제용 교육 서비스이며, "
            "실제 투자 권유나 투자자문이 아닙니다."
        ),
    )
