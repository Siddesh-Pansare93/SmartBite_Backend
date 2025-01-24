import mongoose, { mongo } from "mongoose";

const dailyIntakeSchema = new mongoose.Schema(
    {
      userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
      date: { type: Date, required: true },
      foodConsumed: [
        {
          foodId: { type: mongoose.Schema.Types.ObjectId, ref: "FoodItem", required: true },
          quantity: { type: Number, required: true }
        }
      ],
      totalNutrients: {
        protein: { type: Number, default: 0 },
        carbs: { type: Number, default: 0 },
        fats: { type: Number, default: 0 },
        calories: { type: Number, default: 0 }
      },
      createdAt: { type: Date, default: Date.now },
      updatedAt: { type: Date, default: Date.now }
    },
    { timestamps: true }
  );


  export const dailyIntake = mongoose.model("DailyIntake" , dailyIntakeSchema)