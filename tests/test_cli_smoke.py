import subprocess


def test_cli_invocation():
    result = subprocess.run(["gitter"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Gitter CLI" in result.stdout
