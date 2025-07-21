from flask import Flask, request, render_template_string
from tensorflow.keras.models import load_model
import cv2, numpy as np, os, secrets

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

model = load_model('model/model.h5')
class_names = ['airplane','automobile','bird','cat','deer',
               'dog','frog','horse','ship','truck']

@app.route("/", methods=["GET", "POST"])
def index():
    pred = None
    img_url = None
    if request.method == "POST":
        file = request.files['file']
        if file:
            filename = secrets.token_hex(8) + ".jpg"
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            img = cv2.imread(path)
            img = cv2.resize(img, (32,32)) / 255.0
            img = img[None, ...]

            idx = int(np.argmax(model.predict(img)))
            pred = f"{class_names[idx]}  ({np.max(model.predict(img))*100:.1f}%)"
            img_url = path
    return render_template_string("""
        <h2>Upload an image (32×32 or larger)</h2>
        <form method="POST" enctype="multipart/form-data">
          <input type="file" name="file" required>
          <button>Predict</button>
        </form>
        {% if pred %}
          <h3>Prediction: {{ pred }}</h3>
          <img src="{{ img_url }}" style="max-width:300px">
        {% endif %}
    """, pred=pred, img_url=img_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)