#Import the libraries
from bs4 import BeautifulSoup
import requests
import time
import smtplib
import ssl
from email.mime.text import MIMEText as MT
from email.mime.multipart import MIMEMultipart as MM

#Create a function to get the price of a cryptocurrency
def get_crypto_price(coin):
  #Get the URL
  url = "https://www.google.com/search?q="+coin+"+price"
#Make a request to the website
  HTML = requests.get(url)
#Parse the HTML
  soup = BeautifulSoup(HTML.text, 'html.parser')
#Find the current price
  text = soup.find("div", attrs={'class':'BNeawe iBp4i AP7Wnd'}).text
#Return the text
  return text
  
  #Store the email addresses for the receiver, and the sender and store the senders password
receiver = '<Receiver's email address>'
sender = '<Sender's email address>'
sender_password = '<Sender's password>'

#Create a function to send emails
def send_email(sender, receiver, sender_password, text_price):
  #Create a MIMEMutltipart Object
  msg = MM()
  msg['Subject'] = "New Crypto Price Alert !"
  msg['From']= sender
  msg['To']= receiver
#Create the HTML for the message
  HTML = """
    <html>
      <body>
        <h1>New Crypto Price Alert !</h1> 
        <h2>"""+text_price+"""
        </h2>
      </body>
    </html>
    """
  #Create a html MIMEText Object
  MTObj = MT(HTML, "html")
  #Attach the MIMEText Object
  msg.attach(MTObj)
#Create the secure socket layer (SSL) context object
  SSL_context = ssl.create_default_context()
  #Create the secure Simple Mail Transfer Protocol (SMTP) connection
  server = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=SSL_context)
  #Login to the email
  server.login(sender, sender_password)
  #Send the email
  server.sendmail(sender, receiver, msg.as_string())
  
  #Create a function to send the alert
def send_alert():
  last_price = -1
  #Create an infinite loop to continuously send/show the price 
  while True:
    #Choose the cryptocurrency/coin
    coin = 'bitcoin'
    #Get the price of the cryptocurrency
    price = get_crypto_price(coin)
    #Check if the price has changed
    if price != last_price:
      print(coin.capitalize()+' price: ', price)
      price_text = coin.capitalize()+' is '+price
      send_email(sender, receiver, sender_password, price_text)
      last_price = price #Update the last price
      time.sleep(2)
