import sys
from pathlib import Path


IMAGES = [] #JPEG_IMAGES, JPG_IMAGES, PNG_IMAGES, SVG_IMAGES
DOCUMENTATION = [] #DOC_DOCUMENTATION, DOCX_DOCUMENTATION, TXT_DOCUMENTATION, PDF_DOCUMENTATION, XLSX_DOCUMENTATION, PPTX_DOCUMENTATION
VIDEO = [] #MP4_VIDEO MOV_VIDEO MKV_VIDEO
AUDIO = [] #MP3_AUDIO OGG_AUDIO WAV_AUDIO AMR_AUDIO
ARCHIVES = [] #ZIP_ARCHIVES GZ_ARCHIVES TAR_ARCHIVES
MY_OTHER = []  #Other file extention

REGISTER_EXTENSION = {
    'JPEG': IMAGES,
    'JPG': IMAGES,
    'PNG': IMAGES,
    'SVG': IMAGES,
    'AVI': VIDEO,
    'MP4': VIDEO, 
    'MOV': VIDEO,
    'MKV': VIDEO,
    'DOC': DOCUMENTATION,
    'DOCX': DOCUMENTATION,
    'TXT': DOCUMENTATION,
    'PDF': DOCUMENTATION,
    'XLSX': DOCUMENTATION,
    'PPTX': DOCUMENTATION,
    'MP3': AUDIO,
    'OGG': AUDIO,
    'WAV': AUDIO,
    'AMR': AUDIO,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def scan(folder: Path):
    for item in folder.iterdir():
        # Робота з папкою
        if item.is_dir():
            # Перевіряємо, щоб папка не була тією в яку ми вже складаємо файли.
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'other'):
                FOLDERS.append(item)
                scan(item)  # скануємо цю вкладену папку - рекурсія
            continue  # переходимо до наступного елемента в сканованій папці
        # else:
        # Робота з файлом
        ext = get_extension(item.name)  # беремо розширення файлу
        # full_name = folder / item.name  # беремо повний шлях до файлу
        if not ext:
            MY_OTHER.append(item)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENSIONS.add(ext)
                container.append(item)
            except KeyError:
                UNKNOWN.add(ext)
                MY_OTHER.append(item)


if __name__ == '__main__':
    scan_folder = sys.argv[1]
    print(scan_folder)
    print(f'Start in folder: {scan_folder}')

    scan(Path(scan_folder))
    print(f'IMAGES : {IMAGES}')
    print(f'AUDIO : {AUDIO}')
    print(f'ARCHIVES: {ARCHIVES}')
    print(f'VIDEO: {VIDEO}')
    print(f'DOCUMENTATION: {DOCUMENTATION}')
    print(f'OTHER FILES: {MY_OTHER}')
    print('*' * 25)
    print(f'Types of file in folder: {EXTENSIONS}')
    print(f'UNKNOWN: {UNKNOWN}')
