from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@asynccontextmanager
async def lifespan(app: FastAPI):
   print("Server running and connected to supabase") 
   yield 
   print("After yield")
   
app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"message": "Server is running"} 