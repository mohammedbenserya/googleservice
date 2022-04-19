import requests,time
import urllib.parse
from bs4 import BeautifulSoup as bs4

import os,time,json
from flask import request,make_response
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver import ActionChains

import flask

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    
    query = request.args.get('q')
    op = webdriver.ChromeOptions()
    op.binary_location="/app/.apt/usr/bin/google-chrome"  
    op.add_argument('--headless')
    op.add_argument('--disable-gpu')
    op.add_argument('--no-sandbox')
    op.add_argument('--disable-dev-shm-usage')
    op.add_argument('--remote-debugging-port=9222')

    driver=webdriver.Chrome(executable_path="/app/.chromedriver/bin/chromedriver",options=op)
    driver.get("https://www.google.com/localservices/prolist?g2lbs=AGgkzMy4oY4otlYACabgYCnMb_Bhi0K-SXnTNHTpp7xOyblgDn-Ww4ApC_1XVdSCw0F3BIXdV93jN1W0mh3uxImDy-PmUsWbtw%3D%3D&hl=en-US&gl=us&ssta=1&oq=licensed%20contractors%20in%20texas&src=2&origin=https%3A%2F%2Fwww.google.com&sa=X&scp=ChdnY2lkOmFzcGhhbHRfY29udHJhY3RvchJOEhIJffSKNVXF8IcR7z58vRXIRcMaEgl99Io1VcXwhxHvPny9FchFwyIOQXVzdGluIE1OLCBVU0EqFA2fJAMaFT32jMgdKiINGiVytJ3IGhJhc3BoYWx0IGNvbnRyYWN0b3IqEmFzcGhhbHQgY29udHJhY3Rvcg%3D%3D&q="+urllib.parse.quote(query))
    data=[]
    while True:

        
        links=driver.find_elements(By.XPATH,'//div[@jscontroller="xkZ6Lb"]')
        for link in links:
            try:
                print('...')
                url='https://www.google.com'+str(link.get_attribute('data-profile-url-path'))
                res = requests.get(url)
                soup =bs4(res.text,'lxml')
                title= soup.select_one(".TZpmYe").text
                phone = soup.select_one('.eigqqc').text
                adress = soup.select_one('.fccl3c').text.split(',')
                city=adress[-2]
                state=adress[-1].split(' ')[1]
                service =soup.select_one('.AQrsxc')
                service=(service.text.replace('Services: ', ''))
                data.append({"title":title,'phone':phone,"city":city,'state':state,'industry':service,'email':''})
                print(title + " Done !")
            except:
                pass
            #//*[@id="yDmH0d"]/c-wiz[3]/div/div[2]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div/div[1]
            ##yDmH0d > c-wiz:nth-child(18) > div > div:nth-child(2) > div > div > div.XJInM > div.YhtaGd.aQOEkf > div.jq95K > c-wiz > div > div > div.Jtakfe > c-wiz > div > div:nth-child(1) D1X2y fccl3c VfPpkd-Jh9lGc

            
        ele =driver.find_element(By.TAG_NAME,'body')
        ele.send_keys(Keys.END)
        try:
            
            div =WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@jsname="db9cze"]')))
            ActionChains(driver).click(div).perform()
            driver.refresh()
            
        except:
            print("All Done")
            break
    df = pd.DataFrame.from_dict(data)

    resp = make_response(df.to_csv(index = False,header=True, encoding='utf-8'))
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp

if __name__ == "__main__":
 app.run()