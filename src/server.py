import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Настройки сервера
hostName = "localhost"
serverPort = 8080

# Автоматически определяем путь к папке src, где лежат HTML-файлы
BASE_DIR = Path(__file__).resolve().parent


class MyServer(BaseHTTPRequestHandler):
    """
    Специальный класс, который отвечает за
    обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """Метод для обработки входящих GET-запросов"""
        self.send_response(200)  # Отправка кода ответа

        # Меняем тип данных на text/html и добавляем кодировку для кириллицы
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()  # Завершение формирования заголовков ответа

        # Читаем содержимое HTML-файла с использованием точного пути
        template_path = BASE_DIR / "contacts.html"
        with open(template_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Отправляем HTML-страницу клиенту вместо JSON-строки
        self.wfile.write(bytes(html_content, "utf-8"))

    def do_POST(self):
        """Метод для обработки входящих POST-запросов из формы"""

        # 1. Определяем размер входящих данных (сколько байт прислал браузер)
        content_length = int(self.headers['Content-Length'])

        # 2. Считываем строго указанное количество байт из потока ввода rfile
        raw_post_data = self.rfile.read(content_length)

        # 3. Переводим байты в обычную строку
        post_data_str = raw_post_data.decode('utf-8')

        # 4. Декодируем строку формата application/x-www-form-urlencoded
        parsed_data = urllib.parse.parse_qs(post_data_str)

        # Безопасно извлекаем первые элементы списков, избегая IndexError при пустых полях
        cleaned_data = {key: value[0] for key, value in parsed_data.items() if value}

        # 5. Печатаем принятые данные в консоль сервера
        print("\n" + "=" * 30)
        print("ПОЛУЧЕНЫ ДАННЫЕ ИЗ ФОРМЫ (POST):")
        print(f"Имя пользователя: {cleaned_data.get('username', 'Не указано')}")
        print(f"Электронная почта: {cleaned_data.get('email', 'Не указана')}")
        print(f"Сообщение: {cleaned_data.get('message', 'Пустое сообщение')}")
        print("=" * 30 + "\n")

        # 6. Отправляем ответ пользователю, чтобы страница в браузере не «зависла»
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        # Возвращаем пользователю ту же страницу контактов по точному пути
        template_path = BASE_DIR / "contacts.html"
        with open(template_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        self.wfile.write(bytes(html_content, "utf-8"))


def run():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    run()