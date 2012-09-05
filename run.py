from pooldin import create_app
from pooldin.app.convert import to_int

app = create_app()

if __name__ == '__main__':
    import os
    port = os.environ.get('PORT')
    port = to_int(port) or 5000
    app.run(host='0.0.0.0', port=port)
