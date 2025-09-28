# A4 인쇄용 HTML 디자인 가이드 (모던·심플·세련)

아래 가이드는 **교재/문제집/유인물/팜플렛/전단지** 등 다양한 목적과 **고등학생·대학생·일반 소비자·고급 클라이언트**까지 폭넓게 적용 가능한 **출력 전용(정적) HTML** 디자인 원칙을 **누락 없이** 정리했습니다.

---

## 1) 핵심 철학

* **미니멀리즘**: 불필요한 장식을 제거하고 정보 전달에 집중.
* **일관성**: 색·폰트·간격·정렬·아이콘 스타일을 전 페이지에 통일.
* **위계**: 타이포·크기·굵기·색·여백으로 중요도 차이를 분명히.
* **여백(Whitespace)**: 내용 가독성·고급스러움·집중도를 높이는 핵심 수단.

---

## 2) 색상 (팔레트·대비·톤)

### 원칙

* **팔레트 최소화**: 기본(Neutral) 1–2 + 포인트 1 (총 2–3색 권장).
* **Neutral 기반**: 배경은 #FFFFFF, #F7F8FA, #F2F4F7, #FAFAFA 등 밝은 뉴트럴.
* **포인트 컬러는 절제**: 제목·하이라이트·아이콘·그래프 강조에 제한적으로.
* **충분한 대비**: 본문 텍스트 명암 대비(AA 이상) 확보.

### 피해야 할 것

* 과도하게 **밝은 무지개 그라데이션 배경**
* **이모티콘** 남발 (전문성 저하)
* 목적 없이 **둥근 상자** 남발 (값싸 보임)
* **과도한 네온/형광** 색감, 저대비(회색 위 회색)

### 추천 조합 예시

* **친근·교육용**: Neutral(배경) + Teal(#1AA5A5) or Orange(#F2994A) + Gray(#667085)
* **차분·고급**: White/Off-white + Navy(#0B3558) + Warm Gray(#667085) + Gold 포인트(#C8A24D)
* **밝고 명료**: White + Cobalt Blue(#2F6FED) + Slate Gray(#475467)

---

## 3) 타이포그래피 (글꼴·크기·행간·정렬)

### 글꼴 선택

* **산세리프 중심**: 가독·모던(예: Noto Sans / Pretendard / Inter / Roboto).
* **혼용 시**: 제목=산세리프, 본문=세리프(명조) 가능. 단 **종류는 1–2개**로 제한.
* **변주는 굵기로**: 동일 폰트 패밀리 내 Weight 변화(400/500/700).

### 크기 체계(예시)

* H1: 28–36px / 700
* H2: 22–28px / 700
* H3: 18–22px / 600
* 본문: 12–14px / 400 (인쇄 기준)
* 캡션/주석: 10–12px / 400

### 행간·자간

* 본문 **line-height 1.4–1.6**
* 제목은 1.2–1.35
* 본문 한 줄 폭은 **약 50–70자** 범위 유지

### 정렬

* 본문 **좌측 정렬** 권장(긴 문단 중앙정렬 금지)
* 제목/소제목만 제한적으로 중앙 정렬 사용
* 단락 간 간격(Paragraph spacing)으로 시각적 그룹화

---

## 4) 레이아웃 (그리드·여백·정렬·흐름)

### 페이지 설정

* **A4**: 210×297mm
* 여백 권장: 상·하 18–22mm, 좌·우 15–20mm(출력 프린터 여백 고려)

### 그리드

* **2–3 컬럼 그리드** 권장(교육·리포트: 2컬럼이 무난)
* 칼럼 간격(거터): 6–10mm
* 모든 요소를 **보이지 않는 정렬선**에 맞춰 배치

### 여백 전략

* 텍스트·이미지·상자 주위 **패딩/마진 충분히**
* **비울 곳은 과감히 비우기**(답답함·저가 인상 방지)

### 시선 흐름

* 단면물: **Z-패턴**(좌상 → 우하) 또는 큰 비주얼 중심
* 다면물: 표준 템플릿(본문 페이지 2컬럼, 챕터 오프너 풀블리드 등)으로 **패턴+변주**

---

## 5) 이미지·아이콘·도표

### 이미지

* **고해상도(300dpi)** 원본 사용, 저화질 금지
* 내용과 **직접 관련**된 이미지만 사용(장식성 최소화)
* **풀블리드** 활용 시 제목·캡션 대비 확보
* 이미지 주변 **여백 확보** + 캡션 제공

### 아이콘/일러스트

* **스타일 통일**(선형/면형 중 한 가지)
* 팔레트 내 색상만 사용, 크기·스트로크 굵기 통일
* 이모티콘 대신 **의미 전달용 벡터 아이콘** 소량만

### 표/그래프

* **평면(Flat)**, 3D·그림자·과장 효과 금지
* 헤더/구분선만 약하게, 불필요한 선 제거
* 포인트 데이터만 색으로 강조, 나머지는 저채도 톤

---

## 6) 구성 요소별 가이드

### (1) 표지

* **요소 최소화**: 제목·부제·로고(필요 시 카피 1줄)
* **큰 제목 + 넓은 여백 + 상징 이미지 1개**(또는 단색 배경)
* 브랜드/목적을 직관적으로 암시(교육=아이콘, 기업=제품/추상 비주얼)

### (2) 목차(TOC)

* 단계별 **들여쓰기와 크기 차이**로 계층 표시
* 페이지 번호는 우측 정렬, 점선 리더 도입 가능
* 본문 헤딩 스타일과 **톤·폰트 통일**

### (3) 본문

* 헤딩(H1–H3)·본문·리스트·캡션 **스타일 정의 후 일관 적용**
* 긴 텍스트는 **단락 분할 + 중간 소제목 + 리스트**로 스캔 용이
* 이미지·도표는 **관련 문장 근처 배치 + 캡션**
* 페이지 나눔 시 문장/표가 어색하게 끊기지 않게 조정

### (4) 박스/퀴즈/콜아웃

* **일관 템플릿**(배경색/테두리/아이콘/패딩) 지정 후 반복 사용
* 배경은 팔레트의 **옅은 보조색**, 테두리는 1px 얇게 또는 생략
* 모서리 스타일(각/둥근)은 **문서 전체와 통일**
* 텍스트는 본문 폰트 유지, 크기·톤만 변화

### (5) 연락처/CTA

* **작지만 가독성 유지**, 과장 금지
* 아이콘+텍스트 간 간격 일정
* CTA는 **짧고 명료**(굵기/색만으로 점잖게 강조)

---

## 7) 용도·대상별 톤 조절 (Versatile)

| 대상/용도           | 톤 & 팔레트                           | 타이포                  | 구성 포인트                         |
| --------------- | --------------------------------- | -------------------- | ------------------------------ |
| **교육(고교/대학)**   | 밝은 Neutral + 톤다운 포인트(Teal/Orange) | 산세리프 중심, 가독 최우선      | 예제·정의 박스·아이콘 소량, 2컬럼 본문        |
| **홍보/전단**       | 명도 대비 큰 조합(화이트+딥블루/블랙)            | 굵은 헤드라인 + 간결 본문      | **헤드라인·핵심 포인트·CTA**만 남기고 여백 확대 |
| **기업/고급 클라이언트** | 화이트/워밍레이 + 네이비/골드 포인트             | 산세리프(필요 시 본문 세리프 혼용) | 대칭·정렬·여백, 그래프 모노톤, 문장 간결       |

---

## 8) 출력·제작 유의(인쇄 최적화)

* **@page A4**, 프린터 여백 고려해 **안전 여백** 확보
* **CMYK 인쇄 시** 지나치게 어두운 배경·얇은 연색 텍스트 금지
* 작은 텍스트·얇은 선 **번짐 방지**(선 0.5pt 이상 권장)
* 링크 색/밑줄 등 **웹 UI 흔적 제거**
* 이미지 삽입 시 파일 포맷: **사진=JPEG(고품질), 그래픽=PNG/SVG**
* 최종 출력 전 **시험 인쇄**로 대비·크기·여백 점검

---

## 9) 체크리스트 (빠른 검수용)

**색**

* [ ] 팔레트 2–3색 이내
* [ ] 포인트 색 절제 사용
* [ ] 텍스트 대비 충분

**폰트**

* [ ] 폰트 패밀리 1–2개
* [ ] 굵기로 위계 표현
* [ ] 본문 12–14px, 행간 1.4–1.6

**레이아웃**

* [ ] A4 여백 15–22mm
* [ ] 2–3컬럼 그리드 적용
* [ ] 요소 정렬선 일치

**이미지/도표**

* [ ] 300dpi 고해상도
* [ ] 장식성 최소
* [ ] 평면 그래프, 필요선만

**구성 요소**

* [ ] 표지 요소 3–4개 이하
* [ ] TOC 들여쓰기·페이지번호 정렬
* [ ] 박스 템플릿 일관

**출력**

* [ ] 시험 인쇄로 색·가독 확인
* [ ] 얇은 선/작은 글씨 번짐 점검

---

## 10) HTML/CSS 스타터 (A4 인쇄용, 정적)

> 아래 코드는 **기본 레이아웃·타이포·컬러 토큰**과 **인쇄 설정(@page A4)**, **2컬럼 그리드** 및 **콜아웃 박스** 예시를 담은 **미니 템플릿**입니다.
> 필요에 맞게 토큰만 바꿔 다양한 톤을 빠르게 적용하세요.

```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<title>인쇄용 A4 템플릿</title>
<style>
/* ========= Design Tokens ========= */
:root{
  /* Color */
  --bg: #FFFFFF;
  --ink: #1F2937;          /* 본문 글자 색 */
  --muted: #667085;        /* 보조 텍스트 */
  --line: #E5E7EB;         /* 구분선 */
  --accent: #1AA5A5;       /* 포인트 컬러 (Teal 예시) */
  --accent-weak: #E6F5F5;  /* 포인트 옅은 배경 */
  /* Typography */
  --f-sans: "Pretendard","Noto Sans KR",system-ui,Arial,sans-serif;
  --fs-body: 12.5pt;       /* 인쇄 본문 권장 */
  --fs-small: 10.5pt;
  --lh-body: 1.5;
  /* Layout */
  --page-margin-top: 20mm;
  --page-margin-right: 16mm;
  --page-margin-bottom: 20mm;
  --page-margin-left: 16mm;
  --column-gap: 8mm;       /* 2컬럼 간격 */
}

/* ========= Print Setup ========= */
@page {
  size: A4;
  margin: 0; /* 실제 여백은 body 패딩으로 제어 */
}
@media print {
  a { color: inherit; text-decoration: none; } /* 웹 흔적 제거 */
}

/* ========= Base ========= */
html,body { background: var(--bg); color: var(--ink); }
body{
  font-family: var(--f-sans);
  font-size: var(--fs-body);
  line-height: var(--lh-body);
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
  padding: var(--page-margin-top) var(--page-margin-right)
           var(--page-margin-bottom) var(--page-margin-left);
}

h1,h2,h3{ line-height: 1.25; margin: 0 0 8pt; }
h1{ font-size: 26pt; font-weight: 700; }
h2{ font-size: 20pt; font-weight: 700; margin-top: 12pt; }
h3{ font-size: 16pt; font-weight: 600; margin-top: 10pt; }

p{ margin: 0 0 8pt; color: var(--ink); }
.small{ font-size: var(--fs-small); color: var(--muted); }

/* ========= Grid ========= */
.page{ display: grid; grid-template-columns: 1fr; gap: 10pt; }
.two-col{
  column-count: 2;
  column-gap: var(--column-gap);
}

/* ========= Rules ========= */
.hr{ height: 1px; background: var(--line); margin: 10pt 0; }

/* ========= Callout / Box ========= */
.callout{
  background: var(--accent-weak);
  border: 1px solid #D5EEEE;
  padding: 10pt;
  border-radius: 10px; /* 문서 전체 둥근 스타일이라면 유지, 각이면 0으로 */
  break-inside: avoid;
}
.callout .title{
  font-weight: 600; color: var(--accent); margin-bottom: 6pt;
}

/* ========= Figure ========= */
figure{ margin: 0 0 8pt; break-inside: avoid; }
figcaption{ font-size: var(--fs-small); color: var(--muted); margin-top: 4pt; }

/* ========= TOC ========= */
.toc h2{ margin-bottom: 6pt; }
.toc ol{ margin: 0; padding-left: 0; list-style: none; }
.toc li{
  display: grid; grid-template-columns: 1fr auto; align-items: baseline;
  gap: 8pt; padding: 3pt 0; border-bottom: 1px dotted var(--line);
}
.toc .lvl1{ font-weight: 600; }
.toc .lvl2{ padding-left: 8pt; color: var(--muted); }

/* ========= Footer (contact) ========= */
.footer{
  margin-top: 16pt; padding-top: 8pt; border-top: 1px solid var(--line);
  font-size: var(--fs-small); color: var(--muted);
}
</style>
</head>
<body>

<!-- Cover -->
<section class="page">
  <h1>모던 A4 인쇄물 가이드</h1>
  <p class="small">부제목 혹은 짧은 카피를 여기에 배치합니다.</p>
  <div class="hr"></div>
</section>

<!-- TOC -->
<section class="page toc">
  <h2>Contents</h2>
  <ol>
    <li><span class="lvl1">1. 색상 원칙</span><span>2</span></li>
    <li><span class="lvl1">2. 타이포그래피</span><span>3</span></li>
    <li><span class="lvl2">2.1 본문과 제목</span><span>3</span></li>
    <li><span class="lvl1">3. 레이아웃</span><span>4</span></li>
  </ol>
</section>

<!-- Body (Two Columns) -->
<section class="page two-col">
  <h2>1. 색상 원칙</h2>
  <p>팔레트는 2–3색 내에서… (본문)</p>

  <h2>2. 타이포그래피</h2>
  <p>가독성과 위계를 위해… (본문)</p>

  <div class="callout">
    <div class="title">퀴즈 / 콜아웃</div>
    <p>핵심 요약, 질문, 주의, 팁 등을 담는 상자.</p>
  </div>

  <h2>3. 레이아웃</h2>
  <p>A4 용지에 맞춰… (본문)</p>

  <figure>
    <img src="example.jpg" alt="예시 이미지" style="width:100%; height:auto;" />
    <figcaption>그림 1. 관련 이미지 캡션</figcaption>
  </figure>
</section>

<!-- Contact -->
<section class="page footer">
  문의: 02-1234-5678 · hello@example.com · example.com
</section>

</body>
</html>
```

### 토큰만 바꿔 다양한 톤 적용하기

* **교육용**: `--accent: #F2994A; --accent-weak: #FFF3E8;`
* **기업용**: `--accent: #0B3558; --accent-weak: #EAF0F6;`
* **밝고 명료**: `--accent: #2F6FED; --accent-weak: #EEF2FF;`

> **주의**: 문서 전체가 **각진 스타일**이라면 `.callout { border-radius: 0 }`로 통일하세요. 모서리 스타일 혼용은 산만해 보입니다.

---

## 11) 흔한 함정 & 예방 팁

* (색) **너무 많은 색** → 팔레트 2–3색으로 축소, 포인트만 강조
* (폰트) **폰트 남발** → 패밀리 1–2개, 굵기·크기만 변주
* (정렬) **정렬선 불일치** → 그리드/가이드라인에 스냅
* (여백) **과밀** → 여백 늘리고 정보 요약, 장식성 최소화
* (이미지) **저해상도** → 300dpi 원본 사용, 시험 인쇄로 선명도 확인
* (박스) **둥근 상자 남발** → 목적·템플릿화·일관성 유지(각/둥근 중 택1)
* (웹 티) **밑줄 링크/파란 링크** → 인쇄 모드에서 색/밑줄 제거

---

---

## 12) A4 강제 규격 준수 (PDF 변환 최적화)

> **중요**: 웹에서 보기엔 문제없어도 PDF 변환 시 페이지가 넘치거나 잘리는 문제를 방지하기 위한 **엄격한 규격**입니다.

### A. 페이지 높이 강제 제한

```css
/* ❌ 잘못된 방식 - 내용이 많으면 계속 늘어남 */
.page {
    min-height: 297mm;
}

/* ✅ 올바른 방식 - 고정 높이로 강제 제한 */
.page {
    width: 210mm;
    height: 297mm;  /* 고정 높이 */
    overflow: hidden; /* 넘치는 내용 강제 숨김 */
    page-break-after: always;
}
```

### B. 안전 여백 계산 (Safety Margin)

```css
/* A4 안전 콘텐츠 영역 계산 */
.page {
    width: 210mm;
    height: 297mm;
    padding: 20mm 18mm 20mm 18mm; /* 상우하좌 */
    /* 실제 콘텐츠 영역: 174mm × 257mm */
}

/* 콘텐츠 영역 내부에서 추가 여백 확보 */
.page-content {
    max-height: 217mm; /* 257mm - 40mm(헤더+푸터) */
    overflow: hidden;
}
```

### C. 페이지당 내용량 제한

**페이지당 최대 허용 요소:**
- **제목 1개** + **본문 3-4문단** + **테이블 1개** + **이미지/그래프 1개**
- **또는** **제목 1개** + **본문 6-8문단** (이미지/테이블 없이)
- **또는** **제목 1개** + **큰 테이블 1개** + **설명 2문단**

### D. 테이블 크기 제한

```css
/* 테이블 최대 높이 제한 */
table {
    max-height: 120mm; /* 페이지의 약 절반 */
    overflow: hidden;
}

/* 행 수 제한 가이드라인 */
/* - 헤더 포함 최대 15행
   - 복잡한 테이블은 페이지 분할 고려
   - 열 수는 최대 6개 권장 */
```

### E. 이미지/그래프 크기 제한

```css
/* SVG/이미지 최대 크기 */
.chart-container, figure {
    max-height: 100mm; /* 페이지의 1/3 이하 */
    max-width: 174mm;  /* 안전 콘텐츠 폭 */
}

/* SVG viewBox 표준화 */
svg {
    width: 100%;
    max-height: 80mm;
    viewBox: "0 0 400 200"; /* 비율 고정 */
}
```

### F. 텍스트 줄 수 제한

```css
/* 본문 텍스트 최대 높이 */
.text-content {
    max-height: 180mm; /* 여백 고려한 최대 높이 */
    overflow: hidden;
    text-overflow: ellipsis;
}

/* 문단별 최대 줄 수 가이드라인 */
p {
    max-height: 25mm; /* 약 6-7줄 제한 */
    overflow: hidden;
}
```

### G. 멀티 페이지 설계 원칙

**페이지 1 (표지)**
- 제목 + 부제 + 로고/아이콘 + 간단한 설명 (2-3줄)
- 최대 5개 요소 이하

**페이지 2-N (내용)**
- **단일 주제 원칙**: 한 페이지당 하나의 완결된 주제만
- **70% 규칙**: 페이지 높이의 70%만 사용, 30%는 여백으로 보존
- **분할 우선**: 내용이 많으면 페이지를 늘리지 말고 다음 페이지로 분할

### H. PDF 변환 테스트 필수사항

```css
/* PDF 변환 시 반드시 포함해야 할 CSS */
@page {
    size: A4 portrait;
    margin: 0;
}

@media print {
    .page {
        margin: 0 !important;
        box-shadow: none !important;
        page-break-after: always;
        height: 297mm !important; /* 강제 고정 */
        max-height: 297mm !important;
    }
    
    .page:last-child {
        page-break-after: avoid;
    }
    
    /* 넘치는 내용 강제 숨김 */
    .page-content {
        overflow: hidden !important;
        max-height: 217mm !important;
    }
}
```

### I. 콘텐츠 분할 가이드라인

**자동 분할 규칙:**
1. **테이블**: 10행 초과 시 다음 페이지로 분할
2. **그래프**: 2개 이상 시 페이지 분할
3. **텍스트**: 8문단 초과 시 페이지 분할
4. **이미지**: 60mm 초과 시 단독 페이지 배치

### J. 오류 방지 체크리스트

**설계 단계:**
- [ ] 페이지당 주요 요소 3개 이하로 제한
- [ ] 각 요소 최대 크기 미리 계산
- [ ] 여백 합계가 페이지의 30% 이상인지 확인

**코딩 단계:**
- [ ] `height: 297mm` (min-height 금지)
- [ ] `overflow: hidden` 설정
- [ ] `max-height` 속성으로 요소별 크기 제한
- [ ] `page-break-*` 속성 적절히 활용

**검증 단계:**
- [ ] 브라우저 인쇄 미리보기로 페이지 분할 확인
- [ ] PDF 저장하여 실제 A4 크기 확인
- [ ] 각 페이지가 297mm를 넘지 않는지 개발자 도구로 측정

---

### 결론

이 가이드는 **모던·심플**한 기본기를 토대로, **대상과 용도에 맞춘 미세 조정**으로 언제든 세련된 인쇄물을 만들 수 있도록 설계되었습니다.
**팔레트 최소화, 폰트 절제, 정돈된 그리드, 충분한 여백, 목적 있는 강조**—이 다섯 가지만 지켜도 결과물의 완성도와 신뢰도가 극적으로 향상됩니다.

**추가로, A4 강제 규격 준수를 통해 PDF 변환 시에도 완벽한 페이지 분할과 레이아웃을 보장할 수 있습니다.**
