from pathlib import Path
import shutil
import sys
import file_parse as parser


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", 'i', "ji", "g")


TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name) -> str:
    t_name = name.translate(TRANS)
    path_name = Path(t_name)
    stem_name = path_name.stem
    type_name = path_name.suffix
    result = ''
    for i in stem_name:
        if 'a' <= i <= 'z' or 'A' <= i <= 'Z' or '0' <= i <= '9':
            result += i
            continue
        else:
            result += '_'
    result += type_name

    return result


def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_arhive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return None
    filename.unlink()

def handle_folder(folder: Path) -> None:
    try:
        folder.rmdir()
    except OSError:
        print(f'Sorry, we can not delete the folder: {folder}')


def main(folder: Path) -> None:
    parser.scan(folder)
    for file in parser.IMAGES:
        handle_media(file, folder / 'images')
    for file in parser.AUDIO:
        handle_media(file, folder / 'audio')
    for file in parser.DOCUMENTATION:
        handle_media(file, folder / 'documentation')
    for file in parser.VIDEO:
        handle_media(file, folder / 'video')
    for file in parser.MY_OTHER:
        handle_other(file, folder / 'MY_OTHER')

    for file in parser.ARCHIVES:
        handle_arhive(file, folder / 'archives')

    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


if __name__ == '__main__':
    folder_for_scan = Path(sys.argv[1])
    main(folder_for_scan.resolve())