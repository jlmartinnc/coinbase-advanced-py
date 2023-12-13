import base64
import json
import unittest

import jwt

from coinbase import jwt_generator
from coinbase.constants import REST_SERVICE, WS_SERVICE
from tests.constants import TEST_API_KEY, TEST_API_SECRET


class JwtGeneratorTest(unittest.TestCase):
    def test_build_rest_jwt(self):
        uri = jwt_generator.format_jwt_uri("GET", "/api/v3/brokerage/accounts")
        result_jwt = jwt_generator.build_rest_jwt(uri, TEST_API_KEY, TEST_API_SECRET)

        decoded_data = jwt.decode(
            result_jwt, TEST_API_SECRET, algorithms=["ES256"], audience=[REST_SERVICE]
        )
        header_bytes = base64.urlsafe_b64decode(str(result_jwt.split(".")[0] + "=="))
        decoded_header = json.loads(header_bytes.decode("utf-8"))

        self.assertEqual(decoded_data["sub"], TEST_API_KEY)
        self.assertEqual(decoded_data["iss"], "coinbase-cloud")
        self.assertEqual(decoded_data["aud"], [REST_SERVICE])
        self.assertEqual(decoded_data["uri"], uri)
        self.assertEqual(decoded_header["kid"], TEST_API_KEY)

    def test_build_ws_jwt(self):
        result_jwt = jwt_generator.build_ws_jwt(TEST_API_KEY, TEST_API_SECRET)

        decoded_data = jwt.decode(
            result_jwt, TEST_API_SECRET, algorithms=["ES256"], audience=[WS_SERVICE]
        )
        header_bytes = base64.urlsafe_b64decode(str(result_jwt.split(".")[0] + "=="))
        decoded_header = json.loads(header_bytes.decode("utf-8"))

        self.assertEqual(decoded_data["sub"], TEST_API_KEY)
        self.assertEqual(decoded_data["iss"], "coinbase-cloud")
        self.assertEqual(decoded_data["aud"], [WS_SERVICE])
        self.assertNotIn("uri", decoded_data)
        self.assertEqual(decoded_header["kid"], TEST_API_KEY)
