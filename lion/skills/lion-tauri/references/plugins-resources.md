# 플러그인과 resources

## 1. 플러그인

- single-instance 는 다른 플러그인보다 먼저 등록한다. 두 번째 실행이 넘긴 `args`·`cwd` 는 사용자가 준 입력이라 경로·실행 프로그램을 받는 명령과 같은 확인(정규화, 뿌리 폴더 안, 기대한 종류)을 둔다.
- single-instance 는 Windows 에서 `identifier`(semver 기능을 켜면 판까지)로 같은 앱을 가린다. 같은 identifier 의 사본·변형판은 서로를 두 번째 실행으로 보고 막으므로, 동시에 띄워야 하는 변형판은 identifier 를 달리한다.
- dialog 는 고른 파일의 경로를 돌려준다. Rust 의 `DialogExt` 로 열면 capability 권한이 필요 없다.
- `WindowsAttributes::app_manifest` 로 실행 파일 매니페스트를 바꾸면 Common-Controls v6 의존성을 그 매니페스트에 넣어야 dialog API 가 제대로 돈다.
- opener 를 화면에서 쓰면(`openPath`) `opener:allow-open-path` 에 `path` scope 를 준다. Rust 의 `app.opener().open_path` 는 ACL 을 거치지 않으므로 경로 확인은 명령의 몫이다.

## 2. bundle.resources

- `..` 는 `_up_`, 절대 경로의 뿌리는 `_root_` 로 바뀐다.
- `dir/` 는 하위 폴더까지 구조째 싣고, `dir/*` 는 그 폴더의 파일만(하위 폴더 제외), `dir/**/*` 는 하위 폴더까지의 파일을 모두 싣는다. `dir/**` 는 파일을 찾지 못해 오류다.
- map 꼴에서 glob 으로 고른 파일은 원래 폴더 구조 없이 대상 폴더에 모인다.
- 실행 때 경로는 직접 계산하지 않고 `BaseDirectory::Resource`(JS 는 `resolveResource`)로 얻는다.
- 폴더나 와일드카드로 실으면 저장소에 놓인 파일이 그대로 설치판에 들어간다. 빌드 전에 실릴 목록을 찍어 보거나 파일 목록·map 으로 적는다.
- `currentUser` 설치에서는 리소스 폴더도 그 사용자가 쓸 수 있는 자리다. 리소스로 실은 실행 파일을 관리자 권한으로 돌리는 앱은 `perMachine` 으로 설치한다.
