import json
import os
from xml.dom.minidom import Document
from flask import Flask, flash, render_template, request, redirect, url_for, session,jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for session security

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoid warnings

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# User model for storing sign-up details
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)

# Create the database within the app context
with app.app_context():
    print("Creating the database...")
    db.create_all()  # Creates users.db and the User table
    print("Database created successfully!")



@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rapha Vee</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-image: url('/static/bg.jpg'); 
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                color: #002366;
            }

            .navbar {
                width: 100%;
                position: fixed;
                top: 0;
                left: 0;
                padding: 15px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 1.2em;
                font-weight: bold;
                background: black;
                color: white;
                z-index: 1000;
                box-sizing: border-box;
            }

            .system-name {
                font-size: 1.6em;
                font-weight: bold;
                margin-left: 20px;
            }

            .nav-links {
                display: flex;
                gap: 15px;
                padding-right: 30px;
            }

            .nav-links a {
                text-decoration: none;
                color: white;
                font-weight: bold;
                font-size: 1.1em;
                padding: 10px 12px;
                transition: color 0.3s ease-in-out;
            }

            .nav-links a:hover {
                color: #007BFF;
            }

            .content {
                max-width: 800px;
                margin: 120px auto 0;
                text-align: center;
                padding: 50px 20px;
            }

            .content h1 {
                font-size: 3.5em;
                font-weight: bold;
                margin-bottom: 10px;
            }

            .content p {
                font-size: 1.4em;
                margin-bottom: 30px;
            }

            .button-container {
                display: flex;
                justify-content: center;
            }

            .button-container button {
                background-color: transparent; /* Colorless by default */
                color: #007BFF; /* Blue text */
                padding: 10px 45px;
                border: 2px solid #007BFF; /* Blue border */
                border-radius: 5px;
                font-size: 18px;
                letter-spacing: 1px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease-in-out;
            }

            .button-container button:hover {
                background-color: #007BFF;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="navbar">
            <span class="system-name">Rapha Vee</span>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/about">About</a>
                <a href="/bmi">BMI</a>
                <a href="symptom-diagnosis">Symptom Diagnosis</a>
                <a href="#">Contact</a>
            </div>
        </div>

        <div id="home" class="content">
            <h1>Welcome to Rapha Vee</h1>
            <p>Your Personal Health & Fitness Companion</p>
            <div class="button-container">
                <button onclick="window.location.href='/about'">Get Started</button>  
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/about')
def about():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>About Rapha Vee</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-image: url('/static/fitness.jpg'); 
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                height: 100vh;
                color: black;
            }

            .navbar {
                width: 100%;
                position: fixed;
                top: 0;
                left: 0;
                padding: 15px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 1.2em;
                font-weight: bold;
                background: black;
                color: white;
                z-index: 1000;
                box-sizing: border-box;
            }

            .system-name {
                font-size: 1.6em;
                font-weight: bold;
                margin-left: 20px;
            }

            .nav-links {
                display: flex;
                gap: 15px;
                padding-right: 30px;
            }

            .nav-links a {
                text-decoration: none;
                color: white;
                font-weight: bold;
                font-size: 1.1em;
                padding: 10px 12px;
                transition: color 0.3s ease-in-out;
            }

            .nav-links a:hover {
                color: #007BFF;
            }
            
            #about {
                padding: 120px 50px;
                text-align: left;
                background: white;
                color: black;
                display: flex;
                align-items: flex-start; 
                justify-content: center;
                gap: 50px;
            }

            /* Left Side: Video Container */
            .video-container {
                position: relative;
                width: 650px; 
                height: 500px; 
                border-radius: 10px;
                overflow: hidden;
                background: url('/static/video-placeholder.jpg') center/cover no-repeat;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .video-placeholder{
                filter: contrast(1.1) brightness(1.1);
            }

            video {
                width: 100%;
                height: 100%;
                border-radius: 10px;
                display: none;
            }

           .play-button {
                position: absolute;
                background: rgba(0, 123, 255, 0.9);
                color: white;
                border: none;
                padding: 25px; /* Increase size slightly */
                font-size: 28px; /* Make text larger */
                font-weight: bold;
                cursor: pointer;
                border-radius: 50%;
                transition: all 0.3s ease-in-out;
                animation: blink 1.2s infinite alternate ease-in-out; /* Faster & stronger blink */
            }

            @keyframes blink {
                0% { 
                    box-shadow: 0 0 10px rgba(0, 123, 255, 0.9), 
                                0 0 20px rgba(0, 123, 255, 0.7); 
                    transform: scale(1); /* Normal size */
                }
                50% { 
                    box-shadow: 0 0 30px rgba(0, 123, 255, 1), 
                                0 0 50px rgba(0, 123, 255, 0.8); 
                    transform: scale(1.1); /* Slightly larger */
                }
                100% { 
                    box-shadow: 0 0 10px rgba(0, 123, 255, 0.9), 
                                0 0 20px rgba(0, 123, 255, 0.7); 
                    transform: scale(1); /* Back to normal */
                }
            }


            .play-button:hover {
                background: rgba(0, 123, 255, 1);
            }

            /* Right Side: Text and Icons */
            .about-text {
                max-width: 50%;
            }

            .about-text h2 {
                font-size: 2.5em;
                font-weight: bold;
                margin-bottom: 15px;
            }

            .about-text p {
                font-size: 1.2em;
                margin-bottom: 20px;
                line-height: 1.5;
            }

            .about-icons {
                display: flex;
                flex-direction: column;
                gap: 20px;
                margin-top: 20px;
            }

            .icon-item {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .icon-item img {
                width: 40px;
                height: 40px;
                filter: invert(29%) sepia(91%) saturate(1273%) hue-rotate(195deg) brightness(92%) contrast(100%);
            }
        </style>
    </head>
    <body>
        <div class="navbar">
            <span class="system-name">Rapha Vee</span>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/bmi">BMI</a>
                <a href="/symptom-diagnosis">Symptom Diagnosis</a>
                <a href="/health-advice">Health Advice</a>
                <a href="/contact">Contact</a>
            </div>
        </div>

        <section id="about">
            <!-- Left Side: Video -->
            <div class="video-container">
                <video id="videoPlayer" controls>
                    <source src="/static/video.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <button class="play-button" id="playBtn" onclick="playVideo()">▶</button>
            </div>

            <!-- Right Side -->
            <div class="about-text">
                <h2>About me</h2>
                <p>Rapha Vee is your personal health and fitness companion, providing expert system-based guidance.</p>

                <div class="about-icons">
                    <div class="icon-item">
                        <img src="https://cdn-icons-png.flaticon.com/512/1046/1046786.png" alt="BMI Icon">
                        <div>
                            <h3 style="color: #007BFF;"><a href="/bmi" >BMI Calculation</a></h3>
                            <p>Calculate your Body Mass Index and get personalized recommendations.</p>
                        </div>
                    </div>
                    <div class="icon-item">
                        <img src="https://cdn-icons-png.flaticon.com/512/3532/3532315.png" alt="Diagnosis Icon">
                        <div>
                            <h3 style="color: #007BFF;"><a href="/symptom-diagnosis">Symptom Diagnosis</a></h3>
                            <p>Analyze symptoms to identify potential health conditions.</p>
                        </div>
                    </div>
                    <div class="icon-item">
                        <img src="https://cdn-icons-png.flaticon.com/512/2772/2772699.png" alt="Health Advice Icon">
                        <div>
                            <h3 style="color: #007BFF;"><a href="/health-advice">Health Advice</a></h3>
                            <p>Get dietary and fitness tips to maintain a healthy lifestyle.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <script>
            function playVideo() {
                var video = document.getElementById("videoPlayer");
                var button = document.getElementById("playBtn");
                video.style.display = "block";
                button.style.display = "none";
                video.play();
            }
        </script>
    </body>
    </html>
    """
    
@app.route('/contact')
def contact():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contact Us - Rapha Vee</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/js/all.min.js" crossorigin="anonymous"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: #f8f9fa;
            }

            /* Navigation Bar */
            .navbar {
                width: 100%;
                position: fixed;
                top: 0;
                left: 0;
                padding: 15px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 1.2em;
                font-weight: bold;
                background: black;
                color: white;
                z-index: 1000;
                box-sizing: border-box;
            }

            .system-name {
                font-size: 1.6em;
                font-weight: bold;
                margin-left: 20px;
            }

            .nav-links {
                display: flex;
                gap: 15px;
                padding-right: 30px;
            }

            .nav-links a {
                text-decoration: none;
                color: white;
                font-weight: bold;
                font-size: 1.1em;
                padding: 10px 12px;
                transition: color 0.3s ease-in-out;
            }

            .nav-links a:hover {
                color: #007BFF;
            }

            /* Contact Section */
            .contact-container {
                padding: 100px 50px 30px;
                display: flex;
                justify-content: center;
                gap: 40px;
                flex-wrap:wrap; /* Ensures responsiveness */
            }
            .frame {
                flex: 1; 
                max-width: 500px;
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
                text-align: center;
            }

            .contact-info {
                flex:1;
                width: 50%;
                background: transparent; 
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }

            .contact-info h2 {
                margin-bottom: 20px;
            }

            .contact-box {
                background: white;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 15px;
            }

            .contact-box i {
                font-size: 24px;
                color: #007BFF;
            }

            .social-icons {
                display: flex;
                justify-content: center;
                gap: 15px;
                margin-top: 20px;
            }

            .social-icons a {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                text-decoration: none;
                font-size: 20px;
                color: white;
                transition: transform 0.2s ease-in-out;
            }
            .icon i {
                 font-size: 22px;
                 color :white;
            }

            .social-icons a:hover {
                transform: scale(1.1);
            }

            .social-icons .twitter { background: #1DA1F2; }
            .social-icons .facebook { background: #3b5998; }
            .social-icons .whatsapp { background: #25D366; }
            .social-icons .linkedin { background: #0077B5; }

            .contact-image {
                width: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .contact-image img {
                max-width: 100%;
                height: auto;
                display:block;
                margin:auto;
                max_height: 250px;
                object-fit: cover
                border-radius: 10px;
                box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
            }

            /* Footer */
            .footer {
                text-align: center;
                padding: 15px;
                background: #2c3e50;
                color: white;
                margin-top: 30px;
            }

        </style>
        
    </head>
    <body>

        <!-- Navigation Bar -->
        <div class="navbar">
            <span class="system-name">Rapha Vee</span>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/about">About</a>
                <a href="/bmi">BMI</a>
                <a href="/symptom-diagnosis">Symptom Diagnosis</a>
                <a href="/health-advice">Health Advice</a>
                <a href="/contact">Contact</a>
            </div>
        </div>

        <!-- Contact Section -->
        <div class="contact-container">
            
            <!-- Contact Information -->
            <div class="contact-info">
                <h2>Contact Us</h2>

                <div class="contact-box">
                    <i class="fas fa-map-marker-alt"></i>
                    <div>
                        <strong>Address</strong>
                        <p>Eagle House 3rd floor,Kimathi Street,Nairobi.</p>
                    </div>
                </div>

                <div class="contact-box">
                    <i class="fas fa-phone"></i>
                    <div>
                        <strong>Call Us</strong>
                        <p>+254752113991</p>
                    </div>
                </div>

                <div class="contact-box">
                    <i class="fas fa-envelope"></i>
                    <div>
                        <strong>Email Us</strong>
                        <p>info@RaphaVee.com</p>
                    </div>
                </div>

                <!-- Social Media Icons (Now Clickable) -->
                <!-- Social Media Icons -->
                <div class="social-icons">
                    <a href="https://twitter.com" class="twitter"><i class="fa-brands fa-twitter"></i></a>
                    <a href="https://facebook.com" class="facebook"><i class="fa-brands fa-facebook-f"></i></a>
                    <a href="https://wa.me" class="whatsapp"><i class="fa-brands fa-whatsapp"></i></a>
                    <a href="https://linkedin.com" class="linkedin"><i class="fa-brands fa-linkedin-in"></i></a>
                </div>

            </div>

            <div class="contact-image">
                <img src="/static/contact.jpg" alt="Contact Image">
            </div>

        </div>

        <!-- Footer -->
        <div class="footer">
            &copy; 2025 Rapha Vee. All Rights Reserved.
        </div>

    </body>
    </html>
    """


@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    bmi_value = None
    bmi_category = None

    if request.method == 'POST':
        try:
            height_cm = float(request.form['height'])
            weight_kg = float(request.form['weight'])
            height_m = height_cm / 100  # Convert cm to meters
            bmi_value = round(weight_kg / (height_m ** 2), 2)  # BMI Formula

            # Interpret BMI category
            if bmi_value < 18.5:
                bmi_category = "UNDERWEIGHT. Consider a balanced diet."
            elif 18.5 <= bmi_value < 24.9:
                bmi_category = "NORMAL ~ HEALTHY WEIGHT. Keep up the good lifestyle!"
            elif 25 <= bmi_value < 29.9:
                bmi_category = "OVERWEIGHT. Consider exercising more."
            else:
                bmi_category = "OBESE. A healthier diet and exercise routine is recommended."

        except ValueError:
            bmi_value = "Invalid input"

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Body Mass Index</title>
        <style>
    
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: white;
                color: black;
            }

            .navbar {
                width: 100%;
                position: fixed;
                top: 0;
                left: 0;
                padding: 15px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 1.2em;
                font-weight: bold;
                background: black;
                color: white;
                z-index: 2000;
                box-sizing: border-box;
            }

            .system-name {
                font-size: 1.6em;
                font-weight: bold;
                margin-left: 20px;
            }

            .nav-links {
                display: flex;
                gap: 15px;
                padding-right: 30px;
            }

            .nav-links a {
                text-decoration: none;
                color: white;
                font-weight: bold;
                font-size: 1.1em;
                padding: 10px 12px;
                transition: color 0.3s ease-in-out;
            }

            .nav-links a:hover {
                color: #007BFF;
            }
            
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(to right, #1e3c72, #2a5298);
                color: white;
                padding-top:80px;
            }

            .container {
                display: flex;
                height: 100vh;
                width: 100%;
            }

            .left-frame {
                width: 40%;
                padding: 30px;
                text-align: center;
            }

            .left-frame h2 {
                font-size: 2em;
                margin-bottom: 15px;
            }

            .slideshow-container {
                width: 70%;
                height: 300px;
                overflow: hidden;
                border-radius: 10px;
                margin : 20px auto;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .slide {
                width: 100%;
                height: 100%;
                display: none;
                border-radius: 10px;
            }

            .right-frame {
                width: 60%;
                padding: 20px;
                background: black;
                color: black;
                border-radius: 10px;
                box-shadow: 5px 5px 20px rgba(0, 0, 0, 0.3);
                text-align: center;
            }

            .right-frame h2 {
                font-size: 2em;
                color:rgb(30, 59, 247);
            }

            .input-group {
                margin: 15px 0;
                color: white;
            }

            input {
                width: 40%;
                padding: 10px;
                font-size: 1.1em;
                border: 2px solid #1e3c72;
                border-radius: 5px;
                text-align: center;
            }

            /* Buttons */
            .btn {
                background: #1e3c72;
                color: white;
                font-size: 1.2em;
                padding: 10px 25px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 10px;
                transition: background 0.3s;
            }

            .btn:hover {
                background: #2a5298;
            }

            .reset-btn {
                background: #b0c4de;
                color: black;
            }

            .reset-btn:hover {
                background: #a0b0c0;
            }

            .exit-btn {
                background: #ff4c4c;
            }

            .exit-btn:hover {
                background: #e63939;
            }

            .bmi-result {
                margin-top: 20px;
                font-size: 1.3em;
                font-weight: bold;
                color:rgb(60, 198, 253);
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
                text-align: center;
                font-size: 1.2em;
                background: white; 
                color: black; 
            }

            th, td {
                padding: 10px;
                border: 1px solid #1e3c72; 
            }

            th {
                background: #1e3c72;
                color: white;
                font-weight: bold;
            }

        </style>
    </head>
    <body>
        <div class="navbar">
            <span class="system-name">Rapha Vee</span>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/about" class="active">About</a>
                <a href="/symptom-diagnosis">Symptom Diagnosis</a>
                <a href="/health-advice">Health Advice</a>
                <a href="/contact ">Contact</a>
            </div>
        </div>
        <div class="container">
            <div class="left-frame">
                <h2>Are you fit?</h2>
                <p>Body Mass Index (BMI) is a simple calculation using height and weight to estimate body fat.</br>
                </br>
                Proceed to check your BMI and see if  you are fit</p>
                
                <div class="slideshow-container">
                    <img class="slide" src="/static/bmi (1).jpg" alt="BMI Slide 1">
                    <img class="slide" src="/static/bmi (2).jpg" alt="BMI Slide 2">
                    <img class="slide" src="/static/bmi (3).jpg" alt="BMI Slide 3">
                    <img class="slide" src="/static/bmi (4).jpg" alt="BMI Slide 4">
                    <img class="slide" src="/static/bmi (5).jpg" alt="BMI Slide 5">
                    <img class="slide" src="/static/bmi (6).jpg" alt="BMI Slide 6">
                    <img class="slide" src="/static/bmi (7).jpg" alt="BMI Slide 7">
                    <img class="slide" src="/static/bmi (8).jpg" alt="BMI Slide 8">
                </div>
            </div>

            <div class="right-frame">
                <h2>Body Mass Index</h2>
                <p>Calculate your BMI.</p>

                <form id="bmi-form" method="post">
                    <div class="input-group">
                        <label for="height">Height (cm):</label><br>
                        <input type="text" id="height" name="height" required>
                    </div>

                    <div class="input-group">
                        <label for="weight">Weight (kg):</label><br>
                        <input type="text" id="weight" name="weight" required>
                    </div>

                    <div class="input-group">
                        <label for="bmi">Sum Up BMI:</label><br>
                        <input type="text" id="bmi" name="bmi" readonly>
                    </div>

                    <button type="submit" class="btn">Calculate</button>
                    <button type="reset" class="btn reset-btn">Reset</button>
                    <button type="button" class="btn exit-btn" onclick="exitBMI()">Exit</button>
                </form>

                """ + (f"""
                <div class="bmi-result">
                    Your BMI is: {bmi_value}<br>
                   <span style='color: green;'>{bmi_category}</span>
                </div>
                <script>
                    document.getElementById('bmi').value = '{bmi_value}';
                </script>
                """ if bmi_value else "") + """
            </div>
        </div>

        <script>
            let slideIndex = 0;
            const slides = document.getElementsByClassName("slide");

            function showSlides() {
                for (let i = 0; i < slides.length; i++) {
                    slides[i].style.display = "none";
                }
                slideIndex++;
                if (slideIndex > slides.length) {
                    slideIndex = 1;
                }
                slides[slideIndex - 1].style.display = "block";
                setTimeout(showSlides, 3000);
            }

            showSlides();
            
            function exitBMI() {
                document.querySelector(".right-frame").innerHTML = `
                    <h2>BMI Categories</h2>
                    <table border="1" style="width: 100%; border-collapse: collapse; text-align: center; font-size: 1.2em;">
                        <tr style="background:rgb(76, 118, 253); color: white;">
                            <th>BMI Range</th>
                            <th>Category</th>
                        </tr>
                        <tr>
                            <td>Below 18.5</td>
                            <td style="color: blue;">Underweight</td>
                        </tr>
                        <tr>
                            <td>18.5 - 24.9</td>
                            <td style="color: green;">Normal Weight</td>
                        </tr>
                        <tr>
                            <td>25 - 29.9</td>
                            <td style="color: orange;">Overweight</td>
                        </tr>
                        <tr>
                            <td>30 & Above</td>
                            <td style="color: red;">Obese</td>
                        </tr>
                    </table>
                    
                    <h2 style="margin-top: 20px;">Need Some Advice?</h2>
                    <p>Check out our expert health tips for a better lifestyle.</p>
                    <button class="btn" onclick="window.location.href='/health-advice'">Health Advice</button>
                `;
            }

        </script>
    </body>
    </html>
    """

@app.route('/health-advice')
def health_advice():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Health Advice - FAQs</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                color: black;
            }
            
            .navbar {
                width: 100%;
                position: fixed;
                top: 0;
                left: 0;
                padding: 15px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 1.2em;
                font-weight: bold;
                background: #1e3c72;
                color: white;
                z-index: 1000;
                box-sizing: border-box;
            }

            .system-name {
                font-size: 1.6em;
                font-weight: bold;
                margin-left: 20px;
            }

            .nav-links {
                display: flex;
                gap: 15px;
                padding-right: 30px;
            }

            .nav-links a {
                text-decoration: none;
                color: white;
                font-weight: bold;
                font-size: 1.1em;
                padding: 10px 12px;
                transition: color 0.3s ease-in-out;
            }

            .nav-links a:hover {
                color: #007BFF;
            }
            
            .video-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                z-index: -1;
            }

            .video-container video {
                width: 100%;
                height: 100%;
                object-fit: cover;
                position: absolute;
                top: 0;
                left: 0;
            }
            
            /* Page Content */
            .container {
                max-width: 900px;
                margin: 100px auto;
                text-align: center;
            }

            h2 {
                font-size: 2em;
                margin-bottom: 10px;
                color: #1e3c72;
            }

            p {
                color: #666;
                font-size: 1.1em;
                margin-bottom: 20px;
            }

            .faq-container {
                text-align: left;
                border-radius: 10px;
                padding: 20px;
            }

            .faq-item {
                margin-bottom: 10px;
            }

            .faq-question {
                background: #1e3c72;
                color: white;
                padding: 15px;
                border-radius: 5px;
                font-size: 1.2em;
                font-weight: bold;
                cursor: pointer;
                transition: background 0.3s ease;
            }

            .faq-question:hover {
                background: #2a5298;
            }

            .faq-answer {
                display: none;
                padding: 10px;
                background: #f1f1f1;
                border-radius: 5px;
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        <!-- Background Video -->
        <div class="video-container">
            <video autoplay loop muted>
                <source src="/static/situps.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        
        <div class="navbar">
            <span class="system-name">Rapha Vee</span>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/about" class="active">About</a>
                <a href="/bmi">BMI</a>
                <a href="/symptom-diagnosis">Symptom Diagnosis</a>
                <a href="/contact">Contact</a>
            </div>
        </div>
        
        <!-- Page Content -->
        <div class="container">
            <h2>Frequently Asked Questions</h2>
            <p>Find answers to common questions about BMI, fitness, and nutrition.</p>

            <div class="faq-container">
                <!-- FAQ 1 - General -->
                <div class="faq-item">
                    <div class="faq-question">What is BMI and why is it important?</div>
                    <div class="faq-answer">
                        Body Mass Index (BMI) is a measure of body fat based on height and weight. It helps determine if a person is underweight, normal weight, overweight, or obese.
                    </div>
                </div>

                <div class="faq-item">
                    <div class="faq-question">I am underweight. How can I gain healthy weight?</div>
                    <div class="faq-answer">
                        To gain healthy weight, eat calorie-dense foods rich in <b>healthy fats, protein, and carbs</b>. Include:
                        <ul>
                            <li><b>Foods</b>: Nuts, seeds, whole grains, dairy products, avocados, lean meats, and starchy vegetables.</li>
                            <li><b>Exercises:</b> Strength training to build muscle mass.</li>
                        </ul>
                        Aim for 3-5 meals a day with nutrient-dense snacks.
                    </div>
                </div>

                <div class="faq-item">
                    <div class="faq-question">I have a normal BMI. How do I maintain my weight?</div>
                    <div class="faq-answer">
                        Maintain your weight by </b>balancing diet and exercise</b>:
                        <ul>
                            <li><b>Foods:</b> Lean protein, whole grains, healthy fats, and plenty of fruits & vegetables.</li>
                            <li><b>Exercises:</b> Regular cardio (30 mins/day) + strength training 2-3 times a week.</li>
                        </ul>
                        Stay hydrated and avoid excessive processed foods.
                    </div>
                </div>

                <div class="faq-item">
                    <div class="faq-question">I am overweight. How can I lose weight safely?</div>
                    <div class="faq-answer">
                        Focus on <b>caloric deficit and exercise</b>:
                        <ul>
                            <li><b>Foods:</b> Reduce processed foods & sugar. Eat more lean protein, fiber, and whole grains.</li>
                            <li><b>Exercises:</b> Brisk walking, jogging, cycling, and strength training 3-5 times a week.</li>
                        </ul>
                        Aim to lose <b>0.5 to 1 kg per week</b> for sustainable weight loss.
                    </div>
                </div>

                <div class="faq-item">
                    <div class="faq-question">I am obese. What steps should I take to improve my health?</div>
                    <div class="faq-answer">
                        If your BMI is <b.30+</b>, focus on gradual, <b>long-term</b> lifestyle changes:
                        <ul>
                            <li><b>Diet:</b> Low-calorie meals with vegetables, lean proteins, and whole grains. Avoid sugary drinks.</li>
                            <li><b>Exercise:</b> Start with low-impact activities (walking, swimming) and increase gradually.</li>
                        </ul>
                        Consult a doctor or dietitian for a <b>personalized</b> weight loss plan.
                    </div>
                </div>

                <div class="faq-item">
                    <div class="faq-question">What are the best exercises for overall fitness?</div>
                    <div class="faq-answer">
                        A combination of <b>cardio, strength training, and flexibility exercises</b> is best:
                        <ul>
                            <li><b>Cardio:</b> Running, cycling, swimming (3-5 times a week).</li>
                            <li><b>Strength Training:</b> Weight lifting, resistance bands, or bodyweight exercises.</li>
                            <li><b>Flexibility:</b> Yoga and stretching for mobility.</li>
                        </ul>
                        Aim for <b>150</b> minutes of moderate-intensity activity per week.
                    </div>
                </div>
            </div>
        </div>

        <script>
            /* FAQ Toggle Functionality */
            const questions = document.querySelectorAll('.faq-question');

            questions.forEach(question => {
                question.addEventListener('click', () => {
                    const answer = question.nextElementSibling;
                    if (answer.style.display === "block") {
                        answer.style.display = "none";
                    } else {
                        answer.style.display = "block";
                    }
                });
            });
        </script>

    </body>
    </html>
    """
 
@app.route('/symptom-diagnosis', methods=['GET', 'POST'])
def symptom_diagnosis():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Symptom Diagnosis</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-image: url('/static/Hosp.jpg'); 
                color: black;
            }

            .navbar {
                width: 100%;
                position: fixed;
                top: 0;
                left: 0;
                padding: 15px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 1.2em;
                font-weight: bold;
                background: #1e3c72;
                color: white;
                z-index: 1000;
                box-sizing: border-box;
            }

            .system-name {
                font-size: 1.6em;
                font-weight: bold;
                margin-left: 20px;
            }

            .nav-links {
                display: flex;
                gap: 15px;
                padding-right: 30px;
            }

            .nav-links a {
                text-decoration: none;
                color: white;
                font-weight: bold;
                font-size: 1.1em;
                padding: 10px 12px;
                transition: color 0.3s ease-in-out;
            }

            .nav-links a:hover {
                color: #007BFF;
            }

            #welcome-frame {
                padding: 30px 50px;
                text-align: left;
                background-image: url('/static/symptoms.jpg');
                background-size: cover;
                background-position: center;
                max-width: 90%;
                margin: 10px;
                margin-top: 80px;
            }

            #welcome-frame h1 {
                font-size: 3.0em;
                margin-bottom: 15px;
                margin-top :10px;
            }

            #welcome-frame p {
                font-size: 1.2em;
                margin-bottom: 5px;
                margin-left: 820px;
            }

            .learn-more-btn {
                background: #00bfae;
                color: white;
                padding: 10px 15px;
                text-decoration: none;
                border-radius: 5px;
                font-size: 1.1em;
            }

            #second-frame {
                display: flex;
                gap: 10px;
                padding: 20px 40px;
                justify-content: space-between;
                margin-top: 20px;
            }

            .left-frame {
                width: 60%;
                height :auto;
                padding: 20px;
                background:none;
                color: black;
                text-align: left;
                border-radius: 10px;
                border: 2px solid #1e3c72;
                margin: 10px;
            }

            .left-frame p {
                font-size: 1.2em;
                margin-top:10px;
                line-height: 1.6;
            }

            .middle-frame {
                width: 30%;
                padding: 20px;
                text-align: center;
            }

            .middle-frame img {
                max-width: 100%;
                height: 100%;
                border-radius: 10px;
                object-fit: cover;
            }

            /* Right Frame - Login Form */
            .right-frame {
                width: 30%;
                padding: 20px;
                background: none;
                color: #1e3c72;
                text-align: center;
                border-radius: 5px;
                display: flex;
                flex-direction: column;
                align-items: stretch;
                
            }

            .right-frame h3 {
                font-size: 1.8em;
                margin-bottom: 10px;
                margin-top:10px;
            }
            
            .right-frame .form-group {
                margin-bottom: 20px;
            }

            .right-frame input {
                width: 100%;
                padding: 10px;
                font-size: 1.1em;
                border:  1px solid black;
                border-radius: 2px;
                margin-bottom: 10px;
                background-color: white;
                color: #495057;
            }
            .right-frame .buttons {
                display: flex;
                justify-content: space-between; 
                align-items: center;
                width : 100%;
            }
                        
            .right-frame button {
                background:#00bfae;
                color: #1e3c72;
                padding: 2px 5px;
                border: none;
                border-radius: 5px;
                font-size: 0.8em;
                cursor :pointer;
                width: 25%;
                margin-left:   190px;
                margin-top: 15px;
                
            }
            .right-frame button:hover {
            background: #0007b8f; 
            }
            
            .right-frame a.signup-link {
                display: inline-block;
                margin-top: 0 px;
                color: #1e3c72;
                text-decoration: none;
                font-size: 0.8em;
                width: 48%;
                text-align: left;
                
            }

            .right-frame a.signup-link:hover {
                text-decoration: underline;
            }


        </style>
    </head>
    <body>
        <div class="navbar">
            <span class="system-name">Rapha Vee</span>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/about">About</a>
                <a href="/bmi">BMI</a>
                <a href="/health advice">Health Advice</a>
                 <a href="/contact" >Contact</a>
            </div>
        </div>

        <section id="welcome-frame">
            <h1>Diagnose </h1>
            <br>
            <br><p>Help yourself with accurate diagnosis  </p> 
            <a href="/learn-more" class="learn-more-btn">Learn More</a>
        </section>

        <section id="second-frame">
            <!-- Left Frame - Description -->
            <div class="left-frame">
                <p>Feeling unwell and unsure of your symptoms? </br>Don't worry!</br> Rapha Vee will guide you through a quick symptom check and help you identify potential diseases,
                giving you the insight to take the right steps toward better health.</p>
            </div>

            <!-- Middle Frame - Image -->
            <div class="middle-frame">
                <img src="/static/Hosp.jpg" alt="Symptom Diagnosis Image">
            </div>

            <div class="right-frame">
                <h3>Login</h3>
               <form method="post" action="/login">
                    <input type="email" name="email" placeholder="Email Address" required><br>
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit">Login</button>
                </form>
                 <a href="/signup" class="signup-link">Sign Up?</a>
            </div>
        </section>
    </body>
    </html>
    """
@app.route('/learn-more')
def learn_more():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Learn More - Symptom Diagnosis</title>
        
        <!-- Font Awesome for Icons -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">

        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                text-align: center;
            }
            .container {
                max-width: 1100px;
                margin: 50px auto;
                padding: 20px;
                text-align: center;
            }
            h1 {
                color: #1e3c72;
            }
            .grid-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 20px;
                justify-content: center;
            }
            .card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease-in-out;
                text-align: center;
            }
            .card:hover {
                background-color: #00bfae;
                color: white;
                transform: translateY(-5px);
            }
            .icon {
                font-size: 50px;
                margin-bottom: 15px;
                color: #009688;
                transition: color 0.3s;
            }
            .card:hover .icon {
                color: white;
            }
            .back-btn {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                text-decoration: none;
                background: #1e3c72;
                color: white;
                border-radius: 5px;
                font-size: 1.1em;
            }
            .back-btn:hover {
                background: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Understanding Symptom Diagnosis</h1>
            
            <div class="grid-container">
                <!-- How the system works -->
                <div class="card">
                    <i class="fas fa-stethoscope icon"></i>
                    <h2>How the System Works</h2>
                    <p>The system asks Yes/No questions, analyzes answers, and uses rule-based reasoning to suggest possible diseases.</p>
                </div>

                <!-- Benefits of Early Diagnosis -->
                <div class="card">
                    <i class="fas fa-heartbeat icon"></i>
                    <h2>Benefits of Early Diagnosis</h2>
                    <p>Early detection prevents complications, improves treatment outcomes, and helps users make informed health decisions.</p>
                </div>

                <!-- How to use the symptom checker -->
                <div class="card">
                    <i class="fas fa-notes-medical icon"></i>
                    <h2>How to Use the Symptom Checker</h2>
                    <p>Enter symptoms, answer Yes/No questions, and receive guidance on risk levels and medical recommendations.</p>
                </div>

                <!-- FAQs -->
                <div class="card">
                    <i class="fas fa-hospital icon"></i>
                    <h2>⚠️ DISCLAIMER</h2>
                    <p>This system should not replace professional medical consultation.It provides recommended dosages based on symptoms.</p>
                </div>
            </div>

            <a href="/symptom-diagnosis" class="back-btn">Back</a>
        </div>
    </body>
    </html>
    """


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        gender = request.form.get('gender')
        age = int(request.form.get('age'))
        weight = float(request.form.get('weight'))

        #  Check if user already exists by username OR email
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or Email already exists! Please use a different one.", "danger")
            return redirect(url_for('signup'))

        #  Create new user if it does not exist
        new_user = User(username=username, email=email, password=password,
                        firstname=firstname, lastname=lastname, gender=gender, age=age, weight=weight)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Sign-up successful! Please login.", "success")
            return redirect(url_for('symptom_diagnosis'))
        except Exception as e:
            db.session.rollback()  #  Rollback in case of any error
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect(url_for('signup'))

    return """ 
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sign Up</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #e3f2fd;
                text-align: center;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 400px;
                margin: 50px auto;
                padding: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }
            input, select {
                width: 90%;
                padding: 10px;
                margin: 5px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            .register-btn {
                background: #007BFF;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .register-btn:hover {
                background: #0056b3;
            }
            .login-link {
                display: block;
                margin-top: 10px;
                text-decoration: none;
                color: #007BFF;
            }
            .login-link:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Sign Up</h2>
            <form method="post">
                <input type="text" name="username" placeholder="Username" required>
                <input type="email" name="email" placeholder="Email Address" required>
                <input type="password" name="password" placeholder="Password" required>
                <input type="text" name="firstname" placeholder="First Name" required>
                <input type="text" name="lastname" placeholder="Last Name" required>
                <select name="gender" required>
                    <option value="" disabled selected>Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                </select>
                <input type="number" name="age" placeholder="Age" required>
                <input type="number" name="weight" placeholder="Weight (kg)" required>
                <button type="submit" class="register-btn">Register</button>
            </form>
           <a href='/symptom-diagnosis'>Already Registered? Go back to Login</a>
        </div>
    </body>
    </html>
    """

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Fetch user from the database
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username  # Store username in session
            
            return """
            <script>
                alert('✅ Login successful! Welcome, {0}');
                window.location.href = '/dashboard';  // Redirect to dashboard
            </script>
            """.format(user.username)

        else:
            return """
            <script>
                alert('❌ Invalid email or password. Please try again.');
                window.location.href = '/symptom-diagnosis';  // Redirect back to symptom diagnosis
            </script>
            """

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
    </head>
    <body>
        <h2>Login</h2>

        <form method="post" action="/login">
            <input type="email" name="email" placeholder="Email Address" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>

        <a href='/signup'>Don't have an account? Sign up here</a>                      
    </body>
    </html>
    """



def load_knowledge_base():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
    file_path = os.path.join(script_dir, "knowledge_base.json")  # Get JSON path

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Knowledge base not found: {file_path}")

    with open(file_path, "r") as file:
        try:
            data = json.load(file)
            if not data:
                raise ValueError("❌ Knowledge base is empty.")
            return data
        except json.JSONDecodeError:
            raise ValueError("❌ Error reading JSON file. Check for syntax errors.")


# ✅ Diagnosis Function using Forward Chaining & Rule-Based Inference
def diagnose_disease(user_symptoms):
    knowledge_base = load_knowledge_base()
    user_symptoms = set(user_symptoms)
    match_scores = {}

    for disease, symptoms in knowledge_base.items():
        symptoms_set = set(symptoms)
        matched_symptoms = user_symptoms.intersection(symptoms_set)
        
        if len(symptoms_set) > 0:
            match_percentage = (len(matched_symptoms) / len(symptoms_set)) * 100
        else:
            match_percentage = 0

        match_scores[disease] = match_percentage

    # ✅ Determine the top disease or suggest possibilities
    top_disease = max(match_scores, key=match_scores.get)
    top_score = match_scores[top_disease]

    if top_score >= 75:
        return f"✅ Diagnosis: You most likely have **{top_disease}** (Match: {top_score:.1f}%)."
    else:
        sorted_matches = sorted(match_scores.items(), key=lambda x: x[1], reverse=True)[:2]
        suggestions = "\n".join([f"- {disease} ({score:.1f}%)" for disease, score in sorted_matches])
        return f"⚠ No exact match found.\nPossible conditions:\n{suggestions}\nPlease consult a doctor for further diagnosis."

# ✅ API Endpoint for Symptom Diagnosis
@app.route('/api/diagnose', methods=['POST'])
def api_diagnose():
    data = request.json
    user_symptoms = data.get('symptoms', [])
    diagnosis_result = diagnose_disease(user_symptoms)
    return jsonify({"diagnosis": diagnosis_result})



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return """
        <script>
            alert('⚠️ Please login first!');
            window.location.href = '/symptom-diagnosis';  // Redirect to symptom diagnosis login tab
        </script>
        """
    
    username = session.get('username', 'User')  # Get username safely

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Dashboard - Symptom Diagnosis</title>
        <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background-image: url('/static/Hosp.jpg');  /* ✅ Full-page background */
                background-size: cover;
                background-position: center;
                text-align: center;
                margin: 0;
                padding: 0;
            }}

            /* ✅ Navigation Bar - Matches Symptom Diagnosis Page */
            .navbar {{
                width: 100%;
                position: fixed;
                top: 0;
                left: 0;
                padding: 20px 40px;  
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 1.3em;
                font-weight: bold;
                background: #1e3c72;  
                color: white;
                z-index: 1000;
                box-sizing: border-box;
            }}

            .nav-links a {{
                text-decoration: none;
                color: white;
                font-weight: bold;
                font-size: 1.1em;
                padding: 10px 12px;
                transition: color 0.3s ease-in-out;
            }}

            .nav-links a:hover {{
                color: #00bfae;
            }}

            /* ✅ White Box for Welcome & Diagnosis */
            .container {{
                background: white;
                padding: 40px;
                margin: 120px auto;
                width: 60%;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
            }}

            .container h2 {{
                color: #1e3c72;
                font-size: 2.5em;
            }}

            /* ✅ Symptom Box - Smaller Size & Themed Color */
            .diagnosis-box {{     
                background: #00bfae;;
                color:#1e3c72;
                padding: 10px;
                width: 50%;
                margin: auto;
                border-radius: 10px;
                margin-top: 30px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
                font-size: 1.1em;
                font-weight: bold;  /* Make the text more readable */
                text-align: center;
            }}
            #results-box {{
                background: #00bfae;  /* Keep the current box color */
                color: #1e3c72;       /* Match text color with navbar */
                padding: 20px;
                width: 50%;
                margin: auto;
                border-radius: 10px;
                margin-top: 30px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
                font-size: 1.1em;
                font-weight: bold;
                text-align: center;
            }}

            #results-box p, 
            #results-box strong, 
            #results-box span {{
                background: none !important; /* Remove blue highlight */
                color: inherit !important;   /* Ensure it follows the correct text color */
            }}


            /* ✅ Buttons */
            .start-btn, .yes-btn, .no-btn {{
                background: #00bfae;
                color: white;
                font-size: 16px;
                padding: 12px;
                border: none;
                cursor: pointer;
                margin: 10px;
                border-radius: 5px;
                transition: 0.3s;
            }}

            .yes-btn {{
                background: #28a745;
            }}

            .no-btn {{
                background: #dc3545;
            }}

            .start-btn:hover, .yes-btn:hover, .no-btn:hover {{
                opacity: 0.8;
            }}

            /* ✅ Logout Button */
            .logout-btn {{
                display: block;
                background: #dc3545;
                color: white;
                padding: 10px;
                font-size: 16px;
                border: none;
                cursor: pointer;
                margin: 20px auto;
                width: 20%;
                border-radius: 5px;
                text-align: center;
                text-decoration: none;
                transition: 0.3s;
            }}

            .logout-btn:hover {{
                background: #c82333;
            }}

            .hidden {{
                display: none;
            }}
        </style>
    </head>
    <body>

        <nav class="navbar">
            <span class="system-name">Rapha Vee</span>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/about">About</a>
                <a href="/bmi">BMI</a>
                <a href="/symptom-diagnosis">Symptom Diagnosis</a>
                <a href="/health-advice">Health Advice</a>
                <a href="/contact">Contact</a>
            </div>
        </nav>

        <!-- ✅ White Box for Welcome & Diagnosis -->
        <div class="container">
            <h2>Welcome, {username}!</h2>
            <p>Start your symptom diagnosis below.</p>
            <button class="start-btn" onclick="startDiagnosis()">::Start Diagnosis::<i class="fas fa-power-off"></i></button>

            <div class="diagnosis-box hidden" id="symptom-box">
                <h3>Symptoms</h3>
                <p id="symptom-question">Loading symptoms...</p>
                <button class="yes-btn" onclick="recordResponse(true)">Yes</button>
                <button class="no-btn" onclick="recordResponse(false)">No</button>
            </div>

           <!-- Diagnosis Box (Shows Analyzing... & Countdown) -->
            <div class="diagnosis-box hidden" id="diagnosis-box">
                <h3>Diagnosis In Progress...</h3>
                <p id="countdown-text">Analyzing...</p>
            </div>

            <!-- Results Box (Appears AFTER Clicking OK) -->
            <div class="diagnosis-box hidden" id="results-box">
                <h3>Diagnosis Results</h3>
                <p id="diagnosis-result">Your diagnosis will appear here.</p>
            </div>

        </div>

        <!-- ✅ Logout Button - Visible & Styled -->
        <a href='/logout' class="logout-btn">Logout</a>

        <script>
            let userResponses = [];
            let symptoms = [
                "Do you have fever?",
                "Do you have chills?",
                "Are you sweating excessively?",
                "Do you have a headache?",
                "Do you have muscle pain?",
                "Are you experiencing nausea?",
                "Have you vomited recently?",
                "Do you have shortness of breath?",
                "Do you have wheezing?",
                "Do you feel chest tightness?",
                "Are you coughing frequently?",
                "Do you have difficulty breathing?",
                "Is your skin or eyes turning yellow?",
                "Do you have dark urine?",
                "Are you feeling fatigued?",
                "Do you have abdominal pain?",
                "Have you lost your appetite?",
                "Do you have a persistent cough?",
                "Are you coughing up blood?",
                "Do you have unexplained weight loss?",
                "Are you sweating at night?",
                "Do you experience bloating?",
                "Are you experiencing heartburn?",
                "Do you have sensitivity to light?",
                "Do you have sensitivity to sound?",
                "Do you have acid reflux?",
                "Is your blood pressure high?",
                "Do you feel dizzy?",
                "Do you have blurred vision?",
                "Are you experiencing watery diarrhea?",
                "Are you experiencing dehydration?",
                "Do you have muscle cramps?",
                "Do you have constipation?",
                "Do you have swollen lymph nodes?",
                "Do you have skin rashes?"
            ];

            let currentQuestionIndex = 0;

            function startDiagnosis() {{
                document.querySelector(".start-btn").classList.add("hidden");
                document.getElementById("symptom-box").classList.remove("hidden");
                loadNextQuestion();
            }}

            function loadNextQuestion() {{
                if (currentQuestionIndex < symptoms.length) {{
                    document.getElementById("symptom-question").innerText = symptoms[currentQuestionIndex];
                }} else {{
                    completeDiagnosis();
                }}
            }}

            function recordResponse(response) {{
                if (response) userResponses.push(symptoms[currentQuestionIndex]);
                currentQuestionIndex++;
                loadNextQuestion();
            }}

            function completeDiagnosis() {{
                // Hide symptom question box
                document.getElementById("symptom-box").classList.add("hidden");

                // Show the Diagnosis Box (Analyzing & Countdown)
                let diagnosisBox = document.getElementById("diagnosis-box");
                diagnosisBox.style.display = "block";  
                document.getElementById("countdown-text").innerText = "Analyzing...";

                // Start a countdown (3, 2, 1...)
                let countdown = 3;
                let countdownInterval = setInterval(() => {{
                    document.getElementById("countdown-text").innerText = "Diagnosis in " + countdown + "...";
                    countdown--;

                    if (countdown < 0) {{
                        clearInterval(countdownInterval);

                        // Show alert after countdown
                        setTimeout(() => {{
                            alert("Diagnosis Complete! Click OK to view results.");

                            // Hide Diagnosis Box
                            diagnosisBox.style.display = "none";

                            // Show Results Box
                            let resultsBox = document.getElementById("results-box");
                            resultsBox.style.display = "block";
                            resultsBox.classList.remove("hidden");

                            // Fetch diagnosis results from the backend
                            fetch('/api/diagnose', {{
                                method: 'POST',
                                body: JSON.stringify({{ symptoms: userResponses }}),
                                headers: {{ 'Content-Type': 'application/json' }}
                            }})
                            .then(response => response.json())
                            .then(data => {{
                                document.getElementById("diagnosis-result").innerText = data.diagnosis;
                            }});

                        }}, 500);  // Delay for smooth transition
                    }}
                }}, 1000);  // Countdown interval (1 second each)
            }}



                    </script>

    </body>
    </html>
    """

  
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    
    return """
    <script>
        alert('✅ You have been logged out.');
        window.location.href = '/symptom-diagnosis';  // Redirect back to symptom diagnosis page
    </script>
    """
    



if __name__ == "__main__":
    app.run(debug=True)
