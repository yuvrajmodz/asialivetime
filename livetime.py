from flask import Flask, Response
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict 
import json 
import os

app = Flask(__name__)

@app.route('/timenow', methods=['GET'])
def get_time_now():
    try:
        # URL for scraping time and date from Google Search
        url = "https://www.google.com/search?q=asia+calcutta+time+now"
        
        # Set a user-agent to simulate a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
        }
        
        # Send a GET request with custom headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensure the request was successful
        
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the specific div containing the time based on the classes provided
        time_div = soup.find("div", class_="gsrt vk_bk FzvWSb YwPhnf")
        
        # Extract time if found
        if time_div:
            current_time = time_div.text.strip()
        else:
            current_time = "Time not found"
        
        # Find the specific div containing the date and day
        date_div = soup.find("div", class_="vk_gy vk_sh")
        
        if date_div:
            # Extract the date and day information
            main_day = date_div.contents[0].strip()  # Extract "Wednesday"
            full_date = date_div.find("span", class_="KfQeJ").text.strip()  # Extract "23 October 2024"
            date_and_day = f"{main_day}, {full_date}".replace(",,", ",")  # Clean up any extra commas
        else:
            date_and_day = "Date and day not found"

        # Construct the response in the correct order using OrderedDict
        response_data = OrderedDict()
        response_data["time_now"] = current_time
        response_data["date_and_day"] = date_and_day
        
        # Convert the response to JSON format using the json.dumps() function
        json_response = json.dumps(response_data, indent=4)  # indent for pretty print
        
        # Return the response as JSON with the correct content type
        return Response(json_response, content_type="application/json")

    except Exception as e:
        # Handle errors by returning an error message
        error_response = json.dumps({"error": str(e)}, indent=4)
        return Response(error_response, content_type="application/json", status=500)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6000))
    app.run(host='0.0.0.0', port=port, debug=True)