import os

folder_path = 'D:\\images'  # 파일이 들어 있는 폴더 경로 입력

files = os.listdir(folder_path)


for i, file in enumerate(files, start=1):
    _, ext = os.path.splitext(file)  # 파일 확장자 분리
    new_name = f"{i}{ext}"
    os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_name))