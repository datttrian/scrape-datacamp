import sys
import pytest
from unittest.mock import patch, MagicMock
from project import load_documents


def test_load_documents_exit_on_wrong_arguments():
    with patch.object(sys, "argv", ["project.py"]), pytest.raises(SystemExit):
        load_documents()


def test_load_documents_correct_usage():
    mock_loader = MagicMock()
    mock_loader.load.return_value = ["Document1", "Document2"]

    with patch("project.DirectoryLoader", return_value=mock_loader):
        with patch.object(sys, "argv", ["project.py", "file.pdf"]):
            documents = load_documents()
            assert documents == ["Document1", "Document2"]
            mock_loader.load.assert_called_once()
