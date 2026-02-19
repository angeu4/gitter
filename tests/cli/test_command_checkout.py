"""
def test_checkout_nonexistent_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["checkout", "test"])
    captured = capsys.readouterr()

    assert re.search(r"test does not exist", captured.out)


def test_checkout_new_branch_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["checkout", "-b", "test"])
    captured = capsys.readouterr()

    assert re.search(r"Switched to a new branch", captured.out)

"""