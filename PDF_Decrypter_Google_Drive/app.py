from flask import Flask, request, send_file
import pikepdf
import io

app = Flask(__name__)

@app.route('/decrypt', methods=['POST'])
def decrypt_pdf():
    try:
        password = request.form.get('password')
        uploaded_file = request.files['file']
        
        # Open and decrypt
        pdf = pikepdf.open(uploaded_file, password=password)
        
        # Save to memory
        output_stream = io.BytesIO()
        pdf.save(output_stream)
        output_stream.seek(0)
        
        return send_file(output_stream, mimetype='application/pdf', as_attachment=True, download_name='decrypted.pdf')
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
