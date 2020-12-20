from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_mysqldb import MySQL
from Calculation import Calculation

app = Flask(__name__)

app.secret_key = "dartsfor2player"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mycountry'
app.config['MYSQL_DB'] = 'dart'

mysql = MySQL(app)

# these global variables for sequencing whose turn after whom
turnA = -1
turnB = -1
boolA = True
boolB = True

@app.route('/', methods=['GET', 'POST'])
@app.route('/info', methods=['GET', 'POST'])
def info():
    nameBool1 = False
    nameBool2 = False

    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM player")
    nameData = cur.fetchall()

    if request.method == 'POST':
        name1 = request.form.get("p1")
        name2 = request.form.get("p2")

        if nameData:
            for data in nameData:
                if name1 == data[0]:
                    nameBool1 = True
                if name2 == data[0]:
                    nameBool2 = True

            if not nameBool1:
                cur.execute("INSERT INTO player(name) values(%s)", (name1,))
                mysql.connection.commit()
            else:
                cur.execute("SELECT id FROM player WHERE name = %s", (name1,))
                id1 = cur.fetchone()
                session["player1"] = id1[0]

            if not nameBool2:
                cur.execute("INSERT INTO player(name) values(%s)", (name2,))
                mysql.connection.commit()
            else:
                cur.execute("SELECT id FROM player WHERE name = %s", (name2,))
                id2 = cur.fetchone()
                session["player2"] = id2[0]

        else:
            cur.execute("INSERT INTO player(name) values(%s)", (name1,))
            mysql.connection.commit()
            cur.execute("SELECT id FROM player WHERE name = %s", (name1,))
            id1 = cur.fetchone()
            session["player1"] = id1[0]

            cur.execute("INSERT INTO player(name) values(%s)", (name2,))
            mysql.connection.commit()
            cur.execute("SELECT id FROM player WHERE name = %s", (name2,))
            id2 = cur.fetchone()
            session["player2"] = id2[0]

        cur.close()
        return redirect(url_for("score"))
    return render_template("info.html")


@app.route('/score')
def score():
    if "player1" in session:
        player1 = session["player1"]

    if "player2" in session:
        player2 = session["player2"]

    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM player WHERE id = %s", (player1,))
    p1name = cur.fetchone()
    cur.execute("SELECT name FROM player WHERE id = %s", (player2,))
    p2name = cur.fetchone()
    cur.execute("SELECT score FROM score WHERE id = %s", (player1,))
    scoreA = cur.fetchone()
    cur.execute("SELECT score FROM score WHERE id = %s", (player2,))
    scoreB = cur.fetchone()
    cur.close()

    return render_template("score.html", p1name=p1name[0], p2name=p2name[0], scoreA=scoreA[0], scoreB=scoreB[0], boolA=boolA, boolB=boolB)

@app.route('/player1A', methods=['GET', 'POST'])
def player1A():
    global turnA
    global boolA
    global boolB
    p1 = Calculation()
    if "player1" in session:
        player1 = session["player1"]

    if "player2" in session:
        player2 = session["player2"]

    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM player where id=%s", (player1,))
    nameA = cur.fetchone()
    cur.execute("SELECT score FROM score WHERE id = %s", (player1,))
    scoreA = cur.fetchone()

    if request.method == 'POST':
        score1 = request.form.get("sc1")

        # for maintaining the sequence who will do his first 3 turns
        if turnA<0:
            turnA = int(request.form.get("turnA"))
            boolB = False
        else:
            turnA -= 1
            boolB = False

        if turnA == 0:
            boolA = False
            boolB = True
            turnA = -1


        result = p1.playerA(scoreA[0], int(score1))

        # if someone scores more than required
        if isinstance(result, str):
            flash(result, "danger")
            return redirect(url_for("score"))

        if result>0:
            cur.execute("UPDATE score SET score = %s WHERE id = %s", (result, player1))
            mysql.connection.commit()
        else:
            cur.execute("UPDATE score SET score = %s WHERE id = %s", (501, player1))
            mysql.connection.commit()
            cur.execute("UPDATE score SET score = %s WHERE id = %s", (501, player2))
            mysql.connection.commit()

            flash("Congratulations {0}!!!   You win!!!".format(nameA[0]))
            cur.close()
            return redirect(url_for("info"))

        cur.close()
        return redirect(url_for("score"))

    cur.close()
    return redirect(url_for("score"))


@app.route('/player2B', methods=['GET', 'POST'])
def player2B():
    global turnB
    global boolA
    global boolB

    p2 = Calculation()
    if "player2" in session:
        player2 = session["player2"]

    if "player1" in session:
        player1 = session["player1"]

    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM player where id=%s", (player2,))
    nameB = cur.fetchone()
    cur.execute("SELECT score FROM score WHERE id = %s", (player2,))
    scoreB = cur.fetchone()

    if request.method == 'POST':
        score2 = request.form.get("sc2")

        # for maintaining the sequence who will do his first 3 turns
        if turnB<0:
            turnB = int(request.form.get("turnB"))
            boolA = False
        else:
            turnB -= 1
            boolA = False

        if turnB == 0:
            boolB = False
            boolA = True
            turnB = -1

        result = p2.playerB(scoreB[0], int(score2))

        if isinstance(result, str):
            flash(result, "danger")
            return redirect(url_for("score"))

        if result>0:
            cur.execute("UPDATE score SET score = %s WHERE id = %s", (result, player2))
            mysql.connection.commit()
        else:
            cur.execute("UPDATE score SET score = %s WHERE id = %s", (501, player2))
            mysql.connection.commit()
            cur.execute("UPDATE score SET score = %s WHERE id = %s", (501, player1))
            mysql.connection.commit()

            flash("Congratulations {0}!!!   You win!!!".format(nameB[0]))
            cur.close()
            return redirect(url_for("info"))

        cur.close()
        return redirect(url_for("score"))

    cur.close()
    return redirect(url_for("score"))


if __name__ == '__main__':
    app.run()
