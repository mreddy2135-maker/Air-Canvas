🎨Air Canvas - Virtual Drawing Tool  
Developer: Manvitha Reddy
Domain: AI & Data Science

📖 Project Description  
Air Canvas is a computer vision application that allows users to draw on a digital canvas using hand gestures in the air. By leveraging OpenCV and MediaPipe, the system tracks the index finger's movement in real-time to draw lines, while using the middle finger to toggle between "Drawing Mode" and "Selection Mode."  

This project solves the common issue of camera jitter by implementing a Weighted Smoothing Algorithm, ensuring fluid and stable drawing lines.  

🚀 Features  
Touch-Free Drawing: Draw using only your index finger.  
Smart Hover Mode: Raise two fingers to move the cursor without drawing.  
Color Selection: Interactive UI to switch between Red, Green, and Blue.  
Eraser Tool: Intuitive erasing mechanism.  
Jitter Stabilization: Mathematical smoothing for clean, non-shaky lines.  
Save Artwork: Press s to save your drawing as an image file.  

🛠️ Tech Stack  
Language: Python 3.x  
Libraries:  
opencv-python (Computer Vision & Image Processing)  
mediapipe (Hand Landmark Detection)  
numpy (Canvas Matrix Manipulation)  

🎮 Controls  
Index Finger UP: Draw ✏️  
Index + Middle Finger UP: Hover / Select Color ✋  
Keyboard 's': Save current drawing 💾  
Keyboard 'c': Clear the screen 🧹  
Keyboard 'q': Quit the app ❌  
