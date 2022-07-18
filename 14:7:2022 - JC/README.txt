Fasanara Coding Excercise: FX tracking project.

James Corby. 

Overview:

exchangerate.py 
- This file includes an API wrapper that i have built using Python code. I decided to go for an OOP approach 
  to this task as i felt its better to write a script that is scalable and shows a clear and clean proccess. 
  This task could have been completed with a few lines of code but i felt a more thourough approach was better
  than a 'hacky' solution. 
- Alos, ideally i would have pulled the latest exchangerates with 'datetime.today().strftime('%Y-%m-%d')' but
  didnt want to pull rates from over the weekend, so i opted for the date i had my first round interview.

tests.py
- This file includes some small unit tests i built to ensure the api calls worked properly. 

How to run the code: 
1) Go to exchangeratesapi.io and get a free api key
2) Add you API key to the header dictionairy at the top of the page
3)) How to execute the code:
    - Execute the file with your API key added - python3 exchangerate.py
    

Any questions please ask!

I really enjoyed doing this task was great to get an insight into one form of extracting financial data. 