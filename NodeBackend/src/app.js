import express, { urlencoded } from "express";
import cors from 'cors'
import cookieParser from 'cookie-parser'





const app = express()




// MiddleWares

app.use(cors({
    origin : process.env.CORS_ORIGIN , 
    credentials :  true 
}))


app.use(cookieParser())


app.use(express.json())
app.use(express.urlencoded())
app.use(express.static("public"))




export default app