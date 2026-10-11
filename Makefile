# Test commands for the Specify Grill extension. Declared in the plan's Verification Plan.
# `run-level` treats "no tests found" (exit 5) as a pass so that a level with no tests yet
# does not fail the target; any real failure still exits non-zero.
PY ?= python3
T ?=

define run-level
$(PY) -B -m unittest discover -s tests/$(1) -t . ; rc=$$? ; [ $$rc -eq 0 ] || [ $$rc -eq 5 ]
endef

.PHONY: test test-one test-live test-release

test:
	@$(call run-level,structure)
	@$(call run-level,install)

test-one:
	$(PY) -B -m unittest $(T)

test-live:
	@$(call run-level,behaviour)
	@$(call run-level,regression)

test-release:
	@$(call run-level,release)
