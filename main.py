from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Возвращает страницу Контакты на любой GET-запрос"""
        try:
            with open('templates/contacts.html', 'r', encoding='utf-8') as file:
                html_content = file.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, 'Страница не найдена')

    def do_POST(self):
        """Дополнительное задание: печатаем данные в консоль"""
        if self.path == '/submit-form':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            print("\n" + "=" * 50)
            print("📬 Получены данные от пользователя:")
            for key, value in parsed_data.items():
                print(f"   {key}: {value[0]}")
            print("=" * 50 + "\n")

            # Отправляем ответ пользователю
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b"""
                <!DOCTYPE html>
                <html>
                <head><title>Успешно</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                </head>
                <body>
                <div class="container text-center mt-5">
                    <div class="alert alert-success">
                        <h4>Спасибо! Данные получены.</h4>
                        <a href="/" class="btn btn-primary mt-3">Вернуться на главную</a>
                    </div>
                </div>
                </body>
                </html>
            """)
        else:
            self.send_error(404)


def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'🚀 Сервер запущен: http://localhost:{port}')
    print(f'📞 Открыта страница Контактов')
    print(f'💡 Для завершения нажмите Ctrl+C')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()