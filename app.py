from flask import Flask, render_template, request, redirect, url_for,session
from main_real import agent

app = Flask(__name__)

@app.route('/')
def home():
    if 'messages' not in session:
        session['messages'] = []
        
    print('home', session)
    return render_template('chat.html', messages=session['messages'])

@app.route('/send', methods = ['POST'])
def send():
    user_message = request.form['message']
    user_lat = request.form.get('latitude')
    user_lon = request.form.get('longitude')
    print(user_lat, user_lon)
    
    if user_lat and user_lon:
        session['user_location'] = {'lat': user_lat, 'lon': user_lon}
    
    response = agent.invoke({"messages": [{'role': 'user','content': user_message}]},
                            {'configurable': {'thread_id':'1'}})
    
    session['messages'].append({'type':'human', 'content': user_message})
    session['messages'].append({'type':'ai', 'content': response['messages'][-1].content})
    session.modified = True
    print(session)

    return redirect(url_for('home'))

app.run(debug=True)