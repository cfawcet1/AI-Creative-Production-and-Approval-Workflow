"""App-managed brand repository using the restricted drive.file OAuth scope."""
import hashlib
import io
import mimetypes
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def connect(client_path: Path, token_path: Path):
    credentials = Credentials.from_authorized_user_file(str(token_path), SCOPES) if token_path.exists() else None
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
            except Exception:
                credentials = None
        if not credentials or not credentials.valid:
            credentials = InstalledAppFlow.from_client_secrets_file(str(client_path), SCOPES).run_local_server(port=0)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(credentials.to_json())
        token_path.chmod(0o600)
    return build('drive', 'v3', credentials=credentials)

def make_folder(service, name, parent=None):
    body = {'name': name, 'mimeType': 'application/vnd.google-apps.folder'}
    if parent:
        body['parents'] = [parent]
    return service.files().create(body=body, fields='id').execute()['id']

def fetch_bytes(service, file_id):
    data = io.BytesIO()
    downloader = MediaIoBaseDownload(data, service.files().get_media(fileId=file_id))
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return data.getvalue()

def initialize(service, source: Path):
    if not source.is_dir():
        raise FileNotFoundError(source)
    root = make_folder(service, 'CreativeOps AI - Managed Brand Library')
    folders = {source: root}
    assets = []
    for path in sorted(source.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'Symlinks not supported: {path}')
        if path.is_dir():
            folders[path] = make_folder(service, path.name, folders[path.parent])
        elif path.is_file():
            media = MediaFileUpload(str(path), mimetype=mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
            item = service.files().create(body={'name': path.name, 'parents': [folders[path.parent]]}, media_body=media, fields='id').execute()
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if hashlib.sha256(fetch_bytes(service, item['id'])).hexdigest() != digest:
                raise RuntimeError(f'Integrity verification failed: {path}')
            assets.append({'path': path.relative_to(source).as_posix(), 'id': item['id'], 'sha256': digest})
    return {'root_folder_id': root, 'assets': assets}
