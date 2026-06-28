import sys
import types

from app.models.embedding_model import EmbeddingModel


class FakeSentenceTransformer:
    def __init__(self, model_name):
        self.model_name = model_name

    def encode(self, texts, **kwargs):
        return [[len(texts), 0.1]]


def test_load_model_imports_sentence_transformer(monkeypatch):
    fake_module = types.ModuleType('sentence_transformers')
    fake_module.SentenceTransformer = FakeSentenceTransformer
    monkeypatch.setitem(sys.modules, 'sentence_transformers', fake_module)

    EmbeddingModel._model = None
    model = EmbeddingModel.load_model('test-model')

    assert isinstance(model, FakeSentenceTransformer)
    assert model.model_name == 'test-model'


def test_encode_uses_loaded_model(monkeypatch):
    fake_model = FakeSentenceTransformer('model')
    EmbeddingModel._model = fake_model

    result = EmbeddingModel.encode(['hello'])

    assert result == [[1, 0.1]]
