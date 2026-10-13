from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly"
]


SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly"
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "token.json"


def authenticate():
    credentials = None

    if TOKEN_FILE.exists():
        credentials = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    elif not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(CREDENTIALS_FILE),
            SCOPES
        )

        credentials = flow.run_local_server(port=0)

    TOKEN_FILE.write_text(credentials.to_json())

    return build("drive", "v3", credentials=credentials)


def list_files():
    service = authenticate()

    results = service.files().list(
        pageSize=100,
        fields="nextPageToken, files(id, name, mimeType, parents)"
    ).execute()

    return results.get("files", [])


def list_folder(folder_id):
    service = authenticate()

    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        pageSize=100,
        fields="nextPageToken, files(id, name, mimeType, parents)"
    ).execute()

    return results.get("files", [])


def download_file(file_id, destination):
    service = authenticate()
    request = service.files().get_media(fileId=file_id)

    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("wb") as output:
        downloader = MediaIoBaseDownload(output, request)
        done = False

        while not done:
            status, done = downloader.next_chunk()

    return destination


if __name__ == "__main__":
    MANIFEST_FILE_ID = "1HiauUbwT8fqnOMTL9T8uyJyWCXDhcQuk"

    destination = (
        PROJECT_ROOT
        / "data"
        / "may_madness_campaign_manifest.json"
    )

    downloaded = download_file(MANIFEST_FILE_ID, destination)

    print("\nUpdated campaign manifest downloaded:")
    print(downloaded)