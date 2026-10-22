# 확인

## 1. 게이트

- 앱 전체 빌드·실행은 `tauri build`·`tauri dev`(npm scripts 또는 `cargo tauri`)로 하고, 프론트엔드 빌드는 `tauri.conf.json` 의 `build.beforeBuildCommand`·`beforeDevCommand` 가 잇는다. 화면 게이트는 프로젝트 scripts 에 있는 명령을 쓴다.
- `src-tauri` 에서 cargo 게이트만 따로 돌리면 `build.frontendDist` 폴더가 없을 때 빌드 시점 코드 생성이 실패할 수 있다(`build.devUrl` 이 있는 개발 빌드는 이 검사를 건너뛴다). 프론트엔드 산출물을 먼저 만들거나 그 조건을 확인한 뒤 돌린다.

## 2. 게이트 통과 뒤에 함께 읽는 것

- capability 의 창 label 이 실제로 만드는 창 label 과 맞는지, 권한마다 그 창의 화면 코드가 부르는 API 가 있는지. 권한 표를 시험으로 두면 한쪽만 바뀌는 것을 잡는다.
- `gen/schemas/acl-manifests.json` 의 `__app-acl__` 유무와, 앱 명령 가운데 경로·실행할 프로그램을 받는 명령의 확인 코드.
- `app.security.csp` 가 있고 `dangerousDisableAssetCspModification` 이 없는지.
- 설치판에 실제로 들어간 값: `installer.nsi` 머리의 설치 방식·WebView2 방식·내림 설치 허용·게시자, 그리고 실행 수준과 설치 방식의 조합(관리자 권한으로 도는 앱은 `perMachine`).
- 설치판에 실린 리소스 목록.

## 3. 설치 확인

- 설치 방식·실행 수준·WebView2 방식·리소스·capability 를 바꾼 변경이면, 작업 PC 에서 빌드한 설치판을 표준 사용자 조건으로 설치·첫 실행·제거까지 해 본다.
- 현장 PC 에서만 알 수 있는 것(인터넷 여부, 런타임 판, 스마트 앱 컨트롤 상태)은 앱 시작 로그(Windows 판, WebView2 런타임 판, 설치 자리, 데이터 폴더)로 남기고, 작업 PC 에서 확인하지 못한 항목은 「미확인」으로 남긴다.
- 화면 문구만 바꾼 변경에는 이 설치 확인을 걸지 않는다.
