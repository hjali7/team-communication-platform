from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    """Root endpoint that returns welcome message"""
    return jsonify({
        "status": "ok",
        "message": "Welcome to the Team Communication Platform!"
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "team-communication-platform"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
