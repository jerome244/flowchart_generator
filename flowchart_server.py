import http.server
import socketserver
import cgi
from flowchart_generator import generate_flowchart_from_c_code  # Corrected import

PORT = 8082  # Set a fixed port number

class FlowchartHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Flowchart Generator</title>
                    <style>
                        body {
                            font-family: 'Arial', sans-serif;
                            background: linear-gradient(135deg, #1e1e1e, #2a2a2a);
                            color: #fff;
                            margin: 0;
                            padding: 0;
                            height: 100vh;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                            transition: all 0.3s ease;
                        }
                        h1 {
                            font-size: 2.5rem;
                            color: #FFD700;
                            text-align: center;
                            margin-bottom: 40px;
                            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
                        }
                        form {
                            background: rgba(255, 255, 255, 0.1);
                            padding: 40px;
                            border-radius: 12px;
                            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                            text-align: center;
                            width: 100%;
                            max-width: 400px;
                            transition: background-color 0.3s ease;
                        }
                        form:hover {
                            background: rgba(255, 255, 255, 0.2);
                        }
                        input[type="file"] {
                            background: #333;
                            color: #fff;
                            border: none;
                            border-radius: 5px;
                            padding: 12px;
                            width: 100%;
                            margin: 10px 0;
                            font-size: 16px;
                            cursor: pointer;
                            transition: background-color 0.3s ease;
                        }
                        input[type="file"]:hover {
                            background: #444;
                        }
                        button {
                            background: #FFD700;
                            color: #333;
                            font-size: 18px;
                            padding: 12px 25px;
                            border: none;
                            border-radius: 5px;
                            cursor: pointer;
                            margin-top: 20px;
                            transition: background-color 0.3s ease;
                        }
                        button:hover {
                            background: #FF9900;
                        }
                        .menu {
                            position: absolute;
                            top: 20px;
                            right: 20px;
                            background: rgba(0, 0, 0, 0.5);
                            border-radius: 8px;
                            padding: 10px 20px;
                        }
                        .menu a {
                            color: #FFD700;
                            text-decoration: none;
                            padding: 10px;
                            display: block;
                            transition: background-color 0.3s ease;
                            font-size: 16px;
                        }
                        .menu a:hover {
                            background-color: #FF9900;
                        }
                        footer {
                            position: fixed;
                            bottom: 10px;
                            text-align: center;
                            width: 100%;
                            color: #bbb;
                            font-size: 1rem;
                        }
                        footer a {
                            color: #FFD700;
                            text-decoration: none;
                            font-size: 1rem;
                        }
                        footer a:hover {
                            color: #FF9900;
                        }
                        @media (max-width: 768px) {
                            h1 {
                                font-size: 2rem;
                            }
                            form {
                                width: 90%;
                            }
                        }
                    </style>
                </head>
                <body>
                    <div class="menu">
                        <a href="#about" id="about-link">About</a>
                        <a href="#help" id="help-link">Help</a>
                    </div>
                    <h1>Flowchart Generator</h1>
                    <form enctype="multipart/form-data" method="post" action="/upload">
                        <label for="file" style="font-size: 1.2rem;">Upload Your C Code File</label>
                        <input type="file" name="file" accept=".c" id="file" required><br>
                        <button type="submit">Generate Flowchart</button>
                    </form>
                    <footer>
                        <p>&copy; 2025 Flowchart Converter | <a href="#">Privacy</a></p>
                    </footer>

                    <script>
                        document.getElementById('about-link').addEventListener('click', function(e) {
                            alert('This tool generates flowcharts from C code. Upload a C code file to generate a flowchart!');
                        });

                        document.getElementById('help-link').addEventListener('click', function(e) {
                            alert('For help, please refer to the documentation or contact support.');
                        });
                    </script>
                </body>
                </html>
            ''')

        else:
            self.send_error(404, 'Page Not Found')

    def do_POST(self):
        if self.path == '/upload':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            file_item = form['file']
            if file_item.filename:
                uploaded_code = file_item.file.read().decode('utf-8')
                flowchart_html = generate_flowchart_from_c_code(uploaded_code)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Flowchart Result</title>
                        <style>
                            body {
                                font-family: 'Arial', sans-serif;
                                background: linear-gradient(135deg, #1e1e1e, #2a2a2a);
                                color: #fff;
                                margin: 0;
                                padding: 0;
                                display: flex;
                                flex-direction: column;
                                align-items: center;
                                justify-content: center;
                                min-height: 100vh;
                            }
                            h1 {
                                font-size: 2.5rem;
                                color: #FFD700;
                                margin-bottom: 40px;
                                text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
                            }
                            .flowchart-container {
                                width: 80%;
                                max-width: 1000px;
                                padding: 20px;
                                background: rgba(255, 255, 255, 0.1);
                                border-radius: 12px;
                                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                                margin-bottom: 40px;
                                overflow-wrap: break-word;
                                transition: transform 0.3s ease;
                            }
                            h2 {
                                font-size: 1.8rem;
                                color: #FFD700;
                                text-align: center;
                            }
                            pre {
                                background: #333;
                                padding: 20px;
                                border-radius: 10px;
                                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                                width: 100%;
                                overflow-wrap: break-word;
                                white-space: pre-wrap;
                                word-wrap: break-word;
                            }
                            .zoom-controls {
                                position: fixed;
                                left: 20px;
                                bottom: 20px;
                                display: flex;
                                flex-direction: column;
                                align-items: center;
                                background: rgba(0, 0, 0, 0.5);
                                border-radius: 8px;
                                padding: 10px 20px;
                                z-index: 10;
                            }
                            .zoom-button {
                                padding: 10px 20px;
                                background: #FFD700;
                                color: #333;
                                border: none;
                                font-size: 1.2rem;
                                cursor: pointer;
                                margin: 5px;
                                border-radius: 5px;
                                transition: background-color 0.3s ease;
                            }
                            .zoom-button:hover {
                                background: #FF9900;
                            }
                            .button {
                                margin-top: 20px;
                            }
                            a {
                                text-decoration: none;
                                padding: 10px 20px;
                                background: #FFD700;
                                color: #333;
                                border-radius: 5px;
                                transition: background-color 0.3s ease;
                            }
                            a:hover {
                                background: #FF9900;
                            }
                        </style>
                    </head>
                    <body>
                        <h1>Flowchart Result</h1>
                        <div class="flowchart-container" id="flowchart-container">
                            <h2>Generated Flowchart</h2>
                            <pre>''')
                self.wfile.write(flowchart_html.encode())
                self.wfile.write(b'''</pre>
                        </div>
                        <div class="button">
                            <a href="/">Upload another file</a>
                        </div>
                        <div class="zoom-controls">
                            <button class="zoom-button" id="zoom-in">+</button>
                            <button class="zoom-button" id="zoom-out">-</button>
                        </div>
                        <script>
                            let zoomLevel = 1;
                            const zoomInButton = document.getElementById('zoom-in');
                            const zoomOutButton = document.getElementById('zoom-out');
                            const flowchartContainer = document.getElementById('flowchart-container');

                            zoomInButton.addEventListener('click', () => {
                                zoomLevel += 0.1;
                                flowchartContainer.style.transform = `scale(${zoomLevel})`;
                            });

                            zoomOutButton.addEventListener('click', () => {
                                zoomLevel = Math.max(0.5, zoomLevel - 0.1);  // Minimum zoom out level
                                flowchartContainer.style.transform = `scale(${zoomLevel})`;
                            });
                        </script>
                    </body>
                    </html>
                ''')
            else:
                self.send_error(400, "No file uploaded.")
        else:
            self.send_error(404, 'Invalid endpoint')

if __name__ == '__main__':
    with socketserver.TCPServer(('', PORT), FlowchartHandler) as httpd:
        print(f"Starting server on port {PORT}...")
        httpd.serve_forever()
