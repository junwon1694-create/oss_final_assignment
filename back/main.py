from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


LifeStage = Literal["20~30대", "40~50대", "60대 이상"]
PortfolioType = Literal["성장형", "밸런스형", "안정형"]
AccountType = Literal["개인연금", "퇴직연금 DC", "IRP"]


class RecommendationRequest(BaseModel):
    life_stage: LifeStage
    portfolio_type: PortfolioType
    account_type: AccountType


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
    description="미래에셋 연금투자 가이드북 표 기반 교육용 연금 포트폴리오 추천 API",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ROLE_DESCRIPTIONS = {
    "공격수": "장기 성장과 초과수익을 기대하는 주식형·테마형 자산",
    "미드필더": "대표지수·배당·분산형 상품으로 성장과 안정의 균형을 잡는 자산",
    "수비수+골키퍼": "채권혼합형·단기국채·금현물·TDF/TIF 등 변동성 완충 자산",
}


GUIDE_PORTFOLIOS = {
    ("20~30대", "성장형"): {
        "formation_name": "연금 성장기 성장형",
        "guide_basis": "미래에셋 연금투자 가이드북: 연금 성장기 포트폴리오 제안 표",
        "allocation": {"공격수": 40, "미드필더": 25, "수비수+골키퍼": 35},
        "examples": {
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
    },
    ("20~30대", "밸런스형"): {
        "formation_name": "연금 성장기 밸런스형",
        "guide_basis": "미래에셋 연금투자 가이드북: 연금 성장기 포트폴리오 제안 표",
        "allocation": {"공격수": 30, "미드필더": 30, "수비수+골키퍼": 40},
        "examples": {
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
    },
    ("40~50대", "밸런스형"): {
        "formation_name": "연금 성숙기 밸런스형",
        "guide_basis": "미래에셋 연금투자 가이드북: 연금 성숙기 포트폴리오 제안 표",
        "allocation": {"공격수": 30, "미드필더": 30, "수비수+골키퍼": 40},
        "examples": {
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
    },
    ("40~50대", "안정형"): {
        "formation_name": "연금 성숙기 안정형",
        "guide_basis": "미래에셋 연금투자 가이드북: 연금 성숙기 포트폴리오 제안 표",
        "allocation": {"공격수": 20, "미드필더": 30, "수비수+골키퍼": 50},
        "examples": {
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
    },
    ("60대 이상", "밸런스형"): {
        "formation_name": "연금 인출기 밸런스형",
        "guide_basis": "미래에셋 연금투자 가이드북: 연금 인출기 포트폴리오 제안 표",
        "allocation": {"공격수": 25, "미드필더": 35, "수비수+골키퍼": 40},
        "examples": {
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
    },
    ("60대 이상", "안정형"): {
        "formation_name": "연금 인출기 안정형",
        "guide_basis": "미래에셋 연금투자 가이드북: 연금 인출기 포트폴리오 제안 표",
        "allocation": {"공격수": 20, "미드필더": 30, "수비수+골키퍼": 50},
        "examples": {
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
    },
}

PORTFOLIO_OPTIONS = {
    "20~30대": ["성장형", "밸런스형"],
    "40~50대": ["밸런스형", "안정형"],
    "60대 이상": ["밸런스형", "안정형"],
}


def get_portfolio(request: RecommendationRequest) -> dict:
    if request.portfolio_type not in PORTFOLIO_OPTIONS[request.life_stage]:
        allowed = ", ".join(PORTFOLIO_OPTIONS[request.life_stage])
        raise HTTPException(
            status_code=400,
            detail=f"{request.life_stage}에서 선택 가능한 투자 유형은 {allowed}입니다.",
        )

    return GUIDE_PORTFOLIOS[(request.life_stage, request.portfolio_type)]


def build_allocation_items(portfolio: dict) -> list[AllocationItem]:
    return [
        AllocationItem(
            asset_class=role,
            ratio=ratio,
            role=ROLE_DESCRIPTIONS[role],
            examples=portfolio["examples"][role],
        )
        for role, ratio in portfolio["allocation"].items()
    ]


def build_account_rules(account_type: AccountType, risk_asset_ratio: int) -> list[str]:
    if account_type == "개인연금":
        return [
            "개인연금은 DC/IRP의 위험자산 70% 한도를 직접 적용하지 않습니다.",
            "다만 연금계좌에서는 레버리지·인버스형 상품을 제외하는 보수적 운용 원칙을 함께 확인합니다.",
        ]

    rules = [
        f"{account_type} 계좌는 위험자산 70% 한도를 고려해야 합니다.",
        f"현재 추천 포트폴리오의 위험자산 비중은 {risk_asset_ratio}%입니다.",
    ]
    if risk_asset_ratio <= 70:
        rules.append("따라서 현재 비중은 DC/IRP 위험자산 한도 안에 있습니다.")
    else:
        rules.append("70%를 초과하므로 실제 운용 전 안정자산 비중을 높여야 합니다.")
    return rules


def build_input_effects(request: RecommendationRequest, portfolio: dict) -> list[str]:
    allocation = portfolio["allocation"]
    return [
        f"생애주기: {request.life_stage} 선택으로 {portfolio['guide_basis']}를 적용했습니다.",
        (
            f"투자 유형: {request.portfolio_type} 선택으로 "
            f"공격수 {allocation['공격수']}%, 미드필더 {allocation['미드필더']}%, "
            f"수비수+골키퍼 {allocation['수비수+골키퍼']}% 비중을 적용했습니다."
        ),
        (
            f"계좌 종류: {request.account_type} 선택으로 "
            "개인연금 또는 DC/IRP 위험자산 한도 안내를 다르게 표시했습니다."
        ),
    ]


def build_reasons(request: RecommendationRequest, portfolio: dict) -> list[str]:
    allocation = portfolio["allocation"]
    return [
        "추천 비중은 별도 임의 조정 없이 가이드북 표의 투자 비중을 그대로 사용했습니다.",
        f"{request.life_stage}의 {request.portfolio_type}은 {portfolio['formation_name']}에 해당합니다.",
        (
            f"위험자산은 공격수 {allocation['공격수']}%와 미드필더 {allocation['미드필더']}%를 합산해 "
            f"{allocation['공격수'] + allocation['미드필더']}%입니다."
        ),
        f"안정자산은 수비수+골키퍼 {allocation['수비수+골키퍼']}%입니다.",
    ]


def build_product_types(portfolio: dict) -> list[str]:
    return [
        "공격수: " + ", ".join(portfolio["examples"]["공격수"]),
        "미드필더: " + ", ".join(portfolio["examples"]["미드필더"]),
        "수비수+골키퍼: " + ", ".join(portfolio["examples"]["수비수+골키퍼"]),
    ]


def build_action_plan(account_type: AccountType, risk_asset_ratio: int) -> list[str]:
    plan = [
        "가이드북 표의 공격수·미드필더·수비수+골키퍼 비중을 목표 비중으로 둡니다.",
        "현재 보유 상품을 세 역할로 분류한 뒤 목표 비중과 비교합니다.",
        "분기 1회 정도 비중이 크게 벗어났는지 확인하고 리밸런싱합니다.",
    ]
    if account_type in {"퇴직연금 DC", "IRP"}:
        plan.append(f"DC/IRP에서는 위험자산 비중 {risk_asset_ratio}%가 70% 이내인지 주문 전 확인합니다.")
    return plan


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "PensionFit API"}


@app.post("/recommend", response_model=RecommendationResponse)
def recommend_portfolio(request: RecommendationRequest) -> RecommendationResponse:
    portfolio = get_portfolio(request)
    allocation = portfolio["allocation"]
    risk_asset_ratio = allocation["공격수"] + allocation["미드필더"]
    safe_asset_ratio = allocation["수비수+골키퍼"]

    return RecommendationResponse(
        profile_title=f"{portfolio['formation_name']} 포트폴리오 ({request.portfolio_type})",
        portfolio_summary=(
            f"{request.life_stage}·{request.portfolio_type}·{request.account_type} 조건을 "
            "미래에셋 연금투자 가이드북 표에 그대로 매핑한 결과입니다."
        ),
        formation_name=portfolio["formation_name"],
        guide_basis=portfolio["guide_basis"],
        risk_asset_ratio=risk_asset_ratio,
        safe_asset_ratio=safe_asset_ratio,
        allocation=build_allocation_items(portfolio),
        input_effects=build_input_effects(request, portfolio),
        product_types=build_product_types(portfolio),
        reasons=build_reasons(request, portfolio),
        account_rules=build_account_rules(request.account_type, risk_asset_ratio),
        action_plan=build_action_plan(request.account_type, risk_asset_ratio),
        disclaimer=(
            "본 서비스는 오픈소스소프트웨어실습 과제용 교육 서비스이며, "
            "실제 투자 권유나 투자자문이 아닙니다."
        ),
    )
