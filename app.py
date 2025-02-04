from flask import Flask, request, render_template
import whisper
import os

app = Flask(__name__)
model = whisper.load_model("tiny")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            file_path = os.path.join("uploads", file.filename)
            os.makedirs("uploads", exist_ok=True)
            file.save(file_path)
            
            # Transcrever
            result = model.transcribe(file_path, language="Portuguese")
            with open("uploads/transcricao.txt", "w", encoding="utf-8") as f:
                f.write(result["text"])

            return f"Transcrição concluída! <a href='/uploads/transcricao.txt'>Baixar transcrição</a>"
    return '''
        <form method="post" enctype="multipart/form-data">
            <h1>Transcreva Seu Vídeo/Áudio</h1>
            <input type="file" name="file" accept=".mp4,.mp3,.wav">
            <button type="submit">Transcrever</button>
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
