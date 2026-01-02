from flask import Flask,render_template, url_for

app=Flask(__name__)

@app.route('/',)
def index():
    return render_template('index.html')

@app.route('/commonservices')
def commonservices():
    return render_template('commonservices.html')

@app.route('/officialwebsite')
def officialWebsites():
    return render_template('officalwebsite.html')

if __name__=="__main__":
    app.run(debug=True)
    