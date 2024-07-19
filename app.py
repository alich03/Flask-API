from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from openai import OpenAI
import json

app = Flask(__name__)
CORS(app)  # To handle CORS issues



@app.route('/', methods=['GET'])
def test():
    return jsonify({'response': 'API IS RUNNING'})


@app.route('/send-string', methods=['POST'])
def receive_string():
    data = request.get_json()
    string_data = data.get('string')
    print(f"Received string: {string_data}")
    return jsonify({'message': 'String received', 'string': string_data})


@app.route('/action/<string:action>', methods=['GET'])
def dynamic_route(action):
    if action == 'greet':
        return jsonify({"message": "Hello, welcome!"})
    elif action == 'bye':
        return jsonify({"message": "Goodbye, see you soon!"})
    elif action == 'status':
        return jsonify({"status": "All systems operational"})
    else:
        return jsonify({"error": "Invalid action"}), 400



client = OpenAI(api_key=OPEN_AI_KEY)


@app.route('/generate', methods=['POST'])
def genrating_response():
    data = request.get_json()
    prompt = data.get('prompt')
    reply = generate_response(prompt)

    return jsonify({'message': 'Response Received','prompt':prompt, 'response': reply})


@app.route('/gen_from_url/<string:prompt>',methods=['GET'])
def generate_from_url(prompt):

    reply = generate_response(prompt)
    return jsonify({'message': 'Response Received','prompt':prompt, 'response': reply})


@app.route('/get_form_data',methods=['GET'])
def get_form_data():

    data = request.form

    prompt = data['prompt']
    reply = generate_response(prompt)
    return jsonify({'message': 'Response Received','data': data,'response':reply})


@app.route('/get_param_data',methods=['GET'])
def get_param_data():

    prompt = request.args.get('prompt') 
    reply = generate_response(prompt)
    return jsonify({'message': 'Response Received','prompt': prompt,'reply':reply})


def generate_response(prompt):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": prompt }
    ])
    reply = json.loads(response.choices[0].message.content)

    return reply



if __name__ == '__main__':
    app.run(debug=True)
