from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


df=pd.read_excel("Foundit Activities.xlsx")

options = Options()
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')

user_data_dir = "C:/Users/nandh/AppData/Local/Google/Chrome/User Data"
profile_name = "Profile 1"

options.add_argument(f"user-data-dir={user_data_dir}")
options.add_argument(f"profile-directory={profile_name}")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def scrape_company_info(url):
    try:
#         print(f"Navigating to: {url}")
        driver.get(url)
        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "logName")))
        email_input.clear()
        email = "aneesh0601@gmail.com"
        email_input.send_keys(email)
#         print(f"Entered email: {email}")
        

        pssd_input = driver.find_element(By.ID, "psWd")
        pssd_input.clear()
        pssd = "Anepm@23"
        pssd_input.send_keys(pssd)
#         print("Entered password.")
        

        login_button = driver.find_element(By.ID, "btnLogin")
        login_button.click()
#         print("Clicked the Login button.")
        

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "advanceMenu"))).click()
#         print("Opened the dropdown menu.")
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='jobs.jsp']"))
        ).click()
#         print("Clicked the 'Foundit' link.")
        
        try:
            original_window = driver.current_window_handle
        except:
            print("didnt set original_window")
            
        try:
            
            WebDriverWait(driver, 10).until(EC.new_window_is_opened(driver.window_handles))
        except:
            print("didnt wait for new window")
#         try:
#             # Debug: Print current window handles to check for new window
#             print("Current window handles:", driver.window_handles)
#         except:
#             print("couldnt print")
        
        
        # Get the new window and switch to it
        new_window = [w for w in driver.window_handles if w != original_window][0]
        driver.switch_to.window(new_window)
        print("Switched to the new window.")
        
        time.sleep(2)
        
        
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "query"))
        )
        
        #loop begins...
        
        for company in df['Company name'].unique():
            
        
            
            search_input.clear()
            search_input.send_keys(company)
            print(f"Entered company name: {company}")

            show_jobs_button = WebDriverWait(driver, 12).until(
                EC.element_to_be_clickable((By.ID, "find-job-btn"))
            )
            show_jobs_button.click()
#             print("Clicked the 'Show Jobs' button.")

             #<button class="btn btn-secondary buttons-excel buttons-html5" tabindex="0" aria-controls="jobTable" type="button" style=""><span>Excel</span></button>
             # Scroll down a little using JavaScript execution
            driver.execute_script("window.scrollBy(0, 300);")
            # Wait for job search results to load
            try:
                excel_button = WebDriverWait(driver, 12).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'btn') and contains(@class, 'buttons-excel')]"))
                )
            except:
                print("didnt wait 4 excel button")

            try:

                excel_button.click()
                driver.execute_script("window.scrollTo(0,0);")
            except:
                print("sdkks")
        
        
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("error_screenshot.png") 
        
#     finally:
#         driver.quit()
#         print("Browser closed.")

# Run the scraper
url = "https://knowledgemission.kerala.gov.in/login-official.jsp"
scrape_company_info(url)

