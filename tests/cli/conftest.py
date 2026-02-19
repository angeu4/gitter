import sys
import pytest
from gitter.cli.main import main


@pytest.fixture
def run_cli():
    def _run(monkeypatch, args):
        monkeypatch.setattr(sys, "argv", ["gitter"] + args)
        with pytest.raises(SystemExit) as exc:
            main()
        return exc.value.code

    return _run
