import argparse
import sys
from pathlib import Path

from imagededup.methods import PHash, DHash, AHash, WHash, CNN

from config import (
    IMAGE_DIR,
    METHOD,
    CNN_GPU_WARNING,
    SUPPORTED_EXTENSIONS,
)
from utils.visualize import visualize_duplicate_groups


METHOD_MAP = {
    "PHash": PHash,
    "DHash": DHash,
    "AHash": AHash,
    "WHash": WHash,
    "CNN": CNN,
}


def find_duplicates_in_dir(image_dir: str, method_name: str = METHOD, threshold: int = None):
    if method_name not in METHOD_MAP:
        print(f"[오류] 지원하지 않는 메서드입니다: {method_name}")
        print(f"       사용 가능: {', '.join(METHOD_MAP.keys())}")
        sys.exit(1)
    
    if method_name == "CNN":
        print(CNN_GPU_WARNING)
    
    encoder = METHOD_MAP[method_name]()
    
    if threshold is None:
        threshold = 10 if method_name != "CNN" else 0.25
    
    print(f"\n[탐지 시작] 디렉토리: {image_dir}")
    print(f"[탐지 시작] 메서드: {method_name}")
    print(f"[탐지 시작] threshold: {threshold}\n")
    
    duplicates = encoder.find_duplicates(
        image_dir=image_dir,
        threshold=threshold,
    )
    
    duplicate_groups = {k: v for k, v in duplicates.items() if v}
    
    print("=" * 50)
    print(f"탐지 결과: {len(duplicate_groups)}개 그룹에서 중복 발견")
    print("=" * 50 + "\n")
    
    if not duplicate_groups:
        print("중복 이미지가 발견되지 않았습니다.")
        return duplicates
    
    for original, dups in duplicate_groups.items():
        print(f"원본: {original}")
        for dup in dups:
            print(f"  └─ 중복: {dup}")
        print()
    
    visualize_duplicate_groups(
        image_dir,
        duplicate_groups,
        max_groups=5,
        output_filename=f"duplicates_{method_name}.png",
    )
    
    return duplicates


def main():
    parser = argparse.ArgumentParser(
        description="디렉토리 내 중복 이미지를 탐지합니다."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=str(IMAGE_DIR),
        help="탐색할 이미지 디렉토리 경로 (기본값: images/)",
    )
    parser.add_argument(
        "--method",
        choices=list(METHOD_MAP.keys()),
        default=METHOD,
        help="사용할 알고리즘",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=None,
        help="중복 판정 threshold (기본값: Hash=10, CNN=0.25)",
    )
    
    args = parser.parse_args()
    
    image_dir = Path(args.directory)
    if not image_dir.exists():
        print(f"[오류] 디렉토리가 존재하지 않습니다: {image_dir}")
        sys.exit(1)
    
    find_duplicates_in_dir(str(image_dir), args.method, args.threshold)


if __name__ == "__main__":
    main()
