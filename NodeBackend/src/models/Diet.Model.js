import mongoose from "mongoose";

const dietSchema = new mongoose.Schema(
    {
      userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
      dietName: { type: String, required: true },
      nutrientBreakdown: {
        protein: { type: Number, required: true },
        carbs: { type: Number, required: true },
        fats: { type: Number, required: true },
        calories: { type: Number, required: true }
      },
      meals: [
        {
          mealName: { type: String, required: true },
          foodItems: [
            {
              foodId: { type: mongoose.Schema.Types.ObjectId, ref: "FoodItem", required: true },
              quantity: { type: Number, required: true } // e.g., grams or pieces
            }
          ]
        }
      ],
      createdAt: { type: Date, default: Date.now },
      updatedAt: { type: Date, default: Date.now }
    },
    { timestamps: true }
  );


  export const Diet = mongoose.model("Diet" , dietSchema)