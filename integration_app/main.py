import json
from flask import Flask, render_template, request, jsonify
from current_metadata import CurrentMetadata
from crud import CRUD


app = Flask(__name__)


def api_response(data):
    response = jsonify(data)
    response.headers.set("Content-Type", 'application/json')
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/')
def miro_web_plugin_sync():
    return render_template('miro_web_plugin.html')


@app.route('/syncing_notion', methods=['POST'])
def syncing_notion():
    miro_board_data = json.loads(request.data.decode())
    current_metadata = CurrentMetadata(miro_board_data)
    crud = CRUD(current_metadata.current_card_metadata)
    crud.main()
    return api_response({'success': True}), 200


if __name__ == '__main__':
    app.run(debug=True, port=80)
