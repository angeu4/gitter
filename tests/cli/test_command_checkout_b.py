import re


def test_checkout_b_requires_name(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["checkout", "-b"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == "Branch name required\n"


def test_checkout_b_creates_and_switches(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["checkout", "-b", "dev"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Switched to a new branch 'dev'\n"


def test_checkout_b_branch_already_exists(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    run_cli(monkeypatch, ["branch", "dev"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["checkout", "-b", "dev"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == "Branch already exists\n"


def test_checkout_b_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["checkout", "-b", "feature"])
    captured = capsys.readouterr()

    assert exit_code == 0
    pattern = r"^Switched to a new branch 'feature'\n$"
    assert re.search(pattern, captured.out)