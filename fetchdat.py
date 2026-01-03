from connect import connect_db

def translateData(name):
    mapping={
        'Citizenship':'Citizenship',
        'NIDCard':'NID',
        'DrivingLicense':'License',
        'Passport':'Passport'
    }
    return mapping[name]

def fetchData(name):
    conn= connect_db()
    cur=conn.cursor()
    cur.execute(f"SELECT * FROM DOCUMENT_DETAILS WHERE docName='{name}'")
    data=cur.fetchall()
    conn.close()
    return data