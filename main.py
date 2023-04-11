from flask import Flask, render_template, send_from_directory
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from flask_frozen import Freezer
import shutil

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['DEBUG'] = True
freezer = Freezer(app)

class FontEventHandler(FileSystemEventHandler):
    def __init__(self, path):
        self.path = path

    def on_created(self, event):
        if not event.is_directory and (event.src_path.endswith('.ttf')
                                       or event.src_path.endswith('.otf')):
            if os.path.dirname(event.src_path) == self.path:
                generate_stylesheet()

    def on_deleted(self, event):
        if not event.is_directory and (event.src_path.endswith('.ttf')
                                       or event.src_path.endswith('.otf')):
            if os.path.dirname(event.src_path) == self.path:
                generate_stylesheet()


def generate_stylesheet():
    fonts_path = os.path.join(os.getcwd(), 'fonts')
    fonts = [
        f for f in os.listdir(fonts_path)
        if f.endswith('.ttf') or f.endswith('.otf')
    ]

    with open('static/style.css', 'w') as f:
        for font in fonts:
            font_name = os.path.splitext(font)[0]
            font_ext = os.path.splitext(font)[1][1:]
            font_format = 'opentype' if font_ext == 'otf' else 'truetype'
            f.write('@font-face {\n')
            f.write(f'\tfont-family: "{font_name}";\n')
            f.write(f'\tsrc: url("./fonts/{font}") format("{font_format}");\n')
            f.write('}\n')


observer = Observer()
observer.schedule(FontEventHandler('fonts'), path='fonts', recursive=True)
observer.start()


@app.route('/')
def index():
    fonts_path = os.path.join(os.getcwd(), 'fonts')
    fonts = sorted([
        f for f in os.listdir(fonts_path)
        if f.endswith('.ttf') or f.endswith('.otf')
    ])
    return render_template('index.html', fonts=fonts)

if __name__ == '__main__':
    generate_stylesheet()
    freezer.freeze()
    shutil.copytree('fonts', 'build/fonts', dirs_exist_ok=True)
    shutil.copytree('build/static/style.css', 'build/style.css', dirs_exist_ok=True)
    print("Build Complete.")
    
