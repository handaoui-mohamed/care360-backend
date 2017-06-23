## Installation Commands

1- Install python 2.7.*

2- Install pip : https://docs.python.org/2/installing/

3- Install virtualenv: 
    
        pip install virtualenv

4- Go inside the project folder, create a virtual environment: 

        virtualenv flask

5- To go into the virtual environment:

        Linux: source bin/activate

        Windows: .\flask\Scripts\activate

6- Install project requirements:

        pip install -r requirements.txt

7- Generate DataBase/Fakers: 
    
        python db_generate.py

9- Run server on dev mode: 

        python run.py

10- Run server on prod mode: 

        python runp.py
