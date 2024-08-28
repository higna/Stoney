from flask import Flask, render_template, request, redirect, url_for
from barcode import Code128
from barcode.writer import ImageWriter
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_barcodes = int(request.form['number_of_barcodes'])
        barcodes = []

        for i in range(num_barcodes):
            barcode_text = request.form.get(f'texts_{i}', '')
            barcode = Code128(barcode_text, writer=ImageWriter())
            buffer = io.BytesIO()
            barcode.write(buffer)
            barcode_data = buffer.getvalue()
            barcode_base64 = base64.b64encode(barcode_data).decode('utf-8')
            barcodes.append((barcode_text, barcode_base64))

        return render_template('index.html', barcodes=barcodes)

    return render_template('index.html', barcodes=None)

if __name__ == '__main__':
    app.run(debug=True)
