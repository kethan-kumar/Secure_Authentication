import os

from flask import *

from business_logic import loan_logic, registration_logic, login_logic

app = Flask(__name__)
app.config.from_object('configuration.config.DevelopmentConfig')
app.secret_key = os.urandom(16)
app.config['uploadFolder'] = 'static/upload'


@app.route('/')
def showLoginPage():
    if "username" in session:
        username = session['username']
        return redirect(url_for('success', name=username))
    return render_template("index.html", otp="False")


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        #  userName is the name of the form field "Email Address"
        userId = request.form['userName']
        password = request.form['password']
        otp = None
        try:
            otp = request.form['OTP']
        except:
            pass
        validationResponse = login_logic.isUserValid(userId, password, otp)
        print(validationResponse)
        if (validationResponse['isCorrect']):
            session['username'] = request.form["userName"]
            return redirect(url_for('success', name=userId))
        elif (validationResponse['message'] == "OTP"):
            flash("Login from new device needs second factor authentication. OTP has been sent to your email!", "error")
            return render_template("index.html", OTP="True", userId=userId, password=password)
        else:
            flash(validationResponse['message'], "error")
            return render_template("index.html", userId=userId, password=password)
    else:
        print("NOT POST METHOD")


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':

        requestBody = {
            "account_number": int(request.form['account_number']),
            "emailid": request.form['emailid'],
            "mobile": int(request.form['mobile']),
            "password": request.form['password'],
            "username": request.form['username']
        }
        isUserRegistered = registration_logic.registerUser(requestBody)

        if isUserRegistered:
            flash("Successfully registered!", "success")
            return render_template("index.html")
        else:
            flash("Error Occurred!", "warning")
            return render_template("index.html", message="SOME ERROR OCCURRED")
    else:
        print("Method signature error")


@app.route('/success/<name>')
def success(name):
    if "username" in session:
        return render_template('single.html', name1=name)
    else:
        return redirect(url_for('showLoginPage'))


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('showLoginPage'))


@app.route("/submitLoanApplication", methods=["POST"])
def submitLoanApplication():
    requestBody = {
        "emailid": session["username"],
        "amount": (request.form['amount']),
        "time": request.form['time'],
        "repayment": request.form['repayment'],
        "name": request.form['name'],
        "dob": request.form['dob'],
        "income": request.form['annual'],
        "loanFile": request.files['loanFile'],
        "config": app.config['uploadFolder']
    }

    res = loan_logic.appLoan(requestBody)
    if (res):
        return render_template("single.html",
                               statusFlag=True,
                               application_Status="Application Submitted",
                               applyMessage="Application has been submitted"
                               )
    else:
        return render_template("single.html", statusFlag=True, application_Status="Some error has occured")


@app.route("/track", methods=["POST"])
def trackLoan():
    email = request.form['email']
    res = loan_logic.trackLoan(email)
    if (res):
        return render_template("single.html", statusFlag=True, application_Status=res)
    else:
        return render_template("single.html", statusFlag=True, application_Status="Some error has occured")


if __name__ == '__main__':
    app.run(debug=True)
