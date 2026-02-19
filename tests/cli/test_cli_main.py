import sys
import pytest

from gitter.cli.main import main


def run_cli(monkeypatch, args):
    monkeypatch.setattr(sys, "argv", ["gitter"] + args)
    with pytest.raises(SystemExit) as exc:
        main()
    return exc.value.code


def test_init_creates_repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    exit_code = run_cli(monkeypatch, ["init"])

    assert exit_code == 0
    assert (tmp_path / ".gitter").exists()


def test_add_without_repo_fails(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    exit_code = run_cli(monkeypatch, ["add", "file.txt"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Not a gitter repository" in captured.out


def test_commit_without_staging(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    exit_code = run_cli(monkeypatch, ["commit", "-m", "msg"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Nothing to commit" in captured.out


def test_unknown_command(monkeypatch, capsys):
    exit_code = run_cli(monkeypatch, ["unknown"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Unknown command" in captured.out


def test_missing_commit_message(monkeypatch, capsys):
    exit_code = run_cli(monkeypatch, ["commit"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Usage" in captured.out

def test_full_add_and_commit_flow(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    # init
    run_cli(monkeypatch, ["init"])

    # create file
    file = tmp_path / "file.txt"
    file.write_text("hello")

    # add
    exit_code = run_cli(monkeypatch, ["add", "file.txt"])
    assert exit_code == 0

    # commit
    exit_code = run_cli(monkeypatch, ["commit", "-m", "initial"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Committed as" in captured.out

def test_no_args_prints_banner(monkeypatch, capsys):
    exit_code = run_cli(monkeypatch, [])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Gitter CLI" in captured.out

def test_global_help(monkeypatch, capsys):
    exit_code = run_cli(monkeypatch, ["help"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Available commands" in captured.out


def test_command_help(monkeypatch, capsys):
    exit_code = run_cli(monkeypatch, ["help", "commit"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "gitter commit -m <message>" in captured.out


def test_help_unknown_command(monkeypatch, capsys):
    exit_code = run_cli(monkeypatch, ["help", "unknown"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Unknown command" in captured.out

def test_status_untracked(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    file = tmp_path / "file.txt"
    file.write_text("hello")

    exit_code = run_cli(monkeypatch, ["status"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Untracked" in captured.out
    assert "file.txt" in captured.out

def test_status_staged(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    file = tmp_path / "file.txt"
    file.write_text("hello")

    run_cli(monkeypatch, ["add", "file.txt"])

    exit_code = run_cli(monkeypatch, ["status"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Staged" in captured.out

def test_status_clean(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    file = tmp_path / "file.txt"
    file.write_text("hello")

    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "msg"])

    exit_code = run_cli(monkeypatch, ["status"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Working tree clean" in captured.out

def test_log_no_commits(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    exit_code = run_cli(monkeypatch, ["log"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "No commits yet" in captured.out

def test_log_single_commit(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    file = tmp_path / "file.txt"
    file.write_text("hello")

    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "initial"])

    exit_code = run_cli(monkeypatch, ["log"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "commit" in captured.out
    assert "initial" in captured.out

def test_log_multiple_commits(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    file = tmp_path / "file.txt"
    file.write_text("v1")

    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "first"])

    file.write_text("v2")
    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "second"])

    exit_code = run_cli(monkeypatch, ["log"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "second" in captured.out
    assert "first" in captured.out
