import sys
import pytest
from unittest.mock import patch, MagicMock
from project import load_documents


def test_load_documents_with_correct_arguments():
    with patch.object(sys, "argv", ["project.py", "file.pdf"]):
        mock_loader = MagicMock()
        mock_loader.load.return_value = ["document1", "document2"]

        with patch("project.DirectoryLoader", return_value=mock_loader):
            documents = load_documents()
            assert documents == ["document1", "document2"]
            mock_loader.load.assert_called_once()


def test_load_documents_with_incorrect_arguments():
    with patch.object(sys, "argv", ["project.py"]):
        with pytest.raises(SystemExit) as e:
            load_documents()
        assert str(e.value) == "Usage: python project.py file.pdf"


def test_load_documents_with_empty_result():
    with patch.object(sys, "argv", ["project.py", "empty.pdf"]):
        mock_loader = MagicMock()
        mock_loader.load.return_value = []

        with patch("project.DirectoryLoader", return_value=mock_loader):
            documents = load_documents()
            assert documents == []
            mock_loader.load.assert_called_once()
