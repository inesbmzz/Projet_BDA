from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
import csv

# Configure the driver and the wait time
WAIT_TIMEOUT = 20
driver = webdriver.Chrome()

# 1. [Bookimed](https://us-uk.bookimed.com/clinics/illness=autism/)
# 
# 16 Verified Autism Treatment Clinics Globally
url = 'https://us-uk.bookimed.com/clinics/illness=autism/'

# Initialize the driver and open the URL
driver.get(url)
driver.maximize_window()

# Clean some distracting elements from the page
WebDriverWait(driver, WAIT_TIMEOUT).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.cookie-button.cookie-solution button'))).click()
driver.execute_script('arguments[0].remove()', WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, 'clinics-sticky'))))

# Get the cards of the clinics
cards = WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#clinics.clinics-list div[index]')))

# Extract the data from the cards
data: list[list[str]] = []
for card in cards:
    try:
        # Extract info from the main card
        content_element = WebDriverWait(card, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.clinic-card > .clinic-card__content-container > .clinic-card__content')))
        header_element = content_element.find_element(By.CSS_SELECTOR, '.clinic-card__title')
        title_element = header_element.find_element(By.CSS_SELECTOR, 'div:first-child > h2 > a')
        title = title_element.text.strip()
        link = title_element.get_attribute('href')
        address = header_element.find_element(By.CSS_SELECTOR, '.clinic-card__country ').text.strip()

        # Open the modal and extract info and then close the modal
        WebDriverWait(card, WAIT_TIMEOUT).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.clinic-card__text-container .clinic-card__show-text'))).click()
        modal_wrapper = WebDriverWait(card, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.clinic-card__modal .card-info__wrapper')))
        modal_info = modal_wrapper.find_element(By.CSS_SELECTOR, '.card-info')
        modal_info_block = modal_info.find_element(By.CSS_SELECTOR, '.card-info__container > .card-info__content > .card-info__content-item.active > .card-info__info-block')
        modal_info_block_content = [el.text.strip() for el in modal_info_block.find_elements(By.CLASS_NAME, 'card-info__info-clinic')]
        free_quote_link = modal_info.find_element(By.CSS_SELECTOR, '.card-info__buttons > a').get_attribute('href')
        WebDriverWait(modal_wrapper, WAIT_TIMEOUT).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.card-info__close'))).click()
        
        data.append([title, link, address, ', '.join(modal_info_block_content), free_quote_link])
    except:
        print(f'Error in Card: {card.get_attribute('index')}')
        continue

# Extract location info from each clinic page
for clinic_data in data:
    try:
        driver.get(clinic_data[1])
        clinic_map = WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section.clinic-page__map')))
        address = clinic_map.find_element(By.CLASS_NAME, 'clinic-page__map-title').text.strip()

        # Scroll to the map to load the iframe
        driver.execute_script('arguments[0].scrollIntoView(true);', clinic_map)

        # Extract the latitude and longitude from the map iframe
        clinic_map_iframe = WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section.clinic-page__map .lazy-component > iframe')))
        map_parsed_url = urlparse(clinic_map_iframe.get_attribute('src'))
        map_query = parse_qs(map_parsed_url.query)
        [latitude, longitude] = map_query['ll'][0].split(',')

        clinic_data[1] = clinic_data[2]
        clinic_data[2] = address
        clinic_data.extend([latitude, longitude])
    except:
        print(f'Error in Clinic: {clinic_data[0]}')
        continue

# Switch '0' to '' in latitude and longitude
for clinic_data in data:
    clinic_data[5] = '' if clinic_data[5] == '0' else clinic_data[5]
    clinic_data[6] = '' if clinic_data[6] == '0' else clinic_data[6]

# Write the data to a CSV file
with open('data/autism_treatment_centers_bookimed.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'country', 'address', 'info', 'free_quote_link', 'latitude', 'longitude'])
    writer.writerows(data)

# 2. [Autism Now](https://autismnow.org/map/)
# 
# A growing collection of agencies across the United States that offer services and resources centered on autism and other developmental disabilities
url = 'https://autismnow.org/map/'

# Function to click on the next state link each time
i = 1
def click_link() -> str:
    global i
    try:
        # Open the main URL
        driver.get(url)
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li#toc-nav'))).click()

        # Remove distracting elements
        ele_to_remove = WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#screenOptions')))
        driver.execute_script('arguments[0].remove()', ele_to_remove)

        # Click on the state link
        states_links = WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#stateTOC li > a')))
        if i > 1: # i >= len(states_links):
            return None
        state_name = states_links[i].text.strip()
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.element_to_be_clickable(states_links[i])).click()
        i += 1
        return state_name
    except:
        print(f'Error in State: {state_name}')
        return None

# Extract data from each state page
clinics_data = []
while state_name := click_link():
    try:
        # Extract the clinics data
        clinics_rows = WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.state-list tbody > tr')))
        clinics_matrix = [clinic.find_elements(By.CSS_SELECTOR, 'td') for clinic in clinics_rows]
        clinics_names = [row[0].find_element(By.CSS_SELECTOR, 'a').text.strip() for row in clinics_matrix]
        clinics_links = [row[0].find_element(By.CSS_SELECTOR, 'a').get_attribute('href') for row in clinics_matrix]
        clinics_cities = [row[1].text.strip() for row in clinics_matrix]
        clinics_counties = [row[2].text.strip() for row in clinics_matrix]
        iter_list = list(zip(clinics_names, clinics_links, clinics_cities, clinics_counties))

        # Extract the contact info for each clinic
        for name, link, city, county in iter_list[9:] if i == 48 else iter_list:
            driver.get(link)
            contact_element = WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Contact information')]/following-sibling::p[1]")))
            clinics_data.append([name, state_name, city, county, contact_element.text.strip()])
    except:
        print(f'Error in State: {state_name}')
        continue

# Write the data to a CSV file
with open('data/autism_treatment_centers_autism_now.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'state', 'city', 'county', 'contact info'])
    writer.writerows(clinics_data)

# Close the driver
driver.quit()