# lion 스킬

Claude Code 와 Codex 에 설치해 쓰는 한국어 작업 스킬 28개입니다.

평소 하던 말로 요청하면 맞는 스킬이 열립니다. "버튼 하나 추가해줘" 라고 하면 앱 개발 스킬이, "저장 누르면 에러 떠" 라고 하면 디버깅 스킬이 열립니다. 새 대화마다 `lion-mode` 가 먼저 열려 요청을 보고 스킬을 고르므로 스킬 이름을 외워 두실 필요는 없습니다.

Windows 11 의 Claude Code 2.1 과 Codex CLI 0.157 에서 설치하고 시험했습니다. macOS 와 Linux 에서는 아직 시험하지 못했습니다.

## 설치

Claude Code

```
claude plugin marketplace add lionsd-sms/lion-skills
claude plugin install lion@lion-skills
```

설치한 뒤 `~/.claude/settings.json`(Windows 는 `%USERPROFILE%\.claude\settings.json`)에 읽기 허용 한 줄을 넣고 Claude Code 를 다시 시작해 주세요. 이 줄이 없으면 `lion-mode` 가 스킬 파일을 읽을 때마다 허락 창이 뜹니다. 플러그인이 이 설정을 대신 넣을 수는 없어서 직접 넣으셔야 합니다. 파일이 없으면 아래 내용 그대로 만들면 됩니다.

```json
{
  "permissions": {
    "allow": ["Read(~/.claude/plugins/cache/lion-skills/**)"]
  }
}
```

Codex

```
codex plugin marketplace add lionsd-sms/lion-skills
codex plugin add lion@lion-skills
```

설치한 뒤 새 대화에서 `/hooks` 를 열어 lion 훅을 신뢰해 주세요. 신뢰하기 전에는 훅이 실행되지 않아 `lion-mode` 가 먼저 열리지 않습니다.

설치가 잘 됐는지는 새 대화에 `PDF 두 개 합쳐줘` 를 입력해 보면 알 수 있습니다. `lion-mode` 다음에 `lion-pdf` 의 `SKILL.md` 를 읽으면 제대로 설치된 것입니다.

## 동작 방식

```
"저장 누르면 에러 떠"
  ▼
lion-mode         새 대화 훅이 먼저 엽니다. 표에서 "오류·실패·느림·튕김의 원인 찾기" 줄을 고릅니다
  ▼
lion-debugging    에러가 나는 장면을 먼저 다시 만들고 원인 자리에서 고칩니다. 코드를 고치므로 lion-dev-checks 도 엽니다
  ▼
lion-dev-checks   고친 뒤 같은 장면을 다시 돌려 에러가 사라진 것을 보고 나서야 됐다고 말합니다
  ▼
끝 보고: 한 일, 확인한 것, 확인하지 못한 것
```

코드를 고치는 스킬은 `lion-dev-checks` 를, PDF·한글·엑셀처럼 파일을 만드는 스킬은 `lion-file-work` 를 함께 엽니다. `lion-file-work` 는 원본을 그대로 두고 사본에서 고친 다음 결과 파일을 다시 열어 손대지 않은 곳이 그대로인지 확인합니다.

앱을 새로 만드는 것처럼 큰 일은 세 스킬이 차례로 맡습니다.

```
"사내 비품 대여 앱 하나 만들고 싶어"
  ▼
lion-planning        누가 쓰고 어디까지 만들지 정합니다 → 정하지 못한 것만 객관식으로 여쭙니다 → 작업 단위로 나눕니다
  ▼
lion-orchestration   일의 크기를 봅니다 → executor 서브 에이전트들에 나눠 맡깁니다 → 결과를 합칩니다
  ▼
lion-review          reviewer 가 근거를 달아 지적합니다 → 한 번 고칩니다 → 남은 것은 사용자께 여쭙니다
```

나눠 맡길 때 쓰는 역할 에이전트는 다섯입니다. `scoper` 가 기획, `planner` 가 계획, `executor` 가 실행, `reviewer` 가 검수를 맡습니다. 긴 로그나 외부 문서를 읽고 요약하는 일은 `researcher` 가 합니다.

어느 스킬이 열리든 마지막 보고는 한 일, 확인한 것, 확인하지 못한 것으로 나눠 드립니다. "이것도 할까?" 하고 물으시면 들일 수고에 비해 얻을 것이 적을 때는 하지 않는 편이 낫다고 말씀드립니다.

## 스킬 28개

```
███████ 7  일하는 방식
███████ 7  개발
███████ 7  문서와 파일
████    4  디자인과 영상
███     3  분석과 조사
```

일하는 방식

| 스킬 | 하는 일 | 이런 말에 열립니다 |
|---|---|---|
| `lion-mode` | 요청을 보고 맞는 스킬을 고릅니다. 자동으로 열리는 스킬은 이것 하나입니다 | 할 일이 있는 요청 전부 |
| `lion-planning` | 무엇을 만들지, 무엇을 여쭤볼지, 어떤 순서로 할지 정합니다 | "재고 관리 앱 하나 만들고 싶어", "뭐부터 해야 해?" |
| `lion-orchestration` | 큰 일을 서브 에이전트에 나눠 맡기고 결과를 합칩니다 | "병렬로 돌려", "로그 너무 길어, 서브한테 맡겨서 원인만 뽑아와" |
| `lion-review` | 끝난 작업을 한 번 검수하고 고친 뒤에 한 번 더 봅니다 | "검토해줘", "다 만든 거 요구한 대로 됐는지 확인해줘" |
| `lion-project-rules` | 프로젝트 규칙 문서(AGENTS.md)를 만들고 정한 것을 적어 다음 세션에 넘깁니다 | "새 프로젝트인데 규칙부터 잡아줘", "어디까지 했지? 이어서 해줘" |
| `lion-skill-update` | 스킬을 만들고 고친 뒤 제대로 열리는지 시험합니다 | "이걸 스킬로 만들어줘", "스킬이 자꾸 안 불려, 설명 고쳐줘" |
| `lion-bro` | 이해하기 어려웠던 답을 결론 한 문장과 예로 다시 설명합니다 | "브로", "뭔 소리야?" |

개발

| 스킬 | 하는 일 | 이런 말에 열립니다 |
|---|---|---|
| `lion-app-development` | 앱 기능, 화면, API, 설정을 만들고 고칩니다 | "버튼 하나 추가해줘", "엑셀 내보내기 기능 넣어줘" |
| `lion-tauri` | Tauri 2 앱의 권한, 자동 업데이트, 설치판 설정을 맞춥니다 | "updater 붙여서 자동 업데이트 되게 해줘", "tauri 2.11 로 올려줘" |
| `lion-debugging` | 오류나 느려진 원인을 찾아 고칩니다. 지난 로그도 읽습니다 | "로그인하면 흰 화면만 나와", "어젯밤에 왜 멈췄는지 로그 좀 봐줘" |
| `lion-testing` | 테스트 케이스를 짜서 돌리고 버그인지 가립니다. QA 보고서도 씁니다 | "테스트 케이스 짜줘", "이거 버그야 아니야?" |
| `lion-app-verification` | 앱을 띄워 직접 눌러 보는 확인 절차를 문서로 남깁니다 | "이 앱 확인하는 절차 만들어줘" |
| `lion-release` | 커밋, PR, 빌드, 배포를 그 프로젝트가 해 온 방식대로 합니다 | "푸시하고 PR 올려줘", "설치 파일 만들어줘" |
| `lion-dev-checks` | 패키지를 더하거나 고치기 전후 속도를 잴 때 지킬 것을 챙깁니다 | "axios 패키지 추가해줘", "고치기 전이랑 후 속도 재서 비교해줘" |

문서와 파일

| 스킬 | 하는 일 | 이런 말에 열립니다 |
|---|---|---|
| `lion-document` | Word, Markdown, EPUB 으로 보고서와 회의록을 쓰고 고칩니다 | "월간 업무 보고서 워드로 써줘", "이 마크다운 epub으로 바꿔줘" |
| `lion-writing-polish` | AI 티를 빼고 문장을 다듬습니다. 고치기 전에 AI 티가 몇 %인지 먼저 잽니다 | "AI 티 빼줘", "이 카톡 답장 너무 AI 같아" |
| `lion-spreadsheet` | 엑셀과 CSV 표를 만들고 고치고 계산합니다 | "이 CSV 합계 내줘", "수식 오류 고쳐줘" |
| `lion-ppt` | PPT 와 HTML 발표 자료를 만듭니다 | "발표 자료 만들어줘", "PPT 10장으로 줄여줘" |
| `lion-pdf` | PDF 를 합치고 나누고 고칩니다. 스캔본 글자도 읽습니다 | "PDF 합쳐줘", "스캔본 글자 인식해줘" |
| `lion-hangul` | 한글(HWP, HWPX) 문서를 만들고 고칩니다 | "hwp를 pdf로 바꿔줘", "한글 양식에 내용 채워줘" |
| `lion-file-work` | 파일 형식을 바꾸거나 여러 파일을 한꺼번에 고칩니다. 원본은 두고 사본에서 작업합니다 | "이 폴더 문서 30개 한꺼번에 이름 바꿔줘", "원본은 두고 사본에서 고쳐줘" |

디자인과 영상

| 스킬 | 하는 일 | 이런 말에 열립니다 |
|---|---|---|
| `lion-production` | 영상이나 발표를 만들기 전에 요청서를 채우고 시안을 비교합니다 | "발표자료 들어가기 전에 시안 3개 먼저 비교하자" |
| `lion-video` | 쇼츠, 설명 영상, 모션그래픽을 만들고 자막을 넣습니다 | "이 대본으로 30초 쇼츠 만들어줘", "영상 7초쯤 문구 바꾸고 다시 렌더해줘" |
| `lion-visual-design` | 로고, 배너, 아이콘, 포스터를 만듭니다 | "로고 만들어줘", "인스타 이미지 3종 뽑아줘" |
| `lion-visual-explain` | 개념 하나를 그림 한 장짜리 HTML 페이지로 풀어 드립니다 | "토큰이 뭔지 5살도 알게 설명해줘", "eli5 DNS" |

분석과 조사

| 스킬 | 하는 일 | 이런 말에 열립니다 |
|---|---|---|
| `lion-security` | 권한, 인증, 코드에 박힌 키, 업로드 검사를 점검합니다 | "이거 해킹당할 구멍 없어?", "API 키가 코드에 박혀 있는지 봐줘" |
| `lion-ai-evaluation` | AI 기능의 결과를 시험 입력으로 재고 모델끼리 비교합니다 | "요약 기능에 어느 모델 쓸지 비교해줘", "AI가 뽑은 값 그대로 저장해도 돼?" |
| `lion-research` | 공식 문서 같은 1차 출처로 조사하고 출처마다 날짜를 답니다 | "출처 달아서 알려줘", "기사마다 숫자가 다른데 어느 게 맞아?" |

## 따로 설치하는 것

- Codex 역할 에이전트: Codex 플러그인에는 에이전트를 넣을 수 없어서 `extras/codex-agents/` 의 toml 5개를 `~/.codex/agents/` 에 직접 복사해 주셔야 합니다. 플러그인을 설치하면 `~/.codex/plugins/cache/lion-skills/lion/<판 번호>/extras/codex-agents/` 에도 같이 받아집니다.
- 전역 규칙: `extras/global-rules/` 에 만든 사람이 평소 쓰는 `CLAUDE.md` 와 `AGENTS.md` 가 있습니다. 함께 쓰시려면 `~/.claude/CLAUDE.md` 나 `~/.codex/AGENTS.md` 끝에 붙여 주세요. 붙이지 않아도 스킬은 동작합니다.

## 업데이트와 삭제

```
claude plugin marketplace update lion-skills
claude plugin update lion@lion-skills

codex plugin marketplace upgrade lion-skills
codex plugin add lion@lion-skills
```

```
claude plugin uninstall lion@lion-skills
claude plugin marketplace remove lion-skills

codex plugin remove lion@lion-skills
codex plugin marketplace remove lion-skills
```

삭제할 때 settings.json 에 넣은 줄, 복사한 에이전트, 붙인 전역 규칙은 직접 지워 주세요. 판마다 바뀐 내용은 [CHANGELOG.md](CHANGELOG.md) 에 적어 둡니다.

## 폴더

```
lion-skills/
├─ .claude-plugin/        Claude 설정 (plugin.json, marketplace.json)
├─ .codex-plugin/         Codex 설정 (plugin.json)
├─ .agents/plugins/       Codex 마켓플레이스 목록
├─ skills/                스킬 28개. 두 AI 가 같은 폴더를 읽습니다
│  └─ lion-pdf/
│     ├─ SKILL.md         열리면 먼저 읽는 본문 (60줄 안팎)
│     ├─ references/      필요할 때만 읽는 참고 파일
│     └─ agents/openai.yaml
├─ agents/                Claude 역할 에이전트 5개
├─ hooks/                 새 대화 훅 (hooks.json 은 Claude, codex-hooks.json 은 Codex)
└─ extras/                Codex 역할 에이전트, 전역 규칙
```

`lion-mode` 를 뺀 나머지 스킬은 자동으로 열리지 않게 꺼 두었습니다. Claude 는 `SKILL.md` 머리의 `disable-model-invocation: true` 로, Codex 는 `agents/openai.yaml` 의 `allow_implicit_invocation: false` 로 끕니다.

## 출처와 이용조건

MIT 라이선스입니다([LICENSE](LICENSE)). 아래 저장소들의 생각을 빌려 우리말로 다시 쓴 지침이 있습니다. 원래 저작권 문구는 그 지침이 든 스킬의 `references/LICENSES.md` 에 그대로 두었습니다. 좋은 자료를 공개해 주신 분들께 감사드립니다.

- [agent-skills](https://github.com/addyosmani/agent-skills), Addy Osmani, MIT
- [pstack](https://github.com/cursor/plugins/tree/main/pstack), Lauren Tan, MIT
- [skills](https://github.com/mattpocock/skills), Matt Pocock, MIT
- [ponytail](https://github.com/DietrichGebert/ponytail), DietrichGebert, MIT
- [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), Next Level Builder, MIT (안의 UI 스타일 자료 일부는 Apache License 2.0)
- [im-not-ai](https://github.com/epoko77-ai/im-not-ai), epoko77-ai, MIT
- [yoonmoon](https://github.com/amondnet/yoonmoon), Minsu Lee, MIT
