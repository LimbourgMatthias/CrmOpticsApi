from flask import Flask
from flask import jsonify
from flask import request
import PrepJson
import model

app = Flask(__name__)
endpoint = '/api/v1'

def process_request(content):
    settings = content.get("settings", {})
    years = settings.get("years", 15)
    content = content.get("data")
    data = PrepJson.prep_json(content)
    result = model.get_forecast(data, years)
    return result

@app.route(endpoint + '/forecast', methods=['GET', 'POST'])
def get_forecast():
    content = request.get_json()
    print("content", content)
    try:
        result = process_request(content)
        return jsonify(result),200
    except Exception as e:
        return ('Something went wrong processing the request'),400


# Start app
if __name__ == '__main__':
    app.run()