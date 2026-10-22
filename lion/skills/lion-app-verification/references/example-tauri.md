# 절차 본보기: Windows 데스크톱(Tauri) 재고 앱

아래는 가상의 재고 앱 `stock-app` 에 맞춰 쓴 절차의 한 부분이다. 명령과 이름은 실제 저장소에서 찾은 것으로 바꾼다.

````markdown
# 재고관리 확인 절차

재고관리 데스크톱 앱(Tauri, Windows)을 띄워 사용자처럼 조작하고 증거를 남긴다. 기능을 바꾼 뒤, 또는 "실제로 되나"를 보일 때 연다.

## 실행

- 준비(한 번): `npm ci`, `npm run tauri build -- --debug`
- 확인용 자료 폴더: `$dir = "$env:TEMP\stock-verify-$(Get-Date -Format yyyyMMddHHmmss)"` 를 만들고 `$env:STOCK_DATA_DIR = $dir` (앱이 이 값을 읽는다: src-tauri/src/paths.rs)
- 조작 통로: `$env:WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS = "--remote-debugging-port=9333"`
- 띄우기: `$app = Start-Process src-tauri\target\debug\stock-app.exe -PassThru`
- 준비됨: 로그 `$dir\logs\app.log` 에 `db ready`, 창 제목 `재고관리`, 첫 화면에 `품목 목록` 표가 보임. 첫 실행에 마이그레이션이 돌고 기초 품목 `볼트 M6`(수량 100)이 들어간다.

## 상태 점검

- `(Get-Process -Id $app.Id).MainWindowTitle` 이 `재고관리`
- `Invoke-RestMethod http://127.0.0.1:9333/json/version` 이 응답(이 포트가 이번 실행의 것)
- 앱 `정보` 창의 빌드 시각이 방금 빌드한 시각과 같음
- `$dir\stock.db` 가 있고 사용자의 `%APPDATA%\com.example.stock` 는 건드리지 않음

## 조작

- Playwright 로 웹뷰에 붙는다: `chromium.connectOverCDP('http://127.0.0.1:9333')`
- 손잡이는 역할과 이름: `page.getByRole('button', { name: '품목 추가' })`
- 파일 열기 대화상자·트레이·알림은 웹뷰 밖이다. 화면 조작 도구로 누르거나 사용자에게 부탁하고, 그 사실을 증거에 적는다.
- 사용자가 켜 둔 재고관리 창은 조작하지 않는다.

## 증거

- 폴더: `verify-evidence\<날짜>-<기능 ID>\` (.gitignore 에 있음)
- 화면: 조작 직후 캡처와 접근성 트리
- 값: `sqlite3 -readonly "$dir\stock.db" "select name, qty from items"`
- 로그: `$dir\logs\app.log` 에서 이번 조작 시각의 줄

## 정리

- `Stop-Process -Id $app.Id`
- `Remove-Item -Recurse $dir`
- `Test-Path verify-evidence\<날짜>-<기능 ID>` 가 True

## 기능 지도

### 품목 추가

사용자가 새 품목을 이름·수량과 함께 저장하고, 목록과 다시 연 화면에서 그 값을 본다.

세부 기능
- `item-add-open` 입구마다 빈 입력 창이 열린다
- `item-add-save` 이름·수량을 저장한다
- `item-add-cancel` 쓰다 만 입력을 버린다

들어가는 길
- 도구 막대 `품목 추가` 버튼
- 목록에 초점이 있을 때 `Ctrl+N`

확인 경로
전제: 상태 점검 통과, `너트 M6` 품목이 없음
- 입력 창 열기: `품목 추가` 를 누른다 → `getByRole('button', { name: '품목 추가' }).click()` → `품목 입력` 창이 열리고 `이름` 칸에 초점
- 값 넣기: `getByLabel('이름').fill('너트 M6')`, `getByLabel('수량').fill('40')` → `저장` 버튼이 켜짐
- 저장: `getByRole('button', { name: '저장' }).click()` → `저장했습니다` 알림, 목록에 `너트 M6 · 40`
- 남았는지: 앱을 끄고 다시 띄운 뒤 목록에 `너트 M6 · 40`, `sqlite3 -readonly` 결과에 같은 줄
- 취소: 다시 열어 이름 `버릴 품목` 입력 후 `취소` → 목록에 `버릴 품목` 없음
- 증거: 목록 캡처·접근성 트리·DB 읽기 결과를 `verify-evidence\<날짜>-item-add\` 에

함정
- 이름 칸에 초점이 있으면 `Ctrl+N` 이 글자 입력으로 처리된다
- 수량은 저장할 때 정수로 바뀐다. 입력값 대신 목록에 보이는 값을 본다
- 저장 알림만으로는 증거가 되지 않는다. 다시 띄운 목록과 DB 를 본다
````
