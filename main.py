from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Обработка GET-запросов"""
        if self.path == '/' or self.path == '/home':
            # Возвращаем главную страницу
            try:
                with open('templates/home.html', 'r', encoding='utf-8') as file:
                    html_content = file.read()

                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, 'Страница home.html не найдена')

        elif self.path == '/contacts':
            # Возвращаем страницу контактов
            try:
                with open('templates/contacts.html', 'r', encoding='utf-8') as file:
                    html_content = file.read()

                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, 'Страница contacts.html не найдена')

        else:
            self.send_error(404, 'Страница не найдена')

    def do_POST(self):
        """Дополнительное задание: печать данных из формы в консоль"""
        if self.path == '/submit-form':
            # Получаем длину тела запроса
            content_length = int(self.headers['Content-Length'])
            # Читаем данные
            post_data = self.rfile.read(content_length)
            # Парсим данные формы
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            # Выводим в консоль
            print("\n" + "=" * 50)
            print("📬 Получены данные от пользователя:")
            for key, value in parsed_data.items():
                print(f"   {key}: {value[0]}")
            print("=" * 50 + "\n")

            # Отправляем ответ пользователю
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # HTML-ответ об успешной отправке
            response = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Сообщение отправлено</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body>
                <div class="container text-center mt-5">
                    <div class="alert alert-success">
                        <h4>✅ Спасибо! Ваше сообщение отправлено.</h4>
                        <p>Мы свяжемся с вами в ближайшее время.</p>
                        <a href="/" class="btn btn-primary mt-3">Вернуться на главную</a>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_error(404)


def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'🚀 Сервер запущен на http://localhost:{port}')
    print(f'🏠 Главная страница: http://localhost:{port}/')
    print(f'📞 Страница контактов: http://localhost:{port}/contacts')
    print(f'💡 Для завершения нажмите Ctrl+C')
    print(f'\n📝 Форма отправляет данные на /submit-form')
    print(f'   Все POST-данные будут выведены в эту консоль\n')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()