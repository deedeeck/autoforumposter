# Autoforumposter
* This repository contains a crawler that will go to a forum page and automatically post a comment on threads  
* This will help a user to increase his/her post count  
* Website and credentials are obscured to prevent spamming on the website  

## Setting up
* Download [chrome driver](https://sites.google.com/a/chromium.org/chromedriver/)   
* Place driver in repository root folder  
* Set up python virtual env
```
pip install virtualenv  
virtualenv -p /usr/bin/python3 env  
source env/bin/activate  
pip install -r requirements.txt
```
* Install chrome binaries
```  
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - 
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update 
sudo a

## Running the crawler
```
python3 poster.py
```

## Using selenium standalone server for local testing and debugging
* To test crawling a website without restarting chrome sessions repeatedly
* Download [selenium standalone server](https://www.seleniumhq.org/download/)
* File will be a jar file (eg java -jar selenium-server-standalone-3.141.59.jar)
* Run the server using:
```
java -jar selenium-server-standalone-3.141.59.jar
```
* Once server is running, open a new terminal window and run get_remote_session_id.py to get selenium server session id
  * Eg of selenium server session id : 600b64f7ab85973f6392df872199f534
  * Replace remote_session_id in poster.py with your selenium server session id
* Assign your new chrome session in your script to use this session id via:
```
driver.session_id = <<selenium server session id>>
```

## Current features
* Logging into site  
* Searching a particular thread to see if user has already posted a message  
* Explicit waits in between posts to prevent being blocked by website for spamming  

## Future enhancements  
* Prevent crawler from posting on threads which are more than 3 days old  
* Run crawler through proxy requests to mask IP