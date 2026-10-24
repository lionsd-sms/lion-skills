# Windows 설치판

Tauri Windows 설치판(NSIS)의 설정은 이 파일을 따른다.

## 1. 설치 방식(`bundle.windows.nsis.installMode`)

- `currentUser`(기본): 관리자 권한 없이 `%LOCALAPPDATA%\<productName>` 에 설치하고 HKCU 에 기록한다.
- `perMachine`: 관리자 권한으로 `Program Files` 에 설치하고 HKLM 에 기록한다.
- `both`: 설치 때 고르며, 사용자 설치를 골라도 관리자 권한이 필요하다.
- 관리자 권한으로 도는 앱(매니페스트 `requireAdministrator`, 또는 `runas` 재실행)은 `perMachine` 으로 설치한다. `currentUser` 설치 폴더는 그 사용자 권한으로 바꿀 수 있어서, 거기 놓인 exe·DLL·리소스가 관리자 권한으로 실행되면 사용자 권한의 코드가 관리자 권한을 얻는 길이 된다.
- 관리자 권한으로 도는 앱은 포터블 exe 를 내지 않고 설치본(`perMachine`)으로 낸다. 포터블이 꼭 필요하면 표준 사용자가 쓸 수 없는 자리(관리자만 쓰는 폴더, 쓰기가 막힌 매체)에서만 띄우게 하고 그 까닭을 배포 문서에 적는다. 쓰기 가능한 USB·폴더의 포터블을 관리자 권한으로 띄우는 것은 위와 같은 길이다.
- 이미 `currentUser` 로 설치된 앱을 `perMachine` 으로 바꾸면 설치 자리와 제거 정보가 달라지므로 옛 설치를 어떻게 지울지 함께 정한다.

## 2. WebView2 설치 방식(`bundle.windows.webviewInstallMode` 의 `type`)

| 방식 | 인터넷 | 설치판 크기 | 고를 때 |
|---|---|---|---|
| `downloadBootstrapper`(기본) | 필요 | 늘지 않음 | 설치 PC 가 인터넷에 닿을 때. 런타임이 없으면 설치 중에 내려받고, 받지 못하면 설치를 멈춘다 |
| `embedBootstrapper` | 필요 | 약 1.8MB | Windows 7 에 `.msi` 로 배포할 때 |
| `offlineInstaller` | 불필요 | 약 127MB | 런타임이 없을 수 있는 설치 PC 가 인터넷에 못 닿을 수 있을 때 |
| `fixedRuntime` | 불필요 | 약 180MB | 판을 고정해야 할 때만. 런타임 보안 패치가 자동으로 오지 않는다 |
| `skip` | 불필요 | 늘지 않음 | 런타임이 없으면 앱이 뜨지 않으므로 쓰지 않는다 |

- Windows 11 에는 Evergreen 런타임이 OS 에 들어 있고 Windows 10 도 대부분 가지고 있다. 설치판은 레지스트리 `pv` 값으로 런타임을 확인하고 있으면 설치 단계를 건너뛴다. 인터넷에 닿는 PC 는 기본 방식으로 충분하다. 런타임이 없을 수 있는 설치 PC 가 인터넷에 못 닿을 수 있으면 `offlineInstaller` 를 고르거나 WebView2 Evergreen Standalone Installer 를 따로 준비한다.
- 포터블 exe 에는 WebView2 설치 단계가 없다. 대상 PC 에 런타임이 미리 있어야 한다.
- `minimumWebview2Version` 을 두면 런타임이 낮을 때 부트스트래퍼로 올리려 하므로 인터넷이 필요하다.
- `fixedRuntime` 은 네트워크 위치·UNC 경로에서 실행할 수 없고, Windows 10 에서 Fixed Version 120 이상은 폴더 권한(`icacls`) 설정이 필요하다.
- Evergreen 런타임은 앱을 다시 시작해야 새 판을 쓴다. 계속 켜 두는 앱(상황판·제어 콘솔)은 재시작 시점을 운영 안내에 넣는다.

## 3. WebView2 데이터 폴더

- Tauri 는 Windows 에서 따로 정하지 않으면 `%LOCALAPPDATA%\<identifier>` 를 WebView2 데이터 폴더로 쓴다. `identifier` 는 이 경로에 쓰이므로 앱마다 유일해야 하고, 바꾸면 데이터 자리가 바뀐다.
- 같은 데이터 폴더를 쓰는 앱들은 같은 로그온 세션에서 WebView2 세션을 함께 쓴다. 한 데이터 폴더에는 한 번에 세션 하나만 있고, 다른 로그온 세션의 앱과는 그 폴더를 함께 쓸 수 없다.
- 그래서 같은 identifier 의 사본·변형판은 저장 데이터(localStorage·쿠키 등)를 나눠 가진다. 데이터를 나눠야 하거나 single-instance 로 서로를 막으면 안 되는 변형판은 identifier 를 달리한다.
- 폴더를 옮기면(예: 실행 파일 옆) 그 자리에 쓰기 권한이 있어야 하고 네트워크 드라이브는 피한다. `perMachine` 설치 폴더는 표준 사용자가 쓸 수 없다. 제거기의 앱 데이터 삭제는 `%APPDATA%\<identifier>`·`%LOCALAPPDATA%\<identifier>` 만 지우므로 옮긴 폴더는 남는다.

## 4. 실행 수준(실행 파일 매니페스트의 `requestedExecutionLevel`)

- `asInvoker` 는 시작한 프로세스의 권한, `requireAdministrator` 는 관리자 권한, `highestAvailable` 은 해당 사용자가 얻을 수 있는 가장 높은 권한으로 실행한다.
- 필요한 실행 수준을 `tauri_build::WindowsAttributes::app_manifest` 로 넣는다. 표준·관리자 계정, 이미 상승한 프로세스, 대상 PC 의 UAC 정책에서 실제 실행·상승 동작을 확인한다. 동의·자격 증명 창의 종류와 재확인 여부는 실제로 본 것만 적는다.
- 관리자 권한이 필요한 일이 일부뿐이면 앱 전체를 올리기 전에 그 일만 올리는 방식(따로 도는 도우미, `runas` 재실행)과 비교해 설계 문서에 남긴다.
- 관리자 권한 매니페스트를 가진 실행 파일은 비상승 프로세스가 시험 하네스를 띄우지 못한다. 시험할 로직을 lib 에 두고 그 `[[bin]]` 에 `test = false` 를 둔 뒤 까닭을 `Cargo.toml` 주석으로 남긴다.

## 5. 템플릿과 게시자

- 설치 단계에 몇 가지만 더하려면 템플릿을 통째로 복사하지 않고 `installerHooks` 의 네 hook(`NSIS_HOOK_PREINSTALL`, `NSIS_HOOK_POSTINSTALL`, `NSIS_HOOK_PREUNINSTALL`, `NSIS_HOOK_POSTUNINSTALL`)을 쓴다.
- 템플릿을 이미 복사해 쓰면 복사한 원본의 tauri-bundler 판을 파일 머리에 적고 Tauri 판을 올릴 때 그 판의 원본과 비교한다(확인: @tauri-apps/cli 2.11.4 가 쓰는 원본은 tauri-bundler 2.9.4 판이다).
- `bundle.publisher` 를 비우면 identifier 의 둘째 마디(예: `kr.co.example` 의 `co`)가 Windows 설치 정보의 게시자와 레지스트리 `Software\<게시자>` 키에 들어간다. 새 앱은 처음부터 적는다.
- 이미 배포된 앱의 게시자를 바꾸면 그 키가 `Software\<새 게시자>` 로 바뀌어, 새 설치판이 옛 설치 위치(`Software\<옛 게시자>\<제품명>`)를 읽지 못해 기본 자리에 설치하고 옛 키가 남는다. 바꿀 때는 옛 키와 옛 설치를 어떻게 치울지 함께 정한다.
- 마지막 빌드가 실제로 쓴 값은 `target/release/nsis/<arch>/installer.nsi` 머리의 `INSTALLMODE`·`INSTALLWEBVIEW2MODE`·`ALLOWDOWNGRADES`·`MANUFACTURER` 로 확인한다.
