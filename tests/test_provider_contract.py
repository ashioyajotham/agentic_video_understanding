import unittest
from unittest.mock import patch

from avu_eval.provider import GeminiEAPProvider, GeminiProvider, _file_state_name, _step_type


class Value:
    pass


class ProviderContractTests(unittest.TestCase):
    def test_legacy_provider_name_is_a_compatibility_alias(self):
        self.assertIs(GeminiEAPProvider, GeminiProvider)

    def test_public_response_discriminators_are_normalized(self):
        step = Value(); step.type = "processing_call"
        state = Value(); state.name = "ACTIVE"
        uploaded = Value(); uploaded.state = state
        self.assertEqual(_step_type(step), "processing_call")
        self.assertEqual(_step_type({"type": "processing_result"}), "processing_result")
        self.assertEqual(_step_type(type("ProcessingCall", (), {})()), "processing_call")
        self.assertEqual(_file_state_name(uploaded), "ACTIVE")

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
                    "provider_latency_seconds": 1.2,
                    "processing_step_types": ["processing_call", "processing_result"],
                    "processing_call_count": 1, "processing_result_count": 1,
                    "agentic_processing_observed": True, "google_genai_version": "test"})
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
        self.assertTrue(result.raw_metadata["agentic_processing_observed"])


if __name__ == "__main__":
    unittest.main()
