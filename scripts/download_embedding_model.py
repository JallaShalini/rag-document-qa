from argparse import ArgumentParser
from pathlib import Path

from app.config import settings
from app.models.embedding_model import EmbeddingModel


def download_model(model_name: str, save_dir: str | None = None) -> None:
    print(f"Downloading embedding model '{model_name}'...")
    model = EmbeddingModel.load_model(model_name)
    print(f"Model '{model_name}' loaded into cache.")

    if save_dir:
        target_dir = Path(save_dir).expanduser().resolve()
        target_dir.mkdir(parents=True, exist_ok=True)
        output_path = target_dir / model_name.replace('/', '_')
        model.save(str(output_path))
        print(f"Saved model to: {output_path}")

    print('Download complete.')


def parse_args() -> ArgumentParser:
    parser = ArgumentParser(
        description='Download and cache the embedding model used by the RAG app.'
    )
    parser.add_argument(
        '--model-name',
        default=settings.model_name or 'all-MiniLM-L6-v2',
        help='Embedding model name to download (default: from env or all-MiniLM-L6-v2).',
    )
    parser.add_argument(
        '--save-dir',
        default=None,
        help='Optional directory to save the downloaded model locally.',
    )
    return parser


def main() -> None:
    parser = parse_args()
    args = parser.parse_args()
    download_model(args.model_name, args.save_dir)


if __name__ == '__main__':
    main()
