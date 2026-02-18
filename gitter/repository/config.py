from .exceptions import ConfigError


class RepoConfig:
    """
    Manages repository configuration file.

    Stores basic repository metadata and format version.
    """

    def __init__(self, config_file):
        self.config_file = config_file

    def write_default(self):
        """
        Write default repository configuration if missing.

        Raises:
            ConfigError: If filesystem operations fail.
        """
        try:
            if not self.config_file.exists():
                self.config_file.write_text(
                    "[core]\nrepositoryformatversion = 0\n"
                )
        except OSError as exc:
            raise ConfigError(str(exc)) from exc
