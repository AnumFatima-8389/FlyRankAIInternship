How to test: 
1. Simply open terminal in this folder 
2. run docker compose up -d 
3. go to postman and check the following api endpoints: 
    - http://localhost:3000/getStudents -> you should see list of students with their info 
    - http://localhost:3000/addStudent with body in json format containg student_name and student_gender, you should see Student added! Now the next time you access the former endpoint you should see this new student too. An example for the body: 
                    {
                        "student_name":"Fahad", 
                        "student_gender":"male"
                    } 

                    
A Little About My Approach: 
This was my first attempt of actually working with dockers practically. 
Here's the whole flow: 
1. I went to dockerhub and opened "postgre image documentation". There they had provided a basic docker-compose.yaml. 
2. I copied this yaml file and pasted it into my project file. Now I had a basic compose file that ran db and admin containers. I specified my password etc in this
3. Now that I had my password etc specified in the compose file, I had to find a way for the node app to access them so I included them in the .env and showed an example in the .env.example 
4. I used "docker compose up" and then visited localhost 8081 to see if the admin was running - it was. 
5. The docker had no volume up till now so I added a volume to it and specified in the compose file that whatever the docker stores in data must be stored here too (this volume is in my local machine storage so it will not be lost when the docker stops running). 
6. Next I had to create tables in the db as it was empty. I wrote an sql file with table creation script but I needed a way for docker to know that it has to run this script the first time the container runs 
7. So I added it in the compose file, specifying that whatever is in this file of mine, add it to the default file that docker supposed contains sql script and runs at the start. 
8. I also wanted to start the app whenever the docker container runs so I added app in the compose.yaml but its image needed to be created. 
9. I wrote the dockerfile which contained instructions regarding the image. 
10. in the app section in the compose file, i specified other environmental variables etc 
11. now upon starting the container, our app started where we could add students or get all student info etc 

No Change In Services and Routes: 
Services and routes were unchanged as all we did was add postgre instead of memory. So what changed was the source from where we get data or put data, not the processes to be done on the data. Hence I added repo = require("./postgres_repository") and then called functions using repo. In the postgres_repository.js, the functions are defined, the actual db is accessed using pool. 

How I Checked Persistence: 
Since the app also starts through docker compose up as app image is made and the instruction for it to start is specified in the docker-compose.yaml, stopping or starting the container stops or starts the app too. I checked by 
- adding a student 
- then stopping the app and container simultaneously 
- starting them again
- accessing all students
- this new student still appeared in the list of students 