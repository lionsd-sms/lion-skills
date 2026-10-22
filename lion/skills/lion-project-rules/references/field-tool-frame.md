# 현장 Windows 도구 틀

이 틀을 써 온 사용자의 프로젝트에서 「폴더 틀」 절이 `틀: 현장 Windows 도구 틀`일 때 쓴다. 이 틀의 앱을 새로 만들 때, 표준화로 옮길 때, 루트 폴더와 문서의 자리·이름·머리를 정할 때 연다. 실행 파일·판·작업 기록·커밋·화면 문구는 같은 틀의 「실행 파일·판·기록」 파일이 맡는다.

## 1. 루트

루트에는 사람이 처음 여는 문서, 누르는 실행 파일, 역할 폴더 몇 개만 둔다. 자라는 파일은 역할 폴더 안에 둔다.

```text
<앱>/
├─ README.md              # 처음 여는 문서
├─ AGENTS.md              # 프로젝트 규칙 문서 본문
├─ CLAUDE.md              # @AGENTS.md 한 줄
├─ CHANGELOG.md           # 판올림 이력(존댓말)
├─ VERSION                # 판 번호 한 줄
├─ <앱>-개발 실행.bat     # 루트에 두는 실행 파일은 이것 하나
├─ app/                   # 앱 코드 전부와 실행 파일이 부르는 스크립트
├─ docs/                  # 번호 영역 개발 문서
├─ <앱>-빌드/             # 빌드 배포 실행 파일과 확인용 빌드 결과
├─ <앱>-버전/             # 판 보관 실행 파일과 확정한 판
├─ _archive/              # 폐기·백업 보관(있을 때)
└─ _reference/            # 읽기만 하는 참고 자료(있을 때)
```

- README 순서: 목적 1~3문장 → 빠른 시작(누를 실행 파일 이름) → 역할·위치·뜻 표 → 문서 지도 링크 → 기본 확인 명령.
- CHANGELOG 맨 위에 다음 판(개발 중) 절을 둔다.
- `app/`: 앱 코드 전부. 실행 파일이 부르는 PowerShell·검사 스크립트도 이 안(예: `app/scripts/`)에 둔다. 프레임워크가 정한 모양(`app/src-tauri/` 따위)은 `app/` 안에서 그대로 쓴다. 스택의 기본 배치 그림이 말하는 프로젝트 맨 위는 `app/`이다.
- `_archive/`: 폐기·백업 묶음. 코드가 부르지 않는다. 이전 상태는 먼저 Git 기록으로 남기고, 따로 둘 묶음만 여기 두며 무엇을 왜 두는지 `_archive/README.md`에 적는다.
- `_reference/`: 업무 문서·참고 자료(pdf, xlsx, 스크린샷, 이식 전 원본). 코드·빌드에 잇지 않는다. 경계는 `_reference/README.md`에 적는다.
- 업무 자료(고객·현장 자료)와 끝난 작업의 결과물은 저장소 밖에 둔다.
- 폴더는 내용이 생길 때 만든다.
- `.gitignore`에 넣는 것: `<앱>-빌드/`의 결과 하위 폴더, `<앱>-버전/v<판>/`의 설치 파일·포터블, 앱이 쓰는 `log/`. 두 폴더의 실행 파일과 README는 추적한다.
- 실행 로그 자리: 앱 프로그램(설치했거나 포터블로 푼 .exe) 옆 `log\`. 저장소 루트의 .bat 옆에는 두지 않는다. 앱 프로그램 옆에 쓸 수 없는 설치(예: `C:\Program Files` 아래)면 `%LOCALAPPDATA%\<앱>\log\`.

## 2. 문서 자리

`docs/` 아래에는 번호 영역 폴더만 둔다. 영역 폴더는 내용이 생길 때 만든다.

| 영역 폴더 | 답하는 질문 | 주 문서 |
|---|---|---|
| `01-spec` | 무엇을 만드나 | product-spec.md |
| `02-architecture` | 어떻게 짜였나 | architecture.md |
| `03-ui` | 화면은 어떻게 동작하나 | ui.md (화면 낱말 표도 여기 한 곳) |
| `04-interfaces` | 경계의 약속은 무엇인가 | interfaces.md |
| `05-data` | 데이터는 무엇인가 | data.md |
| `06-development` | 어떻게 개발·실행하나 | development.md |
| `07-quality` | 끝났음을 어떻게 보이나 | quality.md |
| `08-security` | 무엇을 지키나 | security.md |
| `09-delivery` | 어떻게 빌드·배포하나 | delivery.md, user-manual.md |
| `10-operations` | 배포 뒤 어떻게 지켜보나 | operations.md |
| `11-decisions` | 왜 그렇게 정했나 | NNNN-제목.md |
| `12-records` | 작업 경과는 어떤가 | TASK-HISTORY.md, tasks/TASK-YYYY-MM-DD-N.md |
| `13-reference` | 찾아볼 사실은 무엇인가 | 조회용 사실 문서 |

- 이름: 영역 폴더 `NN-영문명`, 파일 영문 kebab-case, 결정 문서만 `NNNN-제목.md`. 한 영역에 문서가 늘면 같은 폴더에 kebab-case로 더한다.
- 영역 밖 문서는 루트 문서들과 문서 지도 `docs/README.md`뿐이다.
- 시험 숫자(개수, 기대값, 확인 못 한 것)는 `docs/07-quality/quality.md` 한 곳에 적고 다른 문서는 그곳을 가리킨다. 추적표가 커지면 `docs/07-quality/test-matrix.md`, 보안 진단은 `docs/08-security/security-audit.md`, 소스 인계 안내는 `docs/09-delivery/source-handoff.txt`.
- 받은 원본 자료는 `_reference/`, 조회용으로 정리한 사실은 `docs/13-reference/`.
- `docs/10-operations/operations.md`에는 화면·로그에 나오는 실패 문구마다 세 줄을 둔다: 뜻 · 먼저 볼 곳 · 현장에서 할 일.
- 이 틀에서 「정해진 결정」이 길어지면 `docs/11-decisions/`로 옮기고 규칙 문서에는 경로만 둔다. 진행 상태는 TASK 문서가 맡는다.

### 문서 머리

```text
# 제목
> **이 문서가 답하는 질문:** …
> 원본과 관련 문서: …
## 한 줄 요약
(본문)
```

기존 문서를 고칠 때 영문 상태값(`Active`·`Planned`·`N/A`·`NOT VERIFIED`)은 한글 상태값으로 바꾼다.

### 문서 지도

`docs/README.md`는 루트 README 다음에 여는 문서 지도다.

- 순서: 영역 표(# · 영역 · 상태 · 답하는 질문 · 내용 또는 「해당 없음」 까닭) → 읽는 순서 → 같은 사실의 주인 문서 표 → 규칙.
- 상태는 `문서 있음` · `작성 예정` · `해당 없음`. 「해당 없음」은 그 질문을 맡은 다른 문서를 까닭에 적는다. 13줄을 늘 다 싣는다.
- 읽는 순서: 처음 여는 사람은 루트 README → 제품 기준 → 개발 방법, 고치러 온 AI는 규칙 문서 → 문서 지도 → 해당 영역 → 최근 TASK.
