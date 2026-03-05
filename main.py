import os
import requests
from datetime import datetime
from flask import Flask, render_template_string

app = Flask(__name__)

# API key - get your free key from https://api-ninjas.com/
API_KEY = os.getenv('NINJA_API_KEY', 'YOUR_API_KEY_HERE')

@app.route('/')
def home():
    # Get current datetime
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Get random quote from API
    try:
        response = requests.get(
            'https://api-ninjas.com/api/quotes',
            headers={'X-Api-Key': API_KEY},
            params={'category': 'happiness'}  # You can change category
        )
        response.raise_for_status()
        quote_data = response.json()[0]
        quote = quote_data['quote']
        author = quote_data['author']
    except Exception as e:
        # Fallback quote if API fails
        quote = "The best way to predict the future is to create it."
        author = "Peter Drucker"
    
    # Get last access time from session or use current time
    last_access = current_time
    
    return render_template_string(HTML_TEMPLATE, 
                                quote=quote, 
                                author=author, 
                                current_time=current_time,
                                last_access=last_access)

# HTML template with centered content and refresh functionality
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Random Quote</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #333;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            padding: 3rem 2rem;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 600px;
            width: 90%;
            backdrop-filter: blur(10px);
        }
        .quote {
            font-size: 1.8rem;
            font-style: italic;
            margin-bottom: 1.5rem;
            line-height: 1.5;
            color: #555;
        }
        .author {
            font-size: 1.2rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 2rem;
        }
        .datetime-info {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            margin-top: 1.5rem;
            font-size: 0.95rem;
        }
        .current-time {
            color: #28a745;
            font-weight: bold;
        }
        .last-access {
            color: #6c757d;
            margin-top: 0.5rem;
        }
        .refresh-hint {
            margin-top: 1.5rem;
            font-size: 0.9rem;
            color: #6c757d;
        }
        @media (max-width: 768px) {
            .quote {
                font-size: 1.4rem;
            }
            .container {
                padding: 2rem 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="quote">"{{ quote }}"</div>
        <div class="author">{{ author }}</div>
        
        <div class="datetime-info">
            <div><strong>Current Time:</strong> <span class="current-time">{{ current_time }}</span></div>
            <div class="last-access"><strong>Last Access:</strong> {{ last_access }}</div>
        </div>
        
        <div class="refresh-hint">
            🔄 Refresh the page to get a new quote!
        </div>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    print("Starting Quote App...")
    print("Get your free API key from: https://api-ninjas.com/")
    print("Set it as environment variable: NINJA_API_KEY=your_key")
    print("\nVisit: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
