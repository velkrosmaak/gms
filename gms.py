from flask import Flask, Markup, render_template, request
import random
import sqlite3

# app = Flask(__name__)
app = Flask(__name__, static_url_path='')

'''
TODO:
Add tag field
list all tags on homepage
search tags form
multiple tags
import csv bulk data

'''

# SQLite db config
global dbtablename
dbtablename = "GMS_table_3"
dbfile = "gms.db"

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
    
colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


# SQlite3 stuff

def connectsqlite3():
    global conn
    conn = sqlite3.connect(dbfile)

def writetosqlite3(tablename, label, value, timestamp, note, tag): #write current track to sqlite3
    global conn
    global timenow
    global dbtablename
    c = conn.cursor()

    tblquery = f"INSERT INTO {dbtablename} VALUES (?,?,?,?,?)"
    c.execute(tblquery, (str(label),str(value),str(timestamp),str(note), str(tag)))
    conn.commit()

def searchsqlite3_tag(stat_tag, limitno):
    global conn
    global dbtablename
    c = conn.cursor()

    # tblquery = ('SELECT * FROM \"{dn}\" WHERE \"{cn}\" = \"{st}\"').format(dn=dbtablename, cn=columnname, st=searchterm)
    tblquery = f"SELECT * FROM {dbtablename} WHERE tag = {stat_tag}"
    # tblquery = ('SELECT * FROM \"{dn}\"').format(dn=dbtablename)
    # tblquery = f"SELECT * FROM {dbtablename}"

    # use graphid to identify a specific set of stats. use tags for stats? 

    c.execute(tblquery)
    #return conn.commit()
    all_rows = c.fetchall()
    return all_rows


def sqlite3_list_tags(limitno):
    '''
    List all unique tags in the DB
    '''
    global conn
    global dbtablename
    c = conn.cursor()

    tblquery = f"SELECT DISTINCT tag FROM {dbtablename}"

    c.execute(tblquery)

    all_rows = c.fetchall()
    return all_rows


def searchsqlite3(graphid, columnname, limitno):
    global conn
    global dbtablename
    c = conn.cursor()

    tblquery = f"SELECT * FROM {dbtablename}"

    c.execute(tblquery)

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
        query = f"CREATE TABLE {dbtablename} (label text, value text, timestamp text, note text, tag text)"
        # query = "CREATE TABLE "
        # query += tablename
        # query += " (label text, value text, timestamp text, note text)"
        c.execute(query)
        conn.commit()
        print (f"INFO: Created new table {dbtablename} in {tablename}")
    except:
        print ("WARNING: Error creating sqlite3 table. The table probably already exists, which is cool.")
        pass

def closesqlite3conn():
    conn.close()

def get_timestamp():
    from datetime import datetime
    dateTimeObj = datetime.now()
    return dateTimeObj


# Flask routes

@app.route('/add_stats')
def addshit():
    return render_template('add_entry.html')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/list_tags')
def list_tags():
    connectsqlite3()
    tag_list = sqlite3_list_tags(100)
    closesqlite3conn()
    return str(tag_list)


@app.route('/do_add_stats', methods=['POST'])
def do_add_stats():
    
    label = request.form['value']
    value = request.form['label']
    note = request.form['note']
    tag2 = request.form['tag']
    ts = get_timestamp()
    
    connectsqlite3()
    writetosqlite3(dbtablename, value, label, ts, note, tag2)
    closesqlite3conn()

    return render_template('record_added.html', ts=ts, note=note, label=label, value=value, tag=tag2)
    

@app.route('/graph')
def graph1():
    graphid = request.args.get('graphid')
    connectsqlite3()
    return_labels = []
    return_values = []
    returnval = searchsqlite3(graphid, "value", 100)
    for ting, blah, shiz, funk, boom in returnval:
        blah_num = int(blah)
        return_labels.append(ting)
        return_values.append(blah_num)
    closesqlite3conn()
    
    # print(max(return_values))
    bar_labels=return_labels
    bar_values=return_values
    return render_template('bar_chart.html', title=graphid, max=max(return_values), labels=bar_labels, values=bar_values)

@app.route('/graph_tag')
def graph_tag():
    graph_tag = request.args.get('tag')
    print(graph_tag)
    connectsqlite3()
    return_labels = []
    return_values = []
    returnval = searchsqlite3_tag(graph_tag, 100)
    for ting, blah, shiz, funk, boom in returnval:
        blah_num = int(blah)
        return_labels.append(ting)
        return_values.append(blah_num)
    closesqlite3conn()
    # return str(return_labels + return_values)

    bar_labels=return_labels
    bar_values=return_values
    return render_template('bar_chart.html', title=graph_tag, max=max(bar_values), labels=bar_labels, values=bar_values)


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