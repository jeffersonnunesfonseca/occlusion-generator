# app.py
from flask import Flask, request, send_file
import tempfile
import os
import numpy as np
from stl import mesh
import dropbox
from dropbox.exceptions import AuthError

app = Flask(__name__)


def download_from_dropbox(file_path, dropbox_path, access_token):
    dbx = dropbox.Dropbox(access_token)
    dbx.files_download_to_file(file_path, dropbox_path)

    return True


@app.route("/", methods=["POST"])
def run_stl_script():
    try:
        data = request.json
        stl_path_1 = data.get("stl_path_1")
        stl_path_2 = data.get("stl_path_2")
        dropbox_token = data.get("dropbox_token")

        # Criar diretório temporário
        temp_dir = tempfile.mkdtemp()

        # Baixar arquivos temporariamente
        stl_file1 = os.path.join(temp_dir, "1.stl")
        stl_file2 = os.path.join(temp_dir, "2.stl")

        # Executar o script STL
        output = os.path.join(temp_dir, "3.stl")

        download_from_dropbox(stl_file1, stl_path_1, dropbox_token)
        download_from_dropbox(stl_file2, stl_path_2, dropbox_token)

        stl_data = mesh.Mesh.from_files([stl_file1, stl_file2])
        t = np.array([10, 20, 30])
        stl_data.translate(t)
        stl_data.save(output)

        file = send_file(output, as_attachment=True)
        os.remove(output)

        return file

    finally:
        # Excluir os arquivos temporários após o uso
        if temp_dir and os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Erro ao excluir arquivo {file_path}: {e}")

            os.rmdir(temp_dir)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
