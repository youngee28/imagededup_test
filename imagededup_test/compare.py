import argparse
import sys
import numpy as np
from pathlib import Path

from imagededup.methods import PHash, DHash, AHash, WHash, CNN

from config import (
    IMAGE_DIR,
    METHODS,
    CNN_GPU_WARNING,
    SUPPORTED_EXTENSIONS,
    classify_distance,
)
from utils.visualize import visualize_comparison


METHOD_MAP = {
    "PHash": PHash,
    "DHash": DHash,
    "AHash": AHash,
    "WHash": WHash,
    "CNN":   CNN,
}


def hamming_distance(hash1: str, hash2: str) -> int:
    """두 해시 문자열 간의 해밍 거리 계산"""
    return bin(int(hash1, 16) ^ int(hash2, 16)).count("1")


def cosine_similarity(enc1: np.ndarray, enc2: np.ndarray) -> float:
    """두 CNN 인코딩 간의 코사인 유사도 계산 (0~1, 높을수록 유사)"""
    enc1 = enc1.flatten()
    enc2 = enc2.flatten()
    return float(np.dot(enc1, enc2) / (np.linalg.norm(enc1) * np.linalg.norm(enc2)))


def validate_image(path: Path) -> bool:
    if not path.exists():
        print(f"[오류] 파일이 존재하지 않습니다: {path}")
        return False
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        print(f"[오류] 지원하지 않는 확장자입니다: {path.suffix}")
        print(f"       지원 확장자: {', '.join(SUPPORTED_EXTENSIONS)}")
        return False
    return True


def run_single_method(path1: str, path2: str, method_name: str) -> dict:
    """단일 방식으로 두 이미지 비교 후 결과 반환"""
    encoder = METHOD_MAP[method_name]()

    if method_name == "CNN":
        enc1 = encoder.encode_image(image_file=path1)
        enc2 = encoder.encode_image(image_file=path2)
        distance = cosine_similarity(enc1, enc2)
    else:
        hash1 = encoder.encode_image(image_file=path1)
        hash2 = encoder.encode_image(image_file=path2)
        distance = hamming_distance(hash1, hash2)

    return {
        "method":   method_name,
        "distance": distance,
        "verdict":  classify_distance(distance, method_name),
    }


def compare_images(path1: str, path2: str, methods: list) -> list:
    """선택된 모든 방식으로 비교 후 결과 리스트 반환"""
    results = []

    for method_name in methods:
        if method_name not in METHOD_MAP:
            print(f"[오류] 지원하지 않는 메서드: {method_name}")
            continue

        if method_name == "CNN":
            print(CNN_GPU_WARNING)

        result = run_single_method(path1, path2, method_name)
        results.append(result)

    # 콘솔 출력
    print("\n" + "=" * 52)
    print(f"  이미지 1 : {Path(path1).name}")
    print(f"  이미지 2 : {Path(path2).name}")
    print("-" * 52)
    for r in results:
        label = "유사도" if r["method"] == "CNN" else "거리  "
        print(f"  {r['method']:<8}  {label}: {r['distance']:<10.4f}  {r['verdict']}")
    print("=" * 52 + "\n")

    # 시각화
    visualize_comparison(
        path1=path1,
        path2=path2,
        results=results,
        output_filename=f"compare_{Path(path1).stem}_{Path(path2).stem}.png",
    )

    return results


def main():
    parser = argparse.ArgumentParser(description="두 이미지의 유사도를 비교합니다.")
    parser.add_argument("image1", help="첫 번째 이미지 파일명")
    parser.add_argument("image2", help="두 번째 이미지 파일명")
    parser.add_argument(
        "--method",
        choices=list(METHOD_MAP.keys()),
        default=None,
        help="단일 방식 지정 (미지정 시 config.METHODS 전체 실행)",
    )
    parser.add_argument(
        "--dir",
        default=str(IMAGE_DIR),
        help="이미지 디렉토리 경로 (기본값: config.IMAGE_DIR)",
    )

    args = parser.parse_args()

    img_dir = Path(args.dir)
    path1   = img_dir / args.image1
    path2   = img_dir / args.image2

    if not validate_image(path1) or not validate_image(path2):
        sys.exit(1)

    # --method 지정 시 해당 방식만, 미지정 시 config.METHODS 전체 실행
    methods = [args.method] if args.method else METHODS

    compare_images(str(path1), str(path2), methods)


if __name__ == "__main__":
    main()
