import uvicorn

if __name__ == '__main__':
    print("app started on http://localhost:8085")
    uvicorn.run('app.app:app', host="0.0.0.0", port=8085, reload=True)