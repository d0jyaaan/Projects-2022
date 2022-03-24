import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.before_request
def make_session_permanent():
    session.permanent = True


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session["user_id"]
    stock_symbol = db.execute("SELECT stock, value FROM stocks WHERE person_id = ?", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

    temp = cash[0]["cash"]

    total = float(cash[0]["cash"])

    if len(stock_symbol) != 0:

        symbol = []
        symbol = stock_symbol

        length = len(symbol)

        for i in range(0, length, 1):

            stock_lookup = lookup(symbol[i]["stock"])

            price = stock_lookup["price"]

            sum_ = price * symbol[i]["value"]

            if sum_ != None:
                total += sum_
                db.execute("UPDATE stocks SET price = ?, total = ? WHERE stock = ? AND person_id = ?",
                           price, sum_, symbol[i]["stock"], user_id)

        stocks = db.execute("SELECT name, stock, total, value, price FROM stocks WHERE person_id = ?", user_id)

        for i in range(0, length, 1):
            stocks[i]["price"] = usd(stocks[i]["price"])
            stocks[i]["total"] = usd(stocks[i]["total"])

        return render_template("index.html", stocks=stocks, total=usd(total), cash=usd(temp))

    else:

        return render_template("index.html", stock=None, total=usd(total), cash=usd(temp))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        # type of stock
        # number of stock
        # user id

        stock = request.form.get("symbol").upper()
        user_id = session["user_id"]

        # error check

        if stock == "":
            return apology("Please input stock", 400)

        try:
            num_stock = int(request.form.get("shares"))
        except:
            return apology("Input integer", 400)

        if num_stock <= 0:
            return apology("Input positive number", 400)

        # lookup stock

        stock_info = lookup(stock)

        if stock_info == None:
            # stock doesnt exist
            return apology("Stock doesnt exist", 400)

        else:
            # get the current stock price
            stock_price = stock_info["price"]

            # amount of cash user has
            cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

            # total price of stock
            total_price = num_stock * stock_price

            # balance if bought the stock
            balance = cash[0]["cash"] - total_price

            if balance < 0:
                # stock price more than users cash
                return apology("Price exceeds user's cash", 400)

            # if user doesnt have that stock, insert this

            # select amount of stock user has
            stock_amount = db.execute("SELECT value FROM stocks WHERE person_id = ? AND stock = ?", user_id, stock)

            if len(stock_amount) != 1:
                # not in database
                db.execute("INSERT INTO stocks (name, person_id, stock, value, price) VALUES (?, ?, ?, ?, ?)",
                           stock_info["name"], user_id, stock, num_stock, stock_info["price"])

                db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, user_id)

            else:
                # in database
                temp = stock_amount[0]["value"]
                num_temp = int(num_stock) + int(temp)

                db.execute("UPDATE stocks SET value = ?, price = ? WHERE person_id = ? AND stock = ?",
                           num_temp, stock_info["price"], user_id, stock)

                db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, user_id)

            now = datetime.now()
            time = now.strftime("%d/%m/%Y %H:%M:%S")

            db.execute("INSERT INTO transactions (name, person_id, type, stock, amount, price, time) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       stock_info["name"], user_id, "BUY", stock, num_stock, stock_price, time)

            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]
    stock = db.execute("SELECT * FROM transactions WHERE person_id = ?", user_id)

    return render_template("history.html", stocks=stock, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        username = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        # error checking
        # symbol
        if symbol == "":
            return apology("Please input symbol", 400)

        # look for symbol
        stock = lookup(symbol)

        # stock doesnt exist
        if stock is None:
            return apology("Symbol doesn't exist", 400)

        # success
        return render_template("quote.html", stock=stock, usd=usd)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if confirmation != password:
            return apology("Passwords don't match", 400)

        if not username:
            return apology("Please input username", 400)

        if not password:
            return apology("Please input password", 400)

        # generate hash
        password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        check = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(check) != 1:
            # if acc doesnt exist
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)
            return render_template("login.html")

        else:
            # if acc already exists, return
            return apology("Account already exists", 400)

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user_id = session["user_id"]
    names = db.execute("SELECT stock FROM stocks WHERE person_id=?", user_id)

    if request.method == "POST":

        # get var from html
        stock = request.form.get("symbol").upper()
        num_stock = request.form.get("shares")

        # error checking
        if num_stock == "":
            return apology("Input valid number of stocks", 400)

        if stock == "":
            return apology("Input valid stock", 400)

        # getting num of stocks
        num_stock = int(num_stock)
        stocks = db.execute("SELECT * FROM stocks WHERE person_id=? AND stock=?", user_id, stock)

        if len(stocks) != 1:
            return apology("You dont own that stock", 400)

        # initialization
        # amount
        number = stocks[0]["value"]
        # cash owned
        cash = db.execute("SELECT cash FROM users WHERE id=?", user_id)[0]["cash"]
        # price of stock
        lookup_ = lookup(stock)
        price = lookup_["price"]

        # time
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")
        time = str(time)

        # if input more than own
        if int(num_stock) > int(number):
            return apology("You dont own that number of stocks", 400)

        # if same amount
        elif int(num_stock) == int(number):

            # total price
            total = num_stock * price
            cash += total

            db.execute("UPDATE users SET cash=? WHERE id=?", cash, user_id)

            db.execute("DELETE FROM stocks WHERE person_id=? AND stock=?", user_id, stock)

            db.execute("INSERT INTO transactions (name, person_id, type, stock, amount, price, time) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       lookup_["name"], user_id, "SELL", stock, num_stock, price, time)

            return redirect("/")

        #  if less than
        elif int(num_stock) < int(number):

            # total price
            total = float(num_stock) * price
            cash += total

            number -= num_stock

            db.execute("UPDATE users SET cash=? WHERE id=?", cash, user_id)

            db.execute("UPDATE stocks SET value=? WHERE person_id=? AND stock=?", number, user_id, stock)

            db.execute("INSERT INTO transactions (name, person_id, type, stock, amount, price, time) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       lookup_["name"], user_id, "SELL", stock, num_stock, price, time)

            return redirect("/")

    else:
        return render_template("sell.html", stocks=names)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

