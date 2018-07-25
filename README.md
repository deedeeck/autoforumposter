# Autoforumposter
* This repository contains a crawler that will go to a forum page and automatically post a comment on threads  
* This will help a user to increase his/her post count  
* Website and credentials are obscured to prevent spamming on the website  


## Setting up
Download [chrome driver](https://sites.google.com/a/chromium.org/chromedriver/)   
Place driver in repository root folder  
Install selenium library  
```
pip install -U selenium
```  

## Running the crawler
```
python3 poster.py
```

## Future Enhancements  
* Prevent crawler from posting on threads which are more than 3 days old  
* Run crawler through proxy requests to mask IP