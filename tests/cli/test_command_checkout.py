import re


def test_checkout_nonexistent_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["checkout", "test"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert re.search(r"^Branch does not exist\n$", captured.out)


def test_checkout_existing_branch_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    run_cli(monkeypatch, ["branch", "dev"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["checkout", "dev"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert re.search(r"^Switched to branch 'dev'\n$", captured.out)


def test_checkout_requires_branch(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["checkout"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == "Branch name required\n"


def test_checkout_nonexistent_branch(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["checkout", "dev"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == "Branch does not exist\n"


def test_checkout_switches_branch(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    run_cli(monkeypatch, ["branch", "dev"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["checkout", "dev"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Switched to branch 'dev'\n"


def test_checkout_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    run_cli(monkeypatch, ["branch", "feature"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["checkout", "feature"])
    captured = capsys.readouterr()

    assert exit_code == 0

    pattern = r"^Switched to branch '(\w+)'\n$"
    assert re.search(pattern, captured.out)


def test_checkout_invalid_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["checkout", "unknown"])
    captured = capsys.readouterr()

    assert exit_code == 1

    pattern = r"^Branch does not exist\n$"
    assert re.search(pattern, captured.out)
