
from main import app, config

if __name__ == '__main__':
    host = config.get('host')
    port = int(config.get('port'))
    app.run(debug=False, host=host, port=port)
