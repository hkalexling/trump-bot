from flask import Flask, request
import numpy as np
import requests, json

app = Flask(__name__, static_url_path='/static')

WORD_COUNT = 6171
INPUT_SIZE = 124

f = open('model/assets/word_index.json', 'r')
WORD_INDEX = json.loads(f.read())
f.close()

f = open('model/assets/index_word.json', 'r')
INDEX_WORD = json.loads(f.read())
f.close()

@app.route('/predict')
def predict():
    string = request.args.get('input')

    # Tokenize the input
    tokens = list(filter(lambda x: x is not None, map(lambda x: WORD_INDEX.get(x), string.lower().split(' '))))

    x = np.array(tokens)
    if x.size < INPUT_SIZE:
        # Paddings
        x = np.pad(x, (INPUT_SIZE - x.size, 0))

    data = json.dumps({
        'instances': [x.tolist()]
    })

    # Invoke the tensorflow/serving API
    res = requests.post(
        'http://localhost:8501/v1/models/speech:predict',
        data = data,
        headers = {'content-type': 'application/json'})

    # Extraction prediction
    y = np.array(json.loads(res.content)['predictions'][0])
    # Normalization
    y /= y.sum()

    # Recover the predicted word
    idx = np.random.choice(WORD_COUNT, p=y)

    return {'new_word': INDEX_WORD[str(idx)]}

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=False)
