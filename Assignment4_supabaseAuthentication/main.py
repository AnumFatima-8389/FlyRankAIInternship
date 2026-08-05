from contextlib import asynccontextmanager
import os
from fastapi import Depends, FastAPI, HTTPException, Header
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

@app.get("/public/info") 
def publicInfo(): 
    return {
        'message':'Welcome stranger! This info is public.'
    } 
def verify_token(authorization:str = Header(None)): 
    if authorization is None: 
        raise HTTPException(
            status_code = 401, 
            detail = 'Access token required'
        ) 
    parts = authorization.split() 
    if len(parts)!=2:
        raise HTTPException(
            status_code = 401, 
            detail = 'Incorrect authorization header format'
        )
    scheme,token = parts
    if scheme != "Bearer": 
        raise HTTPException(
            status_code=401,
            detail = 'Invalid authorization scheme'
        ) 
    try:
        our_user = supabase.auth.get_user(token) 
    except AuthError: 
        if our_user is None: 
            raise HTTPException(
                status_code = 401, 
                detail = 'Invalid or expired token'
            ) 
    user = our_user.user 
    return {
        'user':user, 
        'token':token
    }
    
@app.get("/protected/profile") 
def profile(userDetails = Depends(verify_token)): 
    user = userDetails["user"]
    return JSONResponse(
            status_code = 200, 
             content = {
                'id':user.id, 
                'email':user.email,
                'created at':jsonable_encoder(user.created_at)
            }
        )
    

@app.post('/auth/logout') 
def logout(userDetails = Depends(verify_token)):
    supabase.auth.sign_out(userDetails["token"]) 
    return JSONResponse(
        status_code = 204, 
    ) 
    
@app.get('/protected/dashboard') 
def dashboard(user_details = Depends(verify_token)):
    return JSONResponse(
        status_code = 200, 
        content = {'message':'token verified'}
    )
    
    
    
    