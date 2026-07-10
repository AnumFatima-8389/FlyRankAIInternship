const express = require("express"); 
const app = express();
const port = 3000;

//Home
app.get('/home',(req, res) => { 
    const m = {'title':"HomePage",'content':"Hey there! Welcome to the home page!"};
    res.send(m);
})
// Contact
app.get('/contact',(req,res)=>{
    const m = {'title':"Contact Info", 
        'content':"Contact me at anfatima.bscs24seecs@seecs.edu.pk"
    }
}) 

app.listen(port,()=>{
    console.log("Program running at http://localhost:3000") 
    console.log("Go to http://localhost:3000/home \n or \nGo to http://localhost:3000/contact")
})