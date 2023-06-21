from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from app.database import users_collection
from fastapi.security import OAuth2PasswordBearer
from app.security import create_jwt_token, encrypt_string_sha256


app = FastAPI()

# 6DWVSrgBba8fJXzu

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    return response


@app.get('/', tags=['root'])
async def root() -> dict:
    return {"message": "Hello from your first FastApi project"}

@app.post('/signup', tags=['login'])
async def login(request: Request) -> dict:

    data = await request.json()
    data['password'] = encrypt_string_sha256(data['password'])

    users_collection.insert_one(data)

    token = create_jwt_token(data['email'])

    return {"message": "Login successful", "token": token}


@app.post('/login', tags=['login'])
async def login(request: Request) -> dict:
    
        data = await request.json()
        data['password'] = encrypt_string_sha256(data['password'])
    
        user = users_collection.find_one(data)
    
        if user:
            token = create_jwt_token(data['email'])
            return {"message": "Login successful", "token": token}
        else:
            return {"message": "Invalid credentials"}

# @app.websocket("/socket")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()

#     try:
#         while True:
#             data = await websocket.receive_json()

#             df = pd.DataFrame(
#                 columns=['accx', 'accy', 'accz', 'long', 'lat', 'seconds'])

#             # inserting the data into the dataframe. The data is expected to be a dictionary with the keys being the column names and lists as values
#             for key in data.keys():
#                 df[key] = data[key]

#             results = pipeline(df)
#             print(results)

#             # # uncomment this to save the poi to the database
#             # results = pipeline(df)
#             # for res in results:
#             #     if res.res != 'normal':
#             #         collection.insert_one(res.poi)

#             await websocket.send_json({"results": results})

#     except WebSocketDisconnect as e:
#         print("WebSocket disconnected:", e)


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}
