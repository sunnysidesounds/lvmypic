## WHAT IS lvmypic?

lvmypic is a website image scrapper that scraps images from a domain and emails the results to an email address. 

## HOW TO USE:

Basic Syntax:

    python lvmypic.py <domain/host> <how_many_image> <minimum_image_size>

Example:

    python lvmypic.py http://www.mydomain.com 10 300
    (I want to extract 10 images no less the 300 pixels height)


## TODO:
*	Email is hardcoded into the script. Need to change it to pass a email argument. 
*	Optimize speed and performance issues. 