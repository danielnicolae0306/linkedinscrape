from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import csv
print('S-au importat modulele')

driver = webdriver.Chrome("chromedriver.exe")
sleep(2)
url = 'https://www.linkedin.com/login'
driver.get(url)
print('Se initializeaza driverul')
sleep(2)

credential = open('login.txt')
line = credential.readlines()
nume = line[0]
parola = line[1]
print('S-au importat datele de logare')
sleep(2)

email = driver.find_element_by_id('username')
email.send_keys(nume)
print('S-a importat email')
sleep(3)

password_field = driver.find_element_by_name('session_password')
password_field.send_keys(parola)
print('S-a importat parola')
sleep(2)

logare = driver.find_element_by_xpath(
    '//*[@id="organic-div"]/form/div[3]/button')
logare.click()
sleep(3)

print('Ne-am logat pe linkedin')

cautare = driver.find_element_by_xpath(
    '//*[@class="search-global-typeahead__input always-show-placeholder"]')

cautare_profile = input('Ce profile doriti sa cautati? ')
cautare.send_keys(cautare_profile)

cautare.send_keys(Keys.RETURN)

print('S-au cauatat profilele')


def adunaURL():
    sursapagina = BeautifulSoup(driver.page_source)
    profilele = sursapagina.find_all('a', class_='app-aware-link')
    URLprofile = []
    for profile in profilele:
        profilURL = profile.get('href')
        if profilURL not in URLprofile:
            URLprofile.append(profilURL)
    return URLprofile


introducerepagini = int(input('Cate pagini doriti sa cautati? '))
URLpagini = []
for page in range(introducerepagini):
    URLpagina = adunaURL()
    sleep(2)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(1)
    pagian_urmatoare = driver.find_element_by_id(
        "ember330")
    driver.execute_script("arguments[0].click();", pagian_urmatoare)
    URLpagini = URLpagini + URLpagina


print('S-a facut scrape pe url-urile profilelor')

numefisier = "date.csv"
coloane = ["link", 'nume', 'locatie', 'titlu']
with open(numefisier, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(coloane)
    for linkedin_URL in URLpagini:
        driver.get(linkedin_URL)
        print('Se acceseaza profilul', linkedin_URL)
        sleep(3)
        sursa_pagina = BeautifulSoup(driver.page_source, "html.parser")
        info_div = sursa_pagina.find('div', {'class': 'mt2 relative'})
        name = info_div.find('h1', {
                             'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).get_text().strip()
        print('Numele profilului: ', name)
        location = info_div.find('span', {
                                 'class': 'text-body-small inline t-black--light break-words'}).get_text().strip()
        print('Locatia: ', location)
        title = info_div.find(
            'div', {'class': 'text-body-medium break-words'}).get_text().strip()
        print('Titlul: ', title)
        csvwriter.writerow([linkedin_URL, name, location, title])

print('S-a terminat cautarea')
