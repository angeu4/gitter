def test_add_glob_matches_files(tmp_path, monkeypatch, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    (tmp_path / "a.py").write_text("print(1)")
    (tmp_path / "b.py").write_text("print(2)")
    (tmp_path / "c.txt").write_text("text")

    run_cli(monkeypatch, ["add", "*.py"])

    exit_code = run_cli(monkeypatch, ["status"])

    assert exit_code == 0

def test_add_glob_subdirectory(tmp_path, monkeypatch, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    sub = tmp_path / "sub"
    sub.mkdir()

    (sub / "a.md").write_text("md")
    (sub / "b.txt").write_text("txt")

    run_cli(monkeypatch, ["add", "sub/*.md"])

    exit_code = run_cli(monkeypatch, ["status"])
    assert exit_code == 0

def test_add_glob_no_match(tmp_path, monkeypatch, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    exit_code = run_cli(monkeypatch, ["add", "*.xyz"])
    assert exit_code == 0
