import unittest
from unittest.mock import patch

from avu_eval.provider import GeminiEAPProvider


class Value:
    pass


class ProviderContractTests(unittest.TestCase):
    def test_usage_fields_match_supplied_colab(self):
        provider = object.__new__(GeminiEAPProvider)
        uploaded = Value(); uploaded.uri = "files/video"; uploaded.mime_type = "video/mp4"
        provider._upload = lambda path: uploaded
        provider.client = Value(); provider.client.interactions = Value()
        usage = Value()
        usage.total_input_tokens = 100
        usage.total_output_tokens = 20
        usage.total_tokens = 130
        usage.total_thought_tokens = 10
        modality = Value(); modality.modality = "VIDEO"; modality.tokens = 90
        usage.input_tokens_by_modality = [modality]
        response = Value(); response.output_text = "four"; response.usage = usage
        provider.client.interactions.create = lambda **kwargs: response

        result = provider.ask(model="models/test", video=None, question="q", processing="agentic")
        self.assertEqual(result.input_tokens, 100)
        self.assertEqual(result.total_tokens, 130)
        self.assertEqual(result.raw_metadata["input_tokens_by_modality"][0]["tokens"], 90)


if __name__ == "__main__":
    unittest.main()
