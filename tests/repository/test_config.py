import pytest

from gitter.repository.exceptions import ConfigError
from gitter.repository.config import RepoConfig


def test_write_default_creates_file(tmp_path):
    config_file = tmp_path / "config"

    cfg = RepoConfig(config_file)
    cfg.write_default()

    assert config_file.exists()
    assert "repositoryformatversion" in config_file.read_text()


def test_write_default_idempotent(tmp_path):
    config_file = tmp_path / "config"

    cfg = RepoConfig(config_file)
    cfg.write_default()
    first = config_file.read_text()

    cfg.write_default()
    second = config_file.read_text()

    assert first == second

def test_config_write_permission_error(tmp_path):
    config_file = tmp_path / "config"
    tmp_path.chmod(0o400)

    cfg = RepoConfig(config_file)

    with pytest.raises(ConfigError):
        cfg.write_default()
