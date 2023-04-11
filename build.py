from main import app
from flask_frozen import Freezer
import shutil

freezer = Freezer(app)

if __name__ == '__main__':
    try:
        freezer.freeze()
    except:
        print("Flask app frozen, copying fonts to the build directory.")
    finally:
        shutil.copytree('fonts', 'build/fonts', dirs_exist_ok=True)
        print("Done.")