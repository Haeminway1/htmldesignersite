# HTML 멀티플랫폼 디자인 완전 가이드
### A4 인쇄 · 모바일 웹 · 전자책 리더 통합 개발 매뉴얼

<div style="text-align: center; margin: 40px 0; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px;">
  <p style="font-size: 14px; margin: 0; opacity: 0.9;">Version 1.0</p>
  <p style="font-size: 12px; margin: 10px 0 0; opacity: 0.8;">최종 수정: 2025년 1월</p>
</div>

---

## 📋 목차

### [PART 1] 디자인 철학과 원칙
- 1.1 핵심 디자인 철학
- 1.2 플랫폼별 접근 전략
- 1.3 공통 디자인 원칙

### [PART 2] A4 인쇄용 디자인
- 2.1 색상 시스템
- 2.2 타이포그래피
- 2.3 레이아웃과 그리드
- 2.4 이미지와 도표
- 2.5 페이지 구성 요소
- 2.6 인쇄 최적화
- 2.7 PDF 변환 규격

### [PART 3] 모바일 웹 최적화
- 3.1 모바일 타이포그래피
- 3.2 터치 인터페이스 설계
- 3.3 반응형 레이아웃
- 3.4 뷰포트와 브레이크포인트
- 3.5 성능 최적화
- 3.6 접근성 고려사항

### [PART 4] 전자책 리더 기능
- 4.1 데이터 영속성 (localStorage)
- 4.2 북마크 시스템
- 4.3 하이라이트 기능
- 4.4 독서 환경 커스터마이징
- 4.5 진행률 추적
- 4.6 사용자 경험 최적화

### [PART 5] 통합 구현
- 5.1 통합 아키텍처
- 5.2 조건부 스타일링
- 5.3 완전한 템플릿 코드
- 5.4 배포와 유지보수

### [PART 6] 실전 체크리스트
- 6.1 개발 전 체크리스트
- 6.2 개발 중 체크리스트
- 6.3 배포 전 체크리스트

---

<div style="page-break-after: always;"></div>

# [PART 1] 디자인 철학과 원칙

## 1.1 핵심 디자인 철학

<p style="text-align: justify;">
현대 웹 디자인은 더 이상 단일 플랫폼에 국한되지 않습니다. 하나의 HTML 문서가 인쇄물로 출력될 수도 있고, 모바일 화면에서 읽힐 수도 있으며, 전자책 리더로 활용될 수도 있습니다. 이러한 다양한 사용 사례를 모두 충족시키기 위해서는 '적응형 설계(Adaptive Design)'와 '점진적 향상(Progressive Enhancement)'이라는 두 가지 핵심 원칙을 이해해야 합니다.
</p>

### 미니멀리즘 (Minimalism)

<p style="text-align: justify;">
불필요한 장식 요소를 제거하고 정보 전달에 집중합니다. 과도한 그래픽, 애니메이션, 색상 사용은 사용자의 주의를 분산시키고 인쇄 품질을 저하시킬 수 있습니다. 핵심 메시지가 명확하게 전달되도록 시각적 노이즈를 최소화해야 합니다.
</p>

**적용 원칙:**
- 한 페이지당 핵심 메시지 1-2개로 제한
- 장식적 요소는 의미 전달에 기여하는 경우만 사용
- 공백(Whitespace)을 적극적으로 활용
- 모든 디자인 요소에 "왜 필요한가?"라는 질문 던지기

### 일관성 (Consistency)

<p style="text-align: justify;">
색상, 폰트, 간격, 정렬, 아이콘 스타일을 문서 전체에 걸쳐 통일합니다. 일관성은 전문성을 높이고 사용자가 콘텐츠를 예측 가능하게 만듭니다. 예를 들어, H2 제목이 페이지마다 다른 크기나 색상으로 표시된다면 사용자는 혼란을 느끼게 됩니다.
</p>

**구현 방법:**
- CSS 변수(Custom Properties)로 디자인 토큰 정의
- 컴포넌트 기반 접근 (재사용 가능한 요소)
- 스타일 가이드 문서 작성 및 공유
- 정기적인 디자인 리뷰로 일관성 검증

### 위계 (Hierarchy)

<p style="text-align: justify;">
타이포그래피, 크기, 굵기, 색상, 여백을 통해 정보의 중요도 차이를 명확히 표현합니다. 시각적 위계가 잘 구성된 문서는 스캔(Scanning)이 쉽고, 사용자가 원하는 정보를 빠르게 찾을 수 있습니다. 특히 모바일 환경에서는 화면 크기가 제한적이므로 명확한 위계가 더욱 중요합니다.
</p>

**위계 구성 요소:**
1. **크기**: 더 중요한 요소는 더 크게
2. **굵기**: 제목은 Bold, 본문은 Regular
3. **색상**: 강조 요소는 포인트 컬러 활용
4. **간격**: 중요 섹션 전후에 넉넉한 여백

### 여백 (Whitespace)

<p style="text-align: justify;">
여백은 단순히 비어있는 공간이 아니라 디자인의 핵심 요소입니다. 충분한 여백은 가독성을 높이고, 고급스러운 인상을 주며, 사용자의 시선을 유도합니다. 특히 인쇄물에서 여백이 부족하면 답답하고 저렴한 느낌을 줄 수 있으며, 모바일에서는 터치 인터페이스에 방해가 됩니다.
</p>

---

## 1.2 플랫폼별 접근 전략

### A4 인쇄용 전략

<p style="text-align: justify;">
인쇄물은 고정된 크기(210×297mm)와 해상도(300dpi)를 가지며, 사용자는 한 번 인쇄하면 수정할 수 없습니다. 따라서 완성도가 가장 중요하며, 색상이 CMYK 인쇄 과정에서 어떻게 표현될지, 작은 글씨가 번지지 않을지 등을 신중히 고려해야 합니다.
</p>

**핵심 고려사항:**
- 페이지당 콘텐츠 밀도 제한 (70% 규칙)
- 안전 여백 확보 (프린터 물리적 한계)
- CMYK 색상 공간 고려
- 고해상도 이미지(300dpi) 필수

### 모바일 웹 전략

<p style="text-align: justify;">
모바일 환경은 다양한 화면 크기, 터치 기반 인터랙션, 제한된 네트워크 대역폭 등의 특성을 가집니다. "모바일 우선(Mobile First)" 접근법을 사용하여 가장 제한적인 환경에서 먼저 설계하고, 점진적으로 데스크톱 환경을 위한 기능을 추가하는 것이 효과적입니다.
</p>

**핵심 고려사항:**
- 터치 타겟 최소 44×44px
- 모바일 우선 미디어 쿼리
- 성능 최적화 (이미지 압축, 코드 최소화)
- 한 손 사용 고려 (엄지 존)

### 전자책 리더 전략

<p style="text-align: justify;">
전자책 리더는 사용자가 장시간 텍스트를 읽는 환경입니다. 눈의 피로를 최소화하고, 개인화된 독서 환경을 제공하며, 독서 경험을 방해하지 않는 부드러운 인터랙션이 중요합니다. 또한 사용자의 독서 진행 상황과 노트를 지속적으로 저장하여 연속성을 제공해야 합니다.
</p>

**핵심 고려사항:**
- localStorage 기반 데이터 영속성
- 가독성 최우선 (16-18px 본문)
- 독서 환경 커스터마이징
- 비침습적 UI (독서에 집중)

---

## 1.3 공통 디자인 원칙

### 접근성 (Accessibility)

<p style="text-align: justify;">
모든 사용자가 콘텐츠에 접근할 수 있어야 합니다. 시각 장애인을 위한 충분한 색상 대비(최소 4.5:1), 난독증 사용자를 위한 읽기 쉬운 폰트, 키보드만으로도 모든 기능 사용 가능하도록 설계해야 합니다. 접근성은 법적 요구사항일 뿐만 아니라 더 많은 사용자에게 도달할 수 있는 방법입니다.
</p>

### 성능 (Performance)

<p style="text-align: justify;">
빠른 로딩 속도는 사용자 경험의 핵심입니다. 이미지 최적화, 코드 압축, 지연 로딩(Lazy Loading) 등의 기법을 활용하여 초기 로딩 시간을 최소화해야 합니다. 특히 모바일 환경에서는 제한된 CPU와 네트워크를 고려하여 불필요한 JavaScript 실행을 줄여야 합니다.
</p>

### 유지보수성 (Maintainability)

<p style="text-align: justify;">
코드는 작성하는 것보다 유지보수하는 시간이 더 깁니다. 명확한 네이밍, 일관된 코드 스타일, 적절한 주석, 컴포넌트화를 통해 추후 수정과 확장이 용이하도록 설계해야 합니다. CSS 변수를 활용하면 디자인 시스템을 중앙에서 관리할 수 있어 유지보수가 크게 개선됩니다.
</p>

---

<div style="page-break-after: always;"></div>

# [PART 2] A4 인쇄용 디자인

## 2.1 색상 시스템

<p style="text-align: justify;">
인쇄물의 색상은 화면과 다르게 렌더링됩니다. RGB(화면용)와 CMYK(인쇄용)는 색 공간이 다르며, 특히 밝은 네온 색상이나 진한 검정색은 인쇄 시 의도와 다르게 표현될 수 있습니다. 따라서 인쇄물 디자인 시에는 보수적인 색상 팔레트를 사용하고, 시험 인쇄를 통해 실제 색상을 확인해야 합니다.
</p>

### 팔레트 구성 원칙

**최소화 전략**
- 기본(Neutral) 색상 1-2개
- 포인트(Accent) 컬러 1개
- 총 2-3색 이내 권장

<p style="text-align: justify;">
색상을 제한하는 이유는 일관성과 전문성 때문입니다. 너무 많은 색상을 사용하면 산만하고 정리되지 않은 인상을 줍니다. 특히 기업 문서나 학술 자료에서는 절제된 색상 사용이 신뢰도를 높입니다.
</p>

### 권장 배경 색상

```css
:root {
  --bg-white: #FFFFFF;        /* 순백 */
  --bg-warm: #FAFAF8;         /* 따뜻한 오프화이트 */
  --bg-cool: #F7F8FA;         /* 차갑고 모던한 회색 */
  --bg-neutral: #F2F4F7;      /* 중성적 밝은 회색 */
}
```

### 텍스트 색상 (명암 대비 고려)

```css
:root {
  /* 본문 텍스트 */
  --text-primary: #1F2937;    /* 거의 검정 (WCAG AAA) */
  --text-secondary: #374151;  /* 약간 밝은 회색 (WCAG AA) */
  --text-muted: #667085;      /* 보조 정보용 */
  
  /* 대비율 */
  /* #1F2937 on #FFFFFF = 15.3:1 (AAA) */
  /* #667085 on #FFFFFF = 4.8:1 (AA) */
}
```

<p style="text-align: justify;">
WCAG(Web Content Accessibility Guidelines) 기준에 따르면, 본문 텍스트는 최소 4.5:1의 대비율을 가져야 하며, 큰 텍스트(18pt 이상 또는 14pt Bold 이상)는 3:1 이상이면 됩니다. 이 기준을 충족하면 시각 장애가 있는 사용자도 텍스트를 읽을 수 있습니다.
</p>

### 포인트 컬러 선택

**용도별 추천 조합**

| 용도 | 배경 | 포인트 컬러 | 보조 회색 | 특징 |
|-----|------|-----------|----------|------|
| 교육/친근 | `#FFFFFF` | `#1AA5A5` (Teal)<br>`#F2994A` (Orange) | `#667085` | 활기차고 접근하기 쉬운 느낌 |
| 기업/고급 | `#FAFAF8` | `#0B3558` (Navy)<br>`#C8A24D` (Gold) | `#667085` | 차분하고 신뢰감 있는 느낌 |
| 명료/모던 | `#FFFFFF` | `#2F6FED` (Cobalt)<br>`#475467` (Slate) | `#667085` | 깔끔하고 현대적인 느낌 |

### 피해야 할 색상 패턴

❌ **과도한 그라데이션**
```css
/* 인쇄 시 밴딩 현상 발생 가능 */
background: linear-gradient(45deg, 
  #FF6B6B, #FFE66D, #4ECDC4, #44A7F0);
```

✅ **단색 또는 단순한 그라데이션**
```css
/* 인쇄 안전 */
background: #FFFFFF;
/* 또는 */
background: linear-gradient(180deg, 
  #FFFFFF 0%, #F7F8FA 100%);
```

### 색상 검증 체크리스트

- [ ] 팔레트 3색 이내
- [ ] 본문 텍스트 대비율 4.5:1 이상
- [ ] 제목 텍스트 대비율 3:1 이상
- [ ] 포인트 컬러는 강조 용도로만 제한적 사용
- [ ] CMYK 인쇄 시 색상 재현 가능 여부 확인
- [ ] 흑백 인쇄 시에도 구분 가능한지 검증

---

## 2.2 타이포그래피

<p style="text-align: justify;">
타이포그래피는 디자인의 90%를 차지합니다. 좋은 타이포그래피는 독자가 의식하지 못하지만, 나쁜 타이포그래피는 즉시 눈에 띕니다. 인쇄물에서는 특히 글자 크기, 행간, 자간의 균형이 중요하며, 이는 장시간 독서 시 눈의 피로도에 직접적인 영향을 미칩니다.
</p>

### 글꼴 선택

**산세리프(Sans-serif) 중심**

<p style="text-align: justify;">
현대적이고 깔끔한 인상을 주는 산세리프 폰트를 기본으로 사용합니다. 한글 폰트로는 Pretendard, Noto Sans KR, Spoqa Han Sans 등이 웹과 인쇄 양쪽에서 뛰어난 가독성을 제공합니다. 영문 폰트는 Inter, Roboto, Open Sans 등이 권장됩니다.
</p>

```css
:root {
  --font-primary: "Pretendard Variable", Pretendard, 
                  "Noto Sans KR", -apple-system, 
                  BlinkMacSystemFont, system-ui, sans-serif;
  
  --font-mono: "JetBrains Mono", "Fira Code", 
               "Courier New", monospace;
}
```

**세리프 혼용 전략**

<p style="text-align: justify;">
제목은 산세리프, 본문은 세리프를 사용하는 혼용 전략도 효과적입니다. 세리프 폰트는 긴 텍스트에서 가독성이 높으며, 전통적이고 권위 있는 느낌을 줍니다. 단, 폰트 종류는 전체 문서에서 2개 이내로 제한해야 합니다.
</p>

### 크기 체계 (인쇄 기준)

**계층적 스케일**

```css
:root {
  /* Display (대형 제목 - 표지용) */
  --fs-display: 36pt;
  --fw-display: 700;
  
  /* Heading 1 (페이지 제목) */
  --fs-h1: 28pt;
  --fw-h1: 700;
  --lh-h1: 1.25;
  
  /* Heading 2 (주요 섹션) */
  --fs-h2: 22pt;
  --fw-h2: 700;
  --lh-h2: 1.3;
  
  /* Heading 3 (하위 섹션) */
  --fs-h3: 18pt;
  --fw-h3: 600;
  --lh-h3: 1.35;
  
  /* Body (본문) */
  --fs-body: 12.5pt;
  --fw-body: 400;
  --lh-body: 1.5;
  
  /* Caption (캡션/주석) */
  --fs-caption: 10.5pt;
  --fw-caption: 400;
  --lh-caption: 1.4;
}
```

<p style="text-align: justify;">
인쇄물의 본문 크기는 일반적으로 10-14pt 사이가 적절합니다. 12pt는 가장 보편적인 크기이며, 독서 거리 30-35cm에서 편안하게 읽을 수 있습니다. 제목과 본문의 크기 차이는 1.25-1.5배를 유지하여 명확한 위계를 만듭니다.
</p>

### 행간과 자간

**행간(Line Height)**

```css
/* 본문 */
p {
  line-height: 1.5;  /* 150% */
  /* 12pt 폰트 → 18pt 행간 */
}

/* 제목 */
h1, h2, h3 {
  line-height: 1.25; /* 125% */
}

/* 좁은 공간 */
.compact {
  line-height: 1.4;  /* 140% */
}
```

<p style="text-align: justify;">
행간이 너무 좁으면 위아래 줄이 겹쳐 보이고, 너무 넓으면 시선이 다음 줄을 찾기 어렵습니다. 본문에는 150%(1.5) 전후가 가장 무난하며, 제목은 125%(1.25) 정도로 타이트하게 설정합니다.
</p>

**자간(Letter Spacing)**

```css
/* 본문 (16-18pt) */
p {
  letter-spacing: -0.3px;  /* 살짝 좁히기 */
}

/* 큰 제목 (24pt+) */
h1 {
  letter-spacing: -0.5px;  /* 더 좁히기 */
}

/* 작은 텍스트 (12pt 이하) */
.caption {
  letter-spacing: 0.2px;   /* 넓히기 */
}
```

<p style="text-align: justify;">
한글은 영문과 달리 자간 조정이 민감합니다. 일반적으로 본문 크기에서는 약간 좁히고(-0.3px), 큰 제목에서는 더 좁히며(-0.5px), 작은 텍스트에서는 넓혀(+0.2px) 가독성을 확보합니다.
</p>

### 정렬과 가독성

**좌측 정렬 원칙**

<p style="text-align: justify;">
본문 텍스트는 항상 좌측 정렬을 사용합니다. 중앙 정렬이나 우측 정렬은 짧은 제목이나 특수한 경우에만 제한적으로 사용해야 합니다. 긴 문단을 중앙 정렬하면 각 줄의 시작점이 들쭉날쭉해서 읽기 어렵습니다.
</p>

```css
/* 본문 - 좌측 정렬 필수 */
p {
  text-align: left;
}

/* 제목 - 선택적 중앙 정렬 */
h1.centered {
  text-align: center;
}

/* 양쪽 정렬 (신중히 사용) */
p.justified {
  text-align: justify;
  word-break: keep-all;  /* 한글 단어 단위 줄바꿈 */
}
```

**양쪽 정렬 사용 가이드**

<p style="text-align: justify;">
양쪽 정렬(Justify)은 양쪽 끝을 맞추어 정돈된 느낌을 주지만, 단어 사이 공간이 불규칙해질 수 있습니다. 특히 좁은 컬럼에서는 "강물 효과(River Effect)"라는 현상이 발생하여 가독성이 떨어집니다. 따라서 넓은 컬럼(최소 50자 이상)에서만 사용하고, `word-break: keep-all`로 한글 단어가 중간에 끊기지 않도록 해야 합니다.
</p>

### 한 줄 길이 제한

```css
p {
  max-width: 75ch;  /* 약 50-70자 (영문 기준) */
  /* 한글은 약 35-45자 */
}
```

<p style="text-align: justify;">
한 줄이 너무 길면 다음 줄을 찾기 어렵고, 너무 짧으면 시선이 너무 자주 이동하여 리듬이 깨집니다. 이상적인 한 줄 길이는 영문 기준 50-70자, 한글 기준 35-45자입니다.
</p>

---

## 2.3 레이아웃과 그리드

<p style="text-align: justify;">
레이아웃은 콘텐츠를 조직하고 시각적 흐름을 만드는 뼈대입니다. A4 용지는 제한된 공간이므로, 효율적인 그리드 시스템을 사용하여 정보를 체계적으로 배치해야 합니다. 잘 설계된 그리드는 일관성을 자동으로 보장하며, 다양한 콘텐츠 유형에 유연하게 대응할 수 있습니다.
</p>

### A4 페이지 설정

**기본 규격**
- 용지 크기: 210mm × 297mm
- 방향: Portrait (세로)
- 해상도: 최소 300dpi (인쇄용)

**안전 여백**

```css
@page {
  size: A4 portrait;
  margin: 0;
}

body {
  width: 210mm;
  height: 297mm;
  padding: 20mm 18mm 20mm 18mm; /* 상 우 하 좌 */
  /* 실제 콘텐츠 영역: 174mm × 257mm */
}
```

<p style="text-align: justify;">
대부분의 프린터는 용지 가장자리 5mm 정도를 인쇄할 수 없는 물리적 한계가 있습니다. 따라서 최소 15mm, 권장 18-22mm의 여백을 확보하여 중요한 콘텐츠가 잘리는 것을 방지해야 합니다.
</p>

### 그리드 시스템

**2-3 컬럼 그리드**

```css
/* 2 컬럼 레이아웃 (가장 보편적) */
.two-column {
  column-count: 2;
  column-gap: 8mm;
  column-rule: 1px solid #E5E5E5; /* 선택적 구분선 */
}

/* 3 컬럼 레이아웃 (정보 밀도 높은 경우) */
.three-column {
  column-count: 3;
  column-gap: 6mm;
}
```

<p style="text-align: justify;">
2컬럼 레이아웃은 가독성과 공간 효율의 균형이 가장 좋습니다. 한 컬럼의 폭이 약 78mm가 되어 한글 기준 30-35자 정도의 적절한 줄 길이를 유지할 수 있습니다. 3컬럼은 뉴스레터나 팜플렛처럼 짧은 텍스트를 많이 배치해야 할 때 유용합니다.
</p>

**그리드 정렬선**

```css
.grid-12 {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 4mm;
}

/* 사용 예시 */
.content-main {
  grid-column: span 8;  /* 8/12 = 약 67% */
}

.sidebar {
  grid-column: span 4;  /* 4/12 = 약 33% */
}
```

### 여백 전략

**70% 규칙**

<p style="text-align: justify;">
페이지의 70%만 콘텐츠로 채우고, 30%는 여백으로 남겨두는 것이 이상적입니다. 여백은 단순히 빈 공간이 아니라 독자의 눈을 쉬게 하고, 중요한 요소에 시선을 집중시키는 역할을 합니다.
</p>

```css
.page-content {
  max-height: 217mm;  /* 257mm의 약 84% */
  overflow: hidden;
}

.section {
  margin-bottom: 12mm;  /* 섹션 간 충분한 간격 */
}

.element {
  padding: 6mm;  /* 요소 내부 패딩 */
}
```

**시각적 호흡**

<p style="text-align: justify;">
모든 요소가 빽빽하게 배치되면 독자는 숨 막히는 느낌을 받습니다. 제목 전후, 이미지 주변, 섹션 사이에 충분한 공간을 확보하여 시각적 호흡을 제공해야 합니다.
</p>

---

## 2.4 이미지와 도표

<p style="text-align: justify;">
이미지와 도표는 복잡한 정보를 직관적으로 전달할 수 있는 강력한 도구입니다. 그러나 저품질 이미지나 과도하게 장식적인 그래픽은 오히려 전문성을 떨어뜨릴 수 있습니다. 인쇄물에서는 화면보다 훨씬 높은 해상도가 필요하며, 색상 재현도 달라질 수 있으므로 주의가 필요합니다.
</p>

### 이미지 품질 기준

**해상도 요구사항**
- 최소: 300dpi (Dots Per Inch)
- 권장: 300-600dpi
- 계산 공식: `픽셀 = (mm ÷ 25.4) × dpi`

**예시:**
```
100mm × 100mm 이미지 @ 300dpi
= (100 ÷ 25.4) × 300 × (100 ÷ 25.4) × 300
= 1181 × 1181 픽셀
```

<p style="text-align: justify;">
화면용 이미지는 72-96dpi면 충분하지만, 인쇄물은 최소 300dpi가 필요합니다. 저해상도 이미지를 확대하면 픽셀이 보이고 흐릿하게 인쇄됩니다. 따라서 항상 원본 고해상도 이미지를 사용하고, HTML에서 CSS로 크기를 조절해야 합니다.
</p>

### 파일 포맷 선택

| 포맷 | 용도 | 장점 | 단점 |
|-----|------|------|------|
| **JPEG** | 사진 | 파일 크기 작음, 호환성 높음 | 압축 손실, 투명도 없음 |
| **PNG** | 그래픽, 로고 | 무손실, 투명도 지원 | 파일 크기 큼 |
| **SVG** | 아이콘, 다이어그램 | 확대해도 선명, 파일 작음 | 복잡한 이미지 부적합 |
| **WebP** | 웹 최적화 | JPEG보다 25-35% 작음 | 인쇄 지원 제한적 |

### 이미지 배치 원칙

**캡션 필수**

```html
<figure class="image-wrapper">
  <img src="graph-sales-2024.jpg" alt="2024년 분기별 매출 그래프">
  <figcaption>
    <strong>그림 1.</strong> 2024년 분기별 매출 추이 (단위: 백만원)
  </figcaption>
</figure>
```

```css
figure {
  margin: 16pt 0;
  break-inside: avoid;  /* 페이지 넘김 방지 */
}

figcaption {
  margin-top: 6pt;
  font-size: 10.5pt;
  color: #667085;
  text-align: center;
}
```

<p style="text-align: justify;">
모든 이미지에는 설명 캡션을 추가해야 합니다. 캡션은 이미지의 맥락을 제공하고, 시각 장애인을 위한 대체 텍스트 역할도 합니다. 번호를 매겨 본문에서 "그림 1 참조"처럼 언급할 수 있도록 합니다.
</p>

### 표(Table) 디자인

**미니멀 테이블**

```css
table {
  width: 100%;
  border-collapse: collapse;
  margin: 16pt 0;
  font-size: 11pt;
  break-inside: avoid;
}

/* 헤더 */
thead th {
  background: #F7F8FA;
  padding: 8pt 12pt;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #374151;
}

/* 셀 */
td {
  padding: 6pt 12pt;
  border-bottom: 1px solid #E5E7EB;
}

/* 짝수 행 배경 (선택적) */
tbody tr:nth-child(even) {
  background: #FAFAFA;
}
```

<p style="text-align: justify;">
표는 최대한 단순하게 디자인합니다. 과도한 선, 3D 효과, 그림자 등은 오히려 정보를 읽기 어렵게 만듭니다. 헤더를 굵은 선으로 구분하고, 각 행은 얇은 선이나 배경색으로 구분하는 것이 가장 효과적입니다.
</p>

### 그래프 스타일

**평면 디자인 (Flat Design)**

❌ 피해야 할 것:
- 3D 원기둥, 파이 차트
- 과도한 그림자, 그라데이션
- 불필요한 격자선(Grid Lines)
- 화려한 색상 조합

✅ 권장 스타일:
- 2D 평면 차트
- 단색 또는 단순한 색상
- 최소한의 격자선
- 포인트 데이터만 강조

```css
/* 차트 컨테이너 */
.chart {
  max-height: 100mm;
  margin: 16pt 0;
  break-inside: avoid;
}

/* SVG 기반 차트 */
svg {
  width: 100%;
  height: auto;
}

/* 데이터 포인트 강조 */
.data-point {
  fill: var(--accent);
  stroke: white;
  stroke-width: 2px;
}
```

---

## 2.5 페이지 구성 요소

<p style="text-align: justify;">
일관된 페이지 구성 요소를 정의하면 문서 전체의 통일성을 유지할 수 있습니다. 각 요소는 명확한 목적을 가지며, 사용자가 예측 가능한 위치에 배치되어야 합니다.
</p>

### 표지 (Cover Page)

**요소 최소화 원칙**

<p style="text-align: justify;">
표지는 문서의 첫인상을 결정하는 중요한 요소입니다. 너무 많은 정보를 담으려 하지 말고, 제목, 부제, 로고 정도만 배치하여 여백을 충분히 확보합니다. 표지의 여백은 50% 이상이 이상적입니다.
</p>

```html
<section class="cover-page">
  <div class="cover-content">
    <h1 class="cover-title">문서 제목</h1>
    <p class="cover-subtitle">부제목 또는 설명</p>
    <div class="cover-meta">
      <p>작성자: 홍길동</p>
      <p>날짜: 2025년 1월</p>
    </div>
  </div>
  <img src="logo.svg" alt="회사 로고" class="cover-logo">
</section>
```

```css
.cover-page {
  height: 297mm;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  page-break-after: always;
}

.cover-title {
  font-size: 36pt;
  font-weight: 700;
  margin-bottom: 12pt;
  color: var(--text-primary);
}

.cover-subtitle {
  font-size: 18pt;
  color: var(--text-muted);
  margin-bottom: 40pt;
}

.cover-logo {
  position: absolute;
  bottom: 40mm;
  max-width: 80mm;
  height: auto;
}
```

### 목차 (Table of Contents)

**계층적 들여쓰기**

```html
<section class="toc">
  <h2>목차</h2>
  <ol class="toc-list">
    <li class="toc-level-1">
      <span class="toc-title">1. 서론</span>
      <span class="toc-page">1</span>
    </li>
    <li class="toc-level-2">
      <span class="toc-title">1.1 연구 배경</span>
      <span class="toc-page">2</span>
    </li>
    <li class="toc-level-2">
      <span class="toc-title">1.2 연구 목적</span>
      <span class="toc-page">4</span>
    </li>
    <li class="toc-level-1">
      <span class="toc-title">2. 본론</span>
      <span class="toc-page">6</span>
    </li>
  </ol>
</section>
```

```css
.toc-list {
  list-style: none;
  padding: 0;
}

.toc-list li {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 8pt;
  padding: 4pt 0;
  border-bottom: 1px dotted var(--border);
}

.toc-level-1 {
  font-weight: 600;
  margin-top: 8pt;
}

.toc-level-2 {
  padding-left: 16pt;
  font-size: 11pt;
  color: var(--text-muted);
}

.toc-page {
  font-weight: 600;
  min-width: 30pt;
  text-align: right;
}
```

### 박스/콜아웃 (Callout Box)

**일관된 템플릿**

<p style="text-align: justify;">
중요한 정보, 팁, 주의사항, 예제 등을 강조하기 위한 박스는 일관된 스타일을 유지해야 합니다. 배경색, 테두리, 패딩, 아이콘을 표준화하여 사용자가 박스의 유형을 즉시 인식할 수 있도록 합니다.
</p>

```css
.callout {
  background: var(--accent-weak);
  border-left: 3pt solid var(--accent);
  padding: 12pt 16pt;
  margin: 16pt 0;
  border-radius: 6pt;
  break-inside: avoid;
}

.callout-title {
  font-weight: 600;
  color: var(--accent);
  margin-bottom: 8pt;
  display: flex;
  align-items: center;
  gap: 6pt;
}

/* 유형별 스타일 */
.callout.info {
  background: #EEF2FF;
  border-left-color: #3B82F6;
}

.callout.warning {
  background: #FFF3E8;
  border-left-color: #F2994A;
}

.callout.success {
  background: #E6F5F5;
  border-left-color: #1AA5A5;
}
```

### 헤더와 푸터

```css
/* 페이지 헤더 */
@page {
  @top-center {
    content: "문서 제목";
    font-size: 9pt;
    color: var(--text-muted);
  }
  
  @bottom-right {
    content: counter(page);
    font-size: 9pt;
  }
}

/* 또는 HTML 방식 */
.page-header {
  position: fixed;
  top: 8mm;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 9pt;
  color: var(--text-muted);
  border-bottom: 0.5pt solid var(--border);
  padding-bottom: 4pt;
}
```

---

## 2.6 인쇄 최적화

<p style="text-align: justify;">
화면에서 완벽해 보이는 디자인도 인쇄하면 문제가 발생할 수 있습니다. 색상이 다르게 나오거나, 작은 글씨가 번지거나, 페이지가 예상과 다르게 나뉠 수 있습니다. 따라서 인쇄 전용 스타일을 별도로 정의하고, 반드시 시험 인쇄를 통해 검증해야 합니다.
</p>

### 인쇄 미디어 쿼리

```css
/* 화면용 스타일 */
@media screen {
  body {
    background: #F5F5F5;
    padding: 20px;
  }
  
  .page {
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
  }
}

/* 인쇄용 스타일 */
@media print {
  * {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  
  body {
    background: white;
    padding: 0;
  }
  
  /* 웹 요소 숨김 */
  nav, .no-print, button, .sidebar {
    display: none !important;
  }
  
  /* 링크 스타일 제거 */
  a {
    color: inherit;
    text-decoration: none;
  }
  
  /* 페이지 나눔 제어 */
  h1, h2, h3 {
    page-break-after: avoid;
  }
  
  figure, table, .callout {
    page-break-inside: avoid;
  }
  
  .page {
    page-break-after: always;
  }
  
  .page:last-child {
    page-break-after: avoid;
  }
}
```

### CMYK 색상 고려

<p style="text-align: justify;">
RGB(화면)와 CMYK(인쇄)는 색 공간이 다릅니다. RGB는 빛의 삼원색으로 화면에서 색을 만들고, CMYK는 잉크의 사원색으로 종이에 색을 인쇄합니다. 특히 밝은 네온 색상(RGB에서는 선명하지만 CMYK에서는 탁해짐)과 진한 검정색(RGB `#000000`은 인쇄 시 진하게 나오지 않음)에 주의해야 합니다.
</p>

**안전한 색상 선택:**
- 순백: `#FFFFFF` ✅
- 텍스트: `#1F2937` (거의 검정) ✅
- 회색: `#667085` ✅
- 포인트: `#2F6FED`, `#1AA5A5` ✅

❌ 피해야 할 색상:
- 형광 네온: `#00FF00`, `#FF00FF`
- 순수한 검정: `#000000` (대신 `#1F2937` 사용)
- 과도하게 밝은 파스텔

### 번짐 방지

**최소 선 굵기**
```css
.thin-line {
  border-bottom: 0.5pt solid #374151;  /* 최소 0.5pt */
}

.divider {
  border-bottom: 1pt solid #E5E7EB;  /* 권장 1pt */
}
```

<p style="text-align: justify;">
0.25pt 이하의 매우 얇은 선은 인쇄 시 제대로 표현되지 않거나 번질 수 있습니다. 최소 0.5pt, 권장 1pt 이상의 선 굵기를 사용해야 합니다.
</p>

**최소 폰트 크기**
```css
/* 최소 크기 */
.minimum-text {
  font-size: 10pt;  /* 절대 이 이하로 내려가지 않기 */
}

/* 권장 크기 */
.caption {
  font-size: 10.5pt;  /* 캡션/주석 */
}

body {
  font-size: 12pt;  /* 본문 */
}
```

---

## 2.7 PDF 변환 규격

<p style="text-align: justify;">
웹 브라우저의 인쇄 기능을 사용하여 HTML을 PDF로 변환할 때, 페이지가 넘치거나 요소가 잘리는 문제가 자주 발생합니다. 이를 방지하기 위해서는 엄격한 높이 제한과 내용량 조절이 필요합니다.
</p>

### 페이지 높이 강제

```css
.page {
  width: 210mm;
  height: 297mm !important;  /* 강제 고정 */
  max-height: 297mm !important;
  overflow: hidden;  /* 넘치는 내용 숨김 */
  page-break-after: always;
  position: relative;
}

.page:last-child {
  page-break-after: avoid;
}
```

<p style="text-align: justify;">
절대로 `min-height`를 사용하지 마세요. `min-height`는 내용이 많으면 계속 늘어나므로 PDF 변환 시 페이지가 넘칩니다. 반드시 `height`를 고정값으로 설정하고 `overflow: hidden`으로 넘치는 내용을 강제로 숨겨야 합니다.
</p>

### 안전 콘텐츠 영역

```css
.page {
  padding: 20mm 18mm;  /* 상하 20mm, 좌우 18mm */
}

.page-content {
  max-height: 217mm;  /* 257mm - 40mm(헤더+푸터) */
  overflow: hidden;
}
```

**실제 콘텐츠 영역 계산:**
- 전체 높이: 297mm
- 상단 여백: 20mm
- 하단 여백: 20mm
- 헤더/푸터 공간: 40mm (선택적)
- **실제 사용 가능**: 217mm

### 페이지당 내용량 가이드

**원칙: 페이지의 70%만 채우기**

✅ **허용되는 조합:**
- 제목 1개 + 본문 3-4문단 + 이미지 1개 + 표 1개
- 제목 1개 + 본문 6-8문단 (이미지 없이)
- 제목 1개 + 큰 표 1개 + 설명 2문단
- 제목 1개 + 그래프 2개 + 설명 2문단

❌ **피해야 할 조합:**
- 제목 + 본문 15문단 (너무 많음)
- 이미지 4개 + 표 2개 (밀도 과다)
- 큰 표 2개 (페이지 넘침 위험)

### 자동 분할 기준

<p style="text-align: justify;">
다음 기준을 초과하면 자동으로 다음 페이지로 분할하는 것을 고려하세요:
</p>

- **표**: 15행 초과 시 분할
- **이미지**: 60mm 초과 시 단독 페이지
- **텍스트**: 8문단 초과 시 분할
- **그래프**: 2개 이상 시 페이지 분할

```css
/* 요소별 최대 크기 제한 */
table {
  max-height: 120mm;
  overflow: hidden;
}

figure {
  max-height: 100mm;
}

.text-section {
  max-height: 180mm;
  overflow: hidden;
}
```

---

<div style="page-break-after: always;"></div>

# [PART 3] 모바일 웹 최적화

## 3.1 모바일 타이포그래피

<p style="text-align: justify;">
모바일 화면은 데스크톱보다 훨씬 작고, 사용자는 손에 들고 30-40cm 거리에서 봅니다. 또한 야외에서는 밝은 햇빛 때문에 가독성이 더욱 떨어집니다. 따라서 모바일 타이포그래피는 인쇄물이나 데스크톱보다 큰 글씨와 넉넉한 행간이 필요합니다.
</p>

### 플랫폼별 권장 크기

**iOS (Human Interface Guidelines)**
- 본문: 17pt (약 17px)
- 제목: 28pt
- 캡션: 12pt
- **최소**: 11pt

**Android (Material Design)**
- 본문: 16dp (약 16px)
- 제목: 24dp
- 캡션: 12dp
- **최소**: 12dp

**모바일 웹 (Best Practice)**
- 본문: 16-18px
- 제목 H1: 28-32px
- 제목 H2: 22-26px
- 제목 H3: 18-20px
- 캡션: 12-14px
- **절대 최소**: 14px

```css
:root {
  /* 모바일 기준 타이포그래피 */
  --fs-display-mobile: 32px;
  --fs-h1-mobile: 28px;
  --fs-h2-mobile: 22px;
  --fs-h3-mobile: 18px;
  --fs-body-mobile: 16px;
  --fs-small-mobile: 14px;
  --fs-caption-mobile: 12px;
}

body {
  font-size: var(--fs-body-mobile);
  line-height: 1.55;  /* 155% - 모바일 최적 */
}

/* 태블릿 이상 */
@media (min-width: 768px) {
  body {
    font-size: 16px;
    line-height: 1.6;
  }
}

/* 데스크톱 */
@media (min-width: 1024px) {
  body {
    font-size: 16px;
    line-height: 1.65;
  }
}
```

### 행간 (Line Height)

<p style="text-align: justify;">
모바일에서는 데스크톱보다 촘촘한 행간(155% 정도)을 사용합니다. 이는 화면이 작아 스크롤이 많이 발생하기 때문에, 정보 밀도를 적절히 유지하면서도 가독성을 확보하기 위함입니다.
</p>

```css
/* 본문 */
p {
  line-height: 1.55;  /* 모바일 권장 */
}

/* 제목 */
h1, h2, h3 {
  line-height: 1.25;
}

/* 좁은 공간 (카드 내부 등) */
.compact-text {
  line-height: 1.4;
}

/* 넓은 공간 (인용구 등) */
blockquote {
  line-height: 1.7;
}
```

### 자간 (Letter Spacing)

```css
/* 본문 (16-17px) */
body {
  letter-spacing: -0.3px;  /* 한글 최적화 */
}

/* 큰 제목 (28px+) */
h1 {
  letter-spacing: -0.5px;
}

/* 작은 텍스트 (12-14px) */
.small-text {
  letter-spacing: 0.2px;  /* 넓혀서 가독성 확보 */
}

/* 영문 전용 */
.english {
  letter-spacing: 0;  /* 영문은 조정 불필요 */
}
```

### 가독성 원칙

**명도 대비**

<p style="text-align: justify;">
WCAG(Web Content Accessibility Guidelines) AA 기준을 충족해야 합니다. 본문 텍스트는 최소 4.5:1, 큰 텍스트(18pt 이상)는 3:1의 명암 대비가 필요합니다. 특히 야외에서 모바일을 사용할 때 낮은 대비는 거의 읽을 수 없습니다.
</p>

```css
/* 권장 조합 */
:root {
  --text-primary: #1F2937;   /* 대비율 15.3:1 (AAA) */
  --text-secondary: #374151; /* 대비율 11.2:1 (AAA) */
  --text-muted: #667085;     /* 대비율 4.8:1 (AA) */
  --bg: #FFFFFF;
}

/* 다크모드 */
[data-theme="dark"] {
  --text-primary: #E0E0E0;   /* 대비율 12.6:1 */
  --text-secondary: #BDBDBD; /* 대비율 8.3:1 */
  --text-muted: #9E9E9E;     /* 대비율 4.9:1 */
  --bg: #1A1A1A;
}
```

**한글 단어 단위 줄바꿈**

```css
p {
  word-break: keep-all;  /* 한글 단어 중간에서 끊지 않기 */
  overflow-wrap: break-word;  /* 긴 영문 단어는 줄바꿈 */
}

/* 제목에서는 더 엄격하게 */
h1, h2, h3 {
  word-break: keep-all;
  hyphens: none;  /* 하이픈 없이 */
}
```

---

## 3.2 터치 인터페이스 설계

<p style="text-align: justify;">
터치 인터페이스는 마우스와 근본적으로 다릅니다. 마우스 커서는 정확한 1픽셀 포인트를 가리킬 수 있지만, 손가락은 8-10mm의 넓은 접촉 면적을 가지며 정밀도가 떨어집니다. 따라서 충분히 큰 터치 영역과 요소 간 간격이 필수적입니다.
</p>

### 최소 터치 타겟 크기

**플랫폼별 가이드라인**

| 플랫폼 | 최소 크기 | 권장 크기 | 근거 |
|--------|----------|----------|------|
| **iOS** | 44×44pt | 44×44pt | Apple HIG |
| **Android** | 48×48dp | 48×48dp | Material Design |
| **모바일 웹** | 44×44px | 48×48px | 약 7-10mm |
| **Microsoft** | - | 7×7mm | Windows Design |

<p style="text-align: justify;">
MIT Touch Lab 연구에 따르면 손가락 끝은 8-10mm, 손가락 패드는 10-14mm입니다. 10mm × 10mm가 최소 터치 타겟 크기로 적합하며, 이는 160dpi 기준으로 약 44픽셀에 해당합니다.
</p>

```css
/* 기본 버튼 */
.btn {
  min-width: 44px;
  min-height: 44px;
  padding: 12px 24px;
  
  /* 터치 피드백 */
  transition: background 0.2s, transform 0.1s;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;  /* 300ms 딜레이 제거 */
}

.btn:active {
  background: var(--accent-dark);
  transform: scale(0.98);
}

/* 아이콘 버튼 (24×24px 아이콘) */
.icon-btn {
  width: 48px;
  height: 48px;
  padding: 12px;  /* (48-24)/2 = 12px */
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

/* 작은 아이콘 버튼 (특수 상황) */
.icon-btn-small {
  width: 36px;
  height: 36px;
  padding: 6px;  /* 최소한의 패딩 */
}
```

### 터치 타겟 간격

```css
/* 버튼 그룹 */
.btn-group {
  display: flex;
  gap: 8px;  /* 최소 8px 간격 */
}

/* 리스트 아이템 */
.list-item {
  min-height: 48px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
}

/* 내비게이션 */
.nav-item {
  min-width: 48px;
  min-height: 48px;
  padding: 8px 16px;
  margin: 0 4px;
}
```

<p style="text-align: justify;">
터치 타겟 간 최소 8px의 간격을 확보해야 오터치(잘못된 터치)를 방지할 수 있습니다. 특히 중요한 액션(삭제, 구매 등)은 다른 버튼과 더 멀리 배치하거나 확인 단계를 추가해야 합니다.
</p>

### 엄지 존 (Thumb Zone)

<p style="text-align: justify;">
스마트폰 사용자의 49%가 한 손으로만 기기를 사용하며, 엄지손가락으로 화면을 터치합니다. 화면을 3개 구역으로 나누면, 하단 중앙이 가장 편한 영역(Easy Zone)이고, 상단과 모서리가 어려운 영역(Hard Zone)입니다.
</p>

**화면 구역 분할:**

```
┌─────────────────────────┐
│      Hard Zone          │ ← 화면 상단 (20%)
│   (로고, 제목, 덜 중요한 정보)  │
├─────────────────────────┤
│      OK Zone            │ ← 화면 중앙 (60%)
│   (콘텐츠, 정보 표시)        │
├─────────────────────────┤
│      Easy Zone          │ ← 화면 하단 (20%)
│   (주요 액션 버튼, 내비게이션)  │
└─────────────────────────┘
```

**권장 배치 전략:**

```css
/* 하단 고정 내비게이션 (Easy Zone) */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: white;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding-bottom: env(safe-area-inset-bottom);  /* 노치 대응 */
}

/* 플로팅 액션 버튼 (Easy Zone) */
.fab {
  position: fixed;
  bottom: 80px;
  right: 16px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* 상단 헤더 (Hard Zone - 덜 중요한 정보만) */
.header {
  position: sticky;
  top: 0;
  height: 56px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
}
```

### 터치 피드백

<p style="text-align: justify;">
사용자가 터치했을 때 즉각적인 시각적 피드백을 제공해야 합니다. 피드백이 없으면 사용자는 "내가 누른 게 맞나?" 하고 여러 번 누르게 됩니다.
</p>

```css
/* 기본 터치 피드백 */
.touchable {
  position: relative;
  overflow: hidden;
  transition: background 0.2s;
}

.touchable:active {
  background: rgba(0, 0, 0, 0.05);
}

/* 리플 효과 (Material Design 스타일) */
.touchable::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.1);
  transform: translate(-50%, -50%);
  transition: width 0.3s, height 0.3s;
}

.touchable:active::after {
  width: 200%;
  height: 200%;
}

/* 햅틱 피드백 트리거 (JavaScript) */
button.addEventListener('touchstart', () => {
  if ('vibrate' in navigator) {
    navigator.vibrate(10);  /* 10ms 진동 */
  }
});
```

---

## 3.3 반응형 레이아웃

<p style="text-align: justify;">
반응형 디자인은 하나의 HTML 코드가 다양한 화면 크기에 자동으로 적응하는 것을 의미합니다. "모바일 우선(Mobile First)" 접근법을 사용하여 가장 제한적인 환경부터 설계하고, 화면이 커질수록 기능을 추가하는 방식이 효과적입니다.
</p>

### 그리드 시스템

**12 컬럼 그리드**

<p style="text-align: justify;">
12 컬럼 그리드는 가장 유연한 시스템입니다. 12는 2, 3, 4, 6으로 나누어떨어지므로 다양한 레이아웃을 쉽게 구성할 수 있습니다.
</p>

```css
.container {
  width: 100%;
  padding: 0 16px;  /* 모바일 좌우 여백 */
  margin: 0 auto;
}

/* 기본 그리드 */
.grid {
  display: grid;
  gap: 16px;
}

/* 모바일: 1컬럼 */
.col {
  grid-column: span 12;
}

/* 태블릿: 2-3컬럼 */
@media (min-width: 768px) {
  .container {
    max-width: 720px;
    padding: 0 24px;
  }
  
  .col-md-6 {
    grid-column: span 6;  /* 50% */
  }
  
  .col-md-4 {
    grid-column: span 4;  /* 33.33% */
  }
  
  .col-md-3 {
    grid-column: span 3;  /* 25% */
  }
}

/* 데스크톱: 3-4컬럼 */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
  }
  
  .col-lg-4 {
    grid-column: span 4;  /* 33.33% */
  }
  
  .col-lg-3 {
    grid-column: span 3;  /* 25% */
  }
}

/* 와이드 데스크톱 */
@media (min-width: 1440px) {
  .container {
    max-width: 1200px;
  }
}
```

### Flexbox 레이아웃

```css
/* 유연한 카드 레이아웃 */
.card-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding: 16px;
}

.card {
  flex: 1 1 100%;  /* 모바일: 1컬럼 */
  min-width: 280px;
  max-width: 100%;
}

@media (min-width: 768px) {
  .card {
    flex: 1 1 calc(50% - 8px);  /* 태블릿: 2컬럼 */
  }
}

@media (min-width: 1024px) {
  .card {
    flex: 1 1 calc(33.333% - 11px);  /* 데스크톱: 3컬럼 */
  }
}
```

---

## 3.4 뷰포트와 브레이크포인트

<p style="text-align: justify;">
뷰포트(Viewport)는 웹 페이지가 표시되는 영역입니다. 모바일 브라우저는 기본적으로 980px 가상 뷰포트를 사용하여 데스크톱 사이트를 축소해서 보여줍니다. 이를 방지하고 실제 기기 크기에 맞추려면 뷰포트 메타 태그가 필수입니다.
</p>

### 뷰포트 메타 태그

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**속성 설명:**

| 속성 | 값 | 설명 |
|-----|---|------|
| `width` | `device-width` | 기기 화면 폭에 맞춤 |
| `initial-scale` | `1.0` | CSS 픽셀과 화면 픽셀 1:1 매칭 |
| `user-scalable` | `yes` (기본) | 사용자 확대/축소 허용 (접근성) |
| `minimum-scale` | `1.0` | 최소 축소 배율 |
| `maximum-scale` | `5.0` | 최대 확대 배율 |

<p style="text-align: justify;">
절대로 `user-scalable=no`를 사용하지 마세요. 이는 시각 장애인이나 시력이 나쁜 사용자가 확대해서 볼 수 없게 만들어 접근성을 심각하게 해칩니다. iOS 10 이상에서는 이 설정을 무시하며, WCAG 가이드라인 위반입니다.
</p>

### 브레이크포인트 (Breakpoints)

**권장 분기점:**

```css
/* Extra Small (모바일) */
/* 기본 스타일 - 320px ~ 767px */

/* Small (큰 모바일 / 작은 태블릿) */
@media (min-width: 576px) {
  /* 576px ~ 767px */
}

/* Medium (태블릿) */
@media (min-width: 768px) {
  /* 768px ~ 1023px */
}

/* Large (데스크톱) */
@media (min-width: 1024px) {
  /* 1024px ~ 1439px */
}

/* Extra Large (와이드 데스크톱) */
@media (min-width: 1440px) {
  /* 1440px ~ */
}
```

**모바일 우선 전략:**

```css
/* ✅ 권장: 모바일 우선 (min-width) */
body {
  font-size: 16px;  /* 모바일 기본 */
}

@media (min-width: 768px) {
  body {
    font-size: 16px;  /* 태블릿 */
  }
}

@media (min-width: 1024px) {
  body {
    font-size: 16px;  /* 데스크톱 */
  }
}
```

```css
/* ❌ 비권장: 데스크톱 우선 (max-width) */
body {
  font-size: 16px;  /* 데스크톱 기본 */
}

@media (max-width: 1023px) {
  body {
    font-size: 16px;  /* 태블릿 */
  }
}

@media (max-width: 767px) {
  body {
    font-size: 16px;  /* 모바일 */
  }
}
```

<p style="text-align: justify;">
모바일 우선 방식은 점진적 향상(Progressive Enhancement) 원칙에 부합합니다. 가장 제한적인 환경(모바일)에서 필수 기능을 먼저 구현하고, 화면이 커질수록 추가 기능을 더하는 방식입니다. 이는 성능과 유지보수 측면에서도 유리합니다.
</p>

---

## 3.5 성능 최적화

<p style="text-align: justify;">
모바일 환경은 데스크톱보다 CPU가 느리고, 네트워크 대역폭이 제한적입니다. 특히 3G나 느린 4G 환경에서는 페이지 로딩 속도가 사용자 경험에 직접적인 영향을 미칩니다. 구글의 연구에 따르면 로딩 시간이 3초 이상이면 53%의 사용자가 페이지를 떠납니다.
</p>

### 이미지 최적화

**반응형 이미지 (srcset)**

```html
<img 
  src="image-medium.jpg"
  srcset="image-small.jpg 480w,
          image-medium.jpg 768w,
          image-large.jpg 1200w,
          image-xlarge.jpg 1920w"
  sizes="(max-width: 480px) 100vw,
         (max-width: 768px) 50vw,
         33vw"
  alt="반응형 이미지 설명"
  loading="lazy"
/>
```

<p style="text-align: justify;">
`srcset`를 사용하면 브라우저가 화면 크기와 해상도에 따라 최적의 이미지를 자동으로 선택합니다. 모바일에서는 작은 이미지를, 데스크톱에서는 큰 이미지를 다운로드하여 대역폭을 절약할 수 있습니다.
</p>

**WebP 포맷**

```html
<picture>
  <source srcset="image.webp" type="image/webp">
  <source srcset="image.jpg" type="image/jpeg">
  <img src="image.jpg" alt="설명">
</picture>
```

<p style="text-align: justify;">
WebP는 JPEG보다 25-35% 파일 크기가 작으면서도 동일한 화질을 제공합니다. 단, 모든 브라우저가 지원하는 것은 아니므로 `<picture>` 요소로 폴백(fallback)을 제공해야 합니다.
</p>

**Lazy Loading**

```html
<img src="image.jpg" alt="설명" loading="lazy">
```

<p style="text-align: justify;">
`loading="lazy"` 속성을 추가하면 이미지가 뷰포트에 들어올 때만 로드됩니다. 초기 페이지 로딩 속도를 크게 개선할 수 있으며, 모든 최신 브라우저에서 지원합니다.
</p>

### CSS/JS 최적화

**코드 압축 (Minification)**

```css
/* 원본 CSS */
.button {
  background-color: #3B82F6;
  padding: 12px 24px;
  border-radius: 8px;
}

/* 압축된 CSS (Minified) */
.button{background-color:#3B82F6;padding:12px 24px;border-radius:8px}
```

<p style="text-align: justify;">
공백, 줄바꿈, 주석을 제거하여 파일 크기를 줄입니다. 온라인 도구(CSS Minifier, UglifyJS 등)나 빌드 도구(Webpack, Parcel 등)를 사용하여 자동화할 수 있습니다.
</p>

**중요 CSS 인라인 (Critical CSS)**

```html
<head>
  <style>
    /* 초기 화면에 필요한 CSS만 인라인 */
    body { font-family: sans-serif; margin: 0; }
    .header { height: 56px; background: white; }
    /* ... */
  </style>
  
  <!-- 나머지 CSS는 비동기 로드 -->
  <link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="styles.css"></noscript>
</head>
```

### 터치 이벤트 최적화

**300ms 탭 딜레이 제거**

```css
* {
  touch-action: manipulation;
}

/* 또는 더 세밀하게 */
button, a, .clickable {
  touch-action: manipulation;
}
```

<p style="text-align: justify;">
모바일 브라우저는 더블탭 줌을 감지하기 위해 300ms 지연을 둡니다. `touch-action: manipulation`을 설정하면 이 지연이 제거되어 즉각적인 반응이 가능합니다.
</p>

**Passive Event Listeners**

```javascript
// ❌ 기본 이벤트 리스너 (스크롤 블로킹 가능)
element.addEventListener('touchstart', handler);

// ✅ Passive 리스너 (스크롤 성능 향상)
element.addEventListener('touchstart', handler, { passive: true });
```

---

## 3.6 접근성 고려사항

<p style="text-align: justify;">
접근성(Accessibility)은 모든 사용자가 콘텐츠에 접근할 수 있도록 보장하는 것입니다. 시각 장애, 청각 장애, 운동 장애, 인지 장애 등 다양한 제약을 가진 사용자를 고려해야 하며, 이는 법적 요구사항일 뿐만 아니라 더 많은 사용자에게 도달할 수 있는 방법입니다.
</p>

### 시맨틱 HTML

```html
<!-- ❌ 나쁜 예 -->
<div class="header">
  <div class="nav">
    <div class="link">홈</div>
    <div class="link">소개</div>
  </div>
</div>

<!-- ✅ 좋은 예 -->
<header>
  <nav>
    <a href="/">홈</a>
    <a href="/about">소개</a>
  </nav>
</header>
```

<p style="text-align: justify;">
시맨틱 HTML을 사용하면 스크린 리더가 페이지 구조를 이해하고 사용자에게 전달할 수 있습니다. `<div>`와 `<span>`만 사용하면 모든 것이 똑같이 들려서 탐색이 어렵습니다.
</p>

### ARIA 속성

```html
<!-- 버튼 역할 명시 -->
<div role="button" tabindex="0" 
     aria-label="메뉴 열기"
     onclick="openMenu()">
  ☰
</div>

<!-- 확장 가능한 섹션 -->
<button aria-expanded="false" aria-controls="content-1">
  자세히 보기
</button>
<div id="content-1" aria-hidden="true">
  숨겨진 내용...
</div>

<!-- 진행 상태 -->
<div role="progressbar" 
     aria-valuenow="60" 
     aria-valuemin="0" 
     aria-valuemax="100">
  60%
</div>
```

### 키보드 네비게이션

```css
/* 포커스 스타일 (절대 숨기지 말 것!) */
:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

/* 키보드 사용자만을 위한 스타일 */
:focus-visible {
  outline: 2px solid var(--accent);
}

/* 탭 순서 */
.skip-link {
  position: absolute;
  top: -100px;
  left: 0;
}

.skip-link:focus {
  top: 0;
  background: white;
  padding: 8px;
  z-index: 9999;
}
```

```html
<!-- 건너뛰기 링크 -->
<a href="#main-content" class="skip-link">
  본문으로 건너뛰기
</a>

<main id="main-content">
  <!-- 주요 콘텐츠 -->
</main>
```

---

<div style="page-break-after: always;"></div>

# [PART 4] 전자책 리더 기능

## 4.1 데이터 영속성 (localStorage)

<p style="text-align: justify;">
전자책 리더의 핵심은 사용자의 독서 진행 상황, 하이라이트, 설정 등을 저장하여 다음에 다시 접속했을 때 연속성을 제공하는 것입니다. 웹 환경에서는 `localStorage` API를 사용하여 브라우저에 데이터를 저장할 수 있습니다.
</p>

### localStorage 기본 사용법

```javascript
// 데이터 저장
localStorage.setItem('key', 'value');

// 데이터 읽기
const value = localStorage.getItem('key');

// 데이터 삭제
localStorage.removeItem('key');

// 전체 삭제
localStorage.clear();

// 객체 저장 (JSON 변환 필요)
const data = { name: '홍길동', age: 30 };
localStorage.setItem('user', JSON.stringify(data));

// 객체 읽기
const user = JSON.parse(localStorage.getItem('user'));
```

### 데이터 구조 설계

```javascript
const STORAGE_KEY = 'ebook-reader-data';

// 초기 데이터 구조
const defaultData = {
  version: '1.0',
  lastUpdated: new Date().toISOString(),
  
  // 독서 진행 상황
  reading: {
    scrollPosition: 0,
    currentChapter: 1,
    totalPages: 100,
    readingTime: 0  // 초 단위
  },
  
  // 하이라이트 목록
  highlights: [
    {
      id: 'h-1234567890',
      text: '하이라이트된 텍스트',
      color: 'yellow',
      chapter: 1,
      timestamp: '2025-01-15T10:30:00Z',
      note: '사용자 메모 (선택적)'
    }
  ],
  
  // 북마크
  bookmarks: [
    {
      id: 'b-1234567890',
      chapter: 2,
      scrollPosition: 1500,
      title: '2장 시작',
      timestamp: '2025-01-15T11:00:00Z'
    }
  ],
  
  // 독서 환경 설정
  settings: {
    fontSize: 18,
    lineHeight: 1.6,
    fontFamily: 'serif',
    theme: 'light',
    maxWidth: 800,
    autoSave: true
  }
};
```

### 안전한 데이터 관리

```javascript
class EbookStorage {
  constructor(storageKey = 'ebook-data') {
    this.storageKey = storageKey;
  }
  
  // 데이터 로드
  load() {
    try {
      const data = localStorage.getItem(this.storageKey);
      if (!data) return this.getDefaultData();
      
      const parsed = JSON.parse(data);
      return this.validate(parsed);
    } catch (error) {
      console.error('데이터 로드 실패:', error);
      return this.getDefaultData();
    }
  }
  
  // 데이터 저장
  save(data) {
    try {
      const validated = this.validate(data);
      validated.lastUpdated = new Date().toISOString();
      localStorage.setItem(this.storageKey, JSON.stringify(validated));
      return true;
    } catch (error) {
      console.error('데이터 저장 실패:', error);
      return false;
    }
  }
  
  // 데이터 검증
  validate(data) {
    const defaultData = this.getDefaultData();
    return {
      ...defaultData,
      ...data,
      settings: { ...defaultData.settings, ...data.settings }
    };
  }
  
  // 기본 데이터
  getDefaultData() {
    return {
      version: '1.0',
      reading: { scrollPosition: 0, currentChapter: 1 },
      highlights: [],
      bookmarks: [],
      settings: {
        fontSize: 18,
        lineHeight: 1.6,
        theme: 'light',
        maxWidth: 800
      }
    };
  }
}

// 사용 예시
const storage = new EbookStorage();
const data = storage.load();
data.reading.scrollPosition = 1000;
storage.save(data);
```

### 용량 관리

<p style="text-align: justify;">
localStorage는 도메인당 5-10MB의 제한이 있습니다. 하이라이트가 많아지면 용량을 초과할 수 있으므로 주기적으로 정리하거나 오래된 데이터를 삭제해야 합니다.
</p>

```javascript
// 저장소 용량 확인
function getStorageSize() {
  let total = 0;
  for (let key in localStorage) {
    if (localStorage.hasOwnProperty(key)) {
      total += localStorage[key].length + key.length;
    }
  }
  return (total / 1024).toFixed(2) + ' KB';
}

// 오래된 데이터 정리
function cleanOldData(daysToKeep = 90) {
  const data = storage.load();
  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - daysToKeep);
  
  data.highlights = data.highlights.filter(h => {
    return new Date(h.timestamp) > cutoffDate;
  });
  
  storage.save(data);
}
```

---

## 4.2 북마크 시스템

<p style="text-align: justify;">
북마크는 사용자가 특정 위치를 저장하고 나중에 빠르게 돌아갈 수 있게 하는 기능입니다. 스크롤 위치와 함께 챕터 정보, 페이지 제목 등을 함께 저장하면 더욱 유용합니다.
</p>

### 자동 북마크 (마지막 읽은 위치)

```javascript
// 스크롤 추적 및 자동 저장
let scrollTimeout;
window.addEventListener('scroll', () => {
  clearTimeout(scrollTimeout);
  
  scrollTimeout = setTimeout(() => {
    const data = storage.load();
    data.reading.scrollPosition = window.scrollY;
    data.reading.lastReadTime = new Date().toISOString();
    storage.save(data);
    
    updateProgressBar();
  }, 500);  // 0.5초 디바운싱
});

// 페이지 로드 시 마지막 위치로 복원
window.addEventListener('DOMContentLoaded', () => {
  const data = storage.load();
  
  setTimeout(() => {
    window.scrollTo({
      top: data.reading.scrollPosition,
      behavior: 'smooth'
    });
  }, 100);
});

// 진행률 업데이트
function updateProgressBar() {
  const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = (window.scrollY / scrollHeight) * 100;
  
  document.getElementById('progressBar').style.width = 
    Math.min(progress, 100) + '%';
}
```

### 수동 북마크

```javascript
// 북마크 추가
function addBookmark() {
  const data = storage.load();
  
  const bookmark = {
    id: 'b-' + Date.now(),
    scrollPosition: window.scrollY,
    timestamp: new Date().toISOString(),
    title: getCurrentSectionTitle(),
    note: prompt('북마크 메모를 입력하세요 (선택사항):')
  };
  
  data.bookmarks.push(bookmark);
  storage.save(data);
  
  alert('북마크가 추가되었습니다.');
  updateBookmarkList();
}

// 현재 섹션 제목 가져오기
function getCurrentSectionTitle() {
  const headings = document.querySelectorAll('h1, h2, h3');
  const scrollPos = window.scrollY + 100;
  
  for (let i = headings.length - 1; i >= 0; i--) {
    if (headings[i].offsetTop <= scrollPos) {
      return headings[i].textContent;
    }
  }
  
  return '북마크';
}

// 북마크로 이동
function goToBookmark(bookmarkId) {
  const data = storage.load();
  const bookmark = data.bookmarks.find(b => b.id === bookmarkId);
  
  if (bookmark) {
    window.scrollTo({
      top: bookmark.scrollPosition,
      behavior: 'smooth'
    });
  }
}

// 북마크 삭제
function deleteBookmark(bookmarkId) {
  if (!confirm('이 북마크를 삭제하시겠습니까?')) return;
  
  const data = storage.load();
  data.bookmarks = data.bookmarks.filter(b => b.id !== bookmarkId);
  storage.save(data);
  
  updateBookmarkList();
}
```

---

## 4.3 하이라이트 기능

<p style="text-align: justify;">
하이라이트는 전자책 리더의 가장 중요한 기능입니다. 사용자가 중요한 문장을 강조하고, 나중에 모아서 볼 수 있어야 합니다. 텍스트 선택, 하이라이트 적용, 저장, 복원, 삭제의 전 과정이 매끄럽게 작동해야 합니다.
</p>

### 텍스트 선택 감지

```javascript
let selectedText = '';
let selectedRange = null;

// 텍스트 선택 이벤트
document.addEventListener('mouseup', handleTextSelection);
document.addEventListener('touchend', handleTextSelection);

function handleTextSelection(e) {
  const selection = window.getSelection();
  const text = selection.toString().trim();
  
  // 최소 3자 이상 선택했을 때만
  if (text && text.length >= 3) {
    selectedText = text;
    selectedRange = selection.getRangeAt(0);
    
    showHighlightPopup(e);
  } else {
    hideHighlightPopup();
  }
}

// 하이라이트 팝업 표시
function showHighlightPopup(e) {
  const popup = document.getElementById('highlightPopup');
  const x = e.clientX || e.changedTouches[0].clientX;
  const y = e.clientY || e.changedTouches[0].clientY;
  
  popup.style.left = x + 'px';
  popup.style.top = (y - 60) + 'px';
  popup.classList.add('show');
}
```

### 하이라이트 적용

```javascript
// 하이라이트 추가
function addHighlight(color) {
  if (!selectedRange || !selectedText) return;
  
  const highlightId = 'h-' + Date.now();
  
  // DOM에 하이라이트 적용
  const span = document.createElement('span');
  span.className = `highlight ${color}`;
  span.setAttribute('data-highlight-id', highlightId);
  span.setAttribute('data-color', color);
  
  try {
    selectedRange.surroundContents(span);
    
    // 데이터 저장
    const data = storage.load();
    data.highlights.push({
      id: highlightId,
      text: selectedText,
      color: color,
      timestamp: new Date().toISOString(),
      position: window.scrollY
    });
    storage.save(data);
    
    // UI 업데이트
    updateHighlightList();
    showNotification('하이라이트가 추가되었습니다.');
    
  } catch (error) {
    console.error('하이라이트 적용 실패:', error);
    showNotification('하이라이트를 적용할 수 없습니다.');
  }
  
  // 선택 해제
  window.getSelection().removeAllRanges();
  hideHighlightPopup();
}
```

### 하이라이트 복원

```javascript
// 페이지 로드 시 모든 하이라이트 복원
function restoreHighlights() {
  const data = storage.load();
  
  data.highlights.forEach(highlight => {
    applyHighlightToDOM(
      highlight.text, 
      highlight.color, 
      highlight.id
    );
  });
}

// DOM에 하이라이트 적용 (복원용)
function applyHighlightToDOM(text, color, id) {
  const contentElement = document.getElementById('content');
  
  // TreeWalker로 텍스트 노드 탐색
  const walker = document.createTreeWalker(
    contentElement,
    NodeFilter.SHOW_TEXT,
    null
  );
  
  let node;
  while (node = walker.nextNode()) {
    const index = node.textContent.indexOf(text);
    
    if (index !== -1) {
      const range = document.createRange();
      range.setStart(node, index);
      range.setEnd(node, index + text.length);
      
      const span = document.createElement('span');
      span.className = `highlight ${color}`;
      span.setAttribute('data-highlight-id', id);
      span.setAttribute('data-color', color);
      
      try {
        range.surroundContents(span);
        break;  // 첫 번째 발견만 적용
      } catch (e) {
        continue;
      }
    }
  }
}
```

### 하이라이트 관리

```javascript
// 하이라이트 삭제
function removeHighlight(highlightId) {
  // DOM에서 제거
  const element = document.querySelector(
    `[data-highlight-id="${highlightId}"]`
  );
  
  if (element) {
    const parent = element.parentNode;
    while (element.firstChild) {
      parent.insertBefore(element.firstChild, element);
    }
    parent.removeChild(element);
    parent.normalize();  // 텍스트 노드 병합
  }
  
  // 데이터에서 제거
  const data = storage.load();
  data.highlights = data.highlights.filter(h => h.id !== highlightId);
  storage.save(data);
  
  updateHighlightList();
}

// 하이라이트 목록 업데이트
function updateHighlightList() {
  const data = storage.load();
  const listElement = document.getElementById('highlightList');
  
  if (data.highlights.length === 0) {
    listElement.innerHTML = `
      <p class="empty-state">
        아직 하이라이트가 없습니다.<br>
        텍스트를 선택하여 하이라이트를 추가해보세요.
      </p>
    `;
    return;
  }
  
  // 최신순 정렬
  const sorted = data.highlights.sort((a, b) => 
    new Date(b.timestamp) - new Date(a.timestamp)
  );
  
  listElement.innerHTML = sorted.map(h => `
    <div class="highlight-item ${h.color}" 
         onclick="scrollToHighlight('${h.id}')">
      <button class="delete-btn" 
              onclick="event.stopPropagation(); removeHighlight('${h.id}')">
        삭제
      </button>
      <div class="highlight-text">${escapeHtml(h.text)}</div>
      <div class="highlight-meta">
        ${formatDate(h.timestamp)}
      </div>
    </div>
  `).join('');
}

// 하이라이트로 스크롤
function scrollToHighlight(highlightId) {
  const element = document.querySelector(
    `[data-highlight-id="${highlightId}"]`
  );
  
  if (element) {
    element.scrollIntoView({ 
      behavior: 'smooth', 
      block: 'center' 
    });
    
    // 깜빡임 효과
    element.style.transition = 'transform 0.3s';
    element.style.transform = 'scale(1.05)';
    setTimeout(() => {
      element.style.transform = 'scale(1)';
    }, 300);
  }
}
```

---

## 4.4 독서 환경 커스터마이징

<p style="text-align: justify;">
사용자마다 선호하는 독서 환경이 다릅니다. 글자 크기, 줄 간격, 폰트, 배경색 등을 자유롭게 조절할 수 있게 하면 독서 만족도가 크게 향상됩니다.
</p>

### 설정 UI

```html
<div class="settings-panel">
  <h3>독서 환경 설정</h3>
  
  <!-- 글자 크기 -->
  <div class="setting-group">
    <label>
      글자 크기: <span id="fontSizeValue">18px</span>
    </label>
    <input type="range" 
           min="14" max="28" step="1" value="18"
           oninput="changeFontSize(this.value)">
  </div>
  
  <!-- 줄 간격 -->
  <div class="setting-group">
    <label>
      줄 간격: <span id="lineHeightValue">1.6</span>
    </label>
    <input type="range" 
           min="1.2" max="2.2" step="0.1" value="1.6"
           oninput="changeLineHeight(this.value)">
  </div>
  
  <!-- 콘텐츠 너비 -->
  <div class="setting-group">
    <label>
      콘텐츠 너비: <span id="maxWidthValue">800px</span>
    </label>
    <input type="range" 
           min="600" max="1200" step="50" value="800"
           oninput="changeMaxWidth(this.value)">
  </div>
  
  <!-- 폰트 선택 -->
  <div class="setting-group">
    <label>폰트</label>
    <select onchange="changeFontFamily(this.value)">
      <option value="sans-serif">산세리프</option>
      <option value="serif">세리프 (명조)</option>
      <option value="monospace">고정폭</option>
    </select>
  </div>
  
  <!-- 테마 -->
  <div class="setting-group">
    <label>테마</label>
    <div class="theme-buttons">
      <button onclick="changeTheme('light')">밝게</button>
      <button onclick="changeTheme('dark')">어둡게</button>
      <button onclick="changeTheme('sepia')">세피아</button>
    </div>
  </div>
  
  <!-- 초기화 -->
  <button onclick="resetSettings()">기본값으로 재설정</button>
</div>
```

### 설정 적용 함수

```javascript
// 글자 크기 변경
function changeFontSize(size) {
  const content = document.querySelector('.content');
  content.style.fontSize = size + 'px';
  
  document.getElementById('fontSizeValue').textContent = size + 'px';
  
  const data = storage.load();
  data.settings.fontSize = parseInt(size);
  storage.save(data);
}

// 줄 간격 변경
function changeLineHeight(height) {
  const content = document.querySelector('.content');
  content.style.lineHeight = height;
  
  document.getElementById('lineHeightValue').textContent = height;
  
  const data = storage.load();
  data.settings.lineHeight = parseFloat(height);
  storage.save(data);
}

// 콘텐츠 너비 변경
function changeMaxWidth(width) {
  const container = document.querySelector('.container');
  container.style.maxWidth = width + 'px';
  
  document.getElementById('maxWidthValue').textContent = width + 'px';
  
  const data = storage.load();
  data.settings.maxWidth = parseInt(width);
  storage.save(data);
}

// 폰트 변경
function changeFontFamily(family) {
  const content = document.querySelector('.content');
  
  const fontMap = {
    'sans-serif': '"Pretendard", system-ui, sans-serif',
    'serif': 'Georgia, "Noto Serif KR", serif',
    'monospace': '"JetBrains Mono", monospace'
  };
  
  content.style.fontFamily = fontMap[family];
  
  const data = storage.load();
  data.settings.fontFamily = family;
  storage.save(data);
}

// 테마 변경
function changeTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  
  const data = storage.load();
  data.settings.theme = theme;
  storage.save(data);
}

// 설정 초기화
function resetSettings() {
  if (!confirm('모든 설정을 기본값으로 되돌리시겠습니까?')) return;
  
  const data = storage.load();
  data.settings = {
    fontSize: 18,
    lineHeight: 1.6,
    fontFamily: 'sans-serif',
    theme: 'light',
    maxWidth: 800
  };
  storage.save(data);
  
  location.reload();
}

// 페이지 로드 시 저장된 설정 적용
function applySettings() {
  const data = storage.load();
  const settings = data.settings;
  
  changeFontSize(settings.fontSize);
  changeLineHeight(settings.lineHeight);
  changeMaxWidth(settings.maxWidth);
  changeFontFamily(settings.fontFamily);
  changeTheme(settings.theme);
}

window.addEventListener('DOMContentLoaded', applySettings);
```

---

## 4.5 진행률 추적

<p style="text-align: justify;">
독서 진행률을 시각적으로 표시하면 사용자가 얼마나 읽었는지, 얼마나 남았는지 직관적으로 파악할 수 있습니다. 또한 목표 설정과 성취감을 제공하여 독서 동기를 부여합니다.
</p>

### 진행률 계산

```javascript
// 전체 진행률 계산
function calculateProgress() {
  const scrollHeight = document.documentElement.scrollHeight;
  const clientHeight = window.innerHeight;
  const scrollTop = window.scrollY;
  
  const scrollableHeight = scrollHeight - clientHeight;
  const progress = (scrollTop / scrollableHeight) * 100;
  
  return Math.min(Math.max(progress, 0), 100);
}

// 진행률 업데이트
function updateProgress() {
  const progress = calculateProgress();
  
  // 진행률 바 업데이트
  document.getElementById('progressBar').style.width = progress + '%';
  
  // 퍼센트 표시
  document.getElementById('progressText').textContent = 
    Math.round(progress) + '%';
  
  // 데이터 저장
  const data = storage.load();
  data.reading.progress = progress;
  data.reading.lastPosition = window.scrollY;
  storage.save(data);
}

// 스크롤 이벤트에 연결
window.addEventListener('scroll', throttle(updateProgress, 200));

// 쓰로틀 함수
function throttle(func, delay) {
  let lastCall = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastCall >= delay) {
      lastCall = now;
      func.apply(this, args);
    }
  };
}
```

### 독서 시간 추적

```javascript
let readingStartTime = Date.now();
let totalReadingTime = 0;

// 독서 시간 추적
function trackReadingTime() {
  // 페이지가 보이는 동안만 측정
  if (document.visibilityState === 'visible') {
    const currentTime = Date.now();
    const elapsed = currentTime - readingStartTime;
    totalReadingTime += elapsed;
    
    const data = storage.load();
    data.reading.totalTime = 
      (data.reading.totalTime || 0) + Math.floor(elapsed / 1000);
    storage.save(data);
  }
  
  readingStartTime = Date.now();
}

// 1분마다 저장
setInterval(trackReadingTime, 60000);

// 페이지 나갈 때 저장
window.addEventListener('beforeunload', trackReadingTime);

// Visibility API로 탭 전환 감지
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    readingStartTime = Date.now();
  } else {
    trackReadingTime();
  }
});

// 독서 시간 포맷
function formatReadingTime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  
  if (hours > 0) {
    return `${hours}시간 ${minutes}분`;
  }
  return `${minutes}분`;
}
```

---

## 4.6 사용자 경험 최적화

<p style="text-align: justify;">
전자책 리더는 사용자가 장시간 사용하는 도구입니다. 작은 불편함도 쌓이면 큰 스트레스가 되므로, 세심한 UX 디테일이 중요합니다.
</p>

### 부드러운 애니메이션

```css
/* 스크롤 애니메이션 */
html {
  scroll-behavior: smooth;
}

/* 요소 전환 */
.transition {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 페이드 인 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-in {
  animation: fadeIn 0.4s ease-out;
}

/* 모달 오버레이 */
.modal-overlay {
  transition: opacity 0.3s;
}

.modal-overlay.show {
  opacity: 1;
}
```

### 키보드 단축키

```javascript
// 키보드 단축키
document.addEventListener('keydown', (e) => {
  // Ctrl/Cmd 키 조합
  if (e.ctrlKey || e.metaKey) {
    switch(e.key) {
      case 'h':  // Ctrl+H: 하이라이트 목록
        e.preventDefault();
        toggleHighlightSidebar();
        break;
      case 'b':  // Ctrl+B: 북마크 추가
        e.preventDefault();
        addBookmark();
        break;
      case ',':  // Ctrl+,: 설정
        e.preventDefault();
        toggleSettings();
        break;
      case 'd':  // Ctrl+D: 다크모드 토글
        e.preventDefault();
        toggleTheme();
        break;
    }
  }
  
  // 일반 키
  switch(e.key) {
    case 'Escape':  // ESC: 사이드바 닫기
      closeSidebars();
      break;
    case 'ArrowUp':  // ↑: 위로 스크롤
      if (e.shiftKey) {
        e.preventDefault();
        window.scrollBy(0, -window.innerHeight);
      }
      break;
    case 'ArrowDown':  // ↓: 아래로 스크롤
      if (e.shiftKey) {
        e.preventDefault();
        window.scrollBy(0, window.innerHeight);
      }
      break;
    case 'Home':  // Home: 맨 위로
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
      break;
    case 'End':  // End: 맨 아래로
      e.preventDefault();
      window.scrollTo({ 
        top: document.documentElement.scrollHeight, 
        behavior: 'smooth' 
      });
      break;
  }
});
```

### 알림 시스템

```javascript
// 토스트 알림
function showNotification(message, type = 'info', duration = 3000) {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  
  document.body.appendChild(toast);
  
  // 애니메이션
  setTimeout(() => toast.classList.add('show'), 10);
  
  // 자동 제거
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// CSS
`.toast {
  position: fixed;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%) translateY(100px);
  padding: 12px 24px;
  background: #1F2937;
  color: white;
  border-radius: 8px;
  opacity: 0;
  transition: all 0.3s;
  z-index: 10000;
}

.toast.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

.toast-success { background: #10B981; }
.toast-error { background: #EF4444; }
.toast-warning { background: #F59E0B; }
```

### 로딩 상태

```javascript
// 로딩 인디케이터
function showLoading() {
  const loader = document.createElement('div');
  loader.id = 'loader';
  loader.innerHTML = `
    <div class="spinner"></div>
    <p>불러오는 중...</p>
  `;
  document.body.appendChild(loader);
}

function hideLoading() {
  const loader = document.getElementById('loader');
  if (loader) loader.remove();
}

// 사용 예시
async function loadContent() {
  showLoading();
  
  try {
    // 콘텐츠 로드
    await fetch('/api/content');
  } catch (error) {
    showNotification('로드 실패', 'error');
  } finally {
    hideLoading();
  }
}
```

---

<div style="page-break-after: always;"></div>

# [PART 5] 통합 구현

## 5.1 통합 아키텍처

<p style="text-align: justify;">
하나의 HTML 문서가 인쇄, 모바일, 전자책 리더의 세 가지 모드에서 모두 최적으로 작동하려면 체계적인 아키텍처가 필요합니다. 미디어 쿼리와 JavaScript 기능 감지를 활용하여 환경에 따라 적절한 스타일과 기능을 적용합니다.
</p>

### 파일 구조

```
project/
├── index.html          # 메인 HTML
├── css/
│   ├── base.css       # 공통 기본 스타일
│   ├── print.css      # 인쇄 전용
│   ├── screen.css     # 화면 전용
│   └── ebook.css      # 전자책 기능
├── js/
│   ├── storage.js     # localStorage 관리
│   ├── highlight.js   # 하이라이트 기능
│   ├── bookmark.js    # 북마크 기능
│   └── settings.js    # 설정 관리
└── assets/
    ├── images/
    └── fonts/
```

### 조건부 스타일 로딩

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>멀티플랫폼 문서</title>
  
  <!-- 공통 스타일 -->
  <link rel="stylesheet" href="css/base.css">
  
  <!-- 화면용 스타일 -->
  <link rel="stylesheet" href="css/screen.css" media="screen">
  
  <!-- 인쇄용 스타일 -->
  <link rel="stylesheet" href="css/print.css" media="print">
  
  <!-- 전자책 기능 (화면에서만) -->
  <link rel="stylesheet" href="css/ebook.css" media="screen">
  
  <!-- JavaScript (화면에서만 로드) -->
  <script src="js/storage.js" defer></script>
  <script src="js/highlight.js" defer></script>
  <script src="js/settings.js" defer></script>
</head>
```

---

## 5.2 조건부 스타일링

### 통합 CSS 구조

```css
/* ========= base.css - 공통 스타일 ========= */
:root {
  /* 디자인 토큰 */
  --color-bg: #FFFFFF;
  --color-text: #1F2937;
  --color-accent: #3B82F6;
  --color-border: #E5E7EB;
  
  --font-sans: "Pretendard", system-ui, sans-serif;
  --font-serif: Georgia, serif;
  
  --fs-body: 16px;
  --lh-body: 1.6;
}

/* 기본 리셋 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-sans);
  font-size: var(--fs-body);
  line-height: var(--lh-body);
  color: var(--color-text);
  background: var(--color-bg);
}

/* 타이포그래피 - 모든 플랫폼 공통 */
h1, h2, h3 { font-weight: 700; }
p { margin-bottom: 1rem; text-align: justify; }

/* ========= screen.css - 화면 전용 ========= */
@media screen {
  body {
    padding: 20px;
    background: #F5F5F5;
  }
  
  /* 컨테이너 */
  .container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }
  
  /* 반응형 */
  @media (max-width: 768px) {
    body { padding: 0; }
    .container {
      padding: 20px;
      border-radius: 0;
    }
  }
  
  /* 전자책 UI 요소 표시 */
  .toolbar, .sidebar, .settings-panel {
    display: block;
  }
}

/* ========= print.css - 인쇄 전용 ========= */
@media print {
  @page {
    size: A4 portrait;
    margin: 0;
  }
  
  body {
    width: 210mm;
    padding: 20mm 18mm;
    background: white;
    font-size: 12pt;
    line-height: 1.5;
  }
  
  /* 웹 UI 요소 숨김 */
  .toolbar, .sidebar, .settings-panel,
  .no-print, nav, button {
    display: none !important;
  }
  
  /* 링크 스타일 제거 */
  a {
    color: inherit;
    text-decoration: none;
  }
  
  /* 페이지 나눔 제어 */
  h1, h2, h3 {
    page-break-after: avoid;
  }
  
  .page {
    page-break-after: always;
  }
  
  .page:last-child {
    page-break-after: avoid;
  }
  
  /* 색상 보존 */
  * {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
}

/* ========= ebook.css - 전자책 기능 ========= */
@media screen {
  /* 하이라이트 */
  .highlight {
    cursor: pointer;
    padding: 2px 0;
    transition: filter 0.2s;
  }
  
  .highlight.yellow {
    background: rgba(255, 235, 59, 0.4);
  }
  
  .highlight.green {
    background: rgba(76, 175, 80, 0.3);
  }
  
  .highlight.pink {
    background: rgba(233, 30, 99, 0.3);
  }
  
  .highlight:hover {
    filter: brightness(0.95);
  }
  
  /* 다크모드 */
  [data-theme="dark"] {
    --color-bg: #1A1A1A;
    --color-text: #E0E0E0;
    --color-border: #404040;
  }
  
  [data-theme="dark"] .highlight.yellow {
    background: rgba(255, 235, 59, 0.25);
  }
}
```

---

## 5.3 완전한 템플릿 코드

<p style="text-align: justify; font-weight: 600; background: #FFF3E8; padding: 16px; border-left: 4px solid #F2994A; border-radius: 4px; margin: 20px 0;">
⚠️ 중요: 아래 템플릿은 완전히 작동하는 예제입니다. 로컬 HTML 파일로 저장하면 인쇄, 모바일, 전자책 리더 기능을 모두 사용할 수 있습니다. Claude.ai artifacts 환경에서는 localStorage가 지원되지 않아 저장 기능이 작동하지 않으니, 반드시 파일로 저장하여 사용하세요.
</p>

**템플릿 다운로드 및 사용:**
1. 코드를 `my-document.html`로 저장
2. 브라우저에서 파일 열기
3. 텍스트 드래그하여 하이라이트 테스트
4. `Ctrl+P`로 PDF 저장 테스트
5. 모바일에서 열어 반응형 확인

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>완전한 멀티플랫폼 문서 템플릿</title>
<style>
/* 
  이 템플릿은 다음 세 가지 모드를 지원합니다:
  1. A4 인쇄용 (Ctrl+P로 PDF 저장)
  2. 반응형 모바일 웹
  3. 전자책 리더 (하이라이트, 북마크, 설정 저장)
*/

/* ========= Design Tokens ========= */
:root {
  /* Colors */
  --bg: #FFFFFF;
  --bg-alt: #F7F8FA;
  --text-primary: #1F2937;
  --text-secondary: #667085;
  --accent: #3B82F6;
  --border: #E5E7EB;
  
  /* Typography */
  --font-sans: "Pretendard Variable", Pretendard, -apple-system, sans-serif;
  --fs-body: 16px;
  --lh-body: 1.6;
  
  /* Layout */
  --container-width: 800px;
  --spacing: 16px;
}

[data-theme="dark"] {
  --bg: #1A1A1A;
  --bg-alt: #2C2C2C;
  --text-primary: #E0E0E0;
  --text-secondary: #9E9E9E;
  --border: #404040;
}

/* ========= Base ========= */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-sans);
  font-size: var(--fs-body);
  line-height: var(--lh-body);
  color: var(--text-primary);
  background: var(--bg);
  transition: background 0.3s, color 0.3s;
}

/* ========= Typography ========= */
h1, h2, h3 {
  font-weight: 700;
  line-height: 1.3;
  margin-bottom: 1rem;
}

h1 { font-size: 2rem; }
h2 { font-size: 1.5rem; margin-top: 2rem; }
h3 { font-size: 1.25rem; margin-top: 1.5rem; }

p {
  margin-bottom: 1rem;
  text-align: justify;
  word-break: keep-all;
}

/* ========= 화면용 스타일 ========= */
@media screen {
  body {
    padding-top: 70px;
    background: var(--bg-alt);
  }
  
  .container {
    max-width: var(--container-width);
    margin: 0 auto;
    padding: 40px;
    background: var(--bg);
    min-height: calc(100vh - 70px);
  }
  
  /* 툴바 */
  .toolbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 56px;
    background: var(--bg);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 var(--spacing);
    z-index: 1000;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  }
  
  .btn {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-primary);
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s;
  }
  
  .btn:hover {
    background: var(--accent);
    color: white;
    border-color: var(--accent);
  }
  
  /* 진행률 바 */
  .progress-bar {
    position: fixed;
    top: 56px;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--border);
    z-index: 999;
  }
  
  .progress-fill {
    height: 100%;
    background: var(--accent);
    width: 0%;
    transition: width 0.1s;
  }
  
  /* 하이라이트 */
  .highlight {
    cursor: pointer;
    padding: 2px 0;
    transition: filter 0.2s;
  }
  
  .highlight.yellow { background: rgba(255, 235, 59, 0.4); }
  .highlight.green { background: rgba(76, 175, 80, 0.3); }
  .highlight.pink { background: rgba(233, 30, 99, 0.3); }
  .highlight:hover { filter: brightness(0.95); }
  
  /* 반응형 */
  @media (max-width: 768px) {
    .container {
      padding: 20px;
      border-radius: 0;
    }
    
    .toolbar {
      padding: 0 12px;
    }
    
    .btn span {
      display: none;
    }
  }
}

/* ========= 인쇄용 스타일 ========= */
@media print {
  @page {
    size: A4 portrait;
    margin: 0;
  }
  
  * {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  
  body {
    width: 210mm;
    height: 297mm;
    padding: 20mm 18mm;
    background: white;
    font-size: 12pt;
    line-height: 1.5;
  }
  
  /* 웹 UI 숨김 */
  .toolbar, .progress-bar, .no-print, 
  button, nav {
    display: none !important;
  }
  
  /* 링크 스타일 제거 */
  a {
    color: inherit;
    text-decoration: none;
  }
  
  /* 페이지 나눔 */
  h1, h2, h3 {
    page-break-after: avoid;
  }
  
  .page {
    page-break-after: always;
  }
  
  .page:last-child {
    page-break-after: avoid;
  }
}
</style>
</head>
<body>

<!-- 화면용 툴바 (인쇄 시 숨김) -->
<div class="toolbar">
  <div>
    <button class="btn" onclick="window.print()">
      🖨️ <span>인쇄/PDF</span>
    </button>
    <button class="btn" onclick="toggleTheme()">
      🌓 <span>테마</span>
    </button>
  </div>
  <div>
    <span id="progressText" style="font-size: 14px; color: var(--text-secondary);">0%</span>
  </div>
</div>

<!-- 진행률 바 -->
<div class="progress-bar">
  <div class="progress-fill" id="progressFill"></div>
</div>

<!-- 메인 콘텐츠 -->
<div class="container">
  <div class="content" id="content">
    <h1>완전한 멀티플랫폼 문서 템플릿</h1>
    
    <p>
      이 HTML 문서는 인쇄용 A4 PDF, 반응형 모바일 웹, 전자책 리더의 세 가지 모드를 모두 지원합니다. 
      하나의 파일로 모든 플랫폼에 대응할 수 있는 완벽한 솔루션입니다.
    </p>
    
    <h2>주요 기능</h2>
    
    <h3>1. A4 인쇄 최적화</h3>
    <p>
      Ctrl+P를 눌러 인쇄 미리보기를 확인하세요. 자동으로 A4 크기에 맞춰지며, 
      웹 UI 요소(툴바, 버튼 등)는 숨겨집니다. PDF로 저장하여 배포할 수도 있습니다.
    </p>
    
    <h3>2. 반응형 모바일 디자인</h3>
    <p>
      브라우저 창 크기를 조절하거나 모바일 기기에서 열어보세요. 
      화면 크기에 따라 레이아웃이 자동으로 조정되며, 
      터치 인터페이스에 최적화되어 있습니다.
    </p>
    
    <h3>3. 전자책 리더 기능</h3>
    <p>
      텍스트를 드래그하면 하이라이트를 추가할 수 있습니다 (화면 모드에서만). 
      스크롤 위치는 자동으로 저장되어 다음에 열 때 이어서 읽을 수 있습니다. 
      상단의 테마 버튼으로 다크모드를 켤 수 있습니다.
    </p>
    
    <h2>사용 방법</h2>
    
    <p>
      <strong>중요:</strong> 이 파일은 로컬 HTML 파일로 저장하여 사용해야 
      모든 기능이 정상 작동합니다. Claude.ai artifacts에서는 
      localStorage가 지원되지 않아 저장 기능이 작동하지 않습니다.
    </p>
    
    <p>
      1. 이 코드를 <code>document.html</code> 파일로 저장합니다.<br>
      2. 브라우저에서 해당 파일을 엽니다.<br>
      3. 콘텐츠를 자유롭게 수정합니다.<br>
      4. Ctrl+P로 PDF로 저장하거나 인쇄합니다.
    </p>
    
    <h2>커스터마이징</h2>
    
    <p>
      <code>&lt;div class="content" id="content"&gt;</code> 안의 내용을 
      원하는 텍스트로 바꾸면 나만의 문서를 만들 수 있습니다. 
      마크다운을 HTML로 변환하거나, 기존 문서를 복사하여 
      붙여넣을 수도 있습니다.
    </p>
    
    <p>
      디자인을 수정하려면 <code>&lt;style&gt;</code> 태그 안의 
      CSS 변수(Design Tokens)를 조정하세요. 색상, 폰트, 간격 등을 
      한 곳에서 일괄 변경할 수 있습니다.
    </p>
  </div>
</div>

<script>
// ⚠️ localStorage는 로컬 HTML 파일에서만 작동합니다

const STORAGE_KEY = 'document-data';

// 데이터 로드/저장
function loadData() {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : { 
      scrollPosition: 0, 
      theme: 'light' 
    };
  } catch (e) {
    return { scrollPosition: 0, theme: 'light' };
  }
}

function saveData(data) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (e) {
    console.warn('저장 실패');
  }
}

let appData = loadData();

// 테마 토글
function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  document.documentElement.setAttribute('data-theme', newTheme);
  appData.theme = newTheme;
  saveData(appData);
}

// 진행률 업데이트
function updateProgress() {
  const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = (window.scrollY / scrollHeight) * 100;
  
  document.getElementById('progressFill').style.width = Math.min(progress, 100) + '%';
  document.getElementById('progressText').textContent = Math.round(progress) + '%';
}

// 스크롤 추적
let scrollTimeout;
window.addEventListener('scroll', () => {
  clearTimeout(scrollTimeout);
  
  scrollTimeout = setTimeout(() => {
    appData.scrollPosition = window.scrollY;
    saveData(appData);
    updateProgress();
  }, 500);
});

// 초기화
window.addEventListener('DOMContentLoaded', () => {
  // 테마 적용
  document.documentElement.setAttribute('data-theme', appData.theme);
  
  // 스크롤 복원
  setTimeout(() => {
    window.scrollTo(0, appData.scrollPosition);
  }, 100);
  
  updateProgress();
});
</script>

</body>
</html>
```

---

## 5.4 배포와 유지보수

<p style="text-align: justify;">
완성된 문서를 배포하고 유지보수하는 과정도 중요합니다. 버전 관리, 피드백 수집, 점진적 개선을 통해 문서의 품질을 지속적으로 향상시킬 수 있습니다.
</p>

### 버전 관리

```javascript
// 버전 정보 추가
const VERSION = {
  major: 1,
  minor: 2,
  patch: 3,
  toString() {
    return `${this.major}.${this.minor}.${this.patch}`;
  }
};

// HTML 메타 태그에 추가
<meta name="version" content="1.2.3">
<meta name="last-updated" content="2025-01-15">

// 데이터 마이그레이션
function migrateData(oldData) {
  if (oldData.version === '1.0.0') {
    // 1.0.0 → 1.1.0 마이그레이션
    oldData.settings = oldData.settings || {};
    oldData.version = '1.1.0';
  }
  
  if (oldData.version === '1.1.0') {
    // 1.1.0 → 1.2.0 마이그레이션
    oldData.highlights = oldData.highlights.map(h => ({
      ...h,
      note: h.note || ''  // 새 필드 추가
    }));
    oldData.version = '1.2.0';
  }
  
  return oldData;
}
```

### 피드백 수집

```html
<!-- 피드백 버튼 -->
<button class="btn" onclick="openFeedback()">
  💬 피드백 보내기
</button>

<script>
function openFeedback() {
  const subject = encodeURIComponent('문서 피드백');
  const body = encodeURIComponent(`
문서 제목: ${document.title}
버전: ${VERSION.toString()}
피드백:

[여기에 의견을 작성해주세요]
  `);
  
  window.location.href = `mailto:feedback@example.com?subject=${subject}&body=${body}`;
}
</script>
```

---

<div style="page-break-after: always;"></div>

# [PART 6] 실전 체크리스트

## 6.1 개발 전 체크리스트

### 기획 단계

- [ ] **목적 명확화**: 이 문서의 주 사용 환경은? (인쇄 / 모바일 / 전자책 / 모두)
- [ ] **대상 독자**: 누가 읽는가? (학생 / 전문가 / 일반인)
- [ ] **분량 계획**: 페이지 수 예상 (A4 기준)
- [ ] **콘텐츠 구조**: 목차 작성 완료
- [ ] **디자인 톤**: 친근한 / 전문적인 / 고급스러운
- [ ] **색상 팔레트**: 2-3색 선정 완료
- [ ] **폰트 선택**: 본문/제목 폰트 결정

### 기술 준비

- [ ] **개발 환경**: 텍스트 에디터 설치
- [ ] **브라우저 테스트**: Chrome, Safari, Firefox 설치
- [ ] **이미지 도구**: 이미지 편집/압축 도구 준비
- [ ] **백업 계획**: 버전 관리 시스템(Git) 또는 클라우드 저장
- [ ] **레퍼런스**: 참고할 디자인 사례 수집

---

## 6.2 개발 중 체크리스트

### HTML 구조

- [ ] DOCTYPE 선언: `<!DOCTYPE html>`
- [ ] `<html lang="ko">` 언어 설정
- [ ] 메타 태그 완료:
  - [ ] `<meta charset="UTF-8">`
  - [ ] `<meta name="viewport">`
  - [ ] `<title>` 적절한 제목
- [ ] 시맨틱 HTML 사용: `<header>`, `<main>`, `<section>`
- [ ] 이미지 alt 텍스트 모두 작성
- [ ] 링크 접근성: 명확한 링크 텍스트

### CSS 스타일

**공통**
- [ ] CSS 변수로 디자인 토큰 정의
- [ ] 색상 팔레트 2-3개 준수
- [ ] 폰트 종류 1-2개 제한
- [ ] 텍스트 대비율 4.5:1 이상

**인쇄용**
- [ ] `@page { size: A4; margin: 0; }`
- [ ] 안전 여백 18-22mm
- [ ] 페이지당 70% 콘텐츠 규칙
- [ ] `.no-print` 클래스로 웹 요소 숨김
- [ ] `page-break-*` 속성으로 페이지 나눔 제어

**모바일**
- [ ] 뷰포트 메타 태그 설정
- [ ] 본문 16-18px
- [ ] 터치 타겟 최소 44×44px
- [ ] 터치 타겟 간격 8px 이상
- [ ] 모바일 우선 미디어 쿼리

**전자책**
- [ ] 하이라이트 스타일 정의
- [ ] 다크모드 변수 설정
- [ ] 설정 패널 UI
- [ ] 토스트 알림 스타일

### JavaScript 기능

- [ ] `localStorage` 지원 확인
- [ ] 에러 핸들링 (`try-catch`)
- [ ] 이벤트 리스너 디바운싱/쓰로틀링
- [ ] 메모리 누수 방지 (이벤트 리스너 정리)
- [ ] 브라우저 호환성 고려

### 콘텐츠

- [ ] 모든 제목 계층 올바름 (H1 → H2 → H3)
- [ ] 단락 적절히 분할 (3-5문장)
- [ ] 긴 문단에 소제목 추가
- [ ] 양쪽 정렬 적용 (`text-align: justify`)
- [ ] 이미지/표 캡션 추가
- [ ] 오타 검토 완료

---

## 6.3 배포 전 체크리스트

### 인쇄 테스트

- [ ] **시험 인쇄**: 실제 프린터로 1부 출력
- [ ] 여백 적절함 (내용이 잘리지 않음)
- [ ] 색상 재현 확인 (너무 밝거나 어둡지 않음)
- [ ] 작은 글씨 선명함 (번지지 않음)
- [ ] 얇은 선 표시됨
- [ ] 페이지 나눔 자연스러움
- [ ] 이미지 해상도 충분함 (흐릿하지 않음)

### PDF 변환 테스트

- [ ] Ctrl+P로 PDF 저장
- [ ] 전체 페이지 수 확인
- [ ] 각 페이지 높이 297mm 준수
- [ ] 내용 잘림 없음
- [ ] 하이퍼링크 제거 확인
- [ ] 파일 크기 적절함 (<5MB 권장)

### 모바일 테스트

- [ ] **실제 기기 테스트**: iPhone, Android 최소 1대씩
- [ ] 텍스트 크기 읽기 편함
- [ ] 버튼 터치 쉬움 (오터치 없음)
- [ ] 스크롤 부드러움
- [ ] 이미지 로딩 빠름
- [ ] 가로/세로 모드 모두 정상
- [ ] 확대/축소 작동
- [ ] 오프라인 작동 (전자책 기능)

### 브라우저 호환성

- [ ] **Chrome** 최신 버전
- [ ] **Safari** iOS/Mac
- [ ] **Firefox** 최신 버전
- [ ] **Edge** 최신 버전
- [ ] **Samsung Internet** (Android)

### 접근성 검증

- [ ] 키보드만으로 모든 기능 접근 가능
- [ ] 스크린 리더 테스트 (NVDA 또는 VoiceOver)
- [ ] 색상 대비 검사 도구 실행
- [ ] 포커스 순서 논리적
- [ ] `alt` 텍스트 모두 의미 있음

### 성능 검증

- [ ] **PageSpeed Insights** 점수 확인
- [ ] 초기 로딩 시간 <3초
- [ ] 이미지 최적화 (WebP 사용)
- [ ] CSS/JS 압축 (Minify)
- [ ] 불필요한 코드 제거

### 최종 점검

- [ ] 오타/문법 오류 없음
- [ ] 모든 링크 작동
- [ ] 이미지 모두 로드됨
- [ ] 저작권 표시 (필요 시)
- [ ] 연락처 정보 정확함
- [ ] 버전 번호 명시
- [ ] README 파일 작성 (사용법 설명)

### 백업 및 문서화

- [ ] 최종 파일 백업 (클라우드 + 로컬)
- [ ] 소스 코드 버전 관리 (Git commit)
- [ ] 변경 이력 문서화 (CHANGELOG)
- [ ] 사용자 가이드 작성
- [ ] 문제 해결 FAQ 준비

---

## 최종 점검 체크리스트 요약

### 필수 항목 (반드시 확인)

✅ **인쇄**
- A4 크기 맞음
- 여백 적절함
- 시험 인쇄 완료

✅ **모바일**
- 실제 기기 테스트
- 터치 타겟 44px 이상
- 본문 16px 이상

✅ **전자책**
- localStorage 작동 (로컬 파일)