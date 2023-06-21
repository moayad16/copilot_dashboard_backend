import uvicorn


if __name__ == "__main__":
    port = 8080
    host='localhost'
    uvicorn.run("app.app:app", port=port, host=host, reload=True)
    print("server running on 'http://localhost:'", port)
