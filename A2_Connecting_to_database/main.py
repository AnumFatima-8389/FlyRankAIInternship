
import sqlite3   
from fastapi import FastAPI
from fastapi.responses import JSONResponse 
app = FastAPI()
def returnData(tablename): 
    connection = sqlite3.connect("tasks.db") 
    cursor = connection.cursor() 
    cursor.execute(f"select * from {tablename}") 
    data = cursor.fetchall() 
    datalist=[]
    for d in data: 
        datalist.append({
            "id": d[0],
            "title": d[1],
            "done": bool(d[2])
        }) 
    return datalist 
def returnDetailsOfId(tablename,id):
    connection = sqlite3.connect("tasks.db") 
    cursor = connection.cursor() 
    cursor.execute(
        f"""
            select * from {tablename} 
            where id = ? 
        """   ,(id,)
    )  
    result = cursor.fetchone() 
    if not result: 
        content = {"error": "task not found"}
        return JSONResponse(content=content, status_code=401)
    result = {
        "id":result[0], 
        "title":result[1],
        "done":bool(result[2])
    }
    return result
    
connection = sqlite3.connect("tasks.db") 
cursor = connection.cursor() 

cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS tasks (
            id integer primary key, 
            title text, 
            done boolean 
        )
    """ 
    
) 
print("Table created") 
cursor.execute(
    "select exists(select 1 from tasks)"
) 
hasdata = cursor.fetchone()[0] 
if not hasdata: 
    cursor.execute("""
            INSERT INTO tasks 
            VALUES (1,"watch 1 ep of a german series to learn german",False), 
            (2,"Bake brownies",False), 
            (3,"Do 2 tasks of the internship",False)
        """      
    )  
    connection.commit()
    print("data added")
else: 
    print("Data already exists so no starter-data added")  

@app.get("/tasks") 
def getTasks():
    return{
        "title":"All tasks", 
        "individual tasks":returnData("tasks")
    } 
@app.get("/tasks/{id}") 
def getTaskById(id:int): 
    return returnDetailsOfId("tasks",id)
    

