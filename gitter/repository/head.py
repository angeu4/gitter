from .exceptions import HeadError


class Head:
    """
    Manages HEAD pointer file.

    HEAD points to currently active branch reference.
    """

    def __init__(self, head_file):
        self.head_file = head_file

    def set_branch(self, branch_name: str):
        """
        Update HEAD to reference given branch.

        Raises:
            HeadError: If filesystem write fails.
        """
        try:
            self.head_file.write_text(f"ref: refs/heads/{branch_name}")

        except OSError as exc:
            raise HeadError(str(exc)) from exc

    def get_ref(self) -> str:
        """
        Read HEAD reference string.

        Returns:
            Raw HEAD reference string.

        Raises:
            HeadError: If file missing or unreadable.
        """
        try:
            return self.head_file.read_text().strip()

        except OSError as exc:
            raise HeadError(str(exc)) from exc