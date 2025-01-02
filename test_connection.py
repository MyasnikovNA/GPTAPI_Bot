from gpt_handler import test_connection

if test_connection():
    print("Подключение успешно!")
else:
    print("Ошибка подключения.")
