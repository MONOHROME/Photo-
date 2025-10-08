# Photo Voice Cloner

Этот репозиторий содержит CLI-утилиту `clone_voice.py`, позволяющую извлечь речь из видео и сгенерировать новое аудио с тем же голосом на основе введённого текста.

## Как запустить скрипт, если вы новичок

1. **Убедитесь, что Python установлен.**
   * Windows: скачайте [python.org](https://www.python.org/downloads/), установите, отметив галочку «Add Python to PATH».
   * macOS: Python 3 уже установлен. При необходимости обновите через [Homebrew](https://brew.sh/): `brew install python`.
   * Linux: установите через менеджер пакетов, например `sudo apt install python3 python3-pip`.

2. **Откройте терминал/командную строку** и перейдите в папку с проектом. Например:
   ```bash
   cd путь/к/папке/Photo-
   ```

3. **Создайте виртуальное окружение (необязательно, но полезно):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

4. **Установите зависимости:**
   ```bash
   pip install --upgrade pip
   pip install moviepy TTS
   ```

5. **Запустите скрипт одним из способов:**
   * **С аргументами:**
     ```bash
     python clone_voice.py --video_file sample.mp4 --text_to_speak "Привет, мир" --output_filename result.wav
     ```
   * **В интерактивном режиме (без аргументов):**
     ```bash
     python clone_voice.py
     ```
     Скрипт задаст вопросы и подставит ответы автоматически.

6. **Дождитесь окончания процесса.** При первом запуске модель TTS скачивается (~2 ГБ), поэтому процесс может занять несколько минут.

7. **Готово!** В папке появится файл с озвучкой, который вы указали на шаге 5.
