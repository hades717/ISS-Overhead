import requests 
from datetime import datetime
import smtplib, time

MY_EMAIL = "test@gmail.com" 
MY_APP_PASSWORD = "dummy123" 

# use https://www.latlong.net/ to find your latitude and longitude
MY_LAT = 0 # Your latitude
MY_LONG = 0 # Your longitude

def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json() # get ISS data

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json() # get sunrise and sunset hour for your location
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour # current hour

    if time_now >= sunset or time_now < sunrise:
        return True


while True:
    time.sleep(60)
    if iss_overhead() and is_night():
        try:
            with smtplib.SMTP(host="smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_APP_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=MY_EMAIL,
                    msg="Subject: Look Up!!\n\nThe ISS is above you in the sky."
                )
            print("Email sent successfully!")
            break
        except Exception as e:
            print(f"Failed to send mail: {e}")
            break
