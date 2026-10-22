# 판 가르기·배치·명령 모양·판 올리기

## 1. Tauri 2 인지 가르기

- 이 스킬의 규칙 대상은 Tauri 2 다. `src-tauri/tauri.conf.json` 이 있고 `tauri` 의존성 주 판이 2 이거나(`src-tauri/Cargo.toml`, `tauri = { workspace = true }` 로 물려받으면 워크스페이스 뿌리 `Cargo.toml` 의 `[workspace.dependencies]`) 설정 맨 위에 `app` 키가 있는 프로젝트, 또는 Tauri 2 앱을 새로 만들 때다.
- `tauri.conf.json` 만으로는 Tauri 1과 가르지 못한다. 정확한 판은 워크스페이스 뿌리까지 올라가 찾은 `Cargo.lock`, 첫 빌드 전이면 `Cargo.toml` 의 판 범위로 가른다.
- Tauri 1(`tauri` 1.x, 설정의 `tauri.allowlist`)은 규칙 대상이 아니다.

## 2. 먼저 볼 자리

- 판: `Cargo.lock` 의 `tauri`·`tauri-build`·`tauri-utils`·`tauri-plugin-*`, `node_modules/@tauri-apps/` 아래 cli·api·plugin 패키지의 `package.json`. Tauri 2 설정은 맨 위에 `app`·`build`·`bundle`·`plugins` 를 둔다.
- `src-tauri/tauri.conf.json`(Windows 전용 `tauri.windows.conf.json` 이 있으면 함께): `identifier`, `app.security`, `app.windows`, `bundle`(targets·publisher·resources·externalBin·createUpdaterArtifacts·windows), `plugins`.
- `src-tauri/capabilities/` 의 capability 파일: 창 label(`windows`)·`webviews`·`platforms`·`remote`·permissions.
- `src-tauri/permissions/`(앱 자체 permission)와 `build.rs` 의 `tauri_build::build()` 또는 `try_build(Attributes)`(`AppManifest`, `WindowsAttributes`).
- `src-tauri/gen/schemas/acl-manifests.json`: 설치된 판의 core·플러그인 권한 묶음이 실제로 여는 명령. 키에 `__app-acl__` 가 있으면 앱 명령 ACL 이 켜져 있다.
- `generate_handler!` 에 등록한 명령, 코드로 창을 만드는 곳(`WebviewWindowBuilder::new` 의 label), 플러그인 등록 순서.
- 설치판: `bundle.windows.nsis` 의 `template`·`installerHooks`, 실행 파일 매니페스트 파일, 마지막 빌드가 실제로 쓴 값이 담긴 `src-tauri/target/release/nsis/<arch>/installer.nsi`.

## 3. 배치

- 정해진 구조가 없으면 Tauri 가 정한 layout 을 쓴다(`src-tauri/` 안의 `Cargo.toml`·`build.rs`·`tauri.conf.json`·`capabilities/`·`icons/`·`src/`). 그 안의 Rust crate 는 lib/bin 으로 나누고, 화면 쪽은 그 프레임워크의 기본 배치를 쓴다.
- capability 는 창과 기능 묶음마다 파일을 나눈다. 한 파일에 모든 창과 모든 권한을 모으지 않는다.
- `gen/schemas/` 는 빌드(`tauri-build`)가 만드는 파일이라 손으로 고치지 않는다.
- 기존 프로젝트는 capability 파일 구성, 창 label, 명령 모듈 구조를 먼저 보존한다. 권한을 좁히는 변경은 그 창의 화면 코드가 실제로 부르는 API 목록과 대조한 뒤에 한다.

## 4. 명령 모양

- 명령 함수는 얇게 둔다: 인자 검증, lib 쪽 함수 호출, 직렬화할 수 있는 결과·오류.
- 앱 명령의 오류는 앱 전체에서 `serde::Serialize` 를 구현한 오류 타입 하나(종류 값과 사람이 읽을 메시지)로 돌려주고, 화면은 그 꼴 하나로 처리한다. 명령마다 문자열과 다른 구조를 섞어 돌려주지 않는다.
- `async` 가 없는 명령은 메인 스레드에서 돈다. 파일·네트워크·외부 프로세스처럼 오래 걸리는 일은 `async` 명령으로 하고, 빌린 타입(`&str`, `State<'_, T>`)의 제약을 따른다.
- 명령 이름은 모듈이 달라도 앱 전체에서 유일해야 하고 모든 명령은 한 번의 `generate_handler!` 에 넣는다. `invoke_handler` 를 여러 번 부르면 마지막 것만 쓰인다.
- 상태가 바뀐 것을 알리는 일은 이벤트(보내고 끝나는 한 방향 메시지)로, 요청과 응답은 명령으로 나눈다.
- 앱이 시작할 때 Windows 판, WebView2 런타임 판, 설치 자리, 데이터 폴더를 실행 로그에 남긴다. 현장 PC 에서만 알 수 있는 것을 사람이 따로 확인하지 않게 하려는 것이다.

## 5. 판 올리기와 설정 키 확인

- Tauri 패키지는 함께 올리는 묶음이다: `tauri` crate 와 `@tauri-apps/api`, 플러그인의 Rust crate 와 그 JS 패키지, `@tauri-apps/cli`. 판 번호는 패키지마다 다르므로 번호를 억지로 맞추지 않는다(대조된 빌드 조합의 예: tauri 2.11.3 과 api 2.11.1, plugin-dialog crate 2.7.1 과 JS 2.7.3).
- CLI 가 판 어긋남을 찾아 멈추면 공식 문서가 그 상태를 알 수 없는 동작으로 경고하므로 `--ignore-version-mismatches` 로 넘기지 않는다.
- Tauri·rustc·Node 는 프로젝트의 지원 판과 호환 조합으로 관리한다. 알려진 취약점 검증에 `npm audit`·`cargo audit` 가 필요하면 실행하고, 도구가 없으면 미확인으로 남긴다.
- 설정 키와 기본값은 쓰는 판에서 확인한다. 누리집은 판 번호 없이 최신을 보여 주므로 쓰는 판에 없는 설정도 실려 있다(확인: tauri 2.11.x·tauri-utils 2.9.3 에는 `app.appDirectoriesOverride`·`bundle.windows.bundleVCRuntime` 이 없다).
- 최종 근거는 `Cargo.lock` 의 `tauri`·`tauri-utils` 판(첫 빌드 전이면 `src-tauri/Cargo.toml` 의 판 범위)과 cargo registry 의 그 판 소스(`tauri-utils-<판>/src/config.rs`)다. 설정 머리의 `$schema` 는 `node_modules/@tauri-apps/cli/config.schema.json` 처럼 설치된 CLI 의 것일 때만 보조로 쓴다(`https://schema.tauri.app/config/2` 는 판을 고정하지 않는다).
- 새 플러그인을 들이면 capability 의 권한을 화면 코드가 실제로 부르는 `allow-*` 로 좁힌다.
