import os
import zipfile
import cv2

def prepare_cctv_folder(zip_path='CCTV.zip'):
    """
    CCTV 폴더가 없으면 zip_path의 압축을 풀어 폴더를 생성합니다.
    """
    folder_path = os.path.splitext(zip_path)[0]
    if not os.path.exists(folder_path):
        print(f'\'{folder_path}\' 폴더를 찾을 수 없어 \'{zip_path}\'의 압축을 해제합니다.')
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(folder_path)
        except FileNotFoundError:
            print(f'오류: \'{zip_path}\' 파일을 찾을 수 없습니다.')
            return None
    return folder_path

def get_image_list(folder_path):
    """
    주어진 폴더에서 이미지 파일 목록만 필터링하여 반환합니다.
    """
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
    try:
        files = os.listdir(folder_path)
        image_files = sorted([
            os.path.join(folder_path, f) for f in files 
            if f.lower().endswith(valid_extensions)
        ])
        return image_files
    except FileNotFoundError:
        return []

def find_people_in_images(image_paths):
    """
    이미지 목록을 순회하며 사람을 찾고, 찾으면 화면에 출력합니다.
    - 사람이 감지되면 이미지를 보여주고 Enter 입력을 대기합니다.
    - Enter를 누르면 다음 이미지 검색을 계속합니다.
    - ESC 또는 'q'를 누르면 검색을 중단합니다.
    """
    # OpenCV에 내장된 HOG(Histogram of Oriented Gradients) 기반 사람 감지기 초기화
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    window_name = 'Person Detection'
    
    for i, image_path in enumerate(image_paths):
        print(f'[{i+1}/{len(image_paths)}] \'{os.path.basename(image_path)}\' 파일을 검색 중...')
        
        image = cv2.imread(image_path)
        if image is None:
            print(f'  -> 파일을 읽을 수 없어 건너뜁니다.')
            continue

        # 사람 감지 (detectMultiScale은 사람이라 생각되는 여러 영역을 반환)
        # winStride: 이미지 탐색 시 윈도우 이동 간격. 작을수록 꼼꼼하지만 느려짐.
        # padding: 윈도우 주변에 추가할 여백.
        # scale: 이미지 피라미드 스케일. 1.05는 5%씩 이미지를 줄여가며 탐색.
        (rects, weights) = hog.detectMultiScale(image, winStride=(8, 8), padding=(16, 16), scale=1.05)

        # 사람이 한 명이라도 감지되면
        if len(rects) > 0:
            print(f'  -> 사람을 {len(rects)}명 찾았습니다! 화면에 결과를 표시합니다.')
            
            # (보너스 과제) 감지된 모든 사람 주위에 빨간 사각형 그리기
            for (x, y, w, h) in rects:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            cv2.imshow(window_name, image)
            
            # 키 입력 대기
            key = cv2.waitKey(0)

            if key == 13:  # Enter 키
                print('  -> 다음 파일 검색을 계속합니다.\n')
                cv2.destroyWindow(window_name)
                continue
            elif key == 27 or key == ord('q'):  # ESC 또는 'q' 키
                print('사용자가 검색을 중단했습니다.')
                break
    else: # for-else 구문: for 루프가 break 없이 정상적으로 모두 완료되었을 때 실행
        print('\n모든 사진의 검색이 끝났습니다.')

    cv2.destroyAllWindows()


if __name__ == '__main__':
    # 1. CCTV 폴더 준비
    cctv_folder = prepare_cctv_folder(zip_path='CCTV.zip')

    if cctv_folder:
        # 2. 이미지 파일 목록 가져오기
        images_to_search = get_image_list(cctv_folder)
        
        if images_to_search:
            # 3. 이미지에서 사람 찾기 실행
            find_people_in_images(images_to_search)
        else:
            print(f'\'{cctv_folder}\' 폴더에 검색할 이미지가 없습니다.')