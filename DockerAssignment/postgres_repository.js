
const { Pool } = require("pg");

const pool = new Pool({
    connectionString: process.env.DATABASE_URL
});

async function getAllStudents(){
    const result = await pool.query(
        "SELECT * FROM Students"
    ); 
    return result.rows;
} 

async function addStudent(name,gender){ 
    await pool.query(
        "INSERT INTO Students(student_name, student_gender) VALUES ($1, $2)",
        [name, gender]
    )
    
} 
module.exports = {
    getAllStudents,
    addStudent
};