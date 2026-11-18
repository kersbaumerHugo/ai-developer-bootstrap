import subprocess
import unittest
from unittest.mock import patch

from scripts.doctor import check_opencode


class TestOpenCodeDetection(unittest.TestCase):

    @patch("shutil.which", return_value=None)
    def test_not_found(self, mock_which):
        result = check_opencode()
        self.assertFalse(result["installed"])
        self.assertEqual(result["status"], "not found")
        self.assertIsNone(result["path"])

    @patch("scripts.doctor.subprocess.run")
    @patch("shutil.which", return_value="/opt/bin/opencode")
    def test_running(self, mock_which, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["opencode", "--version"],
            returncode=0,
            stdout="opencode v2.2.5\n",
            stderr="",
        )

        result = check_opencode()

        self.assertTrue(result["installed"])
        self.assertEqual(result["status"], "running")
        self.assertEqual(result["version"], "opencode v2.2.5")
        self.assertEqual(result["path"], "/opt/bin/opencode")

    @patch("scripts.doctor.subprocess.run")
    @patch("shutil.which", return_value="/opt/bin/opencode")
    def test_execution_error(self, mock_which, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["opencode", "--version"],
            returncode=1,
            stdout="",
            stderr="error",
        )

        result = check_opencode()

        self.assertTrue(result["installed"])
        self.assertEqual(result["status"], "error")

    @patch("scripts.doctor.subprocess.run")
    @patch("shutil.which", return_value="/opt/bin/opencode")
    def test_timeout(self, mock_which, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd=["opencode", "--version"],
            timeout=10,
        )

        result = check_opencode()

        self.assertTrue(result["installed"])
        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
