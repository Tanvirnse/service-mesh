import os
from flask import Flask, jsonify

# Initialize Flask App
app = Flask(__name__)

# Get version and pod name from environment variables
# The 'HOSTNAME' fallback is useful for local testing before containerization
APP_VERSION = os.environ.get('APP_VERSION', 'local')
POD_NAME = os.environ.get('POD_NAME', 'local-dev-machine')

def get_page_content(page_name):
    """Helper function to generate page content."""
    return {
        "page": page_name,
        "message": f"Hello from the {page_name} page!",
        "version": APP_VERSION,
        "serving_pod": POD_NAME
    }

@app.route('/')
def home():
    return jsonify(get_page_content("Home"))

@app.route('/page1')
def page1():
    return jsonify(get_page_content("Page 1"))

@app.route('/page2')
def page2():
    return jsonify(get_page_content("Page 2"))

@app.route('/page3')
def page3():
    return jsonify(get_page_content("Page 3"))

@app.route('/page4')
def page4():
    return jsonify(get_page_content("Page 4"))
    
@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)