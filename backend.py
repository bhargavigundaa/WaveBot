from flask import Flask, request, json
from json import JSONEncoder

from langModel import question, test
# from werkzeug.serving import BaseWSGIServer, WSGIRequestHandler
# import signal


class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder



@app.route('/api/question-previous', methods=['POST'])
def questionAnswer():
    data = request.json  # Assuming the question is sent as a JSON object in the request body
    questionFromApi = data.get('question')
    result = question(questionFromApi)  # Replace with your actual function from the converted notebook
    return  CustomJSONEncoder().encode(result)

@app.route('/api/question', methods=['POST'])
def custom():
    data = request.json  # Assuming the question is sent as a JSON object in the request body
    questionFromApi = data.get('question')
    result = test(questionFromApi)  # Replace with your actual function from the converted notebook
    return json.dumps(result)

# def shutdown_server(sig, frame):
#     print('Shutting down the server...')
#     server.shutdown()
#     sys.exit(0)
#
# signal.signal(signal.SIGINT, shutdown_server)
# # Run the Flask app using BaseWSGIServer
# server = BaseWSGIServer(('http://127.0.0.1', 5000), WSGIRequestHandler, app)
# server.serve_forever()


if __name__ == '__main__':
    app.run(debug=True)
