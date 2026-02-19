def test_status_staged(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    # init
    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    # create file
    file = tmp_path / "file.txt"
    file.write_text("hello")

    # add
    run_cli(monkeypatch, ["add", "file.txt"])
    capsys.readouterr()

    # status
    exit_code = run_cli(monkeypatch, ["status"])
    captured = capsys.readouterr()

    assert exit_code == 0
    expected = "Changes to be committed:\n  file.txt\n"
    assert captured.out == expected


def test_status_clean(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    # init
    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    # create file
    file = tmp_path / "file.txt"
    file.write_text("hello")

    # add and commit
    run_cli(monkeypatch, ["add", "file.txt"])
    capsys.readouterr()

    run_cli(monkeypatch, ["commit", "-m", "msg"])
    capsys.readouterr()

    # status
    exit_code = run_cli(monkeypatch, ["status"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Working tree clean\n"


def test_status_untracked(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    # init
    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    # create untracked file
    file = tmp_path / "file.txt"
    file.write_text("hello")

    # status
    exit_code = run_cli(monkeypatch, ["status"])
    captured = capsys.readouterr()

    assert exit_code == 0
    expected = "Untracked files:\n  file.txt\n"
    assert captured.out == expected
