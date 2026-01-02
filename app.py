from flask import Flask,render_template, url_for,request,redirect

app=Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        searchQuery=request.form.get('searchQuery')
        return redirect(url_for('handleSearch'))
    return render_template('index.html')

@app.route('/commonservices')
def commonservices():
    return render_template('commonservices.html')

@app.route('/officialwebsite')
def officialWebsites():
    return render_template('officalwebsite.html')

@app.route('/search')
def handleSearch():
    return render_template('search.html')

if __name__=="__main__":
    app.run(debug=True)
    