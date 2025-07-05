from flask import Flask, request, Response, redirect, url_for, session, render_template_string
from functools import wraps
from picamera2 import Picamera2
from picamera2.outputs import FileOutput
import io
import time

app = Flask(__name__)
picam2 = Picamera2()

# Configure camera
video_config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(video_config)

# Prepare encoder and output
output = io.BytesIO()

picam2.start()
time.sleep(2)  # Let the camera warm up

def generate_frames():
    while True:
        output.seek(0)
        output.truncate()
        picam2.capture_file(output, format="jpeg")
        frame = output.getvalue()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame  + b'\r\n')
               
# Secret key for session management
app.secret_key = 'your_secret_key'              
               
# Simple hardcoded credentials
USERNAME = "admin"
PASSWORD = "secret"

# Custom decorator to require logindef require_login(f):
def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            # Save the requested path before redirecting to login
            session['redirect_to'] = request.url
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
   
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Clear the session completely before showing login page
    session.clear()  # Forces the session to reset (to ensure no auto-login)
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            # Redirect to the original requested page, or index if not available
            redirect_url = session.pop('redirect_to', url_for('live'))
            return redirect(redirect_url)
        else:
            return "Invalid credentials. Please try again.", 401
    return render_template_string('''
        <form method="POST">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username"><br><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password"><br><br>
            <input type="submit" value="Login">
        </form>
    ''')

@app.route('/live')
@require_login
def live():
    response = Response(
        generate_frames(), 
        mimetype='multipart/x-mixed-replace; boundary=frame'
        )
    response.headers["Cache-Control"] = "no-store"
    if 'logged_in' in session and session['logged_in']:
        # Force log out by clearing the session
        session.clear()
    return response
   
@app.route('/')
def index():
    return Response('test')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)