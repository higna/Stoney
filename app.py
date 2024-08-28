from flask import Flask, render_template, request
import barcode
from barcode.writer import ImageWriter
import io
from PIL import Image

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        texts = request.form.get("texts", "").splitlines()
        barcodes = []

        for text in texts:
            if text.strip():  # Skip empty lines
                code = barcode.get_barcode_class('code128')(text, writer=ImageWriter())
                buffer = io.BytesIO()
                code.write(buffer)
                buffer.seek(0)
                image = Image.open(buffer)
                image.save(f'static/{text}.png')
                barcodes.append(f'{text}.png')

        return render_template("index.html", barcodes=barcodes)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)