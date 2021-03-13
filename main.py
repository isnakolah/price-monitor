import time
import requests
import smtplib

from bs4 import BeautifulSoup


# TODO: Add functionality where state a range in which you are comfortable purchasing
# If the price drops by a certain percentage, you send email.

# To be done
# Create a sort of a database, text based data.
# Write to a file -> date: price e.g Date: 13/03/2021:6:53 Price: 2500
# Check the pricing if it has reduced by the stated percentage

# Write/Read to/from a file
# How to use git and github - add, commit, push


URL = "https://www.jumia.co.ke/fashion-ladies-open-ankle-strapped-chunky-heel-black-35027396.html"

headers = {
    "User Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}


# check_price function checks the price of a listing
def check_price(myPrice, margin=0):

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find('h1', {'class': '-fs20 -pts -pbxs'}).get_text()
    str_price = soup.find('span', {'class': '-fs24'}).get_text()
    price = int(''.join(str_price.split(' ')[1].split(',')))

    if price <= myPrice:
        send_email(current_price=price)
        return
    print(f"THE PRICE IS NOT BELOW Ksh {myPrice}, IT IS Ksh {price}")
    return


# send_email function sends an email based on the price
def send_email(current_price=0, message=""):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('nakolahdaniel1@gmail.com', 'jltxloxagtmqoqmh')

    if message != "":
        server.sendmail(
            'nakolahdaniel1@gmail.com',
            'wanjirungugi30@gmail.com',
            {message}
        )
        return

    subject = 'Price within range!!'
    body = f'Price is {current_price}. Check the Jumia link {URL}'

    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(
        'nakolahdaniel1@gmail.com',
        'wanjirungugi30@gmail.com',
        msg
    )
    print('HEY! EMAIL HAS BEEN SENT')
    server.quit()
    return


if __name__ == "__main__":
    while True:
        try:
            check_price(1500)
            print("waiting 30 mins to check again...")
            time.sleep(30*60)
        except KeyboardInterrupt:
            print('^C pressed, exiting...')
            break
        except:
            send_email(message="Server is down")
            break
