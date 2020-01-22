from flask import Flask, Markup, render_template, request
import random
import sqlite3

# app = Flask(__name__)
app = Flask(__name__, static_url_path='')


labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

def generate_random(num_results):
    i = 1
    random_values = []
    while i <= num_results:
        # seed random number generator
        # seed(1)
        random_values.append(random.randrange(0, 17000))
        i = i + 1
    print(random_values)
    return random_values
    
# values = [
#     967.67, 1190.89, 1079.75, 1349.19,
#     2328.91, 2504.28, 2873.83, 4764.87,
#     4349.29, 6458.30, 9907, 16297
# ]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


# SQlite3 stuff

global dbtablename
dbtablename = "GMS_table_1"
dbfile = "gms.db"

def connectsqlite3():
    global conn
    conn = sqlite3.connect(dbfile)

def writetosqlite3(tablename, label, value, timestamp, note): #write current track to sqlite3
    global conn
    global timenow
    global dbtablename
    c = conn.cursor()

    tblquery = f"INSERT INTO {dbtablename} VALUES (?,?,?,?)"
    # tblquery = "INSERT INTO "
    # tblquery += tablename
    # tblquery += (''' VALUES (?,?,?,?,?,?,?,?,?)''')
    c.execute(tblquery, (str(label),str(value),str(timestamp),str(note)))
    conn.commit()

def searchsqlite3(graphid, columnname, limitno):
    global conn
    global dbtablename
    c = conn.cursor()

    # tblquery = ('SELECT * FROM \"{dn}\" WHERE \"{cn}\" = \"{st}\"').format(dn=dbtablename, cn=columnname, st=searchterm)
    # tblquery = ('SELECT * FROM \"{dn}\"').format(dn=dbtablename)
    tblquery = f"SELECT * FROM {dbtablename}"

    # use graphid to identify a specific set of stats. use tags for stats? 

    c.execute(tblquery)
    #return conn.commit()
    all_rows = c.fetchall()
    return all_rows

def total_rows():
    global conn
    global dbtablename
    c = conn.cursor()
    tblquery = ('SELECT COUNT(*) FROM \"{dn}\"').format(dn=dbtablename)
    c.execute(tblquery)
    rowcount = str(c.fetchone()[0])
    return rowcount

def createsqlite3table(tablename):
    global conn
    global pollinterval
    global dbtablename
    c = conn.cursor()

    try:
        query = f"CREATE TABLE {dbtablename} (label text, value text, timestamp text, note text)"
        # query = "CREATE TABLE "
        # query += tablename
        # query += " (label text, value text, timestamp text, note text)"
        c.execute(query)
        conn.commit()
        print ("INFO: Created new table " + tablename)
    except:
        print ("WARNING: Error creating sqlite3 table. The table probably already exists, which is cool.")
        pass

def closesqlite3conn():
    conn.close()


# Flask routes
@app.route('/')
def root():
    return app.send_static_file('index.html')

#  label, value, timestamp, note
@app.route('/add_stats')
def graph2():
    value = request.args.get('label')
    label = request.args.get('value')

    connectsqlite3()
    writetosqlite3(dbtablename, value, label, "note", "time")
    closesqlite3conn()
    
    return "Wrote stuff to DB"

@app.route('/graph')
def graph1():
    graphid = request.args.get('graphid')
    connectsqlite3()
    return_labels = []
    return_values = []
    returnval = searchsqlite3(graphid, "value", 100)
    for ting, blah, shiz, funk in returnval:
        return_labels.append(ting)
        return_values.append(blah)
    closesqlite3conn()
    # return str(return_labels + return_values)

    bar_labels=return_labels
    bar_values=return_values
    return render_template('bar_chart.html', title=graphid, max=max(return_values), labels=bar_labels, values=bar_values)

@app.route('/bar')
def bar():
    values = generate_random(12)
    bar_labels=labels
    bar_values=values
    return render_template('bar_chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=bar_labels, values=bar_values)

@app.route('/line')
def line():
    values = generate_random(12)
    line_labels=labels
    line_values=values
    return render_template('line_chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=line_labels, values=line_values)

@app.route('/pie')
def pie():
    values = generate_random(12)
    pie_labels = labels
    pie_values = values
    return render_template('pie_chart.html', title='Bitcoin Monthly Price in USD', max=17000, set=zip(values, labels, colors))

if __name__ == '__main__':
    print("Checking DB...")
    connectsqlite3()
    createsqlite3table(dbfile)
    closesqlite3conn()
    app.run(host='0.0.0.0', port=8080, debug=True)