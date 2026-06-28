from argparse import ArgumentParser
from pathlib import Path


def cleanup_uploads(upload_path: str = 'uploads', dry_run: bool = True) -> None:
    upload_dir = Path(upload_path).expanduser().resolve()
    if not upload_dir.exists():
        print(f'Upload directory does not exist: {upload_dir}')
        return

    files = [path for path in upload_dir.iterdir() if path.is_file()]
    if not files:
        print(f'No files found in upload directory: {upload_dir}')
        return

    print(f'Found {len(files)} file(s) in {upload_dir}')
    for path in sorted(files):
        print(f'  - {path.name}')

    if dry_run:
        print('Dry run complete. No files were deleted.')
        print('Re-run with --delete to remove files.')
        return

    for path in files:
        path.unlink()
        print(f'Deleted: {path.name}')

    print('Upload directory cleanup complete.')


def parse_args() -> ArgumentParser:
    parser = ArgumentParser(
        description='List and optionally delete files from the upload directory.'
    )
    parser.add_argument(
        '--upload-path',
        default='uploads',
        help='Path to the upload directory.',
    )
    parser.add_argument(
        '--delete',
        action='store_true',
        help='Permanently delete the files listed in the upload directory.',
    )
    return parser


def main() -> None:
    parser = parse_args()
    args = parser.parse_args()
    cleanup_uploads(args.upload_path, dry_run=not args.delete)


if __name__ == '__main__':
    main()
