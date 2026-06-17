import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.font_manager as fm
from PIL import Image
from pathlib import Path

from config import RESULT_DIR

# ── 한글 폰트 설정 ─────────────────────────────────────────────────
def _set_korean_font():
    font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    if not Path(font_path).exists():
        print("[경고] NanumGothic 폰트 없음. sudo apt-get install fonts-nanum 실행 후 재시도하세요.")
        return
    fe = fm.FontEntry(fname=font_path, name="NanumGothic")
    fm.fontManager.ttflist.insert(0, fe)
    plt.rcParams["font.family"]        = "NanumGothic"
    plt.rcParams["axes.unicode_minus"] = False

_set_korean_font()

# ── 판정별 색상 ────────────────────────────────────────────────────
VERDICT_COLORS = {
    "🔵 완전 동일":   "#3498db",
    "🟡 유사 이미지": "#f1c40f",
    "🟠 약한 유사":   "#e67e22",
    "🔴 다른 이미지": "#e74c3c",
}


def visualize_comparison(
    path1: str,
    path2: str,
    results: list,
    output_filename: str,
    show: bool = False,
) -> None:
    """
    두 이미지 + 방식별 비교 결과를 PNG로 저장

    results: [{"method": str, "distance": float, "verdict": str}, ...]
    """
    os.makedirs(RESULT_DIR, exist_ok=True)

    img1 = Image.open(path1).convert("RGB")
    img2 = Image.open(path2).convert("RGB")

    n_methods = len(results)
    fig = plt.figure(figsize=(12, 6 + n_methods * 0.6))
    fig.patch.set_facecolor("#f8f9fa")

    gs = gridspec.GridSpec(
        2, 2,
        height_ratios=[4, n_methods],
        hspace=0.1,
        wspace=0.1,
    )

    # ── 상단: 이미지 두 장 ─────────────────────────────────────────
    # 전체 판정 중 가장 유사한 결과 기준으로 테두리 색상 결정
    best_verdict = results[0]["verdict"] if results else "🔴 다른 이미지"
    border_color = VERDICT_COLORS.get(best_verdict, "#95a5a6")

    for col, (img, path) in enumerate([(img1, path1), (img2, path2)]):
        ax = fig.add_subplot(gs[0, col])
        ax.imshow(img)
        ax.set_title(Path(path).name, fontsize=11, pad=8)
        ax.axis("off")
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor(border_color)
            spine.set_linewidth(5)

    # ── 하단: 방식별 결과 테이블 ───────────────────────────────────
    ax_table = fig.add_subplot(gs[1, :])
    ax_table.axis("off")

    col_labels = ["방식", "거리 / 유사도", "판정"]
    table_data = []
    cell_colors = []

    for r in results:
        label     = "유사도" if r["method"] == "CNN" else "거리"
        dist_str  = f"{r['distance']:.4f}  ({label})"
        table_data.append([r["method"], dist_str, r["verdict"]])
        row_color = VERDICT_COLORS.get(r["verdict"], "#95a5a6") + "33"  # 투명도 적용
        cell_colors.append([row_color, row_color, row_color])

    table = ax_table.table(
        cellText=table_data,
        colLabels=col_labels,
        cellLoc="center",
        loc="center",
        cellColours=cell_colors,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.8)

    # 헤더 스타일
    for col_idx in range(len(col_labels)):
        table[0, col_idx].set_facecolor("#2c3e50")
        table[0, col_idx].set_text_props(color="white", fontweight="bold")

    output_path = Path(RESULT_DIR) / output_filename
    plt.savefig(str(output_path), dpi=150, bbox_inches="tight")

    if show:
        plt.show()
    plt.close()

    print(f"결과 저장 완료: {output_path}")
