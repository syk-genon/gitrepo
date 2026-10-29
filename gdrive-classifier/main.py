import os
import shutil
import tempfile
import traceback
import sys
import unicodedata

# stdout/stderr를 UTF-8로 설정하여 Windows의 cp949 인코딩 에러 방지
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr.encoding != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from gdrive_helper import (
    get_drive_service,
    download_file,
    get_or_create_folder,
    upload_file,
    move_file
)
from classifier import extract_archive, scan_and_classify_files

def find_folder_by_path(service, path_segments):
    """폴더 경로 세그먼트 리스트(예: ['저장', '소설'])를 바탕으로 최하위 폴더 ID를 찾습니다."""
    parent_id = None
    
    for segment in path_segments:
        if parent_id:
            query = f"name = '{segment}' and mimeType = 'application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed = false"
        else:
            # 첫 번째 세그먼트는 전체 드라이브에서 해당 이름의 폴더를 찾습니다.
            query = f"name = '{segment}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
            
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, parents)',
            pageSize=10
        ).execute()
        files = results.get('files', [])
        
        if not files:
            print(f"폴더를 찾을 수 없습니다: '{segment}' (상위 폴더 ID: {parent_id})")
            return None
            
        # 매칭되는 첫 번째 폴더 선택
        parent_id = files[0]['id']
        print(f"폴더 확인: '{segment}' (ID: {parent_id})")
        
    return parent_id

def search_compressed_files_in_folder(service, folder_id):
    """지정된 폴더 ID 내부에 있는 압축 파일(.zip, .tar, .gz, .rar 등)을 검색합니다."""
    query = (
        f"('{folder_id}' in parents) and "
        "("
        "mimeType = 'application/zip' or "
        "mimeType = 'application/x-zip-compressed' or "
        "mimeType = 'application/x-tar' or "
        "mimeType = 'application/gzip' or "
        "name contains '.zip' or "
        "name contains '.tar' or "
        "name contains '.gz' or "
        "name contains '.rar'"
        ") and trashed = false"
    )
    
    results = service.files().list(
        q=query,
        spaces='drive',
        fields='nextPageToken, files(id, name, mimeType, parents)',
        pageSize=100
    ).execute()
    
    return results.get('files', [])

def get_or_create_folder_path(service, relative_path, root_folder_id):
    """지정된 상대 경로(예: 'vol1/chap1')에 맞춰 구글 드라이브 내에 폴더 구조를 재구성하고 최하위 폴더 ID를 반환합니다."""
    if not relative_path or relative_path in ['.', '']:
        return root_folder_id
        
    parts = relative_path.replace('\\', '/').split('/')
    parent_id = root_folder_id
    
    for part in parts:
        if not part:
            continue
        parent_id = get_or_create_folder(service, part, parent_id=parent_id)
        
    return parent_id

def process_archive(service, file_info, archive_root_id, target_parent_id):
    file_id = file_info['id']
    file_name = file_info['name']
    parents = file_info.get('parents', [])
    old_parent_id = parents[0] if parents else target_parent_id
    
    print("\n" + "="*50)
    print(f"작업 시작: {file_name} (ID: {file_id})")
    print("="*50)
    
    # 1. 임시 작업 디렉토리 생성
    with tempfile.TemporaryDirectory() as temp_dir:
        local_archive_path = os.path.join(temp_dir, file_name)
        
        # 2. 구글 드라이브로부터 파일 다운로드
        try:
            download_file(service, file_id, local_archive_path)
        except Exception as e:
            print(f"다운로드 실패: {e}")
            return False
            
        # 3. 압축 해제용 폴더 생성
        extracted_dir = os.path.join(temp_dir, "extracted")
        os.makedirs(extracted_dir, exist_ok=True)
        
        # 4. 압축 해제 실행
        print(f"압축 해제 중: {file_name}")
        if not extract_archive(local_archive_path, extracted_dir):
            print("압축 해제에 실패했거나 지원하지 않는 포맷입니다.")
            return False
            
        # 5. 파일 스캔
        classified_items = scan_and_classify_files(extracted_dir)
        if not classified_items:
            print("압축 파일 내에 유효한 파일이 없습니다.")
            return False
            
        print(f"발견된 파일 수: {len(classified_items)}개")
        
        # 6. 구글 드라이브에 결과 저장할 상위 폴더 생성 (대상 폴더 내에 생성)
        base_name, _ = os.path.splitext(file_name)
        drive_dest_folder_name = f"Extracted_{base_name}"
        dest_folder_id = get_or_create_folder(service, drive_dest_folder_name, parent_id=target_parent_id)
        
        # 7. 원래의 압축파일 내 폴더 구조를 그대로 유지하여 구글 드라이브에 업로드
        folder_cache = {'.': dest_folder_id, '': dest_folder_id}
        
        for item in classified_items:
            local_path = item['local_path']
            name = item['name']
            relative_name = item['relative_name']
            
            # 파일이 들어있는 상대 폴더 경로 구하기
            relative_dir = os.path.dirname(relative_name).replace('\\', '/')
            
            # 캐시에 없는 폴더 경로이면 드라이브에 생성 및 캐시 등록
            if relative_dir not in folder_cache:
                folder_id = get_or_create_folder_path(service, relative_dir, dest_folder_id)
                folder_cache[relative_dir] = folder_id
                
            target_folder_id = folder_cache[relative_dir]
            
            print(f"업로드 중: {relative_name}")
            try:
                upload_file(service, local_path, name, target_folder_id)
            except Exception as e:
                print(f"파일 업로드 오류 ({name}): {e}")
                
        # 8. 원본 압축 파일을 완료 폴더로 이동 (무한 루프 방지 및 정리)
        print(f"원본 압축 파일({file_name})을 완료 폴더(Processed_Archives)로 이동합니다.")
        try:
            move_file(service, file_id, archive_root_id, old_parent_id)
        except Exception as e:
            print(f"원본 파일 이동 실패: {e}")
            
    print(f"작업 완료: {file_name}")
    return True

def main():
    print("구글 드라이브 압축 해제 및 파일 분류 자동화 프로그램 시작...")
    
    # 1. API 서비스 연결
    try:
        service = get_drive_service()
    except FileNotFoundError as e:
        print(f"\n[오류] {e}")
        return
    except Exception as e:
        print(f"로그인 인증 중 에러가 발생했습니다: {e}")
        traceback.print_exc()
        return

    # 2. 대상 폴더 찾기 ('저장' -> '소설')
    path_segments = ['저장', '소설']
    print(f"대상 경로 탐색 중: {' > '.join(path_segments)}")
    target_folder_id = find_folder_by_path(service, path_segments)
    
    if not target_folder_id:
        print(f"오류: 구글 드라이브에서 {' > '.join(path_segments)} 경로를 찾을 수 없습니다.")
        print("드라이브에 '저장' 폴더를 만들고 그 안에 '소설' 폴더가 있는지 확인해 주세요.")
        return

    # 3. 완료된 압축 파일을 보관할 폴더 생성 (대상 폴더 내부에 'Processed_Archives' 생성)
    try:
        archive_root_id = get_or_create_folder(service, "Processed_Archives", parent_id=target_folder_id)
    except Exception as e:
        print(f"보관 폴더 생성 실패: {e}")
        return

    # 4. 대상 폴더 내 압축 파일 검색
    print(f"'{path_segments[-1]}' 폴더에서 압축 파일을 검색 중입니다...")
    compressed_files = search_compressed_files_in_folder(service, target_folder_id)
    
    # Processed_Archives 안에 있는 파일은 필터링하여 제외
    files_to_process = []
    for f in compressed_files:
        # NFD 파일명을 NFC로 정규화
        f['name'] = unicodedata.normalize('NFC', f['name'])
        # 파일 이름이 Processed_Archives가 아니고, 부모 폴더에 archive_root_id가 없어야 함
        if f.get('parents') and archive_root_id in f['parents']:
            continue
        files_to_process.append(f)
        
    if not files_to_process:
        print(f"'{path_segments[-1]}' 폴더에서 처리할 새로운 압축 파일(.zip, .tar 등)을 찾지 못했습니다.")
        return
        
    print(f"총 {len(files_to_process)}개의 압축 파일을 처리합니다.")
    
    # 5. 각 압축 파일 순차적으로 처리
    success_count = 0
    for file_info in files_to_process:
        try:
            if process_archive(service, file_info, archive_root_id, target_folder_id):
                success_count += 1
        except Exception as e:
            print(f"파일 {file_info['name']} 처리 중 치명적 에러 발생: {e}")
            traceback.print_exc()
            
    print(f"\n모든 작업이 완료되었습니다! (성공: {success_count}/{len(files_to_process)})")

if __name__ == '__main__':
    main()
