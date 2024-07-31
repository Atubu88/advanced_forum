import os

def find_duplicates(static_dirs):
    file_paths = {}
    duplicates = []

    for static_dir in static_dirs:
        for root, _, files in os.walk(static_dir):
            for file in files:
                file_path = os.path.relpath(os.path.join(root, file), static_dir)
                if file_path in file_paths:
                    duplicates.append(file_path)
                else:
                    file_paths[file_path] = os.path.join(root, file)

    return duplicates

# Пример использования
static_dirs = [
    os.path.join(BASE_DIR, 'accounts/static'),
    os.path.join(BASE_DIR, 'another_app/static'),
]

duplicates = find_duplicates(static_dirs)
if duplicates:
    print("Найдены дубликаты:")
    for file_path in duplicates:
        print(file_path)
else:
    print("Дубликаты не найдены.")
