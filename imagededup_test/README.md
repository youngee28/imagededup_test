# Image Duplicate Detection System

`imagededup` 라이브러리를 사용한 이미지 중복 탐지 시스템입니다.

## 설치

```bash
pip install imagededup pillow matplotlib
```

## 디렉토리 구조

```
.
├── config.py              # 설정값 관리
├── compare.py             # 두 이미지 비교
├── find_duplicates.py     # 디렉토리 전체 중복 탐지
├── utils/
│   ├── __init__.py
│   └── visualize.py       # 시각화 유틸리티
├── images/
│   ├── test_same/         # 동일 이미지 테스트용
│   ├── test_similar/      # 유사 이미지 테스트용
│   └── test_different/    # 다른 이미지 테스트용
└── output/                # 결과 이미지 저장
```

## 사용법

### 1. 두 이미지 비교

```bash
python compare.py img1.jpg img2.jpg
```

옵션:
- `--method`: PHash | DHash | AHash | WHash | CNN (기본값: PHash)
- `--dir`: 이미지 디렉토리 경로 (기본값: images/)

### 2. 디렉토리 전체 중복 탐지

```bash
python find_duplicates.py [디렉토리 경로]
```

옵션:
- `--method`: 사용할 알고리즘
- `--threshold`: 중복 판정 기준값

## 알고리즘 선택 가이드

| 메서드 | 속도 | 정확도 | 용도 |
|--------|------|--------|------|
| PHash | 빠름 | 중간 | 일반적인 중복 탐지 |
| DHash | 빠름 | 중간 | 리사이즈에 강함 |
| AHash | 매우 빠름 | 낮음 | 빠른 스캐닝 |
| WHash | 빠름 | 중간 | 웨이블릿 기반 |
| CNN | 느림* | 높음 | 의미적 유사도 |

\* CNN은 GPU 없이 CPU만 사용 시 이미지 1장당 수 초 소요

## 설정 변경

`config.py`에서 기본값을 수정할 수 있습니다:

```python
METHOD = "PHash"  # 기본 알고리즘 변경
THRESHOLDS = {...}  # 판정 기준 수정
```
