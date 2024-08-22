import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Function to extract the label and corresponding value
def extract_label_value(driver, label_text):
    try:
        # Use an alternative XPath approach to locate the label and value
        label_element = driver.find_element(By.XPATH, f"//div[contains(., '{label_text}')]/following-sibling::div")
        return label_element.text.strip()
    except NoSuchElementException:
        print(f"Could not find label: {label_text}")
        return None

# Prompt for the URL
url = input("Enter the URL of the property page: ")

# Initialize the WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")  # Run Chrome in incognito mode
chrome_options.add_argument("--no-sandbox")  # Required if running on a server
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--log-level=3")  # Suppress console log output

# Initialize the Chrome WebDriver with options
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# Increase timeout for element loading
try:
    wait = WebDriverWait(driver, 30)  # Increased timeout to 30 seconds
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(., 'Address')]")))
except TimeoutException:
    print("Timeout while waiting for the page to load. Check if you are logged in and if the page structure has changed.")
    driver.quit()
    exit(1)

# Verify if we are redirected to a login page
current_url = driver.current_url
if "login" in current_url or "signin" in current_url:
    print("You have been redirected to a login page. Please log in and try again.")
    driver.quit()
    exit(1)

# Extract the required data
data = {
    "Asking Price": extract_label_value(driver, "Asking Price"),
    "Address": extract_label_value(driver, "Address"),
    "Date Added": extract_label_value(driver, "Date Added"),
    "Days on Market": extract_label_value(driver, "Days on Market"),
    "Time Since Last Update": extract_label_value(driver, "Time Since Last Update"),
    "Property Type": extract_label_value(driver, "Property Type"),
    "Subtype": extract_label_value(driver, "Subtype"),
    "Investment Type": extract_label_value(driver, "Investment Type"),
    "Class": extract_label_value(driver, "Class"),
    "Square Footage": extract_label_value(driver, "Square Footage"),
    "Units": extract_label_value(driver, "Units"),
    "Year Built": extract_label_value(driver, "Year Built"),
    "Stories": extract_label_value(driver, "Stories"),
    "Zoning": extract_label_value(driver, "Zoning"),
    "Parking (spaces)": extract_label_value(driver, "Parking (spaces)"),
    "Ground Lease": extract_label_value(driver, "Ground Lease"),
    "Marketing Description": extract_label_value(driver, "Marketing Description"),
}

# Print the extracted data
for label, value in data.items():
    print(f"{label}: {value}")

# Save the data to a CSV file
with open("scraped_data.csv", "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Label", "Value"])
    for label, value in data.items():
        writer.writerow([label, value])

# Save the data to a JSON file
with open("scraped_data.json", "w", encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, indent=4)

# Close the browser
driver.quit()
