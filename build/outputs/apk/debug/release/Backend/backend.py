from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
import requests
from markupsafe import escape
import random
import string
from flask_socketio import SocketIO, send
import os
import asyncio
from threading import Thread
from datetime import timedelta
import random
import logging
import string
import httpx
import cv2
from flask_socketio import SocketIO
from flask import Flask, render_template, redirect, url_for, request, make_response, Response
from flask import Flask, Blueprint, request
from flask import Flask, request, jsonify
from flask import Flask, render_template, redirect, url_for, request
from flask import Flask, send_file
from flask import Flask, request, jsonify
from flask import Flask
from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_cors import CORS
from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import brotli
from markupsafe import escape
from uuid import uuid4
import aiohttp
from discord import Game, Status
from contextvars import ContextVar
import secrets
import json
import requests
import json
import secrets
from apscheduler.schedulers.background import BackgroundScheduler
import urllib.parse
from urllib.parse import urlparse, parse_qs
import youtube_dl
from pytube import YouTube
import re
import pafy
import uuid
from glob import glob
import os
from datetime import datetime
import RPi.GPIO as GPIO
import time
import threading
import eventlet
ALLOWED_IP = '' # use another server and put it ip here
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = secrets.token_hex(32) 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60) 
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
USER_DATA_FILE = "users.json"
HCAPTCHA_SECRET_KEY = ''
KEY_LENGTH = 32
TOKEN_LENGTH = 64
api_key = ''
api_secret = ''
api_url = 'https://api.mailjet.com/v3.1/send'
sender_name = 'Dev'
sender_email = 'trash-bin@kitty-forums.lol'
subject = 'Verification Code'
# gayass
Website_url = "kitty-forums.lol"
embed_image = "https://cdn.discordapp.com/attachments/1154960779175534612/1246040333041795153/download.jpg?ex=665af0fd&is=66599f7d&hm=e7c3dad4a2251e2cd48254cde14d40a179091fd1d55c2353663db4af403f2bdc&"
discord_invite_link = "https://discord.gg/dH3QzRabg7"


#@app.before_request
#def limit_remote_addr():
#    if request.remote_addr != ALLOWED_IP:
#        return jsonify({'error': 'Unauthorized access'}), 403

@app.route('/api/v1/usernames', methods=['GET'])
def get_usernames():
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
        user_info = [{'username': username, 'banned': info['banned'], 'verified': info['verified'], 'role': info['role']} for username, info in users.items()]
        return jsonify(user_info)
    except FileNotFoundError:
        return jsonify({"error": "users.json file not found"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON from users.json"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-formsssss', methods=['GET'])
def get_topicssss():
    forms_dir = './forms'
    topics = {}

    # Iterate over all files in the forms directory
    for filename in os.listdir(forms_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(forms_dir, filename)
            with open(file_path, 'r') as file:
                form_data = json.load(file)
                topic = form_data.get('topic')
                form_ids = form_data.get('form_id')
                form_id = f"https://kitty-forums.lol/api/form/V1/get-form/{form_ids}"
                
                if topic and form_id:
                    if topic not in topics:
                        topics[topic] = []
                    topics[topic].append(form_id)
    
    return jsonify(topics)    

def send_discord_message(message):
    username = "Kitty-forums"
    avatar_url = "https://cdn.discordapp.com/attachments/1154960779175534612/1246040333041795153/download.jpg?ex=665af0fd&is=66599f7d&hm=e7c3dad4a2251e2cd48254cde14d40a179091fd1d55c2353663db4af403f2bdc&"
    webhook_url = "https://discord.com/api/webhooks/1246038807242084434/jQDeKwWAX_1RTelAkeSOfrt_Brci3-2aND1o-u0gC0dbUL3990a21SE-1XLKgY-VddKt"
    
    data = {
        "username": username,
        "avatar_url": avatar_url,
        "embeds": [
            {
                "title": "New Message",
                "description": message,
                "color": 7506394  # Decimal color value for the embed
            }
        ]
    }
    
    response = requests.post(webhook_url, json=data)
    
    if response.status_code == 204:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")

def verify_password(hashed_password, password_to_check):
    return check_password_hash(hashed_password, password_to_check)

@app.route('/search-username-by-token', methods=['POST'])
def search_username_by_token():
    data = request.json
    token = escape(data.get('token'))
    with open("users.json", 'r') as file:
        user_data = json.load(file)
    
    for username, user_info in user_data.items():
        if user_info.get("token") == token:
            return jsonify({'username': username})
    return jsonify({'message': 'Token not found'}), 404

@app.route('/update-token', methods=['POST'])
def updatetoken():
    data = request.json
    username = escape(data.get('username'))
    new_token = escape(data.get('new_token'))
    with open("users.json", 'r+') as file:
        data = json.load(file)
        if username in data:
            data[username]['token'] = new_token
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

@app.route('/search-by-username', methods=['POST'])
def search_by_username():
    data = request.get_json()
    username = escape(data.get('username'))
    
    if not username:
        return jsonify({'message': 'Username not provided'}), 400

    try:
        with open("users.json", 'r') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        return jsonify({'message': 'User data file not found'}), 500
    except json.JSONDecodeError:
        return jsonify({'message': 'Error decoding user data file'}), 500

    info = user_data.get(username, None)
    
    if info:
        return jsonify(info)
    else:
        return jsonify({'message': 'User not found'}), 404


def update_token(username, new_token):
    with open("users.json", 'r+') as file:
        data = json.load(file)
        if username in data:
            data[username]['token'] = new_token
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

def send_discord_message(message):
    username = "Kitty-forums"
    avatar_url = "https://cdn.discordapp.com/attachments/1154960779175534612/1246040333041795153/download.jpg?ex=665af0fd&is=66599f7d&hm=e7c3dad4a2251e2cd48254cde14d40a179091fd1d55c2353663db4af403f2bdc&"
    webhook_url = "https://discord.com/api/webhooks/1246038807242084434/jQDeKwWAX_1RTelAkeSOfrt_Brci3-2aND1o-u0gC0dbUL3990a21SE-1XLKgY-VddKt"
    
    data = {
        "username": username,
        "avatar_url": avatar_url,
        "embeds": [
            {
                "title": "New Message",
                "description": message,
                "color": 7506394  # Decimal color value for the embed
            }
        ]
    }
    
    response = requests.post(webhook_url, json=data)
    
    if response.status_code == 204:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")

def send_admin_logs(message):
    username = "Kitty site logs"
    avatar_url = "https://cdn.discordapp.com/attachments/1154960779175534612/1246040333041795153/download.jpg?ex=665af0fd&is=66599f7d&hm=e7c3dad4a2251e2cd48254cde14d40a179091fd1d55c2353663db4af403f2bdc&"
    webhook_url = "https://discord.com/api/webhooks/1246737696588824597/wF8QTVaIeTbVq4_gDzMUt_igBlRyWlB0pkVZ8Fz_mfDqvUBYa_SVisKUSWl9JRJ3-k-W"
    
    data = {
        "username": username,
        "avatar_url": avatar_url,
        "embeds": [
            {
                "title": "New action",
                "description": message,
                "color": 7506394  # Decimal color value for the embed
            }
        ]
    }
    
    response = requests.post(webhook_url, json=data)
    
    if response.status_code == 204:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")

def search_username(username):
    with open("users.json", 'r') as file:
        data = json.load(file)
    return data.get(username, None)

def search_username_by_token(token):
    with open("users.json", 'r') as file:
        data = json.load(file)
    
    for username, user_info in data.items():
        if user_info.get("token") == token:
            return username
    return None


def load_user_data():
    with open(USER_DATA_FILE, 'r') as file:
        return json.load(file)

def search_usernames(username, field):
    user_data = search_username(username)
    if user_data:
        return user_data.get(field, None)
    return None

def generate_verification_code():
    code_length = 150
    characters = string.ascii_lowercase + string.digits
    verification_code = ''.join(random.choice(characters) for _ in range(code_length))
    return verification_code

def verify_hcaptcha(token):
    data = {
        'secret': HCAPTCHA_SECRET_KEY,
        'response': token
    }
    response = requests.post('https://hcaptcha.com/siteverify', data=data)
    result = response.json()
    return result.get('success', False)

def create_email_payload(code, recipient_email, username):
    text_message = 'Null'
    
    html_message = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Verification</title>
        <style>
            body {{
                font-family: 'Courier New', Courier, monospace;
                background-color: #1a1a1a;
                color: #e0e0e0;
                margin: 0;
                padding: 0;
            }}
            .navbar {{
                display: flex;
                justify-content: flex-end;
                background-color: #444444;
                padding: 10px;
            }}
            .navbar button {{
                background-color: #666666;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                margin: 0 5px;
                cursor: pointer;
                border-radius: 5px;
                font-family: inherit;
            }}
            .navbar button:hover {{
                background-color: #888888;
            }}
            .container {{
                width: 80%;
                max-width: 800px;
                margin: 40px auto;
                background: #2e2e2e;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
            }}
            .forum-post {{
                border-bottom: 1px solid #999999;
                padding: 10px 0;
                position: relative;
            }}
            .forum-post h2 {{
                margin: 0;
                color: #00ff00;
            }}
            .forum-post p {{
                margin: 5px 0;
            }}
            .delete-btn, .edit-btn {{
                color: #ffffff;
                border: none;
                padding: 5px 10px;
                cursor: pointer;
                border-radius: 5px;
                position: absolute;
                right: 10px;
                top: 10px;
                font-family: inherit;
            }}
            .delete-btn {{
                background-color: #ff0000;
            }}
            .delete-btn:hover {{
                background-color: #ff5555;
            }}
            .edit-btn {{
                background-color: #666666;
                right: 100px;
            }}
            .edit-btn:hover {{
                background-color: #888888;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hello {username}!</h1>
            <p>Welcome to kitty-forums.lol</p>
            <p>Click the button below to verify your account:</p>
            <a href="https://{Website_url}/verify-email?code={code}&username={username}" style="display: inline-block; background-color: #666666; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 10px;">Verify Account</a>
            <p>If you have trouble clicking the button, you can also copy and paste the following link into your browser:</p>
            <p>https://{Website_url}/verify-email?code={code}&username={username}</p>
            <br>
            <p>Discord server {discord_invite_link}<p>
        </div>
    </body>
    </html>
    '''

    payload = {
        'Messages': [
            {
                'From': {
                    'Email': sender_email,
                    'Name': sender_name
                },
                'To': [
                    {
                        'Email': recipient_email
                    }
                ],
                'Subject': subject,
                'TextPart': text_message,
                'HTMLPart': html_message
            }
        ]
    }
    print(payload)
    return payload

def send_verification_email(email, username):
    try:
        verification_code = generate_verification_code()
        recipient_email = email
        payload = create_email_payload(verification_code, recipient_email, username)
        user_data = search_username(username)
        if user_data is None:
            return False
        
        with open('pending.json', 'r') as f:
            pending_users = json.load(f)
            if username in pending_users:
                return False
            
        pending_users[username] = {
            'username': username,
            'verification_code': verification_code,
        }

        with open('pending.json', 'w') as f:
            json.dump(pending_users, f, indent=4)
        response = requests.post(api_url, json=payload, auth=(api_key, api_secret))

        if response.status_code == 200:
            print(f'Email sent successfully to {username}')
        else:
            print(f'Failed to send email. Status code: {response.status_code}')
            print(response.json())

    except Exception as e:
        print(f"An error occurred: {str(e)}")

@app.route('/verify-email', methods=['GET'])
def verify_email():
    try:
        code = request.args.get('code')
        username = request.args.get('username')
        
        with open('pending.json', 'r') as f:
            pending_data = json.load(f)
            
        with open('users.json', 'r') as user_file:
            user_data = json.load(user_file)            
        
        if username in pending_data:
            pending_user = pending_data[username]
            stored_code = pending_user.get('verification_code')
            
            if code == stored_code:
                del pending_data[username]
                with open('pending.json', 'w') as f: 
                    json.dump(pending_data, f, indent=4)
                    
                user_data[username]['verified'] = True
                with open('users.json', 'w') as user_file:
                    json.dump(user_data, user_file, indent=4)
                return redirect('https://kitty-forums.lol/sign-in')
            else:
                return "Incorrect Code"
        else:
            return "User not awaiting verification"    
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


@app.route('/api/V1/login', methods=['POST'])
def loginuser():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    h_captcha_token = data.get('h_captcha_token')

    def handle_verification_and_login(username, password, h_captcha_token):
        if h_captcha_token is None or not verify_hcaptcha(h_captcha_token):
            logging.debug('Failed hCaptcha verification')
            return jsonify({'message': 'Failed hCaptcha verification'}), 400
        
        user_data = search_username(username)
        if user_data is None:
            logging.debug('User not found')
            return jsonify({'message': 'User not found'}), 400
        
        user_password = user_data.get('password', '')
        if not verify_password(user_password, password):
            logging.debug('Incorrect Password')
            return jsonify({'message': 'Incorrect Password'}), 400
        
        verified = user_data.get('verified', False)
        role = user_data.get('role', 'User')
        new_token = secrets.token_hex(TOKEN_LENGTH)
        update_token(username, new_token)
        
        return jsonify({
            'username': username,
            'token': new_token,
            'role': role,
            'verified': verified
        })

    verified = search_usernames(username, 'verified')
    if verified:
        return handle_verification_and_login(username, password, h_captcha_token)
    else:
        logging.debug('Account not verified')
        return jsonify({'message': 'Account not verified'}), 403

@app.route('/api/V1/register', methods=['POST'])
def api_register():
    user_data = load_user_data()
    data = request.json
    username = escape(data.get('username'))
    password = escape(data.get('password'))
    email = data.get('email')
    client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)
    h_captcha_token = data.get('h_captcha_token')
    if not verify_hcaptcha(h_captcha_token):
        return jsonify({'message': 'Failed hCaptcha verification'}), 400
    else:
        if len(username) > 16:
            return jsonify({'message': 'Username must be 16 characters or less'}), 400
        elif len(username) < 1:
            return jsonify({'message': 'Username must be at least 1 characters'}), 400
        if len(password) > 16:
            return jsonify({'message': 'Password MUST be between 8-16 characters'}), 496
        elif len(password) < 8:
            return jsonify({'message': 'Password MUST be at least 8 characters long'}), 495
        if h_captcha_token is None:
            return jsonify({'message': 'Missing hCaptcha token'}), 400
        if password is None:
            return jsonify({'message': 'Missing Password'}), 400
        if username is None:
            return jsonify({'message': 'Missing Username'}), 400
        if username in user_data:
            return jsonify({'message': 'Username already exists'}), 400

    hashed_password = generate_password_hash(password)
    hashed_email = generate_password_hash(email) 
    hashed_ip = generate_password_hash(client_ip) 
    verified = False
    token = secrets.token_hex(TOKEN_LENGTH)
    key = secrets.token_hex(KEY_LENGTH)
    user_data[username] = {
        'password': hashed_password,
        'email': hashed_email,
        'verified': verified,
        'ip': hashed_ip,
        'token': f"{token}",
        'muted': False,
        'banned': False,
        'coins': "",
        'key': f"{key}",
        'posts': 0,
        'invites': 0,
        'userid': 0,
        'likes': 0,
        'followers': 0,
        'role': "user",
        'badge-1': "",
        'badge-2': "",
        'badge-3': "",
        'badge-4': "",
        'blank17': "",
        'blank18': "",
        'blank19': "",
        'blank20': "",
        'blank21': "",
        'blank22': "",
        'blank23': "",
    }
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(user_data, file, indent=2)
    response = jsonify({'message': 'Registration successful. Please login'})
    send_verification_email(email, username)
    response.status_code = 201
    return response


@app.route('/api/form/V1/handle-form', methods=['POST'])
def handle_form():
    data = request.json
    topic = data.get('topic', '')
    message = data.get('message', '')
    title = data.get('title', '')
    token = data.get('token', '')
    username = data.get('username', '')
    form_id = data.get('form_id', '')

    verified = search_usernames(username, 'verified')
    usertoke = search_usernames(username, "token")

    if username:
        if token == usertoke:
            if verified:
                if 'img src=' in message or 'xss' in message or 'video src=x' in message:
                    return jsonify({'error': 'Nice Try buddy XD'}), 400
                if '@here' in message or '@everyone' in message:
                    return jsonify({'error': 'The message cannot contain @here or @everyone.'}), 400
                filename = f'./forms/{form_id}.json'
                if os.path.exists(filename):
                    return jsonify({'error': 'A form with this title already exists. Please choose a different title.'}), 400
                if not username or not message or not title:
                    return jsonify({'error': 'Username, message, and title are required'}), 400
                if len(message) < 1 or len(message) > 1000:
                    return jsonify({'error': 'Post must be between 1 and 1000 characters!'}), 400

                current_date = datetime.now().strftime('%d/%m/%Y')
                newtitle = f"[{topic}] {title}"
                json_data = {
                    "title": newtitle,
                    "author": username,
                    "message": message,
                    "created_at": current_date,
                    "topic": topic,
                    "likes": 0,
                    "comments": [],
                    "viewers": [],
                    "views": 0,
                    "dislikes": 0,
                    "shares": 0,
                    "form_id": form_id
                }

                discord_message = f"New post by {username}\n\nTitle: {newtitle}\n\nPost: {message}\n\nCreated On {current_date}\nPost Url: https://kitty-forums.lol/p/{form_id}"
                send_discord_message(discord_message)
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, 'w') as file:
                    json.dump(json_data, file, indent=4)
                return jsonify({'message': f'Form posted to https://kitty-forums.lol/p/{form_id}'}), 200
            else:
                return jsonify({'message': 'You need to verify your email to continue'}), 403
        else:
            return jsonify({'message': 'Incorrect Token'}), 403


@app.route('/api/topic/V1/get-topics', methods=['GET'])
def get_topics():
    with open('topics.json') as f:
        topics = json.load(f)
    topic_values = list(topics.values())
    return jsonify(topic_values)

@app.route('/api/v1/get-my-posts/', methods=['GET'])
def get_my_posts():
    username = escape(request.args.get('username', ''))
    form_ids = []
    for filename in os.listdir('./forms/'):
        if filename.endswith('.json'):
            with open(os.path.join('./forms/', filename), 'r') as file:
                data = json.load(file)
                if 'author' in data and data['author'] == username:
                    form_ids.append(data.get('form_id'))

    return jsonify(form_ids=form_ids)

@app.route('/api/form/V1/add-view', methods=['POST'])
def add_view():
    data = request.json
    title = escape(data.get('title', '').replace(' ', '-'))
    token = escape(data.get('token', ''))
    user = search_username_by_token(token)
    verified = search_usernames(user, 'verified')
    usertoke = search_usernames(user, "token")
    if user:
        if token == usertoke:
            if verified:
                forms_directory = './forms'
                form_found = False
                filename = None

                files = os.listdir(forms_directory)
                for file in files:
                    if file.endswith('.json'):
                        with open(os.path.join(forms_directory, file), 'r') as f:
                            json_data = json.load(f)
                            if json_data.get('title', '').replace(' ', '-') == title:
                                filename = os.path.join(forms_directory, file)
                                form_found = True
                                break

                if not form_found:
                    return jsonify({'error': f'Form with title {title} does not exist'}), 404
                if 'viewers' not in json_data:
                    json_data['viewers'] = []
                if 'views' not in json_data:
                    json_data['views'] = 0

                views = json_data['viewers']
                for view in views:
                    if view['viewer'] == user:
                        return jsonify({'message': ':)'}), 403

                current_date = datetime.now().strftime('%d/%m/%Y')

                new_view = {
                    "viewer": user,
                    "viewed_at": current_date
                }
                json_data['viewers'].append(new_view)
                json_data['views'] += 1

                with open(filename, 'w') as file:
                    json.dump(json_data, file, indent=4)

                return jsonify({'message': ':)'}), 200
            else:
                return jsonify({'message': 'You need to verify your email to continue'}), 403
        else:
            return jsonify({'message': 'Incorrect Token'}), 403

@app.route('/api/form/V1/add-comment', methods=['POST'])
def add_comment():
    data = request.json
    title = escape(data.get('title', '').replace(' ', '-'))
    comment_text = escape(data.get('comment', ''))
    token = escape(data.get('token', ''))
    commenter = search_username_by_token(token)
    verified = search_usernames(commenter, 'verified')
    usertoke = search_usernames(commenter, "token")
    if commenter:
        if token == usertoke:
            if verified == True:
                if len(comment_text) < 1 or len(comment_text) > 1000:
                    return jsonify({'message': 'Comment must be between 1 and 1000 characters!'}), 400
                if not title or not comment_text or not commenter:
                    return jsonify({'error': 'Title, comment, and commenter are required'}), 400

                forms_directory = './forms'
                form_found = False
                filename = None

                files = os.listdir(forms_directory)
                for file in files:
                    if file.endswith('.json'):
                        with open(os.path.join(forms_directory, file), 'r') as f:
                            json_data = json.load(f)
                            if json_data.get('title', '').replace(' ', '-') == title:
                                filename = os.path.join(forms_directory, file)
                                form_found = True
                                break

                if not form_found:
                    return jsonify({'error': f'Form with title {title} does not exist'}), 404

                current_date = datetime.now().strftime('%d/%m/%Y')

                new_comment = {
                    "commenter": commenter,
                    "comment": comment_text,
                    "commented_at": current_date
                }
                json_data['comments'].append(new_comment)

                with open(filename, 'w') as file:
                    json.dump(json_data, file, indent=4)

                return jsonify({'message': 'Comment added successfully'}), 200
            else:
                return jsonify({'message': 'You need to verify your email to continue'}), 403
        else:
            return jsonify({'message': 'Incorrect Token'}), 403

@app.route('/api/form/V1/delete-post', methods=['POST'])
def delete_post():
    data = request.json
    title = escape(data.get('title', '').replace(' ', '-'))
    token = escape(data.get('token', ''))
    username = search_username_by_token(token)
    badge = search_usernames(username, 'role')
    if username:
        if badge == "Owner" or badge ==  "Admin":
            verified = search_usernames(username, 'verified')
            usertoke = search_usernames(username, "token")

            if token == usertoke:
                if verified:
                    forms_directory = './forms'
                    files = os.listdir(forms_directory)
                    form_found = False

                    for file in files:
                        if file.endswith('.json'):
                            with open(os.path.join(forms_directory, file), 'r') as f:
                                data = json.load(f)
                                if data.get('title', '').replace(' ', '-') == title:
                                    os.remove(os.path.join(forms_directory, file))
                                    form_found = True
                                    break
                                
                    if form_found:
                        message = f"{username} Deleted post :{title}"
                        send_admin_logs(message)
                        return jsonify({'message': 'Post deleted successfully'}), 200
                    else:
                        return jsonify({'error': 'Form with this title does not exist'}), 404
                else:
                    return jsonify({'message': 'You need to verify your email to continue'}), 403
            else:
                return jsonify({'message': 'Incorrect Token'}), 403
        else:
            return jsonify({'message': 'You do not have the required badge to delete posts'}), 403

@app.route('/api/form/V1/delete-comment', methods=['POST'])
def delete_comment():
    data = request.json
    title = escape(data.get('title', '').replace(' ', '-'))
    comment_index = data.get('comment_index', None)
    username = escape(data.get('username', ''))
    badge = search_usernames(username, 'role')

    if badge == "Owner" or badge == "Admin":
        token = escape(data.get('token', ''))
        verified = search_usernames(username, 'verified')
        usertoke = search_usernames(username, "token")

        if token == usertoke:
            if verified:
                forms_directory = './forms'
                form_found = False
                filename = None

                files = os.listdir(forms_directory)
                for file in files:
                    if file.endswith('.json'):
                        with open(os.path.join(forms_directory, file), 'r') as f:
                            json_data = json.load(f)
                            if json_data.get('title', '').replace(' ', '-') == title:
                                filename = os.path.join(forms_directory, file)
                                form_found = True
                                break

                if not form_found:
                    return jsonify({'error': 'Form with this title does not exist'}), 404

                if comment_index is None or not isinstance(comment_index, int) or comment_index < 0 or comment_index >= len(json_data['comments']):
                    return jsonify({'error': 'Invalid comment index'}), 400

                del json_data['comments'][comment_index]

                with open(filename, 'w') as file:
                    json.dump(json_data, file, indent=4)

                message = f"{username} Deleted a comment from {title}"
                send_admin_logs(message)
                return jsonify({'message': 'Comment deleted successfully'}), 200
            else:
                return jsonify({'message': 'You need to verify your email to continue'}), 403
        else:
            return jsonify({'message': 'Incorrect Token'}), 403
    else:
        return jsonify({'message': 'You do not have the required badge to delete comments'}), 403


@app.route('/api/form/V1/search', methods=['GET'])
def search_forms():
    form = request.args.get('form')
    forms_directory = './forms'
    
    if not form:
        return jsonify({'error': 'Form parameter is required'}), 400

    try:
        files = os.listdir(forms_directory)
        matching_forms = []
        
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(forms_directory, file), 'r') as f:
                    data = json.load(f)
                    if form.lower() in data.get('title', '').lower():
                        matching_forms.append({
                            'filename': file,
                            'title': data.get('title', ''),
                            'url': "https://kitty-forums.lol/" + 'api/form/V1/get-form/' + file.replace('.json', '')
                        })
        
        if not matching_forms:
            return jsonify({'message': 'No forms found matching the query'}), 404
        
        return jsonify({'forms': matching_forms}), 200
    except FileNotFoundError:
        return jsonify({'error': 'under construction'}), 404

@app.route('/api/form/V1/list-forms', methods=['POST'])
def list_forms():
    forms_directory = './forms'
    try:
        files = os.listdir(forms_directory)
        json_files = [file for file in files if file.endswith('.json')]
        urls = ["https://kitty-forums.lol/" + 'api/form/V1/get-form/' + file.replace('.json', '') for file in json_files]
        return jsonify({'forms': urls}), 200
    except FileNotFoundError:
        return jsonify({'forms': 'under construction'}), 404

@app.route('/api/form/V1/get-form/<form_id>', methods=['GET'])
def get_form(form_id):
    form_path = os.path.join('./forms', f"{form_id}.json")
    if os.path.exists(form_path):
        with open(form_path, 'r') as f:
            form_data = json.load(f)
        return jsonify(form_data), 200
    else:
        return jsonify({"error": "Form not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5634)