import {User} from "../models/User.model.js"
import bcrypt from 'bcrypt'





// Register a new user
 const registerUser = async (req, res) => {

    console.log("request received")
  try {
    const { name, email, password } = req.body;
    console.log(req.body)

//     // Validate required fields
//     if (!name || !email || !password) {
//       return res.status(400).json({ error: "Name, email, and password are required." });
//     }

//     // Check if the user already exists
//     const existingUser = await User.findOne({ email });
//     if (existingUser) {
//       return res.status(400).json({ error: "User already exists with this email." });
//     }

//     // Hash the password
//     const hashedPassword = await bcrypt.hash(password, 10);

//     // Create the user
//     const newUser = new User({
//       name,
//       email,
//       passwordHash: hashedPassword
//     });

//     await newUser.save();
//     res.status(201).json({ message: "User registered successfully." });
  } catch (error) {
    res.status(500).json({ error: "Internal server error." });
  }
};

// Login user
const loginUser = async (req, res) => {
  try {
    const { email, password } = req.body;

    // Validate required fields
    if (!email || !password) {
      return res.status(400).json({ error: "Email and password are required." });
    }

    // Check if the user exists
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(404).json({ error: "Invalid email or password." });
    }

    // Verify the password
    const isPasswordValid = await bcrypt.compare(password, user.passwordHash);
    if (!isPasswordValid) {
      return res.status(401).json({ error: "Invalid email or password." });
    }

    // Generate a JWT
    const token = jwt.sign({ userId: user._id }, JWT_SECRET, { expiresIn: "7d" });

    res.status(200).json({ message: "Login successful.", token });
  } catch (error) {
    res.status(500).json({ error: "Internal server error." });
  }
};

// Get user profile
const getUserProfile = async (req, res) => {
  try {
    const user = await User.findById(req.userId);
    if (!user) {
      return res.status(404).json({ error: "User not found." });
    }
    res.status(200).json(user);
  } catch (error) {
    res.status(500).json({ error: "Internal server error." });
  }
};

// Update user profile
const updateUserProfile = async (req, res) => {
  try {
    const updates = req.body;

    // Update the user
    const user = await User.findByIdAndUpdate(req.userId, updates, { new: true });
    if (!user) {
      return res.status(404).json({ error: "User not found." });
    }
    res.status(200).json(user);
  } catch (error) {
    res.status(500).json({ error: "Internal server error." });
  }
};


export {
    registerUser,
    loginUser,
    getUserProfile,
    updateUserProfile
}
