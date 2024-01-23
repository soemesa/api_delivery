import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def inicio():
    return {'message': 'Hello World!'}


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", log_level="debug", port=8003, reload=True
    )

