---
version: 1
kind: <video | ppt | document | sheet | image>
name: <디자인 이름>
description: >
  <이 디자인의 인상과 반복되는 특징을 세 문장 안으로>

# 공통 칸
colors:
  canvas: "<바탕>"
  surface: "<카드·상자 속>"
  line: "<구분선>"
  ink: "<본문 글자>"
  ink-muted: "<보조 글자>"
  primary: "<주인공 색>"
  on-primary: "<주인공 색 위 글자>"
  accent: "<강조 한 곳>"
typography:
  font: <글꼴>              # 대체: <대체 글꼴>
  display: { size: <px>, weight: <굵기>, lineHeight: <배수> }
  title:   { size: <px>, weight: <굵기>, lineHeight: <배수> }
  body:    { size: <px>, weight: <굵기>, lineHeight: <배수> }
  label:   { size: <px>, weight: <굵기>, lineHeight: <배수> }   # 영상: 1080 기준 32px 아래로 쓰지 않음
  caption: { size: <px>, maxCharsPerLine: <수>, maxLines: <수> }   # 자막을 쓰는 매체만. 영상 기본: 가로 16·세로 12자, 2줄
spacing:
  unit: <px>
  sm: <px>
  md: <px>
  lg: <px>
shapes:
  rounded: { sm: <px>, md: <px>, full: 9999px }
  stroke: { line: <px>, bold: <px> }
components:
  <부품 이름>:
    fill: "{colors.<이름>}"
    typography: "{typography.<이름>}"

# 영상 칸 (영상이 아니면 지우고 그 매체 칸을 둔다. 적힌 값은 영상 기본값이고, 정한 값이 있으면 바꾼다)
format:
  aspect: "<16:9 | 9:16>"
  resolution: <1920x1080 | 1080x1920>
  fps: 30                    # 값 칸, 기본 30
  duration: <초>s
  safe-area: { action: 96px, title: 192px }                   # 1920x1080 기준, 가장자리에서 떨어질 거리
  vertical-ui: { top: 220px, bottom: 420px, right: 160px }   # 세로에서 앱 버튼·설명이 덮는 곳
motion:                      # 프레임 값은 30fps 기준
  duration: { instant: 3f, micro: 6f, short: 12f, medium: 18f, long: 30f }
  easing: { standard: "cubic-bezier(0.2, 0, 0, 1)", enter: "cubic-bezier(0, 0, 0.2, 1)", exit: "cubic-bezier(0.4, 0, 1, 1)" }   # standard: 빠르게 출발, 천천히 도착
  stagger: 4f
  max-simultaneous: 3
  hold: { min: 45f, reading: "글자 수(공백 뺌) ÷ 6 + 0.5초" }
transitions:
  default: match-move        # 같은 개체가 다음 장면 자리로 옮겨 가며 장면이 바뀜
  match-move: { duration: "{motion.duration.medium}", easing: "{motion.easing.standard}" }
  cut: { duration: 0f }      # 박자 강조, 끝 장면
camera:
  default: static
audio:
  loudness: -14 LUFS
  true-peak: -1 dBTP
  voice-over-music: 12dB
  music: { bpm: <박자> }     # 한 박 = 60 ÷ bpm × fps 프레임
  sfx: { arrive: <소리, 크기>, emphasis: <소리, 크기> }
captions:
  mode: [<burned-in>, <srt>]
  position: <자리, 안전선 안>
  min-duration: 30f
---

## Overview

<이 디자인이 지키는 핵심 규칙 한 문단. 보는 사람이 무엇을 따라가게 하는지.>

## 칸마다 하는 일과 까닭

| 값 이름 | 값 | 하는 일 | 까닭 |
|---|---|---|---|
| `colors.primary` | <값> | <쓰는 곳> | <까닭> |

칸(색, 글자, 여백, 도형, 부품, 그리고 매체 칸)마다 표를 하나씩 둔다.

## 하기와 하지 말 것

하기
- <규칙>

하지 말 것
- <규칙>

## 크기 변형

| 항목 | <기본 크기> | <다른 크기> |
|---|---|---|
| 배치 | <...> | <...> |
| 제목 크기 | <...> | <...> |

## 다루지 않는 것

- <이 디자인이 정하지 않은 영역. 예: 실사 촬영 규칙, 3D>
