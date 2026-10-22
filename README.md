# lion 스킬

lion 스킬 28개와 역할 에이전트 5개가 들어 있다. 새 대화를 열면 길잡이 스킬(lion-mode)이 먼저 열리고, 요청에 맞는 스킬을 골라 읽은 뒤 일을 시작한다.

```
lion-skills
 ├─ .claude-plugin/marketplace.json   Claude Code 가 읽는 목록
 ├─ lion/                             Claude Code 플러그인 (스킬 28 · 에이전트 5 · 새 대화 훅)
 ├─ codex/                            Codex 용 에이전트 5 · 새 대화 훅
 ├─ global-rules/                     전역 규칙 (CLAUDE.md · AGENTS.md, 내용 같음)
 ├─ LICENSE                           MIT
 └─ README.md                         이 파일
```

## Claude Code

1. 터미널에서 차례로 친다. 플러그인이 `%USERPROFILE%\.claude\plugins\cache\lion-skills\` 에 깔린다.
   ```
   claude plugin marketplace add lionsd-sms/lion-skills
   claude plugin install lion@lion-skills
   ```
2. 읽기 허용: `%USERPROFILE%\.claude\settings.json` 의 `permissions.allow` 에 아래 한 줄을 넣는다. 이 줄이 없으면 lion-mode 가 스킬 파일을 읽을 때마다 허락 창이 뜬다. 플러그인은 이 허용을 스스로 넣을 수 없다.
   ```
   "Read(~/.claude/plugins/cache/lion-skills/**)"
   ```
   settings.json 이 없으면 아래 내용으로 새로 만든다.
   ```json
   {
     "permissions": {
       "allow": ["Read(~/.claude/plugins/cache/lion-skills/**)"]
     }
   }
   ```
3. 전역 규칙: `global-rules/CLAUDE.md` 내용을 `%USERPROFILE%\.claude\CLAUDE.md` 끝에 붙여 넣는다. 파일이 없으면 그대로 복사한다.
4. Claude Code 를 껐다 켠다.
5. 확인: 새 대화에서 `PDF 두 개 합쳐줘` 를 친다. 첫 동작으로 `lion:lion-mode` 스킬이 열리고, 허락 창 없이 `lion-pdf\SKILL.md` 를 읽으면 된 것이다.

새 판 받기:

```
claude plugin marketplace update lion-skills
claude plugin update lion@lion-skills
```

## Codex

1. 이 저장소를 내려받는다: `git clone https://github.com/lionsd-sms/lion-skills.git`
2. `lion/skills/` 안의 폴더 28개를 `%USERPROFILE%\.agents\skills\` 에 복사한다.
3. `codex/agents/` 안의 파일 5개를 `%USERPROFILE%\.codex\agents\` 에 복사한다.
4. `codex/hooks.json` 을 `%USERPROFILE%\.codex\hooks.json` 으로 복사한다. 이미 그 파일이 있으면 `SessionStart` 항목만 옮겨 붙인다.
5. Codex 새 대화에서 `/hooks` 를 열어 lion-mode 훅을 신뢰한다. 신뢰하기 전에는 훅이 돌지 않는다.
6. 전역 규칙: `global-rules/AGENTS.md` 내용을 `%USERPROFILE%\.codex\AGENTS.md` 끝에 붙여 넣는다.

새 판은 `git pull` 로 받은 뒤 2~3번을 다시 한다.

## 지우기

- Claude Code: 터미널에서 `claude plugin uninstall lion@lion-skills`, 그다음 `claude plugin marketplace remove lion-skills`. settings.json 에 넣은 읽기 허용 줄도 지운다.
- Codex: 위에서 복사한 스킬 28개 폴더, 에이전트 5개 파일, hooks.json 의 lion-mode 항목을 지운다.
- 전역 규칙: 붙여 넣은 부분을 지운다.

## 출처와 이용조건

이 저장소는 MIT 다([LICENSE](LICENSE)). 일부 지침은 아래 자료의 생각과 내용을 바탕으로 우리 말로 다시 썼다. 각 자료의 원래 저작권 문구는 그 지침이 든 스킬의 `references/LICENSES.md` 에 그대로 있다.

- [agent-skills](https://github.com/addyosmani/agent-skills) · Addy Osmani · MIT
- [pstack](https://github.com/cursor/plugins/tree/main/pstack) · Lauren Tan · MIT
- [skills](https://github.com/mattpocock/skills) · Matt Pocock · MIT
- [ponytail](https://github.com/DietrichGebert/ponytail) · DietrichGebert · MIT
- [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) · Next Level Builder · MIT (그 안의 UI 스타일 자료 일부는 Apache License 2.0)
