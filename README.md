# Image Duplicate Detection System

`imagededup` 라이브러리를 사용한 이미지 중복 탐지 시스템입니다.  
두 이미지를 비교하거나, 디렉토리 전체에서 중복 이미지를 찾을 수 있습니다.

## 요구 사항

- Python **3.12 이상**
- `imagededup`, `pillow`, `matplotlib`  
  (`numpy`는 `imagededup`의 의존성으로 함께 설치됩니다)

## 설치

```bash
pip install imagededup pillow matplotlib
```

또는 `pyproject.toml` 기준으로:

```bash
pip install .
```

## 프로젝트 구조

```
.
├── config.py              # 설정값 (경로, 알고리즘 목록, 판정 임계값)
├── compare.py             # 두 이미지 비교 CLI
├── find_duplicates.py     # 디렉토리 내 중복 탐지 CLI
├── main.py                # 프로젝트 테스트용 엔트리 포인트
├── utils/
│   ├── __init__.py
│   └── visualize.py       # 비교/중복 결과 PNG 저장
├── images/                # 기본 이미지 디렉토리
│   ├── img1.png
│   └── img2.png
├── output/                # 결과 이미지 저장 디렉토리 (자동 생성)
└── pyproject.toml
```

## 사용법

### 1. 두 이미지 비교

```bash
python compare.py <이미지1> <이미지2>
```

이미지는 기본적으로 `images/` 디렉토리에서 찾습니다.  
`--method`를 지정하지 않으면 `config.METHODS`에 등록된 모든 방식을 순차 실행합니다.

| 옵션 | 설명 |
|---|---|
| `--method {PHash,DHash,AHash,WHash,CNN}` | 단일 방식 지정 |
| `--dir DIR` | 이미지 디렉토리 경로 (기본값: `images/`) |

**예시:**

```bash
python compare.py img1.png img2.png
python compare.py img1.png img2.png --method CNN
python compare.py photo1.jpg photo2.jpg --dir ~/my_photos
```

### 2. 디렉토리 전체 중복 탐지

```bash
python find_duplicates.py [디렉토리 경로]
```

| 옵션 | 설명 |
|---|---|
| `--method {PHash,DHash,AHash,WHash,CNN}` | 사용할 알고리즘 |
| `--threshold FLOAT` | 중복 판정 임계값 (Hash 기본값=10, CNN 기본값=0.25) |

**예시:**

```bash
python find_duplicates.py
python find_duplicates.py --method CNN --threshold 0.8
python find_duplicates.py ~/photo_library --method DHash
```

> **참고:** 현재 `find_duplicates.py`는 `config.METHODS`가 아닌 `config.METHOD`를 참조하고 있어 import 시 오류가 발생합니다.  
> `config.py`에 `METHOD` 상수를 추가하거나, `find_duplicates.py`의 import를 `METHODS`로 수정하면 정상 동작합니다.

## 설정

`config.py`에서 기본값을 변경할 수 있습니다.

| 변수 | 기본값 | 설명 |
|---|---|---|
| `IMAGE_DIR` | `images/` | 기본 이미지 디렉토리 |
| `RESULT_DIR` | `output/` | 결과 저장 디렉토리 |
| `METHODS` | `["PHash", "DHash", "CNN"]` | 기본 실행 방식 목록 |
| `SUPPORTED_EXTENSIONS` | `{".jpg", ".jpeg", ".png", ".webp", ".bmp"}` | 지원 이미지 확장자 |
| `HASH_THRESHOLDS` | `identical: 0, similar: 5, weak: 10` | 해시 방식 판정 기준 |
| `CNN_THRESHOLDS` | `identical: 0.99, similar: 0.90, weak: 0.80` | CNN 방식 판정 기준 |

## 알고리즘

| 메서드 | 비교 방식 | 속도 | 정확도 | 특징 |
|---|---|---|---|---|
| **PHash** | Perceptual Hash | 빠름 | 중간 | 일반적인 중복 탐지에 적합 |
| **DHash** | Difference Hash | 빠름 | 중간 | 리사이즈/밝기 변화에 강함 |
| **AHash** | Average Hash | 매우 빠름 | 낮음 | 빠른 1차 스캐닝용 |
| **WHash** | Wavelet Hash | 빠름 | 중간 | 웨이블릿 변환 기반 |
| **CNN** | CNN 임베딩 | 느림* | 높음 | 의미적 유사도 측정 |

\* CNN 방식은 GPU가 없으면 CPU에서 이미지 1장당 수 초 이상 소요될 수 있습니다.

## 출력

비교 및 중복 탐지 결과는 콘솔에 출력됨과 동시에 `output/` 디렉토리에 PNG 파일로 저장됩니다.

| 명령 | 출력 파일 |
|---|---|
| `compare.py` | `output/compare_{이미지1}_{이미지2}.png` |
| `find_duplicates.py` | `output/duplicates_{메서드}.png` |

시각화에는 NanumGothic 폰트가 사용됩니다. 폰트가 없을 경우 다음 명령으로 설치하세요:

```bash
sudo apt-get install fonts-nanum
```

## 라이선스

MIT License
