from pathlib import Path
from gitter.repository.layout import RepoLayout


def test_layout_creates_dirs(tmp_path: Path):
    layout = RepoLayout(tmp_path)
    layout.ensure_exists()

    assert layout.objects_dir.exists()
    assert layout.heads_dir.exists()
