from flask import Flask,render_template, url_for,request,redirect,abort,session,flash
from datetime import datetime
from tables import tables_bp
from fetchdat import fetchData,translateData
import llm

app=Flask(__name__)
app.secret_key = 'super-secret-random-string'


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        searchQuery=request.form.get('searchQuery')
        resultDict=llm.parse_text(searchQuery)
        print(resultDict)
        session['recDict']=resultDict
        if not resultDict['document']:
            return render_template('index.html',trigger_alert=True)
        return redirect(url_for('handleSearch'))
    return render_template('index.html')



@app.route('/commonservices',strict_slashes=False)
@app.route('/commonservices/<path:servicepath>')
def commonservices(servicepath=None):
    print(fetchData('Citizenship'))
    if servicepath==None: 
        return render_template('commonservices.html',data = None)
    elif servicepath == 'Citizenship': 
        return render_template('docs.html',data = fetchData(translateData('Citizenship')))   
    elif servicepath=='DrivingLicense': 
        return render_template('docs.html',data = fetchData(translateData('DrivingLicense')))   
    elif servicepath=='Passport': 
        return render_template('docs.html',data = fetchData(translateData('Passport')))  
    elif servicepath=='NIDCard': 
        return render_template('docs.html',data = fetchData(translateData('NIDCard')))
    else: abort(404)

@app.route('/officialwebsite')
def officialWebsites():
    return render_template('officialwebsite.html')

@app.route('/search',methods=['POST','GET'])
def handleSearch():
    services=['DrivingLicense','NIDCard','Citizenship','Passport']
    result =session.pop('recDict',None) 
    if request.method == 'POST':
        choice=request.form.get('choice')
        service_val = request.form.get("service")
        if choice=='yes':
            return redirect(url_for('commonservices',servicepath=f'{service_val}',_anchor='basic-requirement'))
        else: 
            return render_template('intermediate.html', data=fetchData(translateData(service_val)))
    if not result['criteria_not_met']:
        for document in services: 
            if document in result['document']:
                return render_template('search.html',type=document,button=True,data = fetchData(translateData(document)))
    
    if result['criteria_not_met'] and result['document']:
        return redirect(url_for('commonservices',servicepath=f'{result['criteria_not_met']}'))
    return render_template('search.html')


@app.route('/submit_missing_documents', methods=['POST'])
def submit_missing_documents():
    missing_docs = request.form.getlist('docs')
    services=['DrivingLicense','NID','Citizenship','Passport']
    linkable = []
    unlinkable = []
    for doc in missing_docs:
        if doc in services:
            linkable.append(doc)
        else:
            unlinkable.append(doc)
    
    return render_template('redirecter.html', linkable=linkable, unlinkable=unlinkable)

app.register_blueprint(tables_bp)

if __name__=="__main__":
    app.run(debug=True)
    