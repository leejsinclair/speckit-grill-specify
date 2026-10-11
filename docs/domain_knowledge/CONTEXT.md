# Specify Grill

A Spec Kit extension that runs the grill-with-docs interview straight after a feature spec is written, so that no spec reaches planning with unresolved ambiguity.

## Language

**Grill**:
The exhaustive, one-question-at-a-time interview that clarifies a feature spec and records settled terms and decisions in the knowledge docs.
_Avoid_: Clarify (that is Spec Kit's separate five-question command), quiz

**Grill setting**:
The single project-level choice of how the grill starts after specify: on, strict or off. It has no effect on a standalone run.
_Avoid_: Mode, grill mode, policy

**On**:
The default grill setting: the grill starts without asking permission and its opening carries a skip choice.
_Avoid_: Offered, optional

**Strict**:
The grill setting under which the grill starts with no skip choice. It does not force the interview to be finished.
_Avoid_: Required, mandatory, enforced

**Skip**:
The developer's choice, at the grill's opening, not to be grilled; it leaves the spec untouched.
_Avoid_: Decline, opt out

**Stop early**:
The developer's choice to end a grill after at least one answer has been settled; settled answers are kept.
_Avoid_: Interrupt, abort, cancel

**Upstream**:
The `yoshi1220/speckit-grill-me` extension (id `grill`) whose with-docs interview this extension carries.
_Avoid_: Original, base

**Nested run**:
A grill started automatically by specify, as part of the same specify run.
_Avoid_: Hook run, automatic run

**Standalone run**:
A grill started directly by the developer, outside specify, to re-run or resume.
_Avoid_: Manual run

**Non-interactive run**:
A run that an explicit signal marks as having no human available to answer. A run with no such signal is interactive.
_Avoid_: Headless run, CI run

**Grill outcome**:
The one result of a nested run: completed, stopped early, skipped, switched off, or not run.

**Grilled-on label**:
The single dated line in a spec's header showing when the grill last ran on it and whether it was stopped early. It appears with the first saved answer and its absence means the spec has not been grilled.
