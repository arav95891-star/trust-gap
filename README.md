# The Trust Gap 🚗🔍

## What It Does
"The Trust Gap" is an MVP platform designed to protect first-time used car buyers from hidden repair costs and fraud. It acts as a unified vehicle history and predictive cost layer. By simply entering a car's Registration Number, the platform aggregates data from previously disconnected sources to generate a comprehensive, easy-to-read trust report. 

Key features include:
- **Odometer Rollback Detection:** Automatically flags mileage tampering by analyzing historical service records.
- **Predictive Cost Engine:** Forecasts estimated maintenance and repair costs for the next 12-24 months.
- **Mechanic Portal:** Allows mechanics to submit standardized physical inspection ratings to update the car's condition score.
- **Verified PDF Passport:** Generates a downloadable, shareable PDF certificate of the car's true condition.

## Tech Stack
- **Backend:** Python, FastAPI
- **Database:** SQLite, SQLAlchemy (ORM)
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **PDF Generation:** ReportLab

## How to Run the Project
Follow these steps to run the application on your local machine:

1. **Install Dependencies:**
   Open your terminal in the project folder and install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate the Database & Mock Data:**
   Run the database seeder to create the SQLite file and populate it with 8 test vehicles (including fraud/accident scenarios):
   ```bash
   python mock_data.py
   ```

3. **Start the Web Server:**
   Launch the FastAPI application using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

4. **View the Application:**
   Open your web browser and navigate to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Important Note
*For the purposes of this MVP prototype, all RTO (Regional Transport Office), Insurance, and Service record data is **simulated**. In a full production environment, this application would integrate directly with real government and commercial insurance APIs.*
