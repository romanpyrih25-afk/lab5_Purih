import io
import unittest
from unittest.mock import patch

from bracket_validator import StringValidator, ValidationError, main


class TestFindErrors(unittest.TestCase):
    def check(self, text, expected):
        self.assertEqual(StringValidator(text).find_errors(), expected)

    def test_empty_string(self):
        self.check("", [])

    def test_no_brackets(self):
        self.check("hello world", [])

    def test_round_balanced(self):
        self.check("(a(b)c)()", [])

    def test_all_types_balanced(self):
        self.check("<div>{ (x) }</div>", [])

    def test_extra_closing(self):
        self.check("())", [2])

    def test_unclosed_opening(self):
        self.check("((a)", [0])

    def test_closing_before_opening(self):
        self.check(")(", [0, 1])

    def test_wrong_type(self):
        self.check("(}", [0, 1])

    def test_example_from_task(self):
        self.check("<div><p>{ test }}</p</div>", [16, 17])


class TestValidate(unittest.TestCase):
    def test_valid_returns_true(self):
        self.assertTrue(StringValidator("<p>(ok)</p>").validate())

    def test_raises_value_error(self):
        with patch("sys.stderr", new_callable=io.StringIO):
            with self.assertRaises(ValueError):
                StringValidator("(").validate()

    def test_error_message_and_positions(self):
        with patch("sys.stderr", new_callable=io.StringIO):
            with self.assertRaises(ValidationError) as ctx:
                StringValidator("<div><p>{ test }}</p</div>").validate()
        self.assertEqual(str(ctx.exception), "Дужки незбалансовані на позиціях: 16, 17")
        self.assertEqual(ctx.exception.idx, [16, 17])

    def test_highlight_printed(self):
        with patch("sys.stderr", new_callable=io.StringIO) as err:
            with self.assertRaises(ValidationError):
                StringValidator("a)b(").validate()
        self.assertEqual(err.getvalue(), "a)b(\n ^ ^\n")


class TestMain(unittest.TestCase):
    @patch("builtins.input", return_value="(test)")
    def test_valid_input(self, mock_input):
        with patch("sys.stdout", new_callable=io.StringIO) as out:
            main()
        mock_input.assert_called_once_with("Введіть строку: ")
        self.assertEqual(out.getvalue(), "Строка валідна\n")

    @patch("builtins.input", return_value="(test")
    def test_invalid_input(self, _):
        with patch("sys.stderr", new_callable=io.StringIO):
            with self.assertRaises(ValueError):
                main()


if __name__ == "__main__":
    unittest.main(verbosity=2)
