from flask import Flask, render_template, request, jsonify
from web_runner import MiMotionRunner
from werkzeug.middleware.proxy_fix import ProxyFix
import os

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/update', methods=['POST'])
def update_steps():
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'Invalid request data'}), 400
    
    account = data.get('account')
    password = data.get('password')
    steps = data.get('steps')
    
    if not account or not password or not steps:
        return jsonify({'success': False, 'message': 'Missing account, password, or steps'}), 400
    
    try:
        runner = MiMotionRunner(account, password)
        msg, success = runner.login_and_post_step(steps)
        return jsonify({'success': success, 'message': msg})
    except Exception as e:
        print(f"Error processing request: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 12303))
    app.run(host='0.0.0.0', port=port, debug=True)
