API utilizada para gerar oclusão a partir de arcada dentária superior com a inferior em .stl

# Construir a imagem
docker build -t flask-stl-app .

# Executar o contêiner
docker run  -d -p 5000:5000 --restart always flask-stl-app
# occlusion-generator
