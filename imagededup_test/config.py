from pathlib import Path

# ── 경로 설정 ──────────────────────────────────────────────────────
IMAGE_DIR  = Path(__file__).parent / "images"
RESULT_DIR = Path(__file__).parent / "output"

# ── 탐지 방식 선택 (여러 개 선택 가능) ────────────────────────────
# "PHash" | "DHash" | "AHash" | "WHash" | "CNN"
METHODS = ["PHash", "DHash", "CNN"]

# ── 지원 확장자 ────────────────────────────────────────────────────
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

# ── CNN 경고 문구 ──────────────────────────────────────────────────
CNN_GPU_WARNING = (
    "\n[경고] CNN 방식은 GPU가 없으면 매우 느립니다. "
    "이미지 1장당 수 초 이상 소요될 수 있습니다.\n"
)

# ── 해시 방식 판정 기준 (해시 거리, 낮을수록 유사) ──────────────────
HASH_THRESHOLDS = {
    "identical": 0,   # 완전 동일
    "similar":   5,   # 유사
    "weak":      10,  # 약한 유사
    # 10 초과 → 다른 이미지
}

# ── CNN 방식 판정 기준 (코사인 유사도, 높을수록 유사) ───────────────
CNN_THRESHOLDS = {
    "identical": 0.99,
    "similar":   0.90,
    "weak":      0.80,
    # 0.80 미만 → 다른 이미지
}


def classify_distance(distance: float, method: str) -> str:
    """거리값 또는 유사도를 판정 문자열로 변환"""
    if method == "CNN":
        t = CNN_THRESHOLDS
        if distance >= t["identical"]:
            return "🔵 완전 동일"
        elif distance >= t["similar"]:
            return "🟡 유사"
        elif distance >= t["weak"]:
            return "🟠 약한 유사"
        else:
            return "🔴 다른 이미지"
    else:
        t = HASH_THRESHOLDS
        if distance <= t["identical"]:
            return "🔵 완전 동일"
        elif distance <= t["similar"]:
            return "🟡 유사"
        elif distance <= t["weak"]:
            return "🟠 약한 유사"
        else:
            return "🔴 다른 이미지"
