from tests.cli.conftest import run_cli

def test_init_creates_repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    exit_code = run_cli(monkeypatch, ["init"])

    assert exit_code == 0
    assert (tmp_path / ".gitter").exists()