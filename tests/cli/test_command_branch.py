def test_branch_list(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    exit_code = run_cli(monkeypatch, ["branch"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "* main" in captured.out


def test_branch_create(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    exit_code = run_cli(monkeypatch, ["branch", "feature"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "created" in captured.out

    exit_code = run_cli(monkeypatch, ["branch"])
    captured = capsys.readouterr()

    assert "feature" in captured.out


def test_branch_duplicate(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    run_cli(monkeypatch, ["branch", "feature"])

    exit_code = run_cli(monkeypatch, ["branch", "feature"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "already exists" in captured.out
