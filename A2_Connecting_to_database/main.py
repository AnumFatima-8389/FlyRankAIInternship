
import sqlite3   
from fastapi import FastAPI
from fastapi.responses import JSONResponse  
from pydantic import BaseModel  
class Task(BaseModel): 
    title : str
    done : bool
    
app = FastAPI() 

# function for getting all data
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
# function for getting data of a particular id 
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
# creating table if it doesn't already exist
cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS tasks (
            id integer primary key autoincrement , 
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
# adding data if it doesn't have any already 
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
# get all tasks
@app.get("/tasks") 
def getTasks():
    return{
        "title":"All tasks", 
        "individual tasks":returnData("tasks")
    }  
    
# get tasks based on id 
@app.get("/tasks/{id}") 
def getTaskById(id:int): 
    return returnDetailsOfId("tasks",id)  

# post a new task 
@app.post("/task") 
def addTask(task : Task): 
    connection = sqlite3.connect('tasks.db') 
    cursor = connection.cursor()
    cursor.execute(
        f"""
            insert into tasks (title,done)
            values (?,?)
        """,(task.title,task.done)     
    )  
    connection.commit()
    return {
        "message":"Task added successfully"
    }
    
    

    

