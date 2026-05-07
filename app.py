from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# =========================
# DATABASE INITIALIZATION
# =========================

def init_db():

    conn = sqlite3.connect('responses.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            gain_choice TEXT,
            loss_choice TEXT,

            certainty_choice TEXT,
            sunkcost_choice TEXT,
            herd_choice TEXT,
            overconfidence_choice TEXT
        )
    ''')

    conn.commit()
    conn.close()


# =========================
# HOME PAGE
# =========================

@app.route('/')
def home():
    return render_template('index.html')


# =========================
# GAIN PAGE
# =========================

@app.route('/gain')
def gain():
    return render_template('gain.html')


# =========================
# LOSS PAGE
# =========================

@app.route('/loss', methods=['POST'])
def loss():

    gain_choice = request.form['gain_choice']

    return render_template(
        'loss.html',
        gain_choice=gain_choice
    )


# =========================
# CERTAINTY EFFECT PAGE
# =========================

@app.route('/certainty', methods=['POST'])
def certainty():

    gain_choice = request.form['gain_choice']
    loss_choice = request.form['loss_choice']

    return render_template(
        'certainty.html',
        gain_choice=gain_choice,
        loss_choice=loss_choice
    )


# =========================
# SUNK COST PAGE
# =========================

@app.route('/sunkcost', methods=['POST'])
def sunkcost():

    gain_choice = request.form['gain_choice']
    loss_choice = request.form['loss_choice']
    certainty_choice = request.form['certainty_choice']

    return render_template(
        'sunkcost.html',

        gain_choice=gain_choice,
        loss_choice=loss_choice,
        certainty_choice=certainty_choice
    )


# =========================
# HERD MENTALITY PAGE
# =========================

@app.route('/herd', methods=['POST'])
def herd():

    gain_choice = request.form['gain_choice']
    loss_choice = request.form['loss_choice']
    certainty_choice = request.form['certainty_choice']
    sunkcost_choice = request.form['sunkcost_choice']

    return render_template(
        'herd.html',

        gain_choice=gain_choice,
        loss_choice=loss_choice,
        certainty_choice=certainty_choice,
        sunkcost_choice=sunkcost_choice
    )


# =========================
# OVERCONFIDENCE PAGE
# =========================

@app.route('/overconfidence', methods=['POST'])
def overconfidence():

    gain_choice = request.form['gain_choice']
    loss_choice = request.form['loss_choice']
    certainty_choice = request.form['certainty_choice']
    sunkcost_choice = request.form['sunkcost_choice']
    herd_choice = request.form['herd_choice']

    return render_template(
        'overconfidence.html',

        gain_choice=gain_choice,
        loss_choice=loss_choice,
        certainty_choice=certainty_choice,
        sunkcost_choice=sunkcost_choice,
        herd_choice=herd_choice
    )


# =========================
# SUBMIT RESPONSES
# =========================

@app.route('/submit', methods=['POST'])
def submit():

    gain_choice = request.form['gain_choice']
    loss_choice = request.form['loss_choice']

    certainty_choice = request.form['certainty_choice']
    sunkcost_choice = request.form['sunkcost_choice']
    herd_choice = request.form['herd_choice']
    overconfidence_choice = request.form['overconfidence_choice']

    conn = sqlite3.connect('responses.db')
    cursor = conn.cursor()

    # =========================
    # SAVE RESPONSE
    # =========================

    cursor.execute('''
        INSERT INTO responses (

            gain_choice,
            loss_choice,

            certainty_choice,
            sunkcost_choice,
            herd_choice,
            overconfidence_choice

        )

        VALUES (?, ?, ?, ?, ?, ?)

    ''', (

        gain_choice,
        loss_choice,

        certainty_choice,
        sunkcost_choice,
        herd_choice,
        overconfidence_choice

    ))

    conn.commit()

    # =========================
    # LIVE COUNTS
    # =========================

    gain_a = cursor.execute(
        "SELECT COUNT(*) FROM responses WHERE gain_choice='A'"
    ).fetchone()[0]

    gain_b = cursor.execute(
        "SELECT COUNT(*) FROM responses WHERE gain_choice='B'"
    ).fetchone()[0]

    loss_a = cursor.execute(
        "SELECT COUNT(*) FROM responses WHERE loss_choice='A'"
    ).fetchone()[0]

    loss_b = cursor.execute(
        "SELECT COUNT(*) FROM responses WHERE loss_choice='B'"
    ).fetchone()[0]

    total = cursor.execute(
        "SELECT COUNT(*) FROM responses"
    ).fetchone()[0]

    conn.close()

    # =========================
    # PROFILE LOGIC
    # =========================

    score = 0

    if gain_choice == 'B':
        score += 1

    if loss_choice == 'B':
        score += 1

    if certainty_choice == 'B':
        score += 1

    if sunkcost_choice == 'B':
        score += 1

    if herd_choice == 'B':
        score += 1

    if overconfidence_choice == 'B':
        score += 1

    # =========================
    # PROFILE GENERATION
    # =========================

    if score <= 1:

        profile_title = "Conservative Investor"

        profile_description = (
            "You display cautious financial behavior and prefer stability "
            "over uncertainty. You are less likely to make impulsive "
            "investment decisions."
        )

    elif score <= 3:

        profile_title = "Balanced Decision Maker"

        profile_description = (
            "You demonstrate moderate risk-taking tendencies while still "
            "maintaining rational investment discipline."
        )

    elif score <= 5:

        profile_title = "Aggressive Risk Taker"

        profile_description = (
            "You are highly comfortable with uncertainty and volatility. "
            "You may pursue high-reward opportunities aggressively."
        )

    else:

        profile_title = "Behaviorally Driven Trader"

        profile_description = (
            "Your decisions show strong behavioral influences such as "
            "FOMO, overconfidence, and emotional investing."
        )

    # =========================
    # RESULT PAGE
    # =========================

    return render_template(
        'result.html',

        gain_choice=gain_choice,
        loss_choice=loss_choice,

        certainty_choice=certainty_choice,
        sunkcost_choice=sunkcost_choice,
        herd_choice=herd_choice,
        overconfidence_choice=overconfidence_choice,

        profile_title=profile_title,
        profile_description=profile_description,

        gain_a=gain_a,
        gain_b=gain_b,

        loss_a=loss_a,
        loss_b=loss_b,

        total=total
    )


# =========================
# SECRET FACILITATOR DASHBOARD
# =========================

@app.route('/cicm-facilitator-dashboard')
def dashboard():

    conn = sqlite3.connect('responses.db')
    cursor = conn.cursor()

    gain_a = cursor.execute(
        "SELECT COUNT(*) FROM responses WHERE gain_choice='A'"
    ).fetchone()[0]

    gain_b = cursor.execute(
        "SELECT COUNT(*) FROM responses WHERE gain_choice='B'"
    ).fetchone()[0]

    loss_a = cursor.execute(
        "SELECT COUNT(*) FROM responses WHERE loss_choice='A'"
    ).fetchone()[0]

    loss_b = cursor.execute(
        "SELECT COUNT(*) FROM responses WHERE loss_choice='B'"
    ).fetchone()[0]

    total = cursor.execute(
        "SELECT COUNT(*) FROM responses"
    ).fetchone()[0]

    conn.close()

    gain_total = gain_a + gain_b
    loss_total = loss_a + loss_b

    gain_a_pct = round((gain_a / gain_total) * 100, 1) if gain_total else 0
    gain_b_pct = round((gain_b / gain_total) * 100, 1) if gain_total else 0

    loss_a_pct = round((loss_a / loss_total) * 100, 1) if loss_total else 0
    loss_b_pct = round((loss_b / loss_total) * 100, 1) if loss_total else 0

    return render_template(
        'dashboard.html',

        gain_a=gain_a,
        gain_b=gain_b,

        loss_a=loss_a,
        loss_b=loss_b,

        total=total,

        gain_a_pct=gain_a_pct,
        gain_b_pct=gain_b_pct,

        loss_a_pct=loss_a_pct,
        loss_b_pct=loss_b_pct
    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == '__main__':

    init_db()

    port = int(os.environ.get('PORT', 5000))

    app.run(
        host='0.0.0.0',
        port=port
    )