import os
import shutil
from PIL import Image
import hashlib

def process_images(source_dir, destination_dir):
    # Создаем папку назначения, если она не существует
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    else:
        # Очищаем папку назначения
        shutil.rmtree(destination_dir)
        os.makedirs(destination_dir)

    # Получаем список файлов в директории и фильтруем только изображения
    image_files = [f for f in os.listdir(source_dir) if f.endswith((".jpg", ".jpeg", ".png", ".webp"))]

    # Обработка каждого изображения
    for file_name in image_files:
        # Полный путь к исходному изображению
        source_path = os.path.join(source_dir, file_name)

        # Загрузка исходного изображения
        original_image = Image.open(source_path)

        # Сохранение обработанного изображения с тем же именем
        destination_path = os.path.join(destination_dir, file_name)

        original_image.save(destination_path)

        # Вычисление хеш-суммы исходного изображения
        original_hash = calculate_file_hash(source_path)

        # Вычисление хеш-суммы измененного изображения
        modified_hash = calculate_file_hash(destination_path)

        if original_hash != modified_hash:
            print("Хеш-сумма изображения", file_name, "изменилась.")
        else:
            print("Хеш-сумма изображения", file_name, "не изменилась.")

        remove_metadata(destination_path)

        print("Обработано изображение:", file_name)

def calculate_file_hash(file_path):
    # Создаем объект хеша
    hasher = hashlib.md5()

    # Открываем файл в бинарном режиме и читаем его блоками
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            # Обновляем хеш-сумму
            hasher.update(chunk)

    # Возвращаем полученную хеш-сумму в виде строки
    return hasher.hexdigest()

def remove_metadata(image_path):
    # Открываем изображение
    image = Image.open(image_path)

    # Создаем копию изображения без метаданных
    image_without_metadata = image.copy()

    print("Метаданные до", image_without_metadata.info, os.path.basename(image_path))

    # Удаляем все метаданные из копии изображения
    image_without_metadata.info = {}

    print("Метаданные после", image_without_metadata.info, os.path.basename(image_path))


    # Сохраняем изображение без метаданных (перезаписываем исходное изображение)
    image_without_metadata.save(image_path)

    print("Метаданные удалены из изображения:", os.path.basename(image_path))

source_directory = "src"
destination_directory = "dist"

# Вызов функции для обработки изображений
process_images(source_directory, destination_directory)
