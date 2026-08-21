from flask import Flask, request, redirect, url_for, render_template
import os
import psycopg2
import app_data

app = Flask(__name__)
DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
cur.close()
conn.close()

@app.route("/")
def hello_world():
    return render_template("homepage.html", activeTopics=app_data.activeTopics)
    
@app.route("/test")
def test():
    return render_template("index.html", app_data=app_data.data, make_req=url_for('test_req'))

@app.route("/make_req", methods=['GET'])
def test_req():
    if (app_data.data):
        # test, just make a div out of the first value
        return f"""
            <form method="POST" action="{url_for('remove_item')}">
                <p>{app_data.data}</p>
                <button type="submit" name="urmom" value="{app_data.data[0]}">{app_data.data[0]}</button>
            </form>

            <a href="{url_for('test')}">to the first page</a>
        """
    else:
        return f"<p>no more data</p>"

@app.route("/remove", methods=['POST'])
def remove_item():
    value = request.form.get("urmom")
    value = int(value)

    if value in app_data.data:
        app_data.data.remove(value)
        print(app_data.data)

    # return f"<p>{value}</p>"
    return redirect(url_for('test_req'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)