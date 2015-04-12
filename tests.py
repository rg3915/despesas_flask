import unittest
import flask
import despesas
from despesas import app


class TestIndexView(unittest.TestCase):

    def test_it_runs(self):
        with app.test_request_context("/"):
            result = despesas.index()
            self.assertIn("bem-vindo", result.lower())

if __name__ == "__main__":
    unittest.main()
