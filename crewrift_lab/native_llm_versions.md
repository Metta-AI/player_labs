# Native LLM transport versions

These uploads use the lab's existing strategies with the native Messages endpoint and platform-selected Haiku 4.5 model. They were not submitted to leagues.

| Policy | Version | Policy version ID | Uploaded at (UTC) | Validation |
| --- | --- | --- | --- | --- |
| relh-crewborg-native | v1 | 8c44e2da-4ce0-47a2-a3d5-595310fd50ef | 2026-10-02T17:36:49.139929Z | Linux amd64 build; eight-seat local episode exited cleanly and wrote results and replay. |
| relh-suspectra-native | v1 | c4e55c78-fe24-4676-942b-3d63d50994cc | 2026-10-02T17:38:31.374167Z | Linux amd64 build; eight-seat local episode exited cleanly and wrote results and replay. |

Both versions request `--use-llm --llm-model anthropic/claude-haiku-4.5`. Crewborg runs `python -m crewrift.crewborg.coworld.policy_player`; Suspectra runs `/bin/suspectra`.

The original `crewborg` name belongs to another owner. These uploads use new owned names rather than changing that owner's version history.
