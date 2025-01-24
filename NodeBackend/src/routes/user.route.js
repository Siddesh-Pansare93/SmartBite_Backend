import express from "express";
import { 
  registerUser, 
  loginUser, 
  getUserProfile, 
  updateUserProfile 
} from "../controllers/User.controller.js";
// import { protect } from "../middleware/authMiddleware.js";

const router = express.Router();

// @route   POST /api/users/register
// @desc    Register a new user
// @access  Public
router.post("/register", registerUser);

// @route   POST /api/users/login
// @desc    Authenticate user and get token
// @access  Public
router.post("/login", loginUser);

// @route   GET /api/users/profile
// @desc    Get user profile
// @access  Private
router.get("/profile", getUserProfile);

// @route   PUT /api/users/profile
// @desc    Update user profile
// @access  Private
router.put("/profile", updateUserProfile);

export default router;
