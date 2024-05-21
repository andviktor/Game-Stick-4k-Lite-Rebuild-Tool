# Game Stick 4k Lite - Database rebuild tool

## English manual (Русский - см. ниже)

The tool is designed to organize the game library of console GameStick 4k lite. It allows you to automatically tidy up the names of ROM files and completely rebuild the database.

### How to use
1. Download the ROMs to the appropriate folder inside the “game” folder on the micro SD card.
2. Make sure that the ROM's names do not contain extra dots. **Only one dot is allowed followed by the file extension!**
2. Clone this repository to the game console game folder using the **git clone https://github.com/andviktor/Game-Stick-4k-Lite-Rebuild-Tool** command.
3. Go to the cloned repository folder.
4. Activate the virtual environment with command **venv/scripts/Activate** on **Windows** and **source venv/bin/activate** on **Linux and Macos**
5. Install the necessary packages using command **pip install -r requirements.txt**
6. Change the configuration if necessary in the **.env file**
7. Run the program with command **python rebuild.py**

### Game covers:

If desired, download the game covers in PNG format into the same folder with ROMs. The recommended aspect ratio is 1.75, for example: 875 x 500 or 438 x 250.

After executing the program, you must manually assign the pictures the same names as the ROM files.

Covers are often oriented vertically or have the wrong aspect ratio. In this case, it is convenient to use the Fast Stone Image Viewer program. This program has batch processing that will allow you to first set the height of all covers (for example, 250), and then you can resize the canvas to the required width (for example, 438) with a black background.

## Инструкция на русском

Инструмент предназначен для оформления библиотеки игр консоли GameStick 4k lite. Позволяет автоматически привести в порядок имена файлов ромов и полностью пересобрать базу данных.

### Как пользоваться
1. Загрузите ромы в папку соотв. консоли внутри папки **game** на микро sd карте.
2. Удостоверьтесь, что имена ромов не содержат лишних точек. **Допустима только одна точка после которой следует расширение файла!**
2. Склонируйте данный репозиторий в папку **game** консоли при помощи команды **git clone https://github.com/andviktor/Game-Stick-4k-Lite-Rebuild-Tool**
3. Перейдите в созданную папку репозитория.
4. Активируйте виртуальное окружение командой **venv/scripts/Activate** на **Windows** или **source venv/bin/activate** на **Linux и Macos**
5. Установите необходимые пакеты при помощи команды **pip install -r requirements.txt**
6. Измените конфигурацию при необходимости в файле **.env**
7. Запустите программу командой **python rebuild.py**

### Обложки игр

При желании загрузите обложки игр в формате png в ту же папку где лежат ромы. Рекомендуемое соотношение сторон 1.75, например: 875 х 500 или 438 х 250.

Часто обложки имеют вертикальную ориентацию или неверное соотношение сторон. В этом случае удобно использовать программу Fast Stone Image Viewer. В данной программе есть пакетная обработка, которая позволит сначала задать у всех обложек высоту (например 250), а затем можно изменить размер холста до необходимой ширины (например 438) с черным фоном.