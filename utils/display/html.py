import pandas as pd
from PIL import Image
from io import BytesIO
from IPython.display import HTML
import base64


pd.set_option('display.max_colwidth', -1)

def get_thumbnail(path, size=150):
    i = Image.open(path)
    i.thumbnail((size, size), Image.LANCZOS)
    return i

def image_base64(im):
    if isinstance(im, str):
        im = get_thumbnail(im, display_size)
    with BytesIO() as buffer:
        im.save(buffer, 'jpeg')
        return base64.b64encode(buffer.getvalue()).decode()

def image_formatter(im):
    return f'<img src="data:image/jpeg;base64,{image_base64(im)}">'


# pants_pd['image'] = pants_pd.file.map(lambda f: get_thumbnail(f, size=250))
# HTML(pants_pd[['name', 'image']].to_html(formatters={'image': image_formatter}, escape=False))


