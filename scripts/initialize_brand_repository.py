"""Usage: python -m scripts.initialize_brand_repository /path/to/approved/brand-library"""
import json
import sys
from pathlib import Path
from app.integrations.google_drive import connect, initialize

def main():
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python -m scripts.initialize_brand_repository /path/to/brand-library')
    client = Path('secrets/credentials.json')
    if not client.is_file():
        raise SystemExit('Save your private Desktop OAuth client JSON to secrets/credentials.json first')
    result = initialize(connect(client, Path('secrets/token.json')), Path(sys.argv[1]).expanduser().resolve())
    output = Path('.local/brand_repository.json')
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, indent=2))
    print(f'Uploaded and verified {len(result["assets"])} assets; root folder: {result["root_folder_id"]}')

if __name__ == '__main__':
    main()
