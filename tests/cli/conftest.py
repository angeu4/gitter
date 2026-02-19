import sys
import pytest
from gitter.cli.main import main


def run_cli(monkeypatch, args):
    monkeypatch.setattr(sys, "argv", ["gitter"] + args)
    with pytest.raises(SystemExit) as exc:
        main()
    return exc.value.code
