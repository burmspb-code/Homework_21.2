from http.server import BaseHTTPRequestHandler, HTTPServer

# Настройки сервера
hostName = "localhost"
serverPort = 8080


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

        # Читаем содержимое HTML-файла
        with open("contacts.html", "r", encoding="utf-8") as file:
            html_content = file.read()

        # Отправляем HTML-страницу клиенту вместо JSON-строки
        self.wfile.write(bytes(html_content, "utf-8"))


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрам в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Старт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")