from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home route
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/transaction')
def transaction():
    return render_template('transaction.html')


@app.route('/selection')
def selection():
    user_input = request.args.get('user_input', None)  # Get the 'user_input' query parameter
    print(user_input)
    return render_template('selection.html', user_input=user_input.upper())

@app.route('/category')
def category():
    user_input = request.args.get('user_input', None)  # Get the 'user_input' query parameter
    print(user_input)
    return render_template('category.html',user_input=user_input.upper())

# Form route
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        return render_template('form_response.html', name=name, message=message)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
