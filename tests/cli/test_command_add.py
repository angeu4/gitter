from tests.cli.conftest import run_cli


def test_add_without_repo_fails(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    exit_code = run_cli(monkeypatch, ["add", "file.txt"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Not a gitter repository" in captured.out