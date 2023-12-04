from app.api.registrar import register_app


app = register_app()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('index:app', host='0.0.0.0', port=9088, reload=True)
