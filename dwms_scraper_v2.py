import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Streamlit UI
st.title("Company Info Scraper")
st.sidebar.title("Settings")

# File upload and sidebar inputs
uploaded_file = st.file_uploader("Upload Employers Excel file", type=["xlsx"])
email = st.sidebar.text_input("Enter your email", value="aneesh0601@gmail.com")
password = st.sidebar.text_input("Enter your password", value="Anepm@23", type="password")
user_data_dir = st.sidebar.text_input("Enter User Directory", value="C:/Users/nandh/AppData/Local/Google/Chrome/User Data")
profile_name = st.sidebar.text_input("Enter Google Profile Name", value="Profile 1")
timeout = st.sidebar.slider("Set timeout (seconds)", min_value=5, max_value=30, value=10)
start_button = st.sidebar.button("Start Scraping")

# Selenium options
options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument(f"user-data-dir={user_data_dir}")
options.add_argument(f"profile-directory={profile_name}")


def setup_driver():
    """Sets up the Chrome WebDriver with the appropriate options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Specify the path to the Chrome binary (if required)
    chrome_options.binary_location = "/usr/bin/google-chrome"

    # Use WebDriver Manager to install ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def login(driver, email, password):
    """Logs into the website using the provided email and password."""
    url = "https://knowledgemission.kerala.gov.in/login-official.jsp"
    driver.get(url)
    st.info("Navigated to login page.")
    try:
        email_input = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "logName")))
        email_input.clear()
        email_input.send_keys(email)

        password_input = driver.find_element(By.ID, "psWd")
        password_input.clear()
        password_input.send_keys(password)

        login_button = driver.find_element(By.ID, "btnLogin")
        login_button.click()
        st.success("Logged in successfully!")
    except Exception as e:
        st.error(f"Login failed: {e}")
        driver.quit()
        raise


def navigate_to_job_search(driver):
    st.write("new page")
    """Navigates to the job search page."""
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "advanceMenu"))).click()
#         st.write("Opened the dropdown menu.")
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='jobs.jsp']"))
        ).click()
#         st.write("Clicked the 'Foundit' link.")
        
        try:
            original_window = driver.current_window_handle
        except:
            st.write("didnt set original_window")
            
        try:
            
            WebDriverWait(driver, 10).until(EC.new_window_is_opened(driver.window_handles))
        except:
            st.write("didnt wait for new window")
#         try:
#             # Debug: st.write current window handles to check for new window
#             st.write("Current window handles:", driver.window_handles)
#         except:
#             st.write("couldnt st.write")
        
        
        # Get the new window and switch to it
        new_window = [w for w in driver.window_handles if w != original_window][0]
        driver.switch_to.window(new_window)
        st.write("Switched to the new window.")
        
        time.sleep(2)
        
        
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "query"))
        )
    except Exception as e:
        st.error(f"Navigation failed: {e}")
        driver.quit()
        raise


def search_and_download(driver, companies):
    """Searches for companies and downloads job data."""
    progress = st.progress(0)
    total = len(companies)

    try:
        search_input = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "query")))

        for index, company in enumerate(companies):
            try:
                search_input.clear()
                search_input.send_keys(company)
                # st.write(f"Searching for: {company}")

                show_jobs_button = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.ID, "find-job-btn"))
                )
                show_jobs_button.click()

                # Scroll and click the "Excel" button
                driver.execute_script("window.scrollBy(0, 300);")
                excel_button = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'btn') and contains(@class, 'buttons-excel')]"))
                )
                excel_button.click()
                # st.write(f"Downloaded job data for: {company}")
            except Exception as e:
                st.warning(f"Failed to process company: {company}. Error: {e}")

            # Update progress bar
            progress.progress((index + 1) / total)

            # Optional delay to prevent server throttling
            time.sleep(2)

    except Exception as e:
        st.error(f"An error occurred during job search: {e}")
        driver.save_screenshot("error_screenshot.png")
        st.image("error_screenshot.png", caption="Error Screenshot")
    finally:
        progress.progress(1.0)


# Main scraping logic
def scrape_company_info(file, email, password):
    try:
        # Load Excel file
        df = pd.read_excel(file)
        st.success("Excel file loaded successfully!")

        # Initialize WebDriver
        driver = setup_driver()

        # Perform login and navigation
        login(driver, email, password)
        navigate_to_job_search(driver)

        # Start searching and downloading
        search_and_download(driver, df["Company name"].unique())

        st.success("Scraping completed!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        if "driver" in locals():
            driver.quit()
            st.info("Browser closed.")


# Ensure the scraping only happens when the button is clicked
if start_button:
    if uploaded_file:
        scrape_company_info(uploaded_file, email, password)
    else:
        st.warning("Please upload an Excel file first.")
