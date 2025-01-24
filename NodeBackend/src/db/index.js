import mongoose from "mongoose";
import { DB_NAME } from "../constant.js";



const connectToDb = async()=>{
    try {
        const connectionInstance = await mongoose.connect(`${process.env.MONGODB_URI}/${DB_NAME}`)
        console.log(`mongodb connected with name : ${connectionInstance.connection.name}`)
    } catch (error) {
        console.log(`mongodb connection failed due to : ${error.message}`)
        process.exit(1)
    }
}


export default connectToDb