from decimal import Decimal  # string to decimal for currency change
from re import sub  # parsing data from URL
from bs4 import BeautifulSoup  # parsing data from URL
import requests
import smtplib
import time
import smtplib
import ssl
from email.mime.text import MIMEText  # email libraries
from email.mime.multipart import MIMEMultipart  # email libraries


URL = 'https://www.amazon.com/Sony-Mirrorless-Digital-Camera-Backpack/dp/B019Y6CO90/ref=sr_1_1_sspa?crid=15PFYJLD6C71R&keywords=sony+camera&qid=1565114665&s=gateway&sprefix=sony+ca%2Caps%2C162&sr=8-1-spons&psc=1'

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}


def price_check():
    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(id="productTitle").get_text()
    price = soup2.find(id="priceblock_ourprice").get_text()
    converted_price = Decimal(sub(r'[^\d\-.]', '', price))
    desired_price = 2096.00  # you can change you desired price here
    # send email
    if(converted_price > desired_price):
        send_mail()

    print(title.strip())
    print(price)
    # print(converted_price)


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('harsh@ekta.co', 'cbnlpqgdissjeaoj')

    message = MIMEMultipart("alternative")
    message["Subject"] = "Price has dropped for the product you wanted"
    message["From"] = 'harsh@ekta.co'
    message["To"] = 'harshhasd@gmail.co'

    # Create the plain-text and HTML version of your message
    text = """\
    Hi Harsh,
    How are you?
    The price has dropped for the product you were watching. You can follow the link here https://www.amazon.com/Sony-Mirrorless-Digital-Camera-Backpack/dp/B019Y6CO90/ref=sr_1_1_sspa?crid=15PFYJLD6C71R&keywords=sony+camera&qid=1565114665&s=gateway&sprefix=sony+ca%2Caps%2C162&sr=8-1-spons&psc=1.
    
    Hurry Up!!!"""
    html = """\
    <html>
    <body>
        <p>Hi Harsh,<br>
        How are you? The price has dropped for the product you were watching. You can follow the link
        <a href="https://www.amazon.com/Sony-Mirrorless-Digital-Camera-Backpack/dp/B019Y6CO90/ref=sr_1_1_sspa?crid=15PFYJLD6C71R&keywords=sony+camera&qid=1565114665&s=gateway&sprefix=sony+ca%2Caps%2C162&sr=8-1-spons&psc=1">here.</a> <br>
         Hurry Up!!!.
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    server.sendmail(
        'harsh@ekta.co',
        'harshhasd@gmail.com',
        message.as_string()
    )
    print('A mail has been sent!')

    server.quit()


# price_check()
# This loop runs every hour and gives you an update on the price
while(True):
    price_check()
    time.sleep(60 * 60)
