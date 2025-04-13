
import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()

port = os.getenv("PORT", default=3000)

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
