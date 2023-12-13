from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'
MAX_ATTEMPTS = 5

@app.route('/')
def main():
    session.clear() 
    return render_template('demo.html', num1='', num2='', attempts_left=MAX_ATTEMPTS)

@app.route('/process', methods=['POST'])
def process():
    try:
        if 'attempts' not in session:
            session['attempts'] = 0
            session['num1'] = int(request.form['num1'])
            session['num2'] = int(request.form['num2'])
            session['random_number'] = randoms(session['num1'], session['num2'])

        guess = request.form['guess']
        
        if 'num1' not in session or 'num2' not in session or not guess:
            raise ValueError("Missing input")

        guess = int(guess)
        random_num = int(session['random_number'])
        message = "Never trust anyone"

        if guess < session['num1'] or guess > session['num2']:
            message = "Please enter a value between num1 and num2"

        elif guess == random_num:
            message = "Great job"
            session.clear() 

        else:
            session['attempts'] += 1
            if session['attempts'] >= MAX_ATTEMPTS:
                session.clear() 
                message = "Out of attempts"
            else:
                attempts_left = MAX_ATTEMPTS - session['attempts']
                message = f"Not matched, try again."

        return render_template('demo.html', message=message, num1=session.get('num1', ''), num2=session.get('num2', ''), attempts_left=MAX_ATTEMPTS - session.get('attempts', 0))
    
    except (ValueError, KeyError):
        return render_template('demo.html', message="Please enter num1 and num2", num1='', num2='', attempts_left=MAX_ATTEMPTS)

def randoms(lower, upper):
    x = random.randint(lower, upper)
    print(x)
    return x

if __name__ == '__main__':
    app.run(debug=True)
