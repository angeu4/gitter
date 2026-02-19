import re


def test_init_creates_repo(tmp_path, monkeypatch, run_cli):
    monkeypatch.chdir(tmp_path)

    exit_code = run_cli(monkeypatch, ["init"])

    assert exit_code == 0
    assert (tmp_path / ".gitter").exists()


def test_init_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    exit_code = run_cli(monkeypatch, ["init"])
    captured = capsys.readouterr()

    assert exit_code == 0

    pattern = r"Initialized empty Gitter repository in .+/.gitter/"
    assert re.search(pattern, captured.out)


def test_reinit_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    _ = run_cli(monkeypatch, ["init"])
    captured = capsys.readouterr()

    pattern = r"Gitter repository is already initialised in .+/.gitter/"
    assert re.search(pattern, captured.out)
