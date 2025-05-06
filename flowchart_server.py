import http.server
import socketserver
import cgi
from flowchart_generator import generate_flowchart_from_c_code, generate_flowchart_from_python

PORT = 8082

class FlowchartHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            html = '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Code Reading/Diagram Understand Helper</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background: #121212;
                        color: #fff;
                        margin: 0;
                        padding: 0;
                        height: 100vh;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                    }
                    h1 {
                        color: #FFD700;
                        font-size: 2.5rem;
                        margin-bottom: 40px;
                    }
                    form {
                        background: rgba(255, 255, 255, 0.05);
                        padding: 40px;
                        border-radius: 12px;
                        text-align: center;
                        max-width: 400px;
                        width: 100%;
                    }
                    input[type="file"] {
                        background: #333;
                        color: #fff;
                        border: none;
                        border-radius: 5px;
                        padding: 12px;
                        width: 100%;
                        margin: 10px 0;
                    }
                    button {
                        background: #FFD700;
                        color: #333;
                        font-size: 16px;
                        padding: 12px 25px;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        margin-top: 20px;
                    }
                    button:hover {
                        background: #FF9900;
                    }
                    footer {
                        position: fixed;
                        bottom: 10px;
                        width: 100%;
                        text-align: center;
                        color: #bbb;
                    }
                    footer a {
                        color: #FFD700;
                        text-decoration: none;
                    }
                </style>
            </head>
            <body>
                <h1>Code Reading/Diagram Understand Helper</h1>
                <form enctype="multipart/form-data" method="post" action="/upload">
                    <label for="file">Upload your .c or .py file</label><br>
                    <input type="file" name="file" accept=".c,.py" required><br>
                    <button type="submit">Generate Flowchart</button>
                </form>
                <footer>
                    <p>&copy; 2025 Flowchart Converter</p>
                </footer>
            </body>
            </html>
            '''
            self.wfile.write(html.encode('utf-8'))

        else:
            self.send_error(404, 'Page Not Found')

    def do_POST(self):
        if self.path == '/upload':
            try:
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                if "file" in form:
                    file_item = form["file"]
                    uploaded_code = file_item.file.read().decode("utf-8")

                    if file_item.filename.endswith('.c'):
                        flowchart_html = generate_flowchart_from_c_code(uploaded_code)
                    elif file_item.filename.endswith('.py'):
                        flowchart_html = generate_flowchart_from_python(uploaded_code)
                    else:
                        self.send_error(400, "Unsupported file type. Only .c and .py are supported.")
                        return

                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Flowchart Result</title>
<style>
    body {{
        background-color: #121212;
        color: #f5f5f5;
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 40px;
    }}
    h1 {{
        text-align: center;
        color: #FFD700;
    }}
    .flowchart-container {{
        background: #1e1e1e;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        margin: 0 auto;
        max-width: 1000px;
        transform-origin: top left;
        transition: transform 0.2s ease-in-out;
    }}
    a {{
        display: block;
        width: fit-content;
        margin: 30px auto;
        background: #FFD700;
        color: #000;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
    }}
    .zoom-controls {{
        position: fixed;
        bottom: 20px;
        left: 20px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        z-index: 999;
    }}
    .zoom-button {{
        background: #FFD700;
        color: #000;
        font-weight: bold;
        font-size: 20px;
        border: none;
        border-radius: 5px;
        width: 40px;
        height: 40px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }}
    .zoom-button:hover {{
        background-color: #FF9900;
    }}
</style>
</head>
<body>
<h1>Flowchart Result</h1>
<div class="flowchart-container" id="flowchart-container">
{flowchart_html}
</div>
<a href="/">Upload another file</a>

<div class="zoom-controls">
    <button class="zoom-button" id="zoom-in">+</button>
    <button class="zoom-button" id="zoom-out">–</button>
</div>

<script>
let zoomLevel = 1.0;
const container = document.getElementById('flowchart-container');
document.getElementById('zoom-in').onclick = () => {{
    zoomLevel += 0.1;
    container.style.transform = `scale(${{zoomLevel}})`;
}};
document.getElementById('zoom-out').onclick = () => {{
    zoomLevel = Math.max(0.5, zoomLevel - 0.1);
    container.style.transform = `scale(${{zoomLevel}})`;
}};
</script>
</body>
</html>
'''
                    self.wfile.write(html.encode('utf-8'))

                else:
                    self.send_error(400, "No file uploaded.")

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                error_msg = f"Server error: {e}"
                print(error_msg)
                self.wfile.write(error_msg.encode('utf-8'))

        else:
            self.send_error(404, 'Page Not Found')

with socketserver.TCPServer(("", PORT), FlowchartHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()

