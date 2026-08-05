from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from supabase import AuthError, create_client 
from pydantic import BaseModel 

class Credentials(BaseModel): 
    email:str 
    password : str 

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@asynccontextmanager
async def lifespan(app: FastAPI):
   print("Server running and connected to supabase") 
   yield 
   
app = FastAPI(lifespan=lifespan)

@app.post("/auth/signup")
def signup(credentials:Credentials): 
    if not credentials.email or not credentials.password: 
        return JSONResponse(
            status_code = 400, 
            content = {"message":"Missing email or password."}
        )
    res = supabase.auth.sign_up({'email':credentials.email, 'password' : credentials.password}) 
    return JSONResponse(
        status_code=201, 
        content=jsonable_encoder({"user":res.user.model_dump()})
    )  
@app.post("/auth/login") 
def login(credentials:Credentials): 
    if not credentials.email or not credentials.password: 
        return JSONResponse(
            status_code = 400, 
            content = {"message":"Missing email or password."}
        )  
    try:
        res = supabase.auth.sign_in_with_password({
            'email':credentials.email, 
            'password':credentials.password
        })  
        session = res.session
        return JSONResponse(
            status_code = 200, 
            content = {
                'access token': session.access_token, 
                'refresh token':session.refresh_token
            }
        ) 
    except AuthError as e: 
        return JSONResponse(
            status_code = 401, 
            content = { "error": "Invalid login credentials" }
        )
        