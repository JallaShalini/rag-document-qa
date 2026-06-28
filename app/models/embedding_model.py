class EmbeddingModel:
    _model = None

    @classmethod
    def load_model(cls, model_name: str = 'all-MiniLM-L6-v2'):
        if cls._model is None:
            from sentence_transformers import SentenceTransformer

            cls._model = SentenceTransformer(model_name)
        return cls._model

    @classmethod
    def encode(cls, texts, **kwargs):
        model = cls.load_model()
        return model.encode(texts, **kwargs)
