from argparse import ArgumentParser
from pathlib import Path

from app.database.collection_manager import get_collection
from app.database.chroma_client import get_client
from app.config import settings


def initialize_vector_db(chroma_path: str | None = None) -> None:
    storage_path = chroma_path or settings.chroma_path or 'chroma_db'
    storage_dir = Path(storage_path).expanduser().resolve()
    storage_dir.mkdir(parents=True, exist_ok=True)

    print(f'Initializing vector database at: {storage_dir}')
    client = get_client()
    collection = get_collection()
    print(f"Vector collection '{collection.name}' is ready.")
    print('Initialization complete.')


def parse_args() -> ArgumentParser:
    parser = ArgumentParser(
        description='Initialize the Chroma vector database and ensure the document collection exists.'
    )
    parser.add_argument(
        '--chroma-path',
        default=settings.chroma_path or 'chroma_db',
        help='Directory to use for Chroma DB persistence.',
    )
    return parser


def main() -> None:
    parser = parse_args()
    args = parser.parse_args()
    initialize_vector_db(args.chroma_path)


if __name__ == '__main__':
    main()
