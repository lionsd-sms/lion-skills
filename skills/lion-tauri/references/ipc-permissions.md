# 앱 명령·IPC 권한

## 1. 신뢰 경계

- 웹뷰의 코드는 IPC 로 열어 둔 것에만 닿고, 앱과 플러그인의 Rust 코드는 시스템 자원 전체에 닿는다. 그래서 앱 명령(`#[tauri::command]`)이 경계다.
- 명령 인자는 JSON 에서 역직렬화된 값이다. 명령 안에서 신뢰할 수 없는 입력으로 검증한다(경로·크기·열거값).
- capability 와 별개로 명령 구현의 scope 와 Rust 코드의 자원 접근을 검증한다.

## 2. 앱 명령의 ACL

- 플러그인과 core 명령은 capability 가 그 창에 허용할 때만 불린다. 앱이 `invoke_handler` 로 등록한 명령은 기본값으로 **모든 창과 웹뷰에서** 불린다.
- 앱 명령이 ACL 검사를 받는 때는 둘이다: 앱 ACL 이 켜졌을 때, 요청이 원격 origin 에서 왔을 때. 앱 ACL 은 `build.rs` 에서 `tauri_build::AppManifest::new().commands(&[...])` 를 주거나 `src-tauri/permissions/` 에 permission 파일을 하나라도 두면 켜진다.
- 켜지면 capability 가 허용하지 않은 앱 명령은 전부 거부된다. `permissions/` 에 플러그인 권한을 묶는 set 하나만 두어도 켜지므로 그 파일을 더하는 변경은 모든 앱 명령의 호출 여부를 바꾼다. 켤 때는 `generate_handler!` 의 명령을 빠짐없이 `commands` 에 적고, 창마다 capability 에 자동 생성 권한을 준 뒤, 각 창의 실제 호출을 개발 빌드에서 확인한다.
- 자동 생성 권한의 이름은 명령 이름의 밑줄을 하이픈으로 바꾼 `allow-<명령>` 이다(`set_app_root` 면 `allow-set-app-root`). capability 에 밑줄 그대로 적으면 권한 식별자 형식 오류(영숫자와 하이픈만 받는다)로 빌드가 멈춘다. `AppManifest::permissions_path_pattern` 을 주면 기본 `permissions/` 폴더는 읽지 않는다.
- 앱 ACL 을 켜지 않고 창마다 막아야 하면 명령이 받는 `WebviewWindow` 의 label 을 명령 안에서 확인한다.

## 3. capability 와 권한 묶음

- capability 는 창 label 로 묶인다(창 제목이 아니다). 한 창이 여러 capability 에 들면 권한이 합쳐진다. 창을 만드는 권한은 권한이 높은 창에만 준다.
- 코드로 만드는 보조 창(표시·식별용 창)은 그 창에 필요한 capability 를 따로 두거나 두지 않는다. 앱 ACL 이 꺼져 있으면 그 창에서도 앱 명령이 모두 불린다는 점을 함께 본다.
- 플러그인 권한은 `<플러그인>:default` 대신 화면 코드가 실제로 부르는 `allow-*` 만 준다. `tauri add` 는 플러그인의 default 권한을 capability 에 자동으로 넣으므로 들인 뒤 좁힌다.
- 화면이 플러그인의 JS API 를 부르지 않고 Rust 가 플러그인을 쓰면(`app.dialog()`, `app.opener()`) 그 플러그인 권한은 capability 에 필요 없다. ACL 은 웹뷰에서 온 호출만 판정한다.
- 묶음이 여는 것(확인: tauri 2.11.3·2.11.5 프로젝트가 만든 `gen/schemas/acl-manifests.json`): `core:default` 는 app·event·image·menu·path·resources·tray·webview·window 아홉의 default 이고 창 닫기·크기 바꾸기 같은 조작은 들어 있지 않다. `dialog:default` 는 message·save·open 이다. `opener:default` 는 `mailto:`·`tel:`·`http(s)://` URL 을 기본 앱으로 열기와 탐색기에서 보기다. 다른 판이면 그 프로젝트의 `acl-manifests.json` 으로 다시 확인한다.
- `build.removeUnusedCommands` 를 켜면 빌드 때 ACL 이 허용하지 않은 플러그인 명령을 뺀다. tauri 2.4 이상이 필요하고 `dynamic-acl` 로 더하는 권한은 세지 않는다.

## 4. 경로·실행 프로그램을 받는 명령

- 화면이 준 경로 문자열은 그대로 열거나 지우거나 쓰지 않는다. 정규화한 뒤 앱이 정한 뿌리 폴더 안인지, 기대한 종류(파일·폴더·확장자)인지 확인한다. 지우기·덮어쓰기처럼 되돌릴 수 없는 명령은 이 확인을 빼지 않는다.
- 사용자가 고른 파일이 전제면 Rust 명령이 대화상자를 직접 열어 경로를 받는 쪽이 화면에서 경로 문자열을 받는 쪽보다 좁다.
- 실행할 프로그램과 고정 인자는 Rust 쪽 목록(설치 폴더의 리소스, 알려진 시스템 도구)에서 고르고 화면은 그 항목의 이름만 넘긴다. 사용자가 등록한 외부 프로그램을 실행해야 하면 등록할 때와 실행할 때 모두 절대 경로·존재·확장자를 확인한다. 화면이 준 경로를 연결 프로그램으로 여는 명령(`ShellExecute`, `cmd /c start`, `explorer`)에도 같은 확인을 둔다.
- 관리자 권한으로 도는 앱에서 이런 명령은 화면의 입력을 관리자 권한으로 넘기는 통로가 된다. 앱 ACL 로 부를 수 있는 창을 좁히는 것까지 검토한다.

## 5. CSP 와 웹뷰 설정

- `app.security.csp` 를 둔다. CSP 보호는 설정에 적었을 때만 켜진다(`null` 이면 없다).
- 원격 스크립트(CDN)를 싣지 않고 허용 출처는 앱이 소유한 것으로 좁힌다. IPC 는 현재 판의 연결 규칙에 맞춰 연다(예: `connect-src ipc: http://ipc.localhost`).
- Tauri 가 빌드 때 로컬 스크립트의 해시와 nonce 를 CSP 에 넣으므로 앱은 자기 몫만 적는다. `dangerousDisableAssetCspModification` 은 켜지 않는다.
- `devCsp` 가 없으면 `csp` 가 개발 실행에도 들어간다. 개발 서버 때문에 넓힌 값은 `devCsp` 에만 둔다.
- `assetProtocol` 은 기본으로 꺼져 있다. 켜면 `scope` 를 필요한 폴더로 좁힌다.
- `freezePrototype`(기본 false)은 prototype 오염을 막지만 내장 prototype 을 넓히는 라이브러리를 깨뜨리므로 켜고 시험한 뒤 들인다. `pattern` 의 `isolation` 은 제3자 스크립트를 싣는 등 화면을 믿을 수 없을 때 검토한다(기본은 `brownfield`).
- capability 의 `remote` 로 원격 페이지에 명령을 여는 것은 기본으로 하지 않는다. 기본값은 앱에 실린 코드만 API 에 닿는 것이다.
