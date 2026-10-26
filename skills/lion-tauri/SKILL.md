---
name: lion-tauri
description: >-
  Tauri 2 앱(src-tauri)의 앱 명령(invoke)·IPC 권한(capability)·CSP·플러그인·자동 업데이트·설치판(NSIS, perMachine)·WebView2·관리자 권한 실행·판 올리기를 고친다. 이럴 때 쓴다: Tauri 앱의 권한이 막히거나 업데이트·설치판·오프라인 설치·관리자 권한·판 올리기를 바꿀 때. 범위 밖: Tauri 와 무관한 화면, 오류 원인, 빌드·배포.
---

# Tauri 2 앱

Tauri 2 앱의 앱 명령·권한·웹뷰 설정·플러그인·업데이트·Windows 설치판을 쓰는 판에서 확인한 사실대로 만들고 고친다.

## 함께 여는 스킬

이 스킬을 열었으면 파일을 읽거나 고치기 전에, 아래 조건에 맞는 스킬을 Skill 도구로 연다(Codex 는 그 스킬의 SKILL.md 를 읽는다). 이미 열려 있으면 건너뛴다.

- 코드를 고치거나 패키지를 더하거나 판을 올릴 때: `lion-dev-checks`
- 화면·자료·API 같은 앱 기능 자체를 만들거나, Rust·TypeScript 코드 배치와 게이트 명령이 걸릴 때: `lion-app-development`

## 바로 할 일

1. 판 가르기: 워크스페이스 뿌리까지 올라가 찾은 `Cargo.lock`(첫 빌드 전이면 `Cargo.toml` 의 판 범위)에서 `tauri` 주 판이 2 인지 본다. `tauri.conf.json` 만으로는 Tauri 1과 가르지 못한다. Tauri 1(설정의 `tauri.allowlist`)이면 이 스킬의 규칙을 쓰지 않고 그 사실을 알린다. 완료: 쓰는 `tauri`·`tauri-utils` 판을 적었다.
2. 닿는 주제의 참고 파일을 아래 표에서 골라 읽는다. 설정 키와 기본값은 1의 판에서 확인한다. 누리집은 판 번호 없이 최신을 보여 준다.
3. 고친다. 경계는 앱 명령이다: 명령 인자는 신뢰할 수 없는 입력으로 검증하고, 플러그인 권한은 `<플러그인>:default` 대신 화면이 실제로 부르는 `allow-*` 만 준다. `invoke_handler` 로 등록한 앱 명령은 앱 ACL 이 꺼져 있으면 모든 창에서 불린다.
4. 확인: 앱 전체 빌드(`tauri build`·`tauri dev`)와 프로젝트 게이트를 돌리고, 확인 파일의 「게이트 통과 뒤에 함께 읽는 것」을 실제 파일과 대조한다. 설치 방식·실행 수준·WebView2 방식·리소스·capability 를 바꿨으면 설치판을 표준 사용자 조건으로 설치·첫 실행·제거까지 해 본다. 완료: 돌린 명령과 결과, 설치 확인 여부, 작업 PC 에서 확인하지 못한 「미확인」 항목을 적었다. 필수 결과가 미확인이면 완료로 보고하지 않는다. 시험을 통과시키려고 기대값을 낮추거나, 시험을 지우거나 건너뛰거나, 검사를 끄지 않는다.

참고 파일의 `(확인: 판)` 은 그 판에서 확인한 사실이다. 프로젝트 판이 다르면 그 판의 `gen/schemas/acl-manifests.json`·소스로 다시 확인한다. `미확인:` 으로 시작하는 줄은 실제로 돌려 보지 못한 동작이므로, 그 동작에 기대는 설계는 실제 실행으로 먼저 확인한다.

## 필요할 때만 더 읽기

| 이럴 때 | 읽을 파일 |
|---|---|
| Tauri 2 인지 가르기, 먼저 볼 설정 자리, 새 프로젝트 배치, 앱 명령 함수·오류 모양, Tauri 패키지 판 올리기·설정 키 확인 | [판 가르기·배치·명령 모양·판 올리기](references/project-setup.md) |
| 앱 명령 만들기·고치기, capability·permission·앱 ACL, 경로나 실행 프로그램을 받는 명령, CSP·웹뷰 보안 설정 | [앱 명령·IPC 권한](references/ipc-permissions.md) |
| single-instance·dialog·opener 같은 플러그인, `bundle.resources` 싣기 | [플러그인과 resources](references/plugins-resources.md) |
| 자동 업데이트(공식 updater·자체 업데이트), 코드 서명, SmartScreen·스마트 앱 컨트롤 경고 | [updater 와 서명](references/updater-signing.md) |
| NSIS 설치 방식, WebView2 설치 방식·데이터 폴더, 실행 수준(관리자 권한), 설치 템플릿·게시자 | [Windows 설치판](references/windows-installer.md) |
| 빌드 게이트, 게이트 뒤 대조할 것, 설치판 설치 확인 | [확인](references/verification.md) |

일부 참고 내용의 이용조건은 [라이선스](references/LICENSES.md)에 있다.

끝 보고는 한 일 · 확인한 것 · 확인 못 한 것.
