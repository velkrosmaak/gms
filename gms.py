from flask import Flask, Markup, render_template, request
# from random import seed
# from random import random
import random

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

@app.route('/')
def root():
    return app.send_static_file('index.html')

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
    app.run(host='0.0.0.0', port=8080)