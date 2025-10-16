# MoxymindZadanie

<h3>1. NOTE: Pre-Conditions</h3>
    
**Have VS code installed (default installation)**:

[https://code.visualstudio.com/download](https://code.visualstudio.com/download)

**Have Python installed** (π-thon, right now in version 3,14 :D) with pip and 

**Add python.exe** to **PATH** on first step of installer and press Install now (if you don’t want custom installation):

[https://www.python.org/downloads](https://www.python.org/downloads)

**Have Git installed and setuped**:

If you don’t have installed your Git client locally go to following URL and install it for your OS:

[https://git-scm.com/downloads](https://git-scm.com/downloads)
___

<h3>2.  Set it up with your account credentials in i.e. git CMD console, but without $ symbol:</h3>

  *$ git config --global user.name "<your_name>"*

  *$ git config --global user.email <your_email.com>*

**Clone locally Github repository via command with** [**URL**](https://github.com/Shakul42/MoxymindZadanie/tree/main:) **in Terminal (be in desired folder):**

(**or SSH ->** git@github.com:Shakul42/MoxymindZadanie.git)

git clone [https://github.com/Shakul42/MoxymindZadanie/tree/main](https://github.com/Shakul42/MoxymindZadanie/tree/main):
____

<h3> 3. VS code setup</h3>
    
After Cloning repository to your local machine open location of project in VS code and install all requirements through the terminal (i.e. in VS code) using command:


    pip install -r requirements.txt

To create current requirements.txt you can use command:    pip freeze > requirements.txt

***Alternatively*** use commands in terminal and install all manually:

FOR reference how to install Playwright with Python check this documentation: [https://playwright.dev/python/docs/intro](https://playwright.dev/python/docs/intro)  

**Installing Pytest Playwright package:**

    pip install pytest-playwright

**Installing playwright browsers:**

    playwright install

to **be able to generate reports** please also install same way following package:

    pip install pytest-html
___

<h3>4. Running of the Tests</h3>   

<h4>FE Tests:</h4>

**To run test please use in terminal following command**: -v param is for verbose TC list

    pytest  tests\testLoginFe.py -v

To run ATC in **different browser** (chromium, webkit, firefox...) and **see it + Report**, you can use following cmd:

    pytest --browser chromium --headed --html=reports/report.html --self-contained-html tests\testLoginFe.py -v
<h4>API Tests:</h4>

**For API tests run this command +Report** (with attribute -v instead of -s, print messages won’t be showed inside the terminal) :

    pytest --html=reports/reportApi.html tests\api\testApi.py -s

to **NOT create report** remove --html part:

    pytest tests\api\testApi.py -s

**HERE might happen that the API won’t be initiated**. To do so please follow link:  [https://reqres.in](https://reqres.in) 

And press “**Start free — create a workspace**” button. 

Optionally you can click on “**Get free API key**” and then navigate in browser to endpoint:

[https://reqres.in/api/users?page=2](https://reqres.in/api/users?page=2) 

This should fix the problem with endpoint not returning data but showing Not Authorized error - 401
