"""A scripted developer: drives `claude -p` one turn at a time with --resume."""
import json
import os
import subprocess
import uuid

OUTCOME_PREFIX = "GRILL OUTCOME:"
DEFAULT_MODEL = os.environ.get("GRILL_TEST_MODEL", "haiku")


class Session:
    def __init__(self, project, model=None, env=None, config_dir=None):
        self.project = str(project)
        self.model = model or DEFAULT_MODEL
        self.env = dict(os.environ)
        # Live tests assume a human is present unless a test says otherwise.
        self.env["SPECKIT_GRILL_NONINTERACTIVE"] = "0"
        self.env.update(env or {})
        # A value of None removes the variable, so a test can leave a signal unset.
        self.env = {k: v for k, v in self.env.items() if v is not None}
        if config_dir:
            self.env["CLAUDE_CONFIG_DIR"] = str(config_dir)
        self.session_id = str(uuid.uuid4())
        self.turns = []

    def say(self, message, timeout=900):
        """Send one message and return the agent's text for this turn."""
        args = ["claude", "-p", message, "--model", self.model,
                "--output-format", "json", "--permission-mode", "acceptEdits",
                "--allowedTools", "Bash,Read,Write,Edit,Glob,Grep"]
        if self.turns:
            args += ["--resume", self.session_id]
        else:
            args += ["--session-id", self.session_id]
        proc = subprocess.run(args, cwd=self.project, env=self.env,
                              capture_output=True, text=True, timeout=timeout)
        if proc.returncode != 0:
            raise RuntimeError("claude failed (%d): %s" % (proc.returncode, proc.stderr))
        try:
            text = json.loads(proc.stdout).get("result", "")
        except ValueError:
            text = proc.stdout
        self.turns.append(text)
        log = os.environ.get("GRILL_TEST_LOG")
        if log:
            with open(log, "a") as handle:
                handle.write("\n=== SENT: %s\n--- REPLY:\n%s\n" % (message[:200], text))
        return text


def outcome_block(text):
    """The block starting at the line that begins `GRILL OUTCOME:`, or None."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith(OUTCOME_PREFIX):
            block = []
            for rest in lines[i:]:
                if not rest.strip() and block:
                    break
                block.append(rest.rstrip())
            return "\n".join(block)
    return None


def outcome_first_line(text):
    block = outcome_block(text)
    return block.splitlines()[0].strip() if block else None


def drive_to_end(session, first_message, answer="Option A, the recommended one.",
                 finish="Finish and proceed", max_turns=40):
    """Start the interview with first_message and answer until an outcome block is printed.

    The satisfaction gate is recognised by its option text; it is answered with `finish`.
    Returns (replies, outcome_block_or_None).
    """
    replies = []
    message = first_message
    finished = False
    for _ in range(max_turns):
        reply = session.say(message)
        replies.append(reply)
        block = outcome_block(reply)
        if block:
            return replies, block
        if "Finish and proceed" in reply:
            message = finish
            finished = True
        elif finished:
            message = "Continue, and print the GRILL OUTCOME block now."
        else:
            message = answer
    return replies, None


def drive_standalone(session, first_message, answer="Option A, the recommended one.",
                     finish="Finish and proceed", max_turns=40):
    """Run a standalone grill: answer until the gate, confirm it, return (replies, final_reply)."""
    replies = []
    message = first_message
    for _ in range(max_turns):
        reply = session.say(message)
        replies.append(reply)
        if message == finish:
            return replies, reply
        message = finish if "Finish and proceed" in reply else answer
    return replies, None
