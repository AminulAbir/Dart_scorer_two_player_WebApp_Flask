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

# for recommend functions
#str1 = None
#str2 = None
#str3 = None

# these for the scorecard of playerA
bullsA = 0
score60A = 0
score180A = 0

# these for the scorecard of playerB
bullsB = 0
score60B = 0
score180B = 0

# this local variable to calculate whether 3 60s in a row
countA180 = 0
countB180 = 0

@app.route('/', methods=['GET', 'POST'])
@app.route('/info', methods=['GET', 'POST'])
def info():
    global turnA
    global turnB
    global boolA
    global boolB

    #global str1
    #global str2
    #global str3

    global bullsA
    global score60A
    global score180A

    global bullsB
    global score60B
    global score180B
    # this local variable to calculate whether 3 60s in a row
    global countA180
    global countB180

    # these global variables for sequencing whose turn after whom
    turnA = -1
    turnB = -1
    boolA = True
    boolB = True

    # for recommend functions
    #str1 = None
    #str2 = None
    #str3 = None

    # these for the scorecard of playerA
    bullsA = 0
    score60A = 0
    score180A = 0

    # these for the scorecard of playerB
    bullsB = 0
    score60B = 0
    score180B = 0

    # this local variable to calculate whether 3 60s in a row
    countA180 = 0
    countB180 = 0

    # for checking whether already have accounts with same name
    nameBool1 = False
    nameBool2 = False

    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM player")
    nameData = cur.fetchall()

    if request.method == 'POST':
        name1A = request.form.get("p1")
        name2B = request.form.get("p2")

        # for storing all names in small later
        name1 = name1A.lower()
        name2 = name2B.lower()

        if nameData:
            for data in nameData:
                if name1 == data[0]:
                    nameBool1 = True
                if name2 == data[0]:
                    nameBool2 = True

            if not nameBool1:
                cur.execute("INSERT INTO player(name) values(%s)", (name1,))
                mysql.connection.commit()
                cur.execute("SELECT id FROM player WHERE name = %s", (name1,))
                id1 = cur.fetchone()
                session["player1"] = int(id1[0])

                cur.execute("INSERT INTO scorecard values(%s, %s, %s, %s, %s, %s, %s, %s)",
                            (int(id1[0]), 0, 0, 0, 0, 0, 0, 0))
                mysql.connection.commit()
            else:
                cur.execute("SELECT id FROM player WHERE name = %s", (name1,))
                id1 = cur.fetchone()
                session["player1"] = int(id1[0])

            if not nameBool2:
                cur.execute("INSERT INTO player(name) values(%s)", (name2,))
                mysql.connection.commit()
                cur.execute("SELECT id FROM player WHERE name = %s", (name2,))
                id2 = cur.fetchone()
                session["player2"] = int(id2[0])

                cur.execute("INSERT INTO scorecard values(%s, %s, %s, %s, %s, %s, %s, %s)",
                            (int(id2[0]), 0, 0, 0, 0, 0, 0, 0))
                mysql.connection.commit()
            else:
                cur.execute("SELECT id FROM player WHERE name = %s", (name2,))
                id2 = cur.fetchone()
                session["player2"] = int(id2[0])

        else:
            cur.execute("INSERT INTO player(name) values(%s)", (name1,))
            mysql.connection.commit()
            cur.execute("SELECT id FROM player WHERE name = %s", (name1,))
            id1 = cur.fetchone()
            session["player1"] = int(id1[0])

            cur.execute("INSERT INTO player(name) values(%s)", (name2,))
            mysql.connection.commit()
            cur.execute("SELECT id FROM player WHERE name = %s", (name2,))
            id2 = cur.fetchone()
            session["player2"] = int(id2[0])

            cur.execute("INSERT INTO scorecard values(%s, %s, %s, %s, %s, %s, %s, %s)", (int(id1[0]), 0, 0, 0, 0, 0, 0, 0))
            mysql.connection.commit()
            cur.execute("INSERT INTO scorecard values(%s, %s, %s, %s, %s, %s, %s, %s)", (int(id2[0]), 0, 0, 0, 0, 0, 0, 0))
            mysql.connection.commit()

        cur.close()
        return redirect(url_for("score"))
    return render_template("info.html", nameData=nameData)


@app.route('/score')
def score():
    #global str1
    #global str2
    #global str3

    # to maintain whose recommend call it is
    #bool1 = False
    #bool2 = False

    p1 = Calculation()  # object creation for Calculation class

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

    """
    # for recommended turns for Player1(for 3 shots)
    if turnA == -1:
        if ((int(scoreA[0]) <= 180) and (int(scoreA[0]) >= 101)):
            str1, str2, str3 = p1.recommend_func(int(scoreA[0]))
            bool1 = True
    # for recommended turns for Player1(for 2 shots)
    if turnA == 2:
        if ((int(scoreA[0]) <= 120) and (int(scoreA[0]) >= 1)):
            str1, str2, str3 = p1.recommend_func2(int(scoreA[0]))
            bool1 = True

    # for recommended turns for Player1(for single shot)
    if turnA == 1:
        if ((int(scoreA[0]) <= 60) and (int(scoreA[0]) >= 1)):
            str1, str2, str3 = p1.recommend_func3(int(scoreA[0]))
            bool1 = True

    # for recommended turns for Player2(for 3 shots)
    if turnB == -1:
        if ((int(scoreB[0]) <= 180) and (int(scoreB[0]) >= 101)):
            str1, str2, str3 = p1.recommend_func(int(scoreB[0]))
            bool2 = True

    # for recommended turns for Player2(for 2 shots)
    if turnB == 2:
        if ((int(scoreB[0]) <= 120) and (int(scoreB[0]) >= 1)):
            str1, str2, str3 = p1.recommend_func2(int(scoreB[0]))
            bool2 = True

    # for recommended turns for Player2(for single shot)
    if turnB == 1:
        if ((int(scoreB[0]) <= 60) and (int(scoreB[0]) >= 1)):
            str1, str2, str3 = p1.recommend_func3(int(scoreB[0]))
            bool2 = True
    """

    #when use recommend function then use the given parameters in below template (str1=str1, str2=str2, str3=str3, bool1=bool1, bool2=bool2)
    return render_template("score.html", p1name=p1name[0], p2name=p2name[0], scoreA=scoreA[0], scoreB=scoreB[0], boolA=boolA, boolB=boolB)

@app.route('/player1A', methods=['GET', 'POST'])
def player1A():
    global turnA
    global boolA
    global boolB

    global bullsA
    global score60A
    global score180A

    global bullsB
    global score60B
    global score180B

    global countA180

    p1 = Calculation() # object creation for Calculation class

    if "player1" in session:
        player1 = session["player1"]

    if "player2" in session:
        player2 = session["player2"]

    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM player where id=%s", (player1,))
    nameA = cur.fetchone()
    cur.execute("SELECT score FROM score WHERE id = %s", (player1,))
    scoreA = cur.fetchone()

    # for fetching all the infos from playerA
    cur.execute("SELECT * FROM scorecard where id=%s", (player1,))
    infoA = cur.fetchone()

    # for fetching all the infos from playerB
    cur.execute("SELECT * FROM scorecard where id=%s", (player2,))
    infoB = cur.fetchone()


    if request.method == 'POST':
        score1 = request.form.get("sc1")

        # for maintaining the sequence who will do his first 3 turns
        if turnA < 0:
            turnA = int(request.form.get("turnA"))  # or we can write here direct 3 instead of this request form
            boolB = False

        # for calculating score of bulls, 60 and 180 of playerA
        if int(score1) == 50:
            bullsA += 1

        if int(score1) == 60:
            score60A += 1
            countA180 += 1

        if countA180 == 3:
            score180A += 1

        # for calculation
        result, boolType = p1.playerA(int(scoreA[0]), int(score1))

        # for maintaining the sequence who will do his first 3 turns
        if turnA > 0 and boolType:
            turnA -= 1
            boolB = False

        if turnA == 0 and boolType:
            boolA = False
            boolB = True
            turnA = -1
            countA180 = 0

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

            winRateA = round(((int(infoA[2]) + 1 ) / (int(infoA[1]) + 1 )) * 100, 2)
            winRateB = round((int(infoB[2]) / (int(infoB[1]) + 1 )) * 100, 2)

            # for updating infos for winning in scorecard of playerA
            cur.execute(
                "UPDATE scorecard SET played = %s, win = %s, winRate = %s, bulls = %s, score60 = %s, score180 = %s WHERE id = %s",
                (int(infoA[1]) + 1, int(infoA[2]) + 1, winRateA, int(infoA[5]) + bullsA, int(infoA[6]) + score60A,
                 int(infoA[7]) + score180A, player1))
            mysql.connection.commit()
            # for updating infos for losing in scorecard of playerB
            cur.execute(
                "UPDATE scorecard SET played = %s, loss = %s, winRate = %s, bulls = %s, score60 = %s, score180 = %s WHERE id = %s",
                (int(infoB[1]) + 1, int(infoB[3]) + 1, winRateB, int(infoB[5]) + bullsB, int(infoB[6]) + score60B,
                 int(infoB[7]) + score180B, player2))
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

    global bullsA
    global score60A
    global score180A

    global bullsB
    global score60B
    global score180B

    global countB180

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

    # for fetching all the infos from playerA
    cur.execute("SELECT * FROM scorecard where id=%s", (player1,))
    infoA = cur.fetchone()

    # for fetching all the infos from playerB
    cur.execute("SELECT * FROM scorecard where id=%s", (player2,))
    infoB = cur.fetchone()

    if request.method == 'POST':
        score2 = request.form.get("sc2")

        # for maintaining the sequence who will do his first 3 turns
        if turnB < 0:
            turnB = int(request.form.get("turnB"))  # or we can write here direct 3 instead of this request form
            boolA = False

        # for calculating scores of bulls. 60 and 180 of playerB
        if int(score2) == 50:
            bullsB += 1

        if int(score2) == 60:
            score60B += 1
            countB180 += 1

        if countB180 == 3:
            score180B += 1


        result, boolType = p2.playerB(int(scoreB[0]), int(score2))

        # for maintaining the sequence who will do his first 3 turns
        if turnB > 0 and boolType:
            turnB -= 1
            boolA = False

        if turnB == 0 and boolType:
            boolB = False
            boolA = True
            turnB = -1
            countB180 = 0

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

            winRateA = round((int(infoA[2]) / (int(infoA[1]) + 1)) * 100, 2)
            winRateB = round(((int(infoB[2]) + 1) / (int(infoB[1]) + 1)) * 100, 2)

            # for updating infos for winning in scorecard of playerA
            cur.execute(
                "UPDATE scorecard SET played = %s, win = %s, winRate = %s, bulls = %s, score60 = %s, score180 = %s WHERE id = %s",
                (int(infoB[1]) + 1, int(infoB[2]) + 1, winRateB, int(infoB[5]) + bullsB, int(infoB[6]) + score60B,
                 int(infoB[7]) + score180B, player2))
            mysql.connection.commit()
            # for updating infos for losing in scorecard of playerA
            cur.execute(
                "UPDATE scorecard SET played = %s, loss = %s, winRate = %s, bulls = %s, score60 = %s, score180 = %s WHERE id = %s",
                (int(infoA[1]) + 1, int(infoA[3]) + 1, winRateA, int(infoA[5]) + bullsA, int(infoA[6]) + score60A,
                 int(infoA[7]) + score180A, player1))
            mysql.connection.commit()

            flash("Congratulations {0}!!!   You win!!!".format(nameB[0]))
            cur.close()
            return redirect(url_for("info"))

        cur.close()
        return redirect(url_for("score"))

    cur.close()
    return redirect(url_for("score"))


@app.route('/scorecard')
def scorecard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM displayscore order by win DESC, winRate DESC, name ASC")
    infos = cur.fetchall()
    cur.close()
    return render_template("scorecard.html", infos=infos, showDel=True)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    nameList = []
    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM player") # this querry for autocomplete suggestion box
    nameData = cur.fetchall()

    # for converting tuples in list
    for name in nameData:
        nameList.append(name[0])

    if request.method == "POST":
        name = request.form.get("nm")
        if name in nameList:
            cur.execute("DELETE FROM player WHERE name = %s", (name,))
            mysql.connection.commit()
            cur.close()
            flash("The User Name is successfully deleted", "success")
            return redirect(url_for("scorecard"))
        else:
            flash("The User Name does not exist", "danger")
            return redirect(url_for("scorecard"))

    cur.close()
    return render_template("scorecard.html", condition=True, nameData=nameData)


if __name__ == '__main__':
    app.run()
