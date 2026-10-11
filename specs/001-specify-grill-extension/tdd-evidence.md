# TDD Evidence: 001-specify-grill-extension

<!-- Written by tdd_check.py. Do not edit by hand: use the script's subcommands. -->

## Summary

_Generated from the tables below on 2026-10-11T04:42:53Z._

| Obligation | Requirements | Status | Tests | Latest result |
|------------|--------------|--------|-------|---------------|
| VO-001 | FR-001, FR-005, FR-009, FR-011 | verified | tests.structure.test_manifest | pass (#5) |
| VO-002 | FR-002, FR-016, FR-017, FR-018 | verified | tests.structure.test_manifest | pass (#7) |
| VO-003 | FR-003, FR-020, FR-022 | verified | tests.structure.test_upstream_region | pass (#9) |
| VO-004 | FR-004, FR-025 | verified | tests.structure.test_provenance | pass (#81) |
| VO-005 | FR-005, FR-012, US2-AS4 | verified | tests.structure.test_grill_context | pass (#12) |
| VO-006 | FR-007 | verified | tests.structure.test_grill_context.Interactivity, tests.structure.test_grill_context | pass (#14) |
| VO-007 | FR-008, DC-01 | verified | tests.structure.test_grill_context.ReadOnly, tests.structure.test_grill_context | pass (#17) |
| VO-008 | FR-021 | verified | tests.structure.test_grill_label | pass (#19) |
| VO-009 | FR-021, EC-01 | verified | tests.structure.test_grill_label.LabelReplacementAndFailure, tests.structure.test_grill_label | pass (#21) |
| VO-010 | FR-001, FR-009, US6-AS2 | blocked | - | - |
| VO-011 | FR-005, EC-02 | verified | tests.install.test_install | pass (#24) |
| VO-012 | FR-010, SC-008, US6-AS3 | verified | tests.install.test_remove | pass (#77) |
| VO-013 | FR-016, SC-007, US6-AS1 | verified | tests.install.test_coexist | pass (#79) |
| VO-014 | FR-025, SC-011 | in progress | tests.release.test_release_install | fail (#95) |
| VO-015 | FR-001, FR-011, FR-017, SC-001, US1-AS1, US1-AS6 | verified | tests.behaviour.test_nested_start | pass (#29) |
| VO-016 | FR-003, FR-021, US1-AS2 | verified | tests.behaviour.test_interview_saves | pass (#32) |
| VO-017 | FR-003, SC-004, US1-AS3, US1-AS4 | verified | tests.behaviour.test_knowledge_docs | pass (#33) |
| VO-018 | FR-014, FR-021, US1-AS5 | verified | tests.behaviour.test_completion | pass (#36) |
| VO-019 | FR-012, FR-014, SC-002, US2-AS1, US3-AS1, US3-AS2 | verified | tests.behaviour.test_skip | pass (#57) |
| VO-020 | FR-012, US2-AS2 | verified | tests.behaviour.test_setting.Strict | pass (#51) |
| VO-021 | FR-012, FR-014, SC-002, US2-AS3 | verified | tests.behaviour.test_setting.Off | pass (#53) |
| VO-022 | FR-012, US2-AS4 | verified | tests.behaviour.test_setting.UnknownValue, tests.behaviour.test_setting | pass (#55) |
| VO-023 | FR-014, FR-015, FR-021, SC-010, US4-AS1 | verified | tests.behaviour.test_stop_resume | pass (#59) |
| VO-024 | FR-002, FR-015, SC-006, US4-AS2 | verified | tests.behaviour.test_stop_resume.ResumeStandalone | pass (#63) |
| VO-025 | FR-013, US4-AS3 | verified | tests.behaviour.test_standalone | pass (#66) |
| VO-026 | FR-006, FR-023, US4-AS4 | verified | tests.behaviour.test_nested_hooks | pass (#69) |
| VO-027 | FR-006 | verified | tests.behaviour.test_standalone.StandaloneClarifyHooks | pass (#71) |
| VO-028 | FR-007, FR-014, SC-002, SC-009, US5-AS1, US5-AS2 | verified | tests.behaviour.test_unattended | pass (#74) |
| VO-029 | FR-014, SC-002, SC-010, EC-03 | verified | tests.behaviour.test_stop_resume.StopBeforeFirstAnswer | pass (#61) |
| VO-030 | FR-024 | verified | tests.behaviour.test_nothing_to_settle | pass (#44) |
| VO-031 | FR-008 | verified | tests.behaviour.test_completion.WriteBoundary | pass (#38) |
| VO-032 | FR-003, SC-003 | blocked | tests.behaviour.test_equivalence | fail (#84) |
| VO-033 | FR-003, EC-04 | verified | tests.behaviour.test_persistence_failure | pass (#46) |
| VO-034 | FR-019 | verified | tests.regression.test_user_level_isolation | pass (#86) |
| VO-035 | FR-009, SC-005, US6-AS2 | blocked | - | - |
| VO-036 | FR-001, EC-05 | verified | tests.behaviour.test_open_markers | pass (#88) |
| VO-037 | FR-016, EC-06 | verified | tests.regression.test_cross_grill | pass (#91) |
| VO-038 | FR-018, DC-02 | verified | tests.structure.test_bash32 | pass (#94) |

**Not verified**: FR-001 (VO-010 blocked), FR-009 (VO-010 blocked, VO-035 blocked), FR-003 (VO-032 blocked), FR-025 (VO-014 in progress), US6-AS2 (VO-010 blocked, VO-035 blocked), SC-011 (VO-014 in progress), SC-003 (VO-032 blocked), SC-005 (VO-035 blocked), SC-001 (exempt: see plan).

**Open decisions**: DN-01 holds T065, T066, T071, T072 (Spec Kit 1.1.3's specify template runs after_specify hooks in .specify/extensions.yml file order (install order), not by priority, so priority 5 alone does not satisfy FR-009 (grill first). How should the extension guarantee ordering? Options: (a) document install-first plus priority; (b) the entry-point command reorders its own entry in extensions.yml at run time; (c) other.); DN-02 holds T078 (VO-032 (equivalence with upstream) compares the number of Clarifications recorded by two LLM-driven interviews on the same scripted answers; this count varies run to run for the same code (ours: 10, 6; upstream: 5). Options: (a) compare sections, knowledge-doc paths and coverage statuses but allow the question count to differ by a stated tolerance or only require that every scripted topic is recorded once; (b) keep exact equality and accept the test as unreliable (VO-032 reported not verified); (c) exempt SC-003 from automation and verify it by manual review. Which should apply?). **Exceptions**: EX-01 no-meaningful-red on T029 for VO-015; EX-02 no-meaningful-red on T033 for VO-017; EX-03 no-meaningful-red on T037 for VO-031; EX-04 no-meaningful-red on T041 for VO-033; EX-05 no-meaningful-red on T043 for VO-020; EX-06 no-meaningful-red on T049 for VO-019; EX-07 no-meaningful-red on T055 for VO-024; EX-08 no-meaningful-red on T057 for VO-025; EX-09 no-meaningful-red on T059 for VO-026; EX-10 no-meaningful-red on T067 for VO-012; EX-11 no-meaningful-red on T069 for VO-013; EX-12 no-meaningful-red on T079 for VO-034; EX-13 no-meaningful-red on T081 for VO-036; EX-14 no-meaningful-red on T083 for VO-037; EX-15 no-meaningful-red on T085 for VO-038. **Expectation changes**: XC-01 on T031 for FR-001; XC-02 on T030 for FR-001; XC-03 on T040 for FR-024; XC-04 on T044 for FR-012.

**Pre-existing failures**: #1 fast: Makefile does not exist until T003; baseline rerun after setup tasks.

## Baseline

| Seq | Command | Result | Pre-existing failures |
|-----|---------|--------|-----------------------|
| 1 | fast | fail | Makefile does not exist until T003; baseline rerun after setup tasks |
| 2 | fast | pass | - |

## Test execution records

| Seq | Time | Task | Obligations | Phase | Command | Selector | Result | Valid | Classification | Files | Fingerprint | Note | Check |
|-----|------|------|-------------|-------|---------|----------|--------|-------|----------------|-------|-------------|------|-------|
| 1 | 2026-10-10T23:13:05Z | - | - | baseline | fast | - | fail | yes | environment | - | - | Makefile does not exist until T003; baseline rerun after setup tasks | 700d13 |
| 2 | 2026-10-10T23:14:39Z | - | - | baseline | fast | - | pass | yes | - | - | - | No pre-existing failing tests; only the sanity test exists | 56a837 |
| 3 | 2026-10-10T23:14:42Z | - | - | checkpoint | fast | - | pass | yes | - | - | - | - | bb5494 |
| 4 | 2026-10-10T23:14:51Z | T010 | VO-001 | red | one | tests.structure.test_manifest | fail | yes | assertion | tests/structure/test_manifest.py | fa0515 | expected: No such file or directory | 7baec7 |
| 5 | 2026-10-10T23:14:56Z | T011 | VO-001 | green | one | tests.structure.test_manifest | pass | yes | - | tests/structure/test_manifest.py | fa0515 | - | 9c8723 |
| 6 | 2026-10-10T23:15:01Z | T012 | VO-002 | red | one | tests.structure.test_manifest | fail | yes | assertion | tests/structure/test_manifest.py | e9daaa | expected: KeyError: 'provides' | a995a7 |
| 7 | 2026-10-10T23:15:07Z | T013 | VO-002 | green | one | tests.structure.test_manifest | pass | yes | - | tests/structure/test_manifest.py | e9daaa | - | 9d017b |
| 8 | 2026-10-10T23:15:25Z | T014 | VO-003 | red | one | tests.structure.test_upstream_region | fail | yes | assertion | tests/structure/test_upstream_region.py | 3ea08c | expected: No such file or directory | cd318f |
| 9 | 2026-10-10T23:15:39Z | T016 | VO-003 | green | one | tests.structure.test_upstream_region | pass | yes | - | tests/structure/test_upstream_region.py | 3ea08c | - | b50e7e |
| 10 | 2026-10-10T23:15:57Z | T017 | VO-005 | red | one | tests.structure.test_grill_context | fail | no | assertion | tests/structure/test_grill_context.py | 595999 | failed for a different reason; Test failed for the intended reason (script missing); my --expect text named the wrong message. Re-run as #11 with the correct text | 6172ca |
| 11 | 2026-10-10T23:16:00Z | T017 | VO-005 | red | one | tests.structure.test_grill_context | fail | yes | assertion | tests/structure/test_grill_context.py | 595999 | expected: grill-context.sh: No such file or directory | 3e6b9c |
| 12 | 2026-10-10T23:16:09Z | T018 | VO-005 | green | one | tests.structure.test_grill_context | pass | yes | - | tests/structure/test_grill_context.py | 595999 | - | 61b3ff |
| 13 | 2026-10-10T23:16:22Z | T019 | VO-006 | red | one | tests.structure.test_grill_context.Interactivity | fail | yes | assertion | tests/structure/test_grill_context.py | ed98b9 | expected: KeyError: 'interactive' | 1c3cd3 |
| 14 | 2026-10-10T23:16:28Z | T020 | VO-006 | green | one | tests.structure.test_grill_context | pass | yes | - | tests/structure/test_grill_context.py | ed98b9 | - | bfda2a |
| 15 | 2026-10-10T23:16:36Z | T021 | VO-007 | red | one | tests.structure.test_grill_context.ReadOnly | pass | no | - | tests/structure/test_grill_context.py | c6e887 | passed on first run: investigate | 54e064 |
| 16 | 2026-10-10T23:16:44Z | T021 | VO-007 | red | one | tests.structure.test_grill_context.ReadOnly | fail | yes | assertion | tests/structure/test_grill_context.py | c6e887 | expected: AssertionError | 75eeee |
| 17 | 2026-10-10T23:16:48Z | T022 | VO-007 | green | one | tests.structure.test_grill_context | pass | yes | - | tests/structure/test_grill_context.py | c6e887 | - | 72f5bc |
| 18 | 2026-10-10T23:16:59Z | T023 | VO-008 | red | one | tests.structure.test_grill_label | fail | yes | assertion | tests/structure/test_grill_label.py | 723d6b | expected: grill-label.sh | c8bdf3 |
| 19 | 2026-10-10T23:17:09Z | T024 | VO-008 | green | one | tests.structure.test_grill_label | pass | yes | - | tests/structure/test_grill_label.py | 723d6b | - | e1b091 |
| 20 | 2026-10-10T23:17:17Z | T025 | VO-009 | red | one | tests.structure.test_grill_label.LabelReplacementAndFailure | fail | yes | assertion | tests/structure/test_grill_label.py | 9d7937 | expected: AssertionError | 6706a4 |
| 21 | 2026-10-10T23:17:31Z | T026 | VO-009 | green | one | tests.structure.test_grill_label | pass | yes | - | tests/structure/test_grill_label.py | 9d7937 | - | 53f090 |
| 22 | 2026-10-10T23:17:41Z | T027 | VO-011 | red | one | tests.install.test_install | fail | no | assertion | tests/install/test_install.py | fffc7e | failed for a different reason; Failed for the intended reason (declared command file missing); the --expect text I gave did not match. Re-run with the right text | 8558cc |
| 23 | 2026-10-10T23:17:46Z | T027 | VO-011 | red | one | tests.install.test_install | fail | yes | assertion | tests/install/test_install.py | fffc7e | expected: commands/speckit.grill-specify.auto.md | cc227f |
| 24 | 2026-10-10T23:17:49Z | T028 | VO-011 | green | one | tests.install.test_install | pass | yes | - | tests/install/test_install.py | fffc7e | - | 16960a |
| 25 | 2026-10-10T23:17:53Z | - | - | checkpoint | fast | - | pass | yes | - | - | - | - | 6b27d8 |
| 26 | 2026-10-10T23:19:11Z | T029 | VO-015 | red | one | tests.behaviour.test_nested_start | fail | yes | assertion | tests/behaviour/test_nested_start.py | f40dbf | expected: AssertionError | a5e8b4 |
| 27 | 2026-10-10T23:20:30Z | T029 | VO-015 | red | one | tests.behaviour.test_nested_start | fail | yes | assertion | tests/behaviour/test_nested_start.py | 58d544 | expected: AssertionError | abd508 |
| 28 | 2026-10-10T23:21:33Z | T029 | VO-015 | red | one | tests.behaviour.test_nested_start | pass | no | - | tests/behaviour/test_nested_start.py | b84390 | passed on first run: investigate | 606072 |
| 29 | 2026-10-10T23:24:00Z | T031 | VO-015 | green | one | tests.behaviour.test_nested_start | pass | yes | - | tests/behaviour/test_nested_start.py | b84390 | - | ab45de |
| 30 | 2026-10-10T23:25:16Z | T032 | VO-016 | red | one | tests.behaviour.test_interview_saves | fail | yes | assertion | tests/behaviour/test_interview_saves.py | fe61dd | expected: stopped-early label missing | b503f3 |
| 31 | 2026-10-10T23:26:46Z | T033 | VO-017 | red | one | tests.behaviour.test_knowledge_docs | pass | no | - | tests/behaviour/test_knowledge_docs.py | 7599e5 | passed on first run: investigate | 8eeb5d |
| 32 | 2026-10-10T23:28:09Z | T034 | VO-016 | green | one | tests.behaviour.test_interview_saves | pass | yes | - | tests/behaviour/test_interview_saves.py | fe61dd | - | b13793 |
| 33 | 2026-10-10T23:29:49Z | T034 | VO-017 | green | one | tests.behaviour.test_knowledge_docs | pass | yes | - | tests/behaviour/test_knowledge_docs.py | 7599e5 | - | 8f717a |
| 34 | 2026-10-10T23:33:04Z | T035 | VO-018 | red | one | tests.behaviour.test_completion | fail | yes | assertion | tests/behaviour/test_completion.py | 193ad6 | expected: no outcome block was printed | e393ef |
| 35 | 2026-10-10T23:36:20Z | T036 | VO-018 | green | one | tests.behaviour.test_completion | fail | no | environment | tests/behaviour/test_completion.py | 193ad6 | Test harness limit: the scripted driver stopped at 14 turns before the interview (about 11-15 turns, model dependent) reached its outcome block. Driver cap raised to 26 in tests/support/agent.py; no assertion changed. Rerun passed as #36. | be2a6e |
| 36 | 2026-10-10T23:44:08Z | T036 | VO-018 | green | one | tests.behaviour.test_completion | pass | yes | - | tests/behaviour/test_completion.py | 193ad6 | - | a5f373 |
| 37 | 2026-10-10T23:51:24Z | T037 | VO-031 | red | one | tests.behaviour.test_completion.WriteBoundary | pass | no | - | tests/behaviour/test_completion.py | ed4eb6 | passed on first run: investigate | ac5af4 |
| 38 | 2026-10-10T23:55:21Z | T038 | VO-031 | green | one | tests.behaviour.test_completion.WriteBoundary | pass | yes | - | tests/behaviour/test_completion.py | ed4eb6 | - | f8c4f5 |
| 39 | 2026-10-10T23:56:42Z | T039 | VO-030 | red | one | tests.behaviour.test_nothing_to_settle | fail | yes | assertion | tests/behaviour/test_nothing_to_settle.py | 450cab | expected: AssertionError | 1ffb0f |
| 40 | 2026-10-10T23:58:10Z | T040 | VO-030 | green | one | tests.behaviour.test_nothing_to_settle | fail | no | assertion | tests/behaviour/test_nothing_to_settle.py | 450cab | Fixture tests/fixtures/specs/settled was not actually settled; the interview found real ambiguities. Fixture rewritten; no assertion changed. | 0cf027 |
| 41 | 2026-10-11T00:01:00Z | T040 | VO-030 | green | one | tests.behaviour.test_nothing_to_settle | fail | no | assertion | tests/behaviour/test_nothing_to_settle.py | 450cab | Fixture tests/fixtures/specs/settled was not actually settled; the interview found real ambiguities. Fixture rewritten; no assertion changed. | 708932 |
| 42 | 2026-10-11T00:05:10Z | T040 | VO-030 | green | one | tests.behaviour.test_nothing_to_settle | fail | no | unreliable | tests/behaviour/test_nothing_to_settle.py | 450cab | Reply-count proxy (at most 3 replies) passed in some runs and failed in others against the same code and fixture, because the model sometimes takes an extra turn. Replaced by an outcome-field assertion (XC recorded). | c1fe4d |
| 43 | 2026-10-11T00:07:24Z | T040 | VO-030 | green | one | tests.behaviour.test_nothing_to_settle | fail | no | unreliable | tests/behaviour/test_nothing_to_settle.py | 450cab | Reply-count proxy (at most 3 replies) passed in some runs and failed in others against the same code and fixture, because the model sometimes takes an extra turn. Replaced by an outcome-field assertion (XC recorded). | 6da250 |
| 44 | 2026-10-11T00:09:22Z | T040 | VO-030 | green | one | tests.behaviour.test_nothing_to_settle | pass | yes | - | tests/behaviour/test_nothing_to_settle.py | 6e9685 | - | b58cfa |
| 45 | 2026-10-11T00:10:51Z | T041 | VO-033 | red | one | tests.behaviour.test_persistence_failure | pass | no | - | tests/behaviour/test_persistence_failure.py | ab42ab | passed on first run: investigate | f11f90 |
| 46 | 2026-10-11T00:12:05Z | T042 | VO-033 | green | one | tests.behaviour.test_persistence_failure | pass | yes | - | tests/behaviour/test_persistence_failure.py | ab42ab | - | 152ab7 |
| 47 | 2026-10-11T00:22:17Z | - | - | checkpoint | live | - | fail | no | unclassified | - | - | timed out | 6df933 |
| 48 | 2026-10-11T00:36:25Z | - | - | checkpoint | live | - | fail | no | unreliable | - | - | Phase 3 checkpoint; rerun with a longer timeout after #47 timed out at 600s; 11 of 12 live tests passed; test_completion failed to reach an outcome block, then passed alone on rerun (#36 earlier, and again just now in 10 turns) with identical code. Model-dependent turn count; driver now nudges for the outcome block after the gate is answered. | f313fe |
| 49 | 2026-10-11T00:39:46Z | T043 | VO-020 | red | one | tests.behaviour.test_setting.Strict | fail | yes | assertion | tests/behaviour/test_setting.py | 732a8d | expected: AssertionError | e09bf7 |
| 50 | 2026-10-11T00:40:25Z | T043 | VO-020 | red | one | tests.behaviour.test_setting.Strict | pass | no | - | tests/behaviour/test_setting.py | c8ad2a | passed on first run: investigate | c65f3b |
| 51 | 2026-10-11T00:41:02Z | T044 | VO-020 | green | one | tests.behaviour.test_setting.Strict | pass | yes | - | tests/behaviour/test_setting.py | c8ad2a | - | f54375 |
| 52 | 2026-10-11T00:41:26Z | T045 | VO-021 | red | one | tests.behaviour.test_setting.Off | fail | yes | assertion | tests/behaviour/test_setting.py | 3a8ae1 | expected: AssertionError | 48496e |
| 53 | 2026-10-11T00:41:40Z | T046 | VO-021 | green | one | tests.behaviour.test_setting.Off | pass | yes | - | tests/behaviour/test_setting.py | 3a8ae1 | - | 49ae88 |
| 54 | 2026-10-11T00:42:15Z | T047 | VO-022 | red | one | tests.behaviour.test_setting.UnknownValue | fail | yes | assertion | tests/behaviour/test_setting.py | a4373f | expected: AssertionError | f0cacc |
| 55 | 2026-10-11T00:43:39Z | T048 | VO-022 | green | one | tests.behaviour.test_setting | pass | yes | - | tests/behaviour/test_setting.py | a4373f | - | cb2585 |
| 56 | 2026-10-11T00:44:14Z | T049 | VO-019 | red | one | tests.behaviour.test_skip | pass | no | - | tests/behaviour/test_skip.py | c2d599 | passed on first run: investigate | 001852 |
| 57 | 2026-10-11T00:44:51Z | T050 | VO-019 | green | one | tests.behaviour.test_skip | pass | yes | - | tests/behaviour/test_skip.py | c2d599 | - | 65d559 |
| 58 | 2026-10-11T00:46:14Z | T051 | VO-023 | red | one | tests.behaviour.test_stop_resume | fail | yes | assertion | tests/behaviour/test_stop_resume.py | fa56d7 | expected: AssertionError | 25d0b2 |
| 59 | 2026-10-11T00:47:31Z | T052 | VO-023 | green | one | tests.behaviour.test_stop_resume | pass | yes | - | tests/behaviour/test_stop_resume.py | fa56d7 | - | 9f6869 |
| 60 | 2026-10-11T00:48:53Z | T053 | VO-029 | red | one | tests.behaviour.test_stop_resume.StopBeforeFirstAnswer | fail | yes | assertion | tests/behaviour/test_stop_resume.py | e8b538 | expected: AssertionError | 64fff0 |
| 61 | 2026-10-11T00:50:15Z | T054 | VO-029 | green | one | tests.behaviour.test_stop_resume.StopBeforeFirstAnswer | pass | yes | - | tests/behaviour/test_stop_resume.py | e8b538 | - | 88cc21 |
| 62 | 2026-10-11T00:53:58Z | T055 | VO-024 | red | one | tests.behaviour.test_stop_resume.ResumeStandalone | pass | no | - | tests/behaviour/test_stop_resume.py | 16feeb | passed on first run: investigate | 35df15 |
| 63 | 2026-10-11T00:56:58Z | T056 | VO-024 | green | one | tests.behaviour.test_stop_resume.ResumeStandalone | pass | yes | - | tests/behaviour/test_stop_resume.py | 16feeb | - | e8ed8a |
| 64 | 2026-10-11T00:58:49Z | T057 | VO-025 | red | one | tests.behaviour.test_standalone | pass | no | - | tests/behaviour/test_standalone.py | 9aff2b | passed on first run: investigate | 3f7d2b |
| 65 | 2026-10-11T00:59:56Z | T058 | VO-025 | green | one | tests.behaviour.test_standalone | fail | no | unreliable | tests/behaviour/test_standalone.py | 9aff2b | Failed once, then passed in two further runs (a direct unittest run and #66) with no change to code or test; model-dependent. | 7cc976 |
| 66 | 2026-10-11T01:02:45Z | T058 | VO-025 | green | one | tests.behaviour.test_standalone | pass | yes | - | tests/behaviour/test_standalone.py | 9aff2b | - | 38a83e |
| 67 | 2026-10-11T01:04:09Z | T059 | VO-026 | red | one | tests.behaviour.test_nested_hooks | pass | no | - | tests/behaviour/test_nested_hooks.py | 8ec289 | passed on first run: investigate | a77270 |
| 68 | 2026-10-11T01:05:15Z | T060 | VO-026 | green | one | tests.behaviour.test_nested_hooks | fail | no | defect | tests/behaviour/test_nested_hooks.py | 8ec289 | Real gap: after the outcome block the model ended its turn without running specify's remaining after_specify hook (marker log empty). Entry point and wrapper wording strengthened to continue the hooks; rerun #69 passes. | 93d46f |
| 69 | 2026-10-11T01:07:39Z | T060 | VO-026 | green | one | tests.behaviour.test_nested_hooks | pass | yes | - | tests/behaviour/test_nested_hooks.py | 8ec289 | - | 36bf73 |
| 70 | 2026-10-11T01:15:53Z | T061 | VO-027 | red | one | tests.behaviour.test_standalone.StandaloneClarifyHooks | fail | yes | assertion | tests/behaviour/test_standalone.py | a16e02 | expected: AssertionError | f22033 |
| 71 | 2026-10-11T01:19:13Z | T062 | VO-027 | green | one | tests.behaviour.test_standalone.StandaloneClarifyHooks | pass | yes | - | tests/behaviour/test_standalone.py | a16e02 | - | 7d1f58 |
| 72 | 2026-10-11T01:49:51Z | - | - | checkpoint | live | - | fail | no | unreliable | - | - | Phase 6 checkpoint; 27 of 28 live tests passed; test_interview_saves failed once (3rd answer not yet saved when the next question appeared) and passed on immediate rerun with identical code. Intermittent, model-dependent; reported as unreliable, not as verified by this checkpoint. | 6e34e3 |
| 73 | 2026-10-11T01:53:09Z | T063 | VO-028 | red | one | tests.behaviour.test_unattended | fail | yes | assertion | tests/behaviour/test_unattended.py | 90de2c | expected: AssertionError | ec47c4 |
| 74 | 2026-10-11T01:54:17Z | T064 | VO-028 | green | one | tests.behaviour.test_unattended | pass | yes | - | tests/behaviour/test_unattended.py | 90de2c | - | f90f0f |
| 75 | 2026-10-11T01:54:24Z | - | - | checkpoint | fast | - | pass | yes | - | - | - | - | 88ae11 |
| 76 | 2026-10-11T01:54:37Z | T067 | VO-012 | red | one | tests.install.test_remove | pass | no | - | tests/install/test_remove.py | 122325 | passed on first run: investigate | c59f34 |
| 77 | 2026-10-11T01:54:45Z | T068 | VO-012 | green | one | tests.install.test_remove | pass | yes | - | tests/install/test_remove.py | 122325 | - | 52249b |
| 78 | 2026-10-11T01:54:54Z | T069 | VO-013 | red | one | tests.install.test_coexist | pass | no | - | tests/install/test_coexist.py | df80a0 | passed on first run: investigate | a6ce91 |
| 79 | 2026-10-11T01:55:02Z | T070 | VO-013 | green | one | tests.install.test_coexist | pass | yes | - | tests/install/test_coexist.py | df80a0 | - | 330331 |
| 80 | 2026-10-11T01:55:12Z | T073 | VO-004 | red | one | tests.structure.test_provenance | fail | yes | assertion | tests/structure/test_provenance.py | 485ddb | expected: AssertionError | b7ec2d |
| 81 | 2026-10-11T01:55:28Z | T075 | VO-004 | green | one | tests.structure.test_provenance | pass | yes | - | tests/structure/test_provenance.py | 485ddb | - | c0c86a |
| 82 | 2026-10-11T02:12:04Z | T077 | VO-032 | red | one | tests.behaviour.test_equivalence | fail | yes | assertion | tests/behaviour/test_equivalence.py | 437206 | expected: AssertionError | 7530e4 |
| 83 | 2026-10-11T02:26:38Z | T078 | VO-032 | green | one | tests.behaviour.test_equivalence | fail | no | unreliable | tests/behaviour/test_equivalence.py | 4e3e63 | Single-sample comparison of two model-driven interviews: upstream's run also rewrote the User Scenarios section and ours did not. Not attributable to the wrapper; the test model is raised for this test alone (R15). | dc93e8 |
| 84 | 2026-10-11T02:31:17Z | T078 | VO-032 | green | one | tests.behaviour.test_equivalence | fail | no | unreliable | tests/behaviour/test_equivalence.py | 6a5636 | Sections matched on sonnet, but the number of Clarifications differed (10 vs upstream 5; a later single run of ours recorded 6). The count of questions an LLM interviewer asks varies run to run for both extensions; no wrapper-caused difference was found. | 78ae28 |
| 85 | 2026-10-11T02:35:10Z | T079 | VO-034 | red | one | tests.regression.test_user_level_isolation | pass | no | - | tests/regression/test_user_level_isolation.py | f477a5 | passed on first run: investigate | fd9fcf |
| 86 | 2026-10-11T02:36:11Z | T080 | VO-034 | green | one | tests.regression.test_user_level_isolation | pass | yes | - | tests/regression/test_user_level_isolation.py | f477a5 | - | 06609b |
| 87 | 2026-10-11T02:37:06Z | T081 | VO-036 | red | one | tests.behaviour.test_open_markers | pass | no | - | tests/behaviour/test_open_markers.py | 5a9b90 | passed on first run: investigate | a24a71 |
| 88 | 2026-10-11T02:38:01Z | T082 | VO-036 | green | one | tests.behaviour.test_open_markers | pass | yes | - | tests/behaviour/test_open_markers.py | 5a9b90 | - | 0f4c9d |
| 89 | 2026-10-11T02:56:50Z | T083 | VO-037 | red | one | tests.regression.test_cross_grill | fail | yes | assertion | tests/regression/test_cross_grill.py | 6715d3 | expected: AssertionError | f5efc1 |
| 90 | 2026-10-11T03:42:43Z | T083 | VO-037 | red | one | tests.regression.test_cross_grill | pass | no | - | tests/regression/test_cross_grill.py | 6715d3 | passed on first run: investigate | cbc821 |
| 91 | 2026-10-11T04:08:20Z | T084 | VO-037 | green | one | tests.regression.test_cross_grill | pass | yes | - | tests/regression/test_cross_grill.py | 6715d3 | - | d7265d |
| 92 | 2026-10-11T04:08:34Z | - | - | checkpoint | fast | - | pass | yes | - | - | - | - | 4ad5ed |
| 93 | 2026-10-11T04:08:43Z | T085 | VO-038 | red | one | tests.structure.test_bash32 | pass | no | - | tests/structure/test_bash32.py | 68f81a | passed on first run: investigate | 45b70d |
| 94 | 2026-10-11T04:08:43Z | T086 | VO-038 | green | one | tests.structure.test_bash32 | pass | yes | - | tests/structure/test_bash32.py | 68f81a | - | 134d54 |
| 95 | 2026-10-11T04:08:44Z | T088 | VO-014 | red | one | tests.release.test_release_install | fail | yes | assertion | tests/release/test_release_install.py | 223108 | expected: RuntimeError | 35e4b7 |
| 96 | 2026-10-11T04:42:37Z | - | - | checkpoint | live | - | fail | no | unreliable | - | - | Final live checkpoint; 29 of 33 live tests passed. Failures: test_nested_hooks (after-specify marker not run after the outcome block; passed 2 of 3 earlier runs), test_nested_start (opening had no '?' in a differently phrased reply), test_standalone clarify hooks (did not reach completion), and one more subtest in the unattended/equivalence group. Each passed on earlier runs with the same code; model-dependent, so these obligations are reported as intermittent, not as reliably verified. | b78ed6 |

## Exceptions

| ID | Time | Task | Obligations | Kind | Rationale | Alternative verification | Needs approval | Approved by |
|----|------|------|-------------|------|-----------|--------------------------|----------------|-------------|
| EX-01 | 2026-10-10T23:22:43Z | T029 | VO-015 | no-meaningful-red | The hook entry point already starts the vendored interview in the same session, which opens with a round of questions and writes nothing before the first answer; a first run of the live test therefore passes. Run #26/#27 failed for a different reason (the test input made specify itself ask a question), not because behaviour was missing. | The test is written and passes; it checks the files (no Clarifications, no label, no knowledge docs) and the opening text. T030 and T031 add the wrapper rules that the opening must also carry (point count, skip choice) and the test is rerun for the green record. | no | - |
| EX-02 | 2026-10-10T23:26:55Z | T033 | VO-017 | no-meaningful-red | Recording a term and a qualifying decision is upstream v1.0.1 behaviour carried verbatim between the markers, so the live test passes on its first run: a failing first run would not show missing wrapper behaviour. | The test is written and passes, asserting on files only: the term defined exactly once in CONTEXT.md and exactly one decision record, for the qualifying decision. T034 only adds the label rule and must leave this test passing, which its Green run shows. | no | - |
| EX-03 | 2026-10-10T23:51:38Z | T037 | VO-031 | no-meaningful-red | Upstream v1.0.1 already limits writes to the spec, checklist checkboxes and knowledge docs, and the wrapper adds only the label script, so a complete nested run changes only permitted paths on its first run. | The test is written and passes, snapshotting the whole project tree before and after a run that settles a term and a decision. T038 states the boundary explicitly in the wrapper and the test is rerun for the green record. | no | - |
| EX-04 | 2026-10-11T00:10:58Z | T041 | VO-033 | no-meaningful-red | Upstream v1.0.1's Persistence failure handling, carried verbatim between the markers, already refuses to mark the point resolved, states the failure and stops, so the live test passes on its first run. | The test is written and passes against a read-only knowledge directory, asserting the failure is stated, the outcome is not 'completed' and no knowledge doc appears elsewhere. T042 adds the nested-run reporting rule and the test is rerun for the green record. | no | - |
| EX-05 | 2026-10-11T00:40:32Z | T043 | VO-020 | no-meaningful-red | The opening rule written for T031 offers the skip choice only for a nested run with setting on, so strict already gets no skip choice and the test passes on its first run. Run #49 failed only because the first version of the assertion matched the word 'skip' in the grill's own prose; it was replaced by a behavioural check (see the recorded expectation change). | The test passes and checks behaviour: the opening states a count and a question, and answering 'skip' does not end the run as skipped. T044 states the strict rule explicitly and the test is rerun for the green record. | no | - |
| EX-06 | 2026-10-11T00:44:20Z | T049 | VO-019 | no-meaningful-red | The skip rule and the skipped outcome block were already written for T048, because VO-022 (an unknown setting value, then skip) needs a skipped outcome to carry its Warning line. The skip behaviour therefore exists when VO-019's test is first run. | The test is written and passes, asserting on files (an identical project tree, no label) and the outcome block's first line and fields. T050 has no further wording to add; its green run is recorded against the same test. | no | - |
| EX-07 | 2026-10-11T00:54:09Z | T055 | VO-024 | no-meaningful-red | Upstream v1.0.1 re-reads the spec and its Clarifications and does not re-ask a recorded question, and the label script already replaces a label in place, so the standalone resume passes on its first run. | The test is written and passes, asserting on files: earlier Clarifications lines unchanged and none recorded twice, one plain label with today's date. T056 states the resume rule in the wrapper and the test is rerun for the green record. | no | - |
| EX-08 | 2026-10-11T00:58:53Z | T057 | VO-025 | no-meaningful-red | The wrapper's off rule and skip choice were written for nested runs only, so a standalone run already ignores the setting and offers no skip choice; the test passes on its first run. | The test is written and passes at both settings (off and on). T058 states the standalone rule explicitly and the test is rerun for the green record. | no | - |
| EX-09 | 2026-10-11T01:04:14Z | T059 | VO-026 | no-meaningful-red | The recorded upstream patch (nested-hooks.patch) and the entry point's hand-back already stop a nested grill from processing clarify hooks and return control to specify, so the live test passes on its first run. | The test is written and passes: the marker log shows no hook ran before the grill ended and exactly one after-specify marker afterwards. T060 states the rule in the wrapper and the test is rerun for the green record. | no | - |
| EX-10 | 2026-10-11T01:54:44Z | T067 | VO-012 | no-meaningful-red | The manifest already declares every installed file and the Spec Kit CLI removes exactly its own hook entries and command skills, so removal is clean on the first run of the test. | The test is written and passes against a project holding another extension, a grilled spec and knowledge docs. T068 documents removal in README.md and the test is rerun for the green record. | no | - |
| EX-11 | 2026-10-11T01:55:00Z | T069 | VO-013 | no-meaningful-red | This extension's commands, scripts and config use the speckit.grill-specify namespace and its own extension id, so they cannot conflict with upstream's speckit.grill commands; the install test passes in both orders on its first run. | The test is written and passes, asserting every command of both extensions is present and upstream's installed command files hash the same as when upstream is installed alone. T070 documents the coexistence in README.md and the test is rerun for the green record. | no | - |
| EX-12 | 2026-10-11T02:35:15Z | T079 | VO-034 | no-meaningful-red | The extension was built to ship only project-level files and no subagent delegation, so the isolation test passes on its first run: the shipped command text names no user-level skill or agent and both grills open with a config directory holding only credentials. | The test is written and passes. T080 states the project-level-only requirement in README.md and the test is rerun for the green record. | no | - |
| EX-13 | 2026-10-11T02:37:11Z | T081 | VO-036 | no-meaningful-red | Upstream's ambiguity scan already counts [NEEDS CLARIFICATION] markers and failed checklist items among the points to settle, so the nested grill opens with a question and settles the marker on the test's first run. The task text anticipates this case. | The test is written and passes, asserting on files (marker gone, answer in Clarifications) and that the grill opens with a question. T082 adds no wrapper text, as its task allows, and the test is rerun for the green record. | no | - |
| EX-14 | 2026-10-11T03:43:03Z | T083 | VO-037 | no-meaningful-red | Upstream re-reads Clarifications and does not re-ask a recorded question, and this extension's label script keeps exactly one label directly under Status, so the cross-grill test passes in both directions on its first run. The task text anticipates this. | The test is written and passes in both directions (ours then upstream's, and upstream's then ours), asserting earlier Clarifications unchanged, none recorded twice and exactly one label under Status. T084 changes nothing and the test is rerun for the green record. | no | - |
| EX-15 | 2026-10-11T04:08:43Z | T085 | VO-038 | no-meaningful-red | Both scripts were written for Bash 3.2 from the start and use none of the listed constructs, so the construct check passes on its first run; the second part reports skipped because no Bash 3.2 binary is supplied (never as passed). | The test is written and passes the construct check. T086 makes the two script test files run the scripts through GRILL_TEST_BASH, and the run is recorded with the second part shown as skipped. | no | - |

## Expectation changes

| ID | Time | Task | Files | Requirements | Justification | Alters behaviour | Approved by | New fingerprint |
|----|------|------|-------|--------------|---------------|------------------|-------------|-----------------|
| XC-01 | 2026-10-10T23:24:09Z | T031 | tests/behaviour/test_nested_start.py | FR-001 | Correction to the test's input description, no assertion changed: the first description left a discount choice open, so specify itself asked a clarification question and the hook never ran, which tested specify and not the grill's start. The description now settles every choice specify would otherwise ask about (FR-001: the grill starts in the same session straight after specify). | no | - | b84390 |
| XC-02 | 2026-10-10T23:24:12Z | T030 | tests/behaviour/test_nested_start.py | FR-001 | Same correction as XC-01 (the test input description was made unambiguous so specify does not ask its own question); no assertion changed. T030 and T031 deliver VO-015 together, with one Green run. | no | - | b84390 |
| XC-03 | 2026-10-11T00:09:33Z | T040 | tests/behaviour/test_nothing_to_settle.py | FR-024 | Correction: the assertion that at most three replies occur was an unreliable proxy for 'asks only the satisfaction question' and depended on model turn-taking. It is replaced by the outcome block's 'Questions answered: 0' plus the existing check that the spec has no Clarifications section, which verify FR-024 directly. | no | - | 6e9685 |
| XC-04 | 2026-10-11T00:41:02Z | T044 | tests/behaviour/test_setting.py | FR-012 | Correction: the first assertion matched the word 'skip' anywhere in the reply, which also matched the grill saying there is no skip option. Replaced by a behavioural check that asking to skip does not end the run as skipped; no requirement changed. | no | - | c8ad2a |

## Decisions

| ID | Opened | Question | Tasks | Status | Answer | Decided by | Resolved |
|----|--------|----------|-------|--------|--------|------------|----------|
| DN-01 | 2026-10-10T23:13:35Z | Spec Kit 1.1.3's specify template runs after_specify hooks in .specify/extensions.yml file order (install order), not by priority, so priority 5 alone does not satisfy FR-009 (grill first). How should the extension guarantee ordering? Options: (a) document install-first plus priority; (b) the entry-point command reorders its own entry in extensions.yml at run time; (c) other. | T065, T066, T071, T072 | open | - | - | - |
| DN-02 | 2026-10-11T02:33:52Z | VO-032 (equivalence with upstream) compares the number of Clarifications recorded by two LLM-driven interviews on the same scripted answers; this count varies run to run for the same code (ours: 10, 6; upstream: 5). Options: (a) compare sections, knowledge-doc paths and coverage statuses but allow the question count to differ by a stated tolerance or only require that every scripted topic is recorded once; (b) keep exact equality and accept the test as unreliable (VO-032 reported not verified); (c) exempt SC-003 from automation and verify it by manual review. Which should apply? | T078 | open | - | - | - |
