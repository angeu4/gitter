def test_init_creates_repo(tmp_path, monkeypatch, run_cli):
    monkeypatch.chdir(tmp_path)

    exit_code = run_cli(monkeypatch, ["init"])

    assert exit_code == 0
    assert (tmp_path / ".gitter").exists()