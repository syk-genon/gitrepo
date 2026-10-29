import os
import zipfile
import tarfile
import shutil
import tempfile
import unicodedata

# 카테고리 정의 및 확장자 매핑
EXTENSION_CATEGORIES = {
    '이미지(Images)': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.tiff'],
    '문서(Documents)': ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt', '.txt', '.hwp', '.csv', '.md', '.key', '.odt'],
    '코드(Code)': ['.py', '.js', '.ts', '.html', '.css', '.json', '.java', '.cpp', '.c', '.sh', '.bat', '.xml', '.yml', '.yaml', '.php', '.go', '.rs'],
    '미디어(Media)': ['.mp3', '.wav', '.flac', '.mp4', '.mkv', '.avi', '.mov', '.wmv'],
    '압축파일(Archives)': ['.zip', '.tar', '.gz', '.rar', '.7z', '.tgz']
}

def get_category_by_extension(filename):
    """파일 이름의 확장자를 바탕으로 카테고리를 결정합니다."""
    _, ext = os.path.splitext(filename.lower())
    for category, extensions in EXTENSION_CATEGORIES.items():
        if ext in extensions:
            return category
    return '기타(Others)'

def extract_archive(archive_path, extract_to):
    """압축 파일을 임시 폴더에 해제합니다."""
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            # 한글 깨짐 방지를 위해 cp949 인코딩 처리 대응
            for member in zip_ref.infolist():
                try:
                    # utf-8로 시도 후 에러 발생 시 cp949 적용
                    member.filename = member.filename.encode('cp437').decode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    try:
                        member.filename = member.filename.encode('cp437').decode('cp949')
                    except Exception:
                        pass
                # 자소 분리 방지용으로 미리 NFC 정규화
                member.filename = unicodedata.normalize('NFC', member.filename)
                zip_ref.extract(member, extract_to)
        return True
    elif archive_path.endswith(('.tar', '.tar.gz', '.tgz')):
        with tarfile.open(archive_path, 'r:*') as tar_ref:
            tar_ref.extractall(path=extract_to)
        return True
    else:
        print(f"지원하지 않는 압축 포맷이거나 건너뜁니다: {archive_path}")
        return False

def scan_and_classify_files(directory):
    """디렉토리를 순회하면서 모든 파일의 로컬 경로와 카테고리를 리스트로 반환합니다."""
    classified_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 임시 시스템 파일이나 메타데이터 파일 무시 (예: macOS의 __MACOSX 또는 .DS_Store)
            if '__MACOSX' in root or file.startswith('.') or file == 'Thumbs.db':
                continue
                
            # 맥 OS 등에서 업로드된 NFD(자소 분리) 한글 파일 이름을 Windows 표준인 NFC로 정규화
            normalized_file = unicodedata.normalize('NFC', file)
            local_path = os.path.join(root, file)
            
            if normalized_file != file:
                new_path = os.path.join(root, normalized_file)
                try:
                    os.rename(local_path, new_path)
                    file = normalized_file
                    local_path = new_path
                except Exception:
                    pass
            
            category = get_category_by_extension(file)
            
            # 원본 디렉토리 기준 상대 경로 유지용 이름 구하기
            relative_name = os.path.relpath(local_path, directory)
            
            classified_files.append({
                'local_path': local_path,
                'name': file,
                'relative_name': relative_name,
                'category': category
            })
            
    return classified_files
