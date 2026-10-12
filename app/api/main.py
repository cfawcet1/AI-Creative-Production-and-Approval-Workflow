from fastapi import FastAPI
app = FastAPI(title='CreativeOps AI')

@app.get('/health')
def health():
    return {'status': 'ok'}
