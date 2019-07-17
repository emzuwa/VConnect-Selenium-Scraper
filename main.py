import requests
from selenium import webdriver
from bs4 import BeautifulSoup


def vconnect_scrape(occupation, location):
    py_path = r'C:\Python\Python35-32\driver\phantomjs-2.1.1-windows\bin\phantomjs.exe'
    path = r'.\third_party\phantomjs-2.1.1-windows\bin\phantomjs.exe'
    driver = webdriver.PhantomJS(executable_path = path)

    query = occupation
    file_name = '{} - {}.txt'.format(occupation, location)

    for page in range(1, 101):
        global page_links, bus_name, url
        url = "https://www.vconnect.com/qsearch?sq={}&sl={}&page=".format(query, location)
        driver.get(url + str(page))
        soup = BeautifulSoup(driver.page_source, "lxml")

        divs = soup.find_all(class_="business-sidebar-actions ")
        page_links = []
        for tag in divs:
            link = tag.find('a').get('href')
            page_links.append(link)

        if len(page_links) == 0:
            break

        name, contact, email = '"businessname":"', '"contactperson":"', '"email":"'
        phone, alt_phone, address = '"phone":"', '"alternatephone":"', '"fulladdress":"'
        state, area, city, houseno = '"state":"', '"area":"', '"city":"', '"houseno":"'
        latt, long = '"lattiude":"', '"longitude":"'
        shortdesc = '"shortdesc":"'
        for business in page_links:
        ##    html = requests.get(business)
        ##    soup2 = BeautifulSoup(html.text, "lxml")
            driver.get(business)
            soup2 = BeautifulSoup(driver.page_source, "lxml")

            scr = soup2.find_all('script')
            script = scr[-3]

            bus_name = str(script).split(name)[-1].split('"')[0]
            if bus_name == '': bus_name = 'No Company Name'
            
            bus_contact = str(script).split(contact)[-1].split('"')[0]
            if bus_contact == '': continue#bus_contact = 'No Contact Person'
            
            bus_email = str(script).split(email)[-1].split('"')[0]
            if bus_email == '': bus_email = 'No email'
            
            bus_phone = str(script).split(phone)[-1].split('"')[0]
            if bus_phone == '': bus_phone = 'No Phone'
            
            bus_altphone = str(script).split(alt_phone)[-1].split('"')[0]
            if bus_altphone =='': bus_altphone = 'No alt Phone'
            
            bus_address = str(script).split(address)[-1].split('"')[0]
            if bus_address == '': bus_address = 'No address'

            bus_state = str(script).split(state)[-1].split('"')[0]
            if bus_state == '': bus_state = 'No State'

            bus_area = str(script).split(area)[-1].split('"')[0]
            if bus_area == '': bus_area = 'No Area'

            bus_city = str(script).split(city)[-1].split('"')[0]
            if bus_city == '': bus_city = 'No City'

            bus_houseno = str(script).split(houseno)[-1].split('"')[0]
            if bus_houseno == '': bus_houseno = 'No House Number'

            bus_long = str(script).split(long)[-1].split('"')[0]
            if bus_long == '': bus_long = 'No Longitude position'

            bus_latt = str(script).split(latt)[-1].split('"')[0]
            if bus_latt == '': bus_latt = 'No Lattitude position'

            bus_shortdesc = str(script).split(shortdesc)[-1].split('"')[0]
            if bus_shortdesc == '': bus_shortdesc = 'No Short Description'

            doc = open(file_name, 'a')
            doc.write(bus_name + '\t\t' + bus_contact + '\t\t' + bus_email + '\t\t' +
                      bus_phone + '\t\t' + bus_altphone + '\t\t' + bus_address + '\t\t' +
                      bus_state + '\t\t' + bus_area + '\t\t' + bus_city + '\t\t' + bus_houseno + '\t\t' + bus_long + '\t\t' + bus_latt + '\t\t' + bus_shortdesc + '\n\n')
            doc.close()
            print('A business has been recorded.')
        print('Page {} has been scraped.'.format(page))
            
    driver.quit()

    
file = open("list of occupations in nigeria.txt").readlines()
occupations = []
for item in file:
    occupations.append(item.replace('\n', ''))
    
    
file2 = open("Local Government in Nigeria.txt").readlines()
locations = []
for item in file2:
    locations.append(item.replace('\n', ''))


for occupation in occupations:
    for area in locations:
        vconnect_scrape(occupation, area)
