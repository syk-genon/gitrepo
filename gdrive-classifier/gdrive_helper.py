import os
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

# 전체 드라이브 읽기/쓰기 권한
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service(credentials_path='credentials.json', token_path='token.json'):
    """구글 드라이브 API 서비스 객체를 생성하여 반환합니다."""
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        
        if not creds:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"'{credentials_path}' 파일을 찾을 수 없습니다. "
                    "Google Cloud Console에서 OAuth 클라이언트 ID를 다운로드하여 "
                    "이 파일 이름으로 저장해 주세요."
                )
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(host="127.0.0.1", port=0, timeout_seconds=3600)
            
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
            
    return build('drive', 'v3', credentials=creds)

def search_compressed_files(service):
    """구글 드라이브에서 압축 파일(.zip, .tar, .gz, .rar 등)을 검색합니다."""
    # 압축 파일 형식에 대한 쿼리 정의
    query = (
        "mimeType = 'application/zip' or "
        "mimeType = 'application/x-zip-compressed' or "
        "mimeType = 'application/x-tar' or "
        "mimeType = 'application/gzip' or "
        "name contains '.zip' or "
        "name contains '.tar' or "
        "name contains '.gz' or "
        "name contains '.rar'"
    )
    # 휴지통에 있는 파일은 제외
    query = f"({query}) and trashed = false"
    
    results = service.files().list(
        q=query,
        spaces='drive',
        fields='nextPageToken, files(id, name, mimeType, parents)',
        pageSize=100
    ).execute()
    
    return results.get('files', [])

def download_file(service, file_id, local_path):
    """구글 드라이브의 파일을 로컬 경로에 다운로드합니다."""
    request = service.files().get_media(fileId=file_id)
    with io.FileIO(local_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        print(f"다운로드 시작: ID {file_id} -> {local_path}")
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                print(f"다운로드 진행률: {int(status.progress() * 100)}%")
        print("다운로드 완료!")

def get_or_create_folder(service, folder_name, parent_id=None):
    """구글 드라이브에 폴더가 존재하면 가져오고, 없으면 새로 생성합니다."""
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    
    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)'
    ).execute()
    
    files = results.get('files', [])
    if files:
        return files[0]['id']
    
    # 존재하지 않으면 폴더 생성
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        folder_metadata['parents'] = [parent_id]
        
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    print(f"새 드라이브 폴더 생성 완료: {folder_name} (ID: {folder['id']})")
    return folder['id']

def upload_file(service, local_path, file_name, parent_id, mime_type=None):
    """로컬 파일을 구글 드라이브의 특정 폴더로 업로드합니다."""
    file_metadata = {
        'name': file_name,
        'parents': [parent_id]
    }
    media = MediaFileUpload(local_path, mimetype=mime_type, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    print(f"업로드 완료: {file_name} -> 드라이브 폴더 ID: {parent_id} (파일 ID: {file.get('id')})")
    return file.get('id')

def move_file(service, file_id, new_parent_id, old_parent_id=None):
    """파일을 다른 폴더로 이동시킵니다. (압축 해제 후 원본 정리용)"""
    # 이전 부모 폴더 제거 및 새 부모 폴더 추가
    file = service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents', []))
    
    # 만약 old_parent_id가 지정되지 않았다면 조회한 값을 사용
    remove_parents = old_parent_id if old_parent_id else previous_parents
    
    service.files().update(
        fileId=file_id,
        addParents=new_parent_id,
        removeParents=remove_parents,
        fields='id, parents'
    ).execute()
    print(f"파일 이동 완료: 파일 ID {file_id} -> 새 폴더 ID {new_parent_id}")
