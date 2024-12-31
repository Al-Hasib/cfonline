import os, json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from src.Tele import SendPdf, TryAgainMsg
from src.Tele import SendPdf
from src.img import convert_folder_to_pdf
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


if not os.path.exists('PDF'):
    os.mkdir('PDF')


with open('Config.json', 'r') as f:
    config = json.load(f)

url = config['url']
email = config['email']
pasw = config['password']
apiToken = '6625435370:AAG2rib8Oplf02kzYp0eGNR-rlleoo338uE'
chatID = '5491808070'

download_directory = os.path.join(os.getcwd(), 'PDF')
# 100.0.1216.0
# agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/100.0.1216.0 Safari/537.2'
agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

def get_browser(headless=False, proxy=False):
    path = ChromeDriverManager().install()
    path = path.replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver.exe")
    s = Service(executable_path=path)
    chrome_option = webdriver.ChromeOptions()
    if headless:
        chrome_option.add_argument('--headless')
        chrome_option.add_argument(f'user-agent={agent}')

    chrome_option.add_argument('--log-level=3')
    chrome_option.page_load_strategy = "none"
    chrome_option.add_argument('--ignore-certificate-errors')
    chrome_option.add_argument('--ignore-ssl-errors')
    chrome_option.add_argument('--ignore-certificate-errors-spki-list')
    prefs = {"profile.managed_default_content_settings.images": 1}
    chrome_option.add_experimental_option("prefs", prefs)
    chrome_option.add_experimental_option("useAutomationExtension", False)
    chrome_option.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    chrome_option.add_argument("--disable-web-security")
    driver = webdriver.Chrome(service=s, options=chrome_option)    
    return driver


def main(url, email, pasw, vin, api_token, chat_id, driver):
    driver.implicitly_wait(30)
    try:
        print("scraping vin search page....")
        vin_input = driver.find_element(By.ID, 'vin')
        vin_input.clear()
        vin_input.send_keys(vin)
        submit = driver.find_element(By.ID, 'run_vhr_button')
        driver.execute_script("arguments[0].click();", submit)
        sleep(10)
        
        if len(driver.window_handles) > 1:
            print("inside if condition")
            driver.switch_to.window(driver.window_handles[1])
            # body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            # body.send_keys(Keys.F5)
            
            print("web driver wait")
            wait = WebDriverWait(driver, 120)  # Replace "timeout_in_seconds" with your desired wait time
            print("web driver wait for t seconds")
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "report-header-print-button")))
            print("executing script")

            driver.execute_script("document.querySelector('.do-not-print').style.display='none';")


            width = driver.execute_script("return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);")
            height = driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
            print("width: ", width)
            print("height:", height)


            driver.set_window_size(width, height)   
            scroll_height = driver.execute_script("return window.innerHeight")

            try:
                driver.execute_script("document.querySelector('.back-to-top-button').style.display='none';")
            except Exception as e:
                print("no back to top button")

            scroll_offset = 0
            counter = 1
            print("saving screenshot")
            driver.save_screenshot('screenshots/Image_1.png')
            while scroll_offset < (height - (scroll_height)):
                try:
                    driver.execute_script("document.querySelector('.back-to-top-button').style.display='none';")
                except Exception as e:
                    print("no back to top button")
            
                print("running while")
                driver.execute_script(f"window.scrollTo(0, {scroll_offset})")
                sleep(2)
                driver.save_screenshot(f'screenshots/Image_{counter}.png')
                scroll_offset += scroll_height
                counter += 1

            input_path = 'screenshots'
            output_path = 'PDF/' + vin + '.pdf'
            convert_folder_to_pdf(folder_path=input_path, output_path=output_path)
            print('Pdf Formatting...')
            SendPdf(vin=vin, chat_id=chat_id,bot_token=api_token)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
            driver.maximize_window()
            
            if os.path.exists("screenshots"):
                # Directory exists, remove files within it
                for filename in os.listdir("screenshots"):
                    file_path = os.path.join("screenshots", filename)
                    os.remove(file_path)  # Remove individual files
            else:
                # Directory doesn't exist, create it
                os.makedirs("screenshots")
        else:
            print('Nothing found...')
            TryAgainMsg(chat_id=chat_id, bot_token=api_token)
    except Exception as e:
        print("exception: ", str(e))


def main_api(url, email, pasw, vin, driver):
    driver.implicitly_wait(30)
    try:
        print("scraping vin search page....")
        vin_input = driver.find_element(By.ID, 'vin')
        vin_input.clear()
        vin_input.send_keys(vin)
        submit = driver.find_element(By.ID, 'run_vhr_button')
        driver.execute_script("arguments[0].click();", submit)
        sleep(10)
        
        if len(driver.window_handles) > 1:
            print("inside if condition")
            driver.switch_to.window(driver.window_handles[1])
            # body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            # body.send_keys(Keys.F5)
            
            print("web driver wait")
            wait = WebDriverWait(driver, 120)  # Replace "timeout_in_seconds" with your desired wait time
            print("web driver wait for t seconds")
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "report-header-print-button")))
            print("executing script")

            driver.execute_script("document.querySelector('.do-not-print').style.display='none';")


            width = driver.execute_script("return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);")
            height = driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
            print("width: ", width)
            print("height:", height)


            driver.set_window_size(width, height)   
            scroll_height = driver.execute_script("return window.innerHeight")

            try:
                driver.execute_script("document.querySelector('.back-to-top-button').style.display='none';")
            except Exception as e:
                print("no back to top button")

            scroll_offset = 0
            counter = 1
            print("saving screenshot")
            driver.save_screenshot('screenshots/Image_1.png')
            while scroll_offset < (height - (scroll_height)):
                try:
                    driver.execute_script("document.querySelector('.back-to-top-button').style.display='none';")
                except Exception as e:
                    print("no back to top button")
            
                print("running while")
                driver.execute_script(f"window.scrollTo(0, {scroll_offset})")
                sleep(2)
                driver.save_screenshot(f'screenshots/Image_{counter}.png')
                scroll_offset += scroll_height
                counter += 1

            input_path = 'screenshots'
            output_path = 'PDF/' + vin + '.pdf'
            convert_folder_to_pdf(folder_path=input_path, output_path=output_path)
            print('Pdf Formatting...')
            # SendPdf(vin=vin, chat_id=chat_id,bot_token=api_token)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
            driver.maximize_window()
            
            if os.path.exists("screenshots"):
                # Directory exists, remove files within it
                for filename in os.listdir("screenshots"):
                    file_path = os.path.join("screenshots", filename)
                    os.remove(file_path)  # Remove individual files
            else:
                # Directory doesn't exist, create it
                os.makedirs("screenshots")
        else:
            print('Nothing found...')
            # TryAgainMsg(chat_id=chat_id, bot_token=api_token)
    except Exception as e:
        print("exception: ", str(e))

if __name__ == '__main__':
    vin = input('Enter Vin Number: ').strip()
    main(url='https://www.carfaxonline.com/', email=email, pasw=pasw, vin=vin, api_token=apiToken, chat_id=chatID)