# EC530_SQL-Application-Project

This is a hackathon project, where I created a chat-based spreadsheet assistant that loads CSV files and answers questions using SQL queries.

Description of the Code files attached:
- step1.py: Loads a CSV into SQLite.
- step2.py: Dynamically creates tables from CSV and handles data types.
- step3.py: Handles schema conflicts (e.g., adding missing columns).
- step4.py: Simulates an interactive chat where users can load CSVs and run SQL queries.
- step5.py: Integrates AI (like GPT-4) to generate SQL queries from plain language input

Instructions on how to run this Chat assisstant:
1. Install the relevent systems like openai and pandas. 
2. Set Your OpenAI API Key In PowerShell: $env:OPENAI_API_KEY="sk-your-secret-key"
3. Run python step5.py
   - This will then activate the chat assisitant in which it will ask you questions.
   - Start by loading your csv file by inputting the name of the csv file. Make sure the .csv file is in the current directory you are running in.
   - Ask the chat AI any questions you'd like related to the information you have in the .csv file.
4. ENJOY!

   
