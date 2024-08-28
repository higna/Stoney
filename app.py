from flask import Flask, render_template, request
from io import BytesIO
from barcode import Code128
from barcode.writer import ImageWriter
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        texts = request.form.getlist('texts')
        barcodes = []

        for text in texts:
            if text:
                barcode = Code128(text, writer=ImageWriter())
                buffer = BytesIO()
                barcode.write(buffer)
                buffer.seek(0)
                barcode_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                barcodes.append((text, barcode_base64))

        return render_template('index.html', barcodes=barcodes, number_of_barcodes=len(barcodes))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)