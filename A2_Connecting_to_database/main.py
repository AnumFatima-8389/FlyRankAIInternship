
import sqlite3  
def printData(tablename):
    cursor.execute(f"select * from {tablename}") 
    data = cursor.fetchall() 
    for d in data: 
        print(d)
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
print("Write now the data in the db is: ")
printData("tasks") 
    