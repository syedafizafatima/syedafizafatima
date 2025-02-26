from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import csv
from datetime import datetime

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_hospitals():
    driver = setup_driver()
    # Create a list to store all hospital data
    all_hospitals = []
    
    try:
        # Navigate to the page
        driver.get("https://www.fhpl.net/WhatsappNetworkhospitals/")
        
        # Wait for the insurance dropdown to be present
        insurance_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddinsurance"))
        )
        
        # Select Magma HDI
        Select(insurance_dropdown).select_by_visible_text("Magma HDI General Insurance Company Ltd")
        time.sleep(2)
        
        # Select State (Telangana)
        state_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlState"))
        state_dropdown.select_by_visible_text("Telangana")
        time.sleep(2)
        
        # Select City (Hyderabad)
        city_dropdown = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlCity"))
        city_dropdown.select_by_visible_text("Hyderabad")
        time.sleep(2)
        
        # Click Search button
        search_button = driver.find_element(By.ID, "ContentPlaceHolder1_btnGo")
        search_button.click()
        time.sleep(3)
        
        # Find and extract data from the table
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_grdProviderDetails"))
        )
        
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        # Skip header row and process data rows
        for row in rows[1:]:  # Skip header row
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 4:
                hospital_data = {
                    'Serial No': cols[0].text.strip(),
                    'Hospital Name': cols[1].text.strip(),
                    'Address': cols[2].text.strip(),
                    'Contact': cols[3].text.strip()
                }
                all_hospitals.append(hospital_data)
                print(hospital_data)  # Still print for monitoring
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hospitals_data_.csv"
        
        # Write to CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Define CSV headers
            fieldnames = ['Serial No', 'Hospital Name', 'Address', 'Contact']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write headers and data
            writer.writeheader()
            writer.writerows(all_hospitals)
            
        print(f"\nData has been saved to {filename}")
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_hospitals()
