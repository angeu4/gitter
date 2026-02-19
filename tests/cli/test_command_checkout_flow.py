def test_checkout_restores_files(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    # init
    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    # create + commit file on main
    file = tmp_path / "file.txt"
    file.write_text("main version")

    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "main commit"])
    capsys.readouterr()

    # create new branch
    run_cli(monkeypatch, ["branch", "dev"])
    run_cli(monkeypatch, ["checkout", "dev"])
    capsys.readouterr()

    # modify file in dev
    file.write_text("dev version")
    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "dev commit"])
    capsys.readouterr()

    # switch back to main
    run_cli(monkeypatch, ["checkout", "main"])
    capsys.readouterr()

    # file should now contain main version
    assert file.read_text() == "main version"
