
# Import the necessary Libraries
from flask_cors import CORS,cross_origin
from flask import Flask, render_template, request,jsonify
import os
import requests
from bs4 import BeautifulSoup
import urllib.request

# initialising the flask app with the name 'app'
app = Flask(__name__) 

# route for redirecting to the home page
@app.route('/') 
@cross_origin()
def home():
    return render_template('index.html')


@app.route('/downloadImages',methods = ['Get','POST'])
@cross_origin()
def downloadImages():
    if request.method == 'POST':
        search_term = request.form['searchTerm']
        image_number = request.form['imageNumber']
        print(image_number)
        url = "https://www.google.com/search?q=" + search_term + "&source=lnms&tbm=isch"
        response = requests.get(url)
        data_scraped = BeautifulSoup(response.text, "lxml")
        currentimage_number = 0
        for image in data_scraped.find_all('img'):
            current_image = image.attrs.get("src")
            path = os.getcwd()
            filepath = os.path.join(path,'static')
            fullfilename = os.path.join(filepath, "Image{}.jpg".format(currentimage_number))
            if(int(currentimage_number) == int(image_number)):
                break
            if (current_image.startswith('http')):
                urllib.request.urlretrieve(current_image, fullfilename)
                currentimage_number = currentimage_number+1
           
               
        images = os.listdir('static')
        images.remove('style.css')
        
        return render_template('showImage.html',user_images=images)
    else:
        print("in a wrong method")                 
                                      
    

if __name__ == "__main__":
    # port to run on local machine
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0    
    app.run(host='127.0.0.1', port=8000) 
   
