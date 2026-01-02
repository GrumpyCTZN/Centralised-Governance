from flask import Flask,render_template, url_for,request,redirect,session,abort

app=Flask(__name__)
app.secret_key='6...7'

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        searchQuery=request.form.get('searchQuery')
        session['searchRequest']=True
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
    if not session.get('searchRequest'):
        abort(403)
    return render_template('search.html')

if __name__=="__main__":
    app.run(debug=True)
    