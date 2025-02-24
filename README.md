# DocumentationAI
AI powewered software that comments and cleans code as well as writing documentation

Step 3: Build the Application
Backend (FastAPI)
The backend will handle code processing, including cleanup, comment generation, and documentation creation.
Install Dependencies
First, install the required Python packages:
bash
pip install fastapi uvicorn openai black python-multipart

run the Backend
Start the FastAPI server:
bash
uvicorn main:app --reload
This will run the backend on http://localhost:8000.
Run the Frontend
Start the React app:
bash
npm start
This will run the frontend on http://localhost:3000.
Test the App
Open the frontend in your browser.
Enter some Python code, such as:
python
def greet(name):
    print(f"Hello, {name}!")
Click "Process Code".
The app will clean up the code, add comments and docstrings, and display documentation.
Step 5: Deploy the Application
Backend Deployment
Deploy the FastAPI app on Heroku or any Python-supported cloud platform.
Set the OPENAI_API_KEY environment variable in your deployment settings.
Frontend Deployment
Build the React app:
bash
npm run build
Serve the build folder from the FastAPI backend using StaticFiles, or deploy it separately on platforms like Vercel or Netlify.
Combined Deployment
For simplicity, you can serve the React build from FastAPI:
Copy the build folder to the FastAPI project directory.
Update the FastAPI app to serve static files:
python
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="build", html=True), name="static")
Deploy the combined app on Heroku.
