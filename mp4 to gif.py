import os
import subprocess
import glob
import sys


def check_ffmpeg(ffmpeg_path='ffmpeg'):
    """Проверяет, доступен ли FFmpeg по указанному пути"""
    try:
        subprocess.run([ffmpeg_path, '-version'],
                       capture_output=True,
                       check=True,
                       text=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def find_ffmpeg_windows():
    """Пытается найти FFmpeg в типичных местах установки в Windows"""
    possible_paths = [
        r'C:\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe',
        os.path.join(os.environ.get('ProgramFiles', ''), 'ffmpeg', 'bin', 'ffmpeg.exe'),
        os.path.join(os.environ.get('ProgramFiles(x86)', ''), 'ffmpeg', 'bin', 'ffmpeg.exe'),
    ]

    for path in possible_paths:
        if os.path.isfile(path):
            return path
    return None


def convert_videos_to_gif(folder_path, ffmpeg_path):
    # Поддерживаемые форматы видео
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.flv', '*.wmv']

    # Находим все видеофайлы в папке
    video_files = []
    for extension in video_extensions:
        video_files.extend(glob.glob(os.path.join(folder_path, extension)))

    if not video_files:
        print("В указанной папке не найдено видеофайлов.")
        return

    for video_path in video_files:
        # Генерируем имя для выходного файла
        base_name = os.path.splitext(video_path)[0]
        output_path = base_name + ".gif"

        # Создаем временный файл для палитры
        palette_path = base_name + "_palette.png"

        # Двухэтапный процесс для лучшего качества:
        # 1. Генерация оптимальной палитры
        # 2. Создание GIF с использованием палитры

        # Первый этап: генерация палитры
        palette_command = [
            ffmpeg_path,
            '-i', video_path,
            '-vf', 'fps=15,scale=800:-1:flags=lanczos,palettegen=stats_mode=diff',
            '-y',  # Перезаписать файл, если существует
            palette_path
        ]

        # Второй этап: создание GIF с использованием палитры
        gif_command = [
            ffmpeg_path,
            '-i', video_path,
            '-i', palette_path,
            '-filter_complex',
            'fps=15,scale=800:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=sierra2:diff_mode=rectangle',
            '-loop', '0',  # Бесконечное зацикливание
            '-y',  # Перезаписать файл, если существует
            output_path
        ]

        try:
            print(f"Обрабатывается: {os.path.basename(video_path)}")

            # Генерируем палитру
            print("Генерация палитры...")
            subprocess.run(palette_command, check=True, capture_output=True, text=True)

            # Создаем GIF
            print("Создание GIF...")
            subprocess.run(gif_command, check=True, capture_output=True, text=True)

            # Удаляем временный файл палитры
            if os.path.exists(palette_path):
                os.remove(palette_path)

            print(f"Успешно конвертирован: {os.path.basename(video_path)}")

        except subprocess.CalledProcessError as e:
            print(f"Ошибка при конвертации {video_path}: {e.stderr}")
            # Удаляем временный файл палитры в случае ошибки
            if os.path.exists(palette_path):
                os.remove(palette_path)
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            # Удаляем временный файл палитры в случае ошибки
            if os.path.exists(palette_path):
                os.remove(palette_path)


if __name__ == "__main__":
    # Проверяем наличие FFmpeg в PATH
    ffmpeg_path = 'ffmpeg'
    if not check_ffmpeg(ffmpeg_path):
        print("FFmpeg не найден в PATH. Пытаемся найти в стандартных местах...")
        custom_ffmpeg_path = find_ffmpeg_windows()

        if custom_ffmpeg_path and check_ffmpeg(custom_ffmpeg_path):
            print(f"Найден FFmpeg по пути: {custom_ffmpeg_path}")
            ffmpeg_path = custom_ffmpeg_path
        else:
            print("FFmpeg не установлен. Пожалуйста, установите FFmpeg:")
            print("1. Скачайте с https://github.com/BtbN/FFmpeg-Builds/releases")
            print("2. Распакуйте архив в C:\\ffmpeg")
            print("3. Добавьте C:\\ffmpeg\\bin в системную переменную PATH")
            print("Или введите полный путь к ffmpeg.exe вручную:")
            custom_ffmpeg_path = input("Путь к ffmpeg.exe: ").strip().strip('"')

            if os.path.isfile(custom_ffmpeg_path) and check_ffmpeg(custom_ffmpeg_path):
                ffmpeg_path = custom_ffmpeg_path
            else:
                print("Указанный файл не существует или не является рабочей версией FFmpeg!")
                sys.exit(1)

    folder_path = input("Введите путь к папке с видеофайлами: ").strip().strip('"')

    # Проверяем существование папки
    if not os.path.isdir(folder_path):
        print("Указанная папка не существует!")
    else:
        convert_videos_to_gif(folder_path, ffmpeg_path)
