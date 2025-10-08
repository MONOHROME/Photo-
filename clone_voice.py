import sys
import os
import argparse
import traceback

# --- ГЛАВНАЯ ДИАГНОСТИКА: Показываем, какой Python используется ---
print("--- Скрипт clone_voice.py успешно запущен ---")
print(f"!!! Этот скрипт выполняется с помощью Python по пути: {sys.executable}")
print(f"Версия Python: {sys.version}\n")

try:
    from moviepy.editor import VideoFileClip
    from TTS.api import TTS
except ImportError as e:
    print(f"!!! ОШИБКА ИМПОРТА: Не удалось найти необходимую библиотеку: {e}")
    print("\n--- Что делать? ---")
    print("1. Убедитесь, что вы установили библиотеки командой 'pip install moviepy TTS'.")
    print(
        "2. Если ошибка повторяется, выполните в терминале следующую команду, чтобы установить библиотеки именно для этого Python:"
    )
    print(f'"{sys.executable}" -m pip install moviepy TTS')
    sys.exit()

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def clone_voice_from_video(video_file: str, text_to_speak: str, output_filename: str) -> None:
    """Извлекает аудио из видео, клонирует голос и синтезирует речь из текста."""
    temp_audio_file = "temp_audio_for_cloning.wav"

    try:
        print("\n--- Процесс клонирования голоса запущен ---")

        if not os.path.exists(video_file):
            print(f"!!! ОШИБКА: Видеофайл не найден по пути: {video_file}")
            return

        print(f"\n[Шаг 1 из 3] Извлечение аудио из '{video_file}'...")
        video_clip = VideoFileClip(video_file)
        video_clip.audio.write_audiofile(temp_audio_file, codec="pcm_s16le", logger=None)
        video_clip.close()
        print(f"-> Аудио успешно извлечено и сохранено в '{temp_audio_file}'")

        print("\n[Шаг 2 из 3] Загрузка модели Text-to-Speech...")
        print("-> Это может занять много времени при первом запуске, так как модель скачивается (~2 ГБ).")
        print("-> Пожалуйста, дождитесь окончания загрузки...")

        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False, progress_bar=True)
        print("-> Модель успешно загружена.")

        print(f"\n[Шаг 3 из 3] Клонирование голоса и синтез речи в файл '{output_filename}'...")
        tts.tts_to_file(
            text=text_to_speak,
            file_path=output_filename,
            speaker_wav=temp_audio_file,
            language="ru",
        )
        print("-> Синтез речи завершен!")

    except Exception as exc:
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!           ПРОИЗОШЛА ОШИБКА            !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"\nТип ошибки: {type(exc).__name__}")
        print(f"Сообщение: {exc}")
        print("\n--- Полная трассировка ошибки: ---")
        traceback.print_exc()
        print("\n------------------------------------")

    finally:
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)
            print(f"\n-> Временный аудиофайл '{temp_audio_file}' удален.")

        print(
            f"\n--- Работа скрипта завершена. Результат должен быть в файле: {output_filename} ---"
        )


def _prompt_for_missing_args() -> argparse.Namespace:
    """Интерактивно запрашивает недостающие параметры у пользователя."""
    print("\nПохоже, что вы запустили скрипт без аргументов.")
    print("Сейчас программа задаст несколько вопросов и подставит ответы автоматически.\n")

    video_file = input("Введите полный путь к видеофайлу: ").strip()
    while not video_file:
        print("Путь к видео обязателен.")
        video_file = input("Введите полный путь к видеофайлу: ").strip()

    text_to_speak = input("Введите текст, который нужно озвучить: ").strip()
    while not text_to_speak:
        print("Текст не может быть пустым.")
        text_to_speak = input("Введите текст, который нужно озвучить: ").strip()

    output_filename = input(
        "Введите имя выходного аудиофайла (по умолчанию cloned_voice.wav): "
    ).strip()
    if not output_filename:
        output_filename = "cloned_voice.wav"

    return argparse.Namespace(
        video_file=video_file,
        text_to_speak=text_to_speak,
        output_filename=output_filename,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Клонирование речевого стиля из видеофайла.",
        add_help=len(sys.argv) > 1,
    )
    parser.add_argument("--video_file", type=str, help="Путь к входному видеофайлу.")
    parser.add_argument("--text_to_speak", type=str, help="Текст, который нужно озвучить.")
    parser.add_argument("--output_filename", type=str, help="Имя выходного аудиофайла.")

    if len(sys.argv) > 1:
        args = parser.parse_args()
        missing = [
            name
            for name, value in [
                ("--video_file", args.video_file),
                ("--text_to_speak", args.text_to_speak),
                ("--output_filename", args.output_filename),
            ]
            if not value
        ]
        if missing:
            parser.error(
                "Не все аргументы указаны. Отсутствуют: " + ", ".join(missing)
            )
    else:
        args = _prompt_for_missing_args()

    clone_voice_from_video(args.video_file, args.text_to_speak, args.output_filename)

    if sys.platform == "win32":
        input("\nНажмите Enter, чтобы закрыть окно...")


if __name__ == "__main__":
    main()
