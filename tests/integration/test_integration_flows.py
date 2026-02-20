"""
Integration Test Suite for Gitter CLI

These tests validate realistic user flows across multiple commands,
ensuring proper state transitions and cross-command consistency.

All assertions strictly match current CLI behavior.
"""

import re


# ------------------------------------------------------------
# Scenario 1: Full repository lifecycle
# ------------------------------------------------------------

def test_full_repository_lifecycle(monkeypatch, capsys, run_cli, tmp_path):
    """
    Flow:
    init → add → commit → status → log
    """

    monkeypatch.chdir(tmp_path)

    # init
    exit_code = run_cli(monkeypatch, ["init"])
    assert exit_code == 0
    capsys.readouterr()

    # create file
    file = tmp_path / "file.txt"
    file.write_text("hello")

    # add
    run_cli(monkeypatch, ["add", "file.txt"])
    capsys.readouterr()

    # commit
    exit_code = run_cli(monkeypatch, ["commit", "-m", "initial commit"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert re.search(r"Committed as [0-9a-f]{40}", captured.out)

    # status
    run_cli(monkeypatch, ["status"])
    captured = capsys.readouterr()
    assert "Working tree clean" in captured.out

    # log
    run_cli(monkeypatch, ["log"])
    captured = capsys.readouterr()
    assert "initial commit" in captured.out


# ------------------------------------------------------------
# Scenario 2: Branch creation and checkout
# ------------------------------------------------------------

def test_branch_creation_and_checkout(monkeypatch, capsys, run_cli, tmp_path):
    """
    Flow:
    init → commit → branch feature → checkout feature
    """

    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    (tmp_path / "a.txt").write_text("v1")
    run_cli(monkeypatch, ["add", "a.txt"])
    run_cli(monkeypatch, ["commit", "-m", "base"])
    capsys.readouterr()

    # branch create
    exit_code = run_cli(monkeypatch, ["branch", "feature"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "feature" in captured.out

    # checkout
    exit_code = run_cli(monkeypatch, ["checkout", "feature"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Switched to branch 'feature'" in captured.out


# ------------------------------------------------------------
# Scenario 3: commit -am flow
# ------------------------------------------------------------

def test_commit_am_flow(monkeypatch, capsys, run_cli, tmp_path):
    """
    Flow:
    init → add → commit → modify → commit -am
    """

    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    file = tmp_path / "file.txt"
    file.write_text("v1")

    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "first"])
    capsys.readouterr()

    # modify tracked file
    file.write_text("v2")

    exit_code = run_cli(monkeypatch, ["commit", "-am", "update"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert re.search(r"Committed as [0-9a-f]{40}", captured.out)


# ------------------------------------------------------------
# Scenario 4: Reset flow
# ------------------------------------------------------------

def test_reset_head(monkeypatch, capsys, run_cli, tmp_path):
    """
    Flow:
    init → commit → commit → reset HEAD~1
    """

    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    file = tmp_path / "file.txt"

    file.write_text("v1")
    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "first"])
    capsys.readouterr()

    file.write_text("v2")
    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "second"])
    capsys.readouterr()

    # reset
    exit_code = run_cli(monkeypatch, ["reset", "HEAD~1"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == ""  # reset currently silent

    # log should not contain second commit
    run_cli(monkeypatch, ["log"])
    captured = capsys.readouterr()

    assert "second" not in captured.out
    assert "first" in captured.out


# ------------------------------------------------------------
# Scenario 5: Checkout with uncommitted changes
# ------------------------------------------------------------

def test_checkout_with_uncommitted_changes(monkeypatch, capsys, run_cli, tmp_path):
    """
    Flow:
    init → commit → branch → modify → checkout
    """

    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    file = tmp_path / "file.txt"
    file.write_text("v1")

    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "base"])
    capsys.readouterr()

    run_cli(monkeypatch, ["branch", "dev"])
    capsys.readouterr()

    # modify without committing
    file.write_text("modified")

    exit_code = run_cli(monkeypatch, ["checkout", "dev"])
    captured = capsys.readouterr()

    # Current implementation allows switch
    assert exit_code == 0
    assert "Switched to branch 'dev'" in captured.out