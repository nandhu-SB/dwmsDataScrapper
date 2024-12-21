# DWMS WEBSCRAPPER v2
## helloii Nandhu here,Detailed ReadMe docs generated from chat gpt becuse i was low on time,If you have any doubts first read this,then if you have any doubts read this again,And then if you have any doubts ,just contact me.Enjoy

### important points:
#### If chrome driver exception comes up,use google chrome Version 104.0.5112.81 (Official Build) (64-bit) OR Version 131.0.6778.205 (Official Build) (64-bit) , or sometimes chrome driverumai match aakamatten.Download the mentioned version and then turn off the auto update in the google chrome settings.I have also included a working google chrome setup with this .
#### aneeshettante login ithil .env akkathe public aakki vachittund,so use it carefully
#### dwms_scrapper.py 21,22 lines <br>
#### user_data_dir = "C:/Users/nandh/AppData/Local/Google/Chrome/User Data" <br>
#### profile_name = "Profile 1" <br>
#### Ith ningalude systathile google profilumayit match aakkanam



# Web Scraper for Automating Job Portal Tasks

## Overview
This project automates interactions with a job portal using Selenium. The script logs into the portal, navigates to the job search section, performs searches for company names from a dataset, and downloads job information as Excel files.

---

## Features
- Automates login using pre-defined credentials.
- Navigates to specific sections of the job portal.
- Iterates through a list of company names and performs searches.
- Downloads job search results as Excel files.
- Handles multiple browser windows and ensures smooth transitions between them.
- Provides error handling and debug information via screenshots and console logs.

---

## Prerequisites

### Software Requirements:
- Python 3.7 or higher
- Google Chrome browser

### Python Dependencies:
Install the required libraries by running:
```bash
pip install -r requirements.txt
```
The `requirements.txt` file contains:
```
selenium==4.12.0
webdriver-manager==3.8.6
pandas==2.1.1
```

---

## Configuration

1. **User Data Directory:**
   Update the `user_data_dir` and `profile_name` variables in the script with the path to your Chrome user profile.
   ```python
   user_data_dir = "C:/Users/nandh/AppData/Local/Google/Chrome/User Data"
   profile_name = "Profile 1"
   ```

2. **Login Credentials:**
   Replace the `email` and `pssd` variables with your login email and password:
   ```python
   email = "your_email@example.com"
   pssd = "your_password"
   ```

3. **Dataset:**
   Ensure you have a DataFrame `df` containing a column `Company name` with the list of companies to search for.

---

## How to Use

1. **Run the Script:**
   Execute the Python script:
   ```bash
   python scraper.py
   ```

2. **Login Automation:**
   The script will automatically log into the portal using the provided credentials.

3. **Job Search:**
   The script will iterate through the company names in `df` and perform searches on the portal.

4. **Downloading Results:**
   For each search, the script will download the results as an Excel file.

---

## Error Handling
- If an error occurs, the script saves a screenshot named `error_screenshot.png` in the working directory.
- Console logs provide detailed debug information about failures in locating elements or performing actions.

---

## Limitations
- The script depends on specific HTML element IDs and XPaths, which may change if the portal is updated.
- Requires Google Chrome and the appropriate ChromeDriver version.

---

## Future Enhancements
- Add support for headless browsing to improve performance.
- Implement dynamic credential management for enhanced security.
- Support for multiple job portals.
- Add retry mechanisms for failed operations.

---

## Disclaimer
This script is intended for educational purposes. Ensure you comply with the terms of service of the website you are automating and obtain necessary permissions before scraping data.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
