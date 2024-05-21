from app.app import app
import uvicorn
import os


uvicorn.run(app, host=os.environ.get('HOST', '0.0.0.0'), port=int(os.environ.get('PORT', 80)),
            workers=int(os.environ.get('WORKERS', 1)), )
