import flask
import sqlite3
import os

app = flask.Flask(__name__)

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
            loss_choice TEXT
        )
    ''')

    conn.commit()
    conn.close()


# =========================
# HOME PAGE
# =========================

@app.route('/')
def home():
    return flask.render_template('index.html')


# =========================
# GAIN PAGE
# =========================

@app.route('/gain')
def gain():
    return flask.render_template('gain.html')


# =========================
# LOSS PAGE
# =========================

@app.route('/loss', methods=['POST'])
def loss():

    gain_choice = flask.request.form['gain_choice']

    return flask.render_template(
        'loss.html',
        gain_choice=gain_choice
    )


# =========================
# SUBMIT RESPONSES
# =========================

@app.route('/submit', methods=['POST'])
def submit():

    gain_choice = flask.request.form['gain_choice']
    loss_choice = flask.request.form['loss_choice']

    conn = sqlite3.connect('responses.db')
    cursor = conn.cursor()

    # SAVE RESPONSE
    cursor.execute('''
        INSERT INTO responses (gain_choice, loss_choice)
        VALUES (?, ?)
    ''', (gain_choice, loss_choice))

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

    if gain_choice == 'A' and loss_choice == 'B':

        profile_title = "Classic Loss Aversion"

        profile_description = (
            "You preferred certainty during gains but became risk-seeking "
            "while facing losses. This is one of the strongest indicators "
            "of loss aversion in behavioral economics."
        )

    elif gain_choice == 'A' and loss_choice == 'A':

        profile_title = "Highly Risk Averse"

        profile_description = (
            "You preferred certainty in both scenarios. "
            "This suggests a conservative investment personality."
        )

    elif gain_choice == 'B' and loss_choice == 'B':

        profile_title = "High Risk Seeker"

        profile_description = (
            "You consistently preferred risky outcomes in both situations. "
            "This indicates a higher tolerance for uncertainty and volatility."
        )

    else:

        profile_title = "Balanced Risk Behavior"

        profile_description = (
            "Your choices indicate mixed behavioral tendencies. "
            "You may evaluate opportunities differently depending on context."
        )

    return flask.render_template(
        'result.html',

        gain_choice=gain_choice,
        loss_choice=loss_choice,

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

    return flask.render_template(
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
