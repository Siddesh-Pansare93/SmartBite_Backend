import mongoose from "mongoose";


const healthProfileSchema = new mongoose.Schema(
    {
      userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
      age: { type: Number, required: true },
      weight: { type: Number, required: true }, // in kg
      height: { type: Number, required: true }, // in cm
      gender: { type: String, required: true, enum: ["male", "female"] },
      goal: { type: String, required: true }, // e.g., "weight loss"
      activityLevel: { type: String, enum: ["sedentary", "active", "very active"], required: true },
      medicalConditions: [{ type: String }],
      allergies: [{ type: String }],
      dailyCalorieTarget: { type: Number },
      dailyMacros: {
        protein: { type: Number },
        carbs: { type: Number },
        fats: { type: Number }
      },
      createdAt: { type: Date, default: Date.now },
      updatedAt: { type: Date, default: Date.now }
    },
    { timestamps: true }    
  );

  export const healthProfile = mongoose.model("HealthProfile" , healthProfileSchema)