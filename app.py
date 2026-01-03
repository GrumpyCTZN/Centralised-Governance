from flask import Flask,render_template, url_for,request,redirect,abort,session,flash
from datetime import datetime
from tables import tables_bp
import llm

app=Flask(__name__)
app.secret_key = 'super-secret-random-string'


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        searchQuery=request.form.get('searchQuery')
        resultDict=llm.parse_text(searchQuery)
        session['recDict']=resultDict
        if not resultDict['document']:
            return render_template('index.html',trigger_alert=True)
        return redirect(url_for('handleSearch'))
    return render_template('index.html')



@app.route('/commonservices',strict_slashes=False)
@app.route('/commonservices/<path:servicepath>')
def commonservices(servicepath=None):
    if servicepath==None: return render_template('commonservices.html')
    elif servicepath == 'citizenship': return render_template('citizenship.html')   
    elif servicepath=='drivinglicense': return render_template('drivinglicense.html')   
    elif servicepath=='passport': return render_template('passport.html')  
    elif servicepath=='nidcard': return render_template('nidcard.html')
    else: abort(404)

@app.route('/officialwebsite')
def officialWebsites():
    return render_template('officialwebsite.html')

@app.route('/search',methods=['POST','GET'])
def handleSearch():
    services=['drivinglicense','nidcard','citizenship','passport']
    result =session.pop('recDict',None) 
    if request.method == 'POST':
        choice=request.form.get('choice')
        service_val = request.form.get("service")
        if choice=='yes':
            return redirect(url_for('commonservices',servicepath=f'{service_val}',_anchor='closest-office'))
        else: return render_template('intermediate.html')
    if not result['criteria_not_met']:
        for document in services: 
            if document in result['document']:
                return render_template('search.html',type=document,button=True)
    
    if result['criteria_not_met'] and result['document']:
        return redirect(url_for('commonservices',servicepath=f'{result['criteria_not_met'][2:]}'))
    return render_template('search.html')

app.register_blueprint(tables_bp)

if __name__=="__main__":
    app.run(debug=True)
    