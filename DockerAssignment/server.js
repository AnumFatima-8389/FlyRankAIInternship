const express = require("express"); 
const app = express(); 
app.use(express.json());
const port = 3000;
const repo = require("./postgres_repository");
//Home
app.get('/getStudents',async (req, res) => { 
    try {
        const students = await repo.getAllStudents();
        res.json(students);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
})
// Contact 
app.post('/addStudent',async (req,res)=>{
     try {
        const {student_name, student_gender } = req.body;

        await repo.addStudent(
            student_name,
            student_gender
        );

        res.status(201).json({
            message: "Student added."
        });

    } catch (err) {
        res.status(500).json({ error: err.message });
    }
}) 

app.listen(port,()=>{
    console.log("Program running at http://localhost:3000") 
    console.log("Go to http://localhost:3000/getStudents \n or \nGo to http://localhost:3000/addStudent")
})