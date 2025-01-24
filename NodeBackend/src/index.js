import dotenv from 'dotenv'
dotenv.config({
    path: "./.env"
})

// YAHA PE THOUGH ENV PEHLE HAI .....PAR IN JS IMPORT STATEMENT SAB SE PEHLE SYNC RUN HOTE HAI
// AND THEN ENV KA PART RUN HOGA UPAR VALA 
// "-r dotenv/config" in run command yeh problem solve kar deta hai
// because it run dotenv.config() before anything in app

import app from "./app.js";
import connectToDb from './db/index.js';




connectToDb()
    .then(() => {
        app.listen(process.env.PORT, () => {
            console.log("server ok and listening on : ", process.env.PORT)
        })
    })
    .catch(()=>{
        console.log("Failed to connect to Database")
    })


