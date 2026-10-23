import os
import tempfile
import unittest
from unittest.mock import Mock, patch

import requests

from main import find_in_file, find_in_url, find_passports, is_valid_passport


class TestIsValidPassport(unittest.TestCase):
    def test_valid_formats(self):
        for s in ["4506 123456", "45 06 123456", "4506123456", "45 06 № 123456"]:
            with self.subTest(s=s):
                self.assertTrue(is_valid_passport(s))

    def test_strip_edges(self):
        self.assertTrue(is_valid_passport("  4506 123456\n"))

    def test_wrong_length(self):
        for s in ["4506 12345", "4506 1234567"]:
            with self.subTest(s=s):
                self.assertFalse(is_valid_passport(s))

    def test_wrong_characters(self):
        for s in ["45a6 123456", "4506-123456"]:
            with self.subTest(s=s):
                self.assertFalse(is_valid_passport(s))

    def test_region_00(self):
        self.assertFalse(is_valid_passport("0006 123456"))

    def test_empty(self):
        self.assertFalse(is_valid_passport(""))

    def test_extra_text(self):
        self.assertFalse(is_valid_passport("паспорт 4506 123456"))


class TestFindPassports(unittest.TestCase):
    def test_two_in_text(self):
        text = "Паспорт 45 06 123456, выдан 2010; второй: 4608 654321."
        self.assertEqual(find_passports(text), ["45 06 123456", "4608 654321"])

    def test_no_match(self):
        self.assertEqual(find_passports("Тут нет данных 12345"), [])

    def test_long_digit_string(self):
        self.assertEqual(find_passports("12345678901234"), [])


class TestFindInFile(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")

    def tearDown(self):
        self.tmp.close()
        os.remove(self.tmp.name)

    def test_find_in_file(self):
        self.tmp.write("Иванов, паспорт 4506 123456\nПетров, 45 08 654321\n")
        self.tmp.close()
        self.assertEqual(find_in_file(self.tmp.name), ["4506 123456", "45 08 654321"])

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            find_in_file("no_such_file.txt")


class TestFindInUrl(unittest.TestCase):
    @patch("requests.get")
    def test_find_in_url(self, mock_get):
        mock_get.return_value = Mock(
            text="<p>Паспорт 4506 123456</p>", raise_for_status=Mock())
        self.assertEqual(find_in_url("http://example.com"), ["4506 123456"])
        mock_get.assert_called_once_with("http://example.com", timeout=10)

    @patch("requests.get")
    def test_http_error(self, mock_get):
        resp = Mock(text="")
        resp.raise_for_status.side_effect = requests.exceptions.HTTPError("404")
        mock_get.return_value = resp
        with self.assertRaises(requests.exceptions.HTTPError):
            find_in_url("http://example.com/missed")


if __name__ == "__main__":
    unittest.main()
 
