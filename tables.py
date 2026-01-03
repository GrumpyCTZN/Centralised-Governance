from flask import Flask,render_template, url_for,request,redirect,Blueprint ,jsonify
from connect import connect_db
tables_bp = Blueprint('tables', __name__)
@tables_bp.route('/tables')
def display_tables():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    table_names = [row[0] for row in cur.fetchall()]
    tables_data = {}

    for table_name in table_names:
        cur.execute(f"SELECT * FROM {table_name}")
        columns = [description[0] for description in cur.description]
        rows = cur.fetchall()
        tables_data[table_name] = {'columns': columns, 'rows': rows}
    
    conn.close()
    return render_template('tables.html', tables_data=tables_data)

@tables_bp.route('/execute_sql', methods=['POST'])
def execute_sql():
    
    sql_query = request.json.get('query', '').strip()
    
    if not sql_query:
        return jsonify({'error': 'No query provided'})
    
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        cur.execute(sql_query)
        
        # Check if it's a SELECT query
        if sql_query.upper().startswith('SELECT'):
            columns = [description[0] for description in cur.description] if cur.description else []
            rows = cur.fetchall()
            conn.close()
            return jsonify({
                'success': True,
                'columns': columns,
                'rows': rows,
                'row_count': len(rows)
            })
        else:
            # For INSERT, UPDATE, DELETE, etc.
            conn.commit()
            affected = cur.rowcount
            conn.close()
            return jsonify({
                'success': True,
                'message': f'Query executed successfully. {affected} row(s) affected.',
                'affected_rows': affected
            })
    except Exception as e:
        conn.close()
        return jsonify({
            'success': False,
            'error': str(e)
        })