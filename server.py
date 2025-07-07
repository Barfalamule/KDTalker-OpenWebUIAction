from flask import Flask, request
import threading
import KDtalkerGradio  # Import your existing script as a module

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print("Webhook received - Starting avatar generation")
        
        # Run the main function in a separate thread to avoid blocking
        thread = threading.Thread(target=KDtalkerGradio.main)
        thread.start()
        
        return "Video generation started", 202
    
    return "Invalid method", 405

if __name__ == "__main__":
    print("Starting Flask server on port 5000...")
    app.run(host="127.0.0.1", port=5000, debug=False)
