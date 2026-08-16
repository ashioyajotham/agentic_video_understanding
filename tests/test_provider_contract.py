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
        provider.timeout_seconds = 10

        class FakeQueue:
            def __init__(self): self.value = None
            def put(self, value): self.value = value
            def get(self, timeout=None): return self.value

        class FakeProcess:
            def __init__(self, q): self.q = q; self.exitcode = 0
            def start(self):
                self.q.put({"ok": True, "text": "four", "input_tokens": 100,
                    "output_tokens": 20, "total_tokens": 130, "thought_tokens": 10,
                    "strategy_trace": None, "modality_usage": [{"modality": "VIDEO", "tokens": 90}],
                    "provider_latency_seconds": 1.2})
            def join(self, timeout=None): pass
            def is_alive(self): return False

        class FakeContext:
            def __init__(self): self.q = FakeQueue()
            def Queue(self): return self.q
            def Process(self, target, args): return FakeProcess(self.q)

        with patch("avu_eval.provider.mp.get_context", return_value=FakeContext()):
            result = provider.ask(model="models/test", video=None, question="q", processing="agentic")
        self.assertEqual(result.input_tokens, 100)
        self.assertEqual(result.total_tokens, 130)
        self.assertEqual(result.raw_metadata["input_tokens_by_modality"][0]["tokens"], 90)


if __name__ == "__main__":
    unittest.main()
