# occlusion-generator
API utilizada para gerar oclusão a partir de arcada dentária superior com a inferior em .stl que deve estar hospedado no dropbox.

# Construir a imagem
docker build -t flask-stl-app .

# Executar o contêiner
docker run  -d -p 5000:5000 --restart always flask-stl-app --name occlusion-generator

# Exemplo de uso
```shell
curl --location 'http://127.0.0.1:5000' \
--header 'Content-Type: application/json' \
--data '{
    "stl_path_1": "/public/uploads/exams/222121/2/1.stl",
    "stl_path_2":"/public/uploads/exams/222121/2/2.stl",
    "dropbox_token": "xxx"
}'
```