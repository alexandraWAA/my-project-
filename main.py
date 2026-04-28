from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Обработка GET-запросов для всех страниц"""

        # Маршрутизация страниц
        routes = {
            '/': 'templates/home.html',
            '/home': 'templates/home.html',
            '/catalog': 'templates/catalog.html',
            '/category': 'templates/category.html',
            '/contacts': 'templates/contacts.html',
            '/orders': 'templates/category.html',  # пока просто категория
        }

        if self.path in routes:
            try:
                with open(routes[self.path], 'r', encoding='utf-8') as file:
                    html_content = file.read()

                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, f'Страница {routes[self.path]} не найдена')
        else:
            self.send_error(404, 'Страница не найдена')

    def do_POST(self):
        """Обработка POST-запросов (печать в консоль)"""
        if self.path == '/submit-form':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            print("\n" + "=" * 50)
            print("📬 Получены данные от пользователя:")
            for key, value in parsed_data.items():
                print(f"   {key}: {value[0]}")
            print("=" * 50 + "\n")

            # HTML-ответ
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

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
    print(f'🏠 Главная: http://localhost:{port}/')
    print(f'📦 Каталог: http://localhost:{port}/catalog')
    print(f'📂 Категория: http://localhost:{port}/category')
    print(f'📞 Контакты: http://localhost:{port}/contacts')
    print(f'💡 Для завершения нажмите Ctrl+C')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()