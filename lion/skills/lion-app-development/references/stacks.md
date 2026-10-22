# 기술별 기준

이번 일이 닿는 기술의 절만 읽는다. Tauri 2 앱은 `src-tauri/` 의 Rust 코드에 Rust 절을, 화면 코드에 TypeScript 절을 쓴다.

프로젝트가 스스로 선언한 명령(CI, package scripts, preset, Makefile, `.cargo/config.toml` 의 alias)을 아래 기본 명령보다 먼저 쓴다. 이번 검증에 필요한 보안 점검 도구(clang-tidy·cppcheck·sanitizer, `cargo audit`·`cargo deny`, `npm audit` 따위)가 설치돼 있지 않으면 그 항목은 미확인으로 남긴다.

## Rust

- 정해진 구조가 없으면 로직은 `src/lib.rs` 에, `src/main.rs` 에는 인자 해석과 실행 연결만, 통합 시험은 `tests/` 에 둔다. 통합 시험은 lib 타깃의 공개 API 만 링크하므로 검증할 로직을 bin 에 두면 `tests/` 에서 닿지 않는다. 단위 시험은 같은 파일의 `#[cfg(test)] mod tests` 에 둔다.
- 타깃 설정(`[[bin]]`·`[lib]` 의 `test`, `crate-type`)은 시험 명령이 실제로 무엇을 빌드하고 돌리는지 바꾸므로 명령을 고르기 전에 읽는다.
- `[[bin]]` 에 `test = false` 가 있으면 `cargo test` 가 그 실행 파일을 건너뛰므로 검증할 로직이 lib 에 있는지 확인한다. 실행 파일이 관리자 권한 매니페스트를 가져 비상승 프로세스가 시험 하네스를 띄울 수 없을 때 이 설정을 쓰고, 그 까닭을 `Cargo.toml` 주석으로 남긴다.

기본 게이트(`cargo audit`·`cargo deny check` 는 설치돼 있을 때만):

```text
cargo build
cargo clippy --all-targets -- -D warnings
cargo test
cargo fmt --check
cargo audit
cargo deny check
```

- workspace 면 build·clippy·test 에 `--workspace` 를 준다. `cargo fmt` 는 `--all` 이 workspace 전체이고 `--workspace` 옵션이 없다. `cargo audit` 는 `Cargo.lock` 단위라 workspace 옵션이 없다.
- `cargo deny check` 는 루트 `Cargo.toml` 이 virtual manifest(`[package]` 없음)면 전체가 대상이다. 루트가 `[package]` 이면서 `[workspace]` 를 가지면 루트 crate 하나만 graph root 이므로 subcommand 앞에 옵션을 둔다(`cargo deny --workspace check`).
- feature 가 있으면 프로젝트가 지원하는 조합(기본, `--no-default-features`, `--all-features`) 가운데 실제 쓰는 조합을 돌린다.
- `-D warnings` 는 기본 켜진 lint 만 오류로 만든다. `cast_possible_truncation`·`cast_sign_loss`·`arithmetic_side_effects` 와 `// SAFETY:` 누락을 잡는 `undocumented_unsafe_blocks` 는 기본 allow 다. 정수·변환 안전의 통과를 주장하려면 `[lints.clippy]` 나 `-W clippy::<lint>` 로 켠 결과를 따로 남긴다.

코드:

- `unwrap`·`expect` 는 시험과 「여기서 실패하면 프로그램 불변식이 깨진 것」인 자리에만 두고 외부 입력 경로에는 두지 않는다.
- `unsafe` 는 가장 작은 블록으로 줄여 안전한 함수로 감싸고, 블록마다 지키는 불변식을 `// SAFETY:` 주석으로 적는다. FFI 경계에서는 포인터의 수명·null 가능성·길이 인자의 출처를 타입과 검사로 고정하고, 패닉이 `extern` 함수 밖으로 나가지 않게 한다.
- `unsafe`·FFI·정수 산술은 외부 입력이 실제로 닿는 경로부터 판정한다.

## TypeScript

- 변형은 `kind` 같은 판별 칸을 둔 유니온으로 만들고 선택 칸 묶음으로 만들지 않는다. switch 기본 갈래에 `const _exhaustive: never = x;` 를 두어 새 변형을 빠뜨리면 컴파일이 실패하게 한다.
- 뜻이 다른 문자열·숫자 ID는 브랜드 타입으로 나누고, 브랜드 값은 실제로 검사하는 타입 가드(`input is UserId`)에서만 만든다.
- 외부 자료는 `unknown` 으로 받아 경계에서 업무 타입으로 파싱한다. 프로젝트에 런타임 스키마 도구(zod 따위)가 있으면 스키마에서 타입을 끌어내고(`z.infer`) 속성마다 손으로 가드를 쓰지 않는다.
- `as` 는 검증 뒤에만 쓰고, 값이 타입에 맞는지 보려면 `satisfies` 를 쓴다. 좁히기는 판별 칸 switch → `in` → `typeof`·`instanceof` → 타입 가드 차례로 고른다. 타입 가드는 이름(`isX`·`hasX`)이 말하는 것을 실제로 검사한다.
- 느슨한 타입이 `!`·형 변환·「일어날 수 없음」 예외를 강요하는 자리에서만 `[T, ...T[]]` 같은 강한 타입으로 바꾼다.
- 새 interface 를 선언하기 전에 `Pick`·`Omit`·`Parameters`·`ReturnType`·`Awaited`·`typeof` 로 끌어낼 수 있는지 본다.
- 인자가 여럿이면 객체로 넘긴다. 프레임마다 도는 렌더링·파서 같은 뜨거운 경로는 예외다.
- 배포 코드에 `console.log` 를 남기지 않고 프로젝트의 구조화 로그를 쓴다.

## C/C++

- 정해진 build system 과 배치가 없으면 루트 `CMakeLists.txt` + `include/<project>/` 의 공개 헤더 + `src/` 의 구현과 내부 헤더 + `tests/`(GoogleTest·Catch2 를 CTest 에 등록)로 둔다. Makefile·MSBuild 는 기존 프로젝트가 쓸 때만 따른다. 라이브러리 target 과 실행 파일 target 을 나눠 시험이 라이브러리에 링크하게 한다.
- 경고 수준과 sanitizer 가 CI 에만 있고 로컬 빌드에 없으면 두 빌드가 다른 코드를 통과시킨다. 플래그는 target 옵션·preset 에 넣어 로컬과 CI 가 같게 빌드한다.
- 다중 구성 generator(Visual Studio, Xcode, Ninja Multi-Config)면 빌드와 시험에 구성을 준다: `cmake --build build --config Release`, `ctest --test-dir build -C Release`. 어느 generator 가 쓰였는지는 구성 뒤 `build/CMakeCache.txt` 의 `CMAKE_GENERATOR` 로 확인한다.
- 정수·변환 안전의 통과를 주장하려면 `-Wall -Wextra` 에 더해 `-Wconversion` 을 켠 빌드 결과를 따로 남긴다.
- 길이 인자의 출처와 목적지 크기, 변수인 포맷 인자, 해제 뒤 사용과 이중 해제, 초기화하지 않은 변수, 크기·오프셋 계산의 넘침과 부호 변환은 외부 입력이 실제로 닿는 경로부터 판정한다.

## Python

- 정해진 구조나 framework 의 필수 배치가 없으면 오래 관리할 앱·라이브러리·CLI 는 `src/<package>/` + `tests/` 로 둔다. Django 처럼 framework 가 배치를 정하면 그것을 따른다.
- 단일 임시 스크립트·노트북은 오래 관리할 경계가 생길 때만 이 구조로 옮긴다.

## 여러 기술이 섞인 저장소

- 새 구조를 만들기 전에 CI 가 실제로 돌리는 build·test 명령을 읽고 루트 README·AGENTS 의 명령과 견줘 지금 실행 경로를 복원한다.
- 정해진 구조가 없으면 독립 실행·배포 앱이 둘 이상일 때 `apps/<app>/`, 여러 앱이 실제로 공유하는 패키지는 `packages/<package>/`, 공유 자동화는 `scripts/` 에 둔다. 앱이 하나면 그 기술의 기본 배치를 바로 쓴다.
- 프로젝트 규칙 문서의 폴더 틀이 루트 모양과 코드 폴더(예: `app/`)를 정했으면 그것을 따르고, `apps/`·`packages/`·manifest 는 그 코드 폴더 안에 둔다. 폴더 틀이 없으면 `docs/`·`scripts/`·`resources/`·`data/`·`tools/`·`archive/` 는 실제 역할이 생길 때만 만든다.
- framework·vendor 가 위치를 강제하는 생성·외부 영역은 옮기지 않는다.
- 검증 명령은 CI → package·build scripts → 문서에 적힌 명령 → 도구 기본 명령 차례로 고른다. 서로 어긋나면 실제 실행 결과와 최신 설정으로 정하고 낡은 안내를 고친다.
