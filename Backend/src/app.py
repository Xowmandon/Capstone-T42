from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask on EC2!"



@app.route('/messages/send')
def sendMessage():
    return "Message sent!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
