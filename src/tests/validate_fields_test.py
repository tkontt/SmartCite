import unittest
from util import validate_fields, UserInputError

class TestTodoValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_fields_do_not_raise_error(self):
        validate_fields({'author': 'Author', 'title': 'Title'})

    def test_missing_required_fields_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_fields({'author': 'Author', 'title': ''})