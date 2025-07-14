from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from io import BytesIO
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'slips'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    images = []
    for i in range(1, 4):
        file = request.files.get(f'image{i}')
        if file:
            image = Image.open(file.stream).convert("RGB")
            images.append(image)

    if len(images) != 3:
        return redirect(url_for('index'))

    widths, heights = zip(*(img.size for img in images))
    max_width = max(widths)
    total_height = sum(heights) + 100  

    combined = Image.new('RGB', (max_width, total_height), color='white')

    y_offset = 0
    for img in images:
        combined.paste(img, (0, y_offset))
        y_offset += img.height

    draw = ImageDraw.Draw(combined)
    timestamp = datetime.now().strftime("duBooth • %d %B %Y %H:%M")

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font_path = os.path.join('static', 'fonts', 'OpenSans-Regular.ttf')  # You must provide this font
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, 40)
        else:
            font = ImageFont.load_default()

   
    bbox = draw.textbbox((0, 0), timestamp, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (max_width - text_width) // 2
    y = total_height - text_height - 20

    draw.text((x, y), timestamp, fill="black", font=font)

   
    filename = f"{uuid.uuid4().hex}.png"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    combined.save(file_path)

    return redirect(url_for('preview', filename=filename))

@app.route('/preview')
def preview():
    filename = request.args.get('filename')
    if not filename:
        return redirect(url_for('index'))
    return render_template('preview.html',
                           image_url=url_for('slip_file', filename=filename),
                           filename=filename)

@app.route('/slips/<filename>')
def slip_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), mimetype='image/png')

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename),
                     mimetype='image/png',
                     as_attachment=True,
                     download_name='photo_slip.png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
