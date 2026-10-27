# 시험 실행 환경

호출 시험과 따름 확인을 Claude·Codex CLI로 실제로 돌릴 때 쓴다: 후보 판 놓기, 같은 이름 설치본 끄기, 명령, 열림 판정.

2026-10-19에 Claude Code 2.1.296, Codex CLI 0.163.0-alpha(데스크톱 앱이 넣은 실행 파일)에서 확인한 방법이다. 다음에 쓸 때 첫 실행에서 출력 모양이 같은지 다시 본다.

## Claude

- 후보 스킬은 플러그인 폴더에 담는다: `.claude-plugin/plugin.json`(name, version)과 `skills/<이름>/`.
- 같은 이름 설치본은 설정 파일로 끈다: `{"skillOverrides": {"<이름>": "off"}}`.
- 플러그인 폴더와 시험 폴더도 `%TEMP%` 밖 보통 폴더에 둔다. `tempfile.mkdtemp` 로 만든 잠긴 폴더에 두면 플러그인은 실리고 그 안의 스킬은 0개로 실려, 모든 문장이 「안 열림」으로 나온다. 첫 실행의 `system` `init` 줄에서 `skills` 에 `플러그인이름:` 스킬 수가 후보 수와 같은지 본다(2026-10-27).
- 출력이 빈 실행은 오류로 따로 센다(설정 파일 경로가 셸에서 깨졌을 때 등). Windows 경로는 앞으로 슬래시로 넘긴다.
- 명령:

```
claude -p "<문장>" --plugin-dir <플러그인 폴더> --settings <설정 파일> --output-format stream-json --verbose --permission-mode default --no-session-persistence --allowedTools Skill Read Grep Glob --disallowedTools Edit Write Bash
```

- 열림 판정: 출력 줄 가운데 `type`이 `assistant`인 줄의 `message.content`에서 `tool_use` 이름이 `Skill`인 항목의 `input.skill`. 플러그인 스킬은 `플러그인이름:스킬이름`으로 보인다. 모드 방식이면 `Read` 로 읽은 `<이름>/SKILL.md` 도 열림으로 센다. 자동 호출을 끈 스킬을 부른 `Skill` 호출은 "cannot be used with Skill tool" 로 막히므로 열림에서 뺀다.
- 모드 방식이면 세션 시작 훅도 시험에 켠다: 플러그인 폴더의 `hooks/hooks.json` 에 `{"hooks": {"SessionStart": [{"hooks": [{"type": "command", "command": "cat \"${CLAUDE_PLUGIN_ROOT}/skills/<모드>/hook.md\""}]}]}}`.
- 시험 대화에는 읽기와 스킬 열기만 준다. 시험하는 스킬이 열리면 그 지시대로 실제 자리(위키 수집함, 설치본, 기억 폴더)에 파일을 쓸 수 있다. 2026-10-19 시험에서 쓰기 도구를 준 대화가 실제 위키 수집함과 위키에 가짜 프로젝트 파일을 썼다. 읽기만 줘도 스킬은 같은 비율로 열렸다.
- 기본 권한 모드가 계획 모드인 환경은 `--permission-mode`를 주지 않으면 계획서 파일이 생긴다. `default`를 준다.

## Codex

- 시험 폴더에서 `git init`을 하고 후보를 `.agents/skills/<이름>/`에 둔다.
- Windows 에서는 시험 폴더를 사용자 임시 폴더(`%TEMP%`) 밖에, 위 폴더 권한을 잇는 보통 폴더로 만들고 그 폴더 안에서 실행한다. Python `tempfile.mkdtemp` 는 만든 사람만 접근하게 잠가 Codex 보안 상자가 못 읽는다. 그때 Codex 는 설치본 옛 판을 읽거나 스킬 없이 답해, 결과가 시험 판을 가리키지 않는다(2026-10-20).
- 같은 이름 설치본은 실행 옵션으로 끈다: `-c 'skills.config=[{path="<SKILL.md 경로>",enabled=false}]'`. 설치 위치(`~/.agents/skills`, `~/.codex/skills`)마다 경로를 나열한다.
- 명령:

```
codex exec --json -s read-only -C <시험 폴더> "<문장>"
```

- 열림 판정: JSON 줄 가운데 `item.started`의 `command_execution` 항목 명령에 `<스킬>/SKILL.md`가 읽히는지.
