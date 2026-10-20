import unittest

from app import response_for


class ResponseContractTests(unittest.TestCase):
    def test_root_returns_service_metadata(self):
        status, body, content_type = response_for("/")
        self.assertEqual(status, 200)
        self.assertIn(b"demo-servicio", body)
        self.assertTrue(content_type.startswith("application/json"))

    def test_health_endpoint_is_ok(self):
        status, body, _ = response_for("/health")
        self.assertEqual(status, 200)
        self.assertIn(b'"status": "ok"', body)

    def test_unknown_path_returns_404(self):
        status, body, _ = response_for("/does-not-exist")
        self.assertEqual(status, 404)
        self.assertIn(b"not found", body)


if __name__ == "__main__":
    unittest.main()
