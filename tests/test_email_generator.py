import importlib
import sys
import os
from pathlib import Path
from types import ModuleType, SimpleNamespace


def setup_fake_openai():
    fake_module = ModuleType('openai')
    class FakeClient:
        def __init__(self, api_key=None):
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))
        def create(self, model=None, messages=None, stream=False):
            chunks = [
                SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content="Hello"))]),
                SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=" World"))]),
            ]
            return iter(chunks)
    fake_module.OpenAI = FakeClient
    return fake_module


def test_stream_generated_email_yields_tokens(monkeypatch):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    monkeypatch.setitem(sys.modules, 'openai', setup_fake_openai())
    module = importlib.import_module('email_generator.generator')
    importlib.reload(module)
    tokens = list(module.stream_generated_email('input', 'Friendly', 'purpose', 'key'))
    assert tokens == ["Hello", " World"]
