from flask import Flask, request, render_template

app = Flask('__name__')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list')
def shopping_list():
    return render_template('shopping.html')


if __name__ == '__main__':
    app.run(debug=True)
