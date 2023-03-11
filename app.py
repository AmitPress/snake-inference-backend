from ultralytics import YOLO
from PIL import Image
from bs4 import BeautifulSoup
import requests
model = YOLO('resources/twenty-eight-first.pt')
classes = ['Ahaetulla nasuta', 'Ahaetulla prasina', 'Boiga cynodon', 'Boiga multomaculata', 'Bungarus caeruleus', 'Bungarus fasciatus', 'Chrysopelea ornata', 'Coelognathus radiatus', 'Daboia russelii', 'Dendrelaphis pictus', 'Dendrelaphis tristis', 'Echis carinatus', 'Fowlea piscator', 'Hydrophis platurus', 'Indotyphlops braminus', 'Laticauda colubrina', 'Lycodon aulicus', 'Malayopython reticulatus', 'Naja kaouthia', 'Naja naja', 'Oreocryptophis porphyraceus', 'Psammodynastes pulverulentus', 'Ptyas korros', 'Ptyas mucosa', 'Python bivittatus', 'Rhabdophis subminiatus', 'Trimeresurus albolabris', 'Xenochrophis piscator']

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Snake Detection API</h1>"


@app.route('/upload', methods=['POST'])
def upload():
    img = request.files['image']
    img.save('resources/image.jpg')
    image = Image.open('resources/image.jpg')
    box = model(image)[0].boxes[0]
    cls = int(box.cls[0])
    name = classes[cls]
    genus, species = name.split(' ')
    data = requests.get(f'https://reptile-database.reptarium.cz/species?genus={genus}&species={species}')
    bs = BeautifulSoup(data.content, 'html.parser')
    desc = bs.find('td', string='Comment').find_next_sibling('td').text
    res = {
        'snake': name,
        'details': desc
    }
    return res

if __name__=="main":
    app.run(port=5000)