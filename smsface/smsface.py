from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import datetime
import requests, json, flask, sys, os

app = Flask(__name__)
app.secret_key = 'testing this out'


def api_request(payload):

    baseurl = str(app.config.get('baseurl'))
    url = (baseurl + '/api')
    headers = {'content-type': 'application/json', 'token':app.config.get('token')}
    payload = payload
    response = requests.post(url, data=payload, headers=headers)
    return json.loads(response.text)


def get_blog(id):
    return api_request(('blog -get=' + str(id)))


def get_personal(id):
    return api_request(('personal -get=' + str(id)))


def get_random(id):
    return api_request(('random -get=' + str(id)))


def get_reminders():
    return api_request('reminders -get=all')


@app.route('/sms', methods=['POST'])
def sms_handler():

    baseurl = str(app.config.get('baseurl'))
    url = (baseurl + '/sms')
    response = requests.post(url, request)

    resp = MessagingResponse()
    num = str(request.form['From'])
    resp.message(response)
    return str(resp)


@app.route('/login', methods=['post', 'get'])
def login():

    if request.method == 'POST':

        password = str(request.form.get('password'))

        if password == str(app.config.get('password')):
            session['owner'] = 'valid'
            return redirect(url_for('home'))
        else:
            return render_template('login.html', failed=True)
    else:
        return render_template('login.html')


@app.route('/logout', methods=['get'])
def logout():
    if 'owner' in session:
        session.pop('owner', None)

    return redirect(url_for('home'))


@app.route('/', methods=['get'])
def home():

    admin = False

    personal = "not_admin"
    reminders = "not_admin"
    random = "not_admin"

    blog = get_blog('all')

    return render_template('home.html', admin=admin, blog=blog, random=random,
                           personal=personal, reminders=reminders)

@app.route('/blog', methods=['get'])
def blog():

    blog = get_blog('all')

    return render_template('blog.html', blog=blog)

@app.route('/blog/<category>', methods=['get'])
def blog_category(category):

    blog = get_blog('all')

    return render_template('blog.html', blog=blog, category=category)

@app.route('/blog/<id>', methods=['get'])
def blog_id(id):

    blog = get_blog(id)

    return render_template('blog.html', blog=blog, id=id)

@app.route('/personal', methods=['get'])
def personal():

    if 'owner' not in session:
        return redirect(url_for('login'))

    personal = get_personal('all')

    return render_template('personal.html', personal=personal)

@app.route('/personal/<category>', methods=['get'])
def personal_category(category):

    if 'owner' not in session:
        return redirect(url_for('login'))

    personal = get_personal('all')

    return render_template('personal.html', personal=personal, category=category)


@app.route('/personal/<id>', methods=['get'])
def personal_id(id):

    if 'owner' not in session:
        return redirect(url_for('login'))

    personal = get_personal(id)

    return render_template('personal.html', personal=personal, id=id)

@app.route('/random', methods=['get'])
def random():

    if 'owner' not in session:
        return redirect(url_for('login'))

    random = get_random('all')

    return render_template('random.html', random=random)

@app.route('/random/<category>', methods=['get'])
def random_category(category):

    if 'owner' not in session:
        return redirect(url_for('login'))

    random = get_random('all')

    return render_template('random.html', random=random, category=category)

@app.route('/random/<id>', methods=['get'])
def random_id(id):

    if 'owner' not in session:
        return redirect(url_for('login'))

    random = get_random(id)

    return render_template('random.html', random=random, id=id)

@app.route('/reminders', methods=['get'])
def reminders():

    if 'owner' not in session:
        return redirect(url_for('login'))

    reminders = get_reminders()

    return render_template('reminders.html', reminders=reminders)


if __name__=='__main__':
    app.config['baseurl'] = '?'
    app.config['token'] = '?'
    app.config['password'] = '?'
    app.run()
