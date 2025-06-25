from flask import Flask, render_template
import requests
app = Flask(__name__)


app.config['STATIC_FOLDER'] = 'static'
app.config['IMAGES_FOLDER'] = 'images'

borealcoffee = f"{app.config['STATIC_FOLDER']}/{app.config['IMAGES_FOLDER']}/boreal-coffee-clone.jpeg"
dopefolio = f"{app.config['STATIC_FOLDER']}/{app.config['IMAGES_FOLDER']}/dopefolio.jpg"
wilsonport = f"{app.config['STATIC_FOLDER']}/{app.config['IMAGES_FOLDER']}/wilsonport.jpeg"
crowntemplate = f"{app.config['STATIC_FOLDER']}/{app.config['IMAGES_FOLDER']}/crowntemplate.jpg"

flutter = f"{app.config['STATIC_FOLDER']}/{app.config['IMAGES_FOLDER']}/flutter.png"
monitor = f"{app.config['STATIC_FOLDER']}/{app.config['IMAGES_FOLDER']}/monitor.png"
react = f"{app.config['STATIC_FOLDER']}/{app.config['IMAGES_FOLDER']}/react.png"

@app.route('/')
def index():
    return render_template(
        'index.html'
)
    
@app.route('/about')
def about():
    return render_template(
        'about.html'
)

@app.route('/experiences')
def experiences():
    return render_template(
        'experiences.html',
        flutter=flutter,
        monitor=monitor,
        react=react
)
    
@app.route('/contact')
def contact():
    return render_template(
        'contact.html'
)

@app.route('/project')
def project():
    return render_template(
        'project.html',
        borealcoffee=borealcoffee,
        crowntemplate=crowntemplate,
        dopefolio=dopefolio,
        wilsonport=wilsonport,       
        
)