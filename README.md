# Entry
Scrape lowes and home depot entry decisions


## Dependecies
1. selenium
* This program opens up a browser window and lets you input commands using python
* I installed using anacondas but pip should work
* There's a helpful browser extension you can play with that "automatically" writes code
https://www.selenium.dev/selenium-ide/

2. geckodriver- This program provides the browser for selenium to issue commands to
* I also installed using anacondas

3. sqlite 
* I have found the following graphical shell helpful, https://sqlitebrowser.org/

## Configuring the repo
In order to run the program you will need to create your own `config.ini` in the parent directory. I have included `config_example.ini` to demonstrate what's involved.

Right now, there are 2 different paths that need to be specified
* The database
* The location where geckodriver is installed