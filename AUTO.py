import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASS")
CAMINHO_FATURAS = os.path.join(os.getcwd(), "Faturas")
def Config():
    print(">> Configurando Selenium Puro...")
    
    
    if not os.path.exists(CAMINHO_FATURAS):
        os.makedirs(CAMINHO_FATURAS)

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") 
    
    
    prefs = {
        "download.default_directory": CAMINHO_FATURAS,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True 
    }
    chrome_options.add_experimental_option("prefs", prefs)

    servico = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=servico, options=chrome_options)
    

    wait = WebDriverWait(driver, 20)

    Enel_N(driver, wait)
    return driver, wait

def Enel_N(driver, wait):
    try:
        

        driver.get("https://www.enel.com.br/pt-saopaulo/login.html")
        

        wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(email)
        

        wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys(password)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="formlogin"]/div/div/div[4]/button'))).click()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="spa-root"]/div/app-main/aem-page/aem-model-provider/aem-responsivegrid/div[2]/aem-responsivegrid/div/app-enel-home/div/div[3]/div/div[2]/div/div[1]/a/div'))).click()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="spa-root"]/div/app-main/aem-page/aem-model-provider/aem-responsivegrid/div[2]/aem-responsivegrid/div[1]/app-enel-debtcontrol/div/div[3]/div[1]/div/div[2]/app-enel-button/button'))).click()

        time.sleep(2)
        driver.execute_script("document.body.style.zoom='25%'")
        time.sleep(2)
        Dowload(driver, wait)
    except:
        print("erro")
        
def Dowload(driver, wait):
    print(">> Iniciando Loop de Download (5 faturas)...")
    
    
    for i in range(5, 0, -1):
        print(f">> Baixando fatura {i}...")
        try:
            
            wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="spa-root"]/div/app-main/aem-page/aem-model-provider/aem-responsivegrid/div[2]/aem-responsivegrid/div[1]/app-enel-debtcontrol/div/div[3]/div[3]/app-enel-debtcontrol-paymenthistory/div[3]/div[{i}]/div/div/div[2]/div/a'))).click()

            time.sleep(3)
            driver.execute_script("document.body.style.zoom='25%'")
            time.sleep(1)
           
            
            wait.until(EC.element_to_be_clickable((By.XPATH, '//app-enel-billsdisplay//button[last()]')))
            time.sleep(2)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[alt='baixar pdf']"))).click()
            time.sleep(5) 
            
            
            driver.back()
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="spa-root"]/div/app-main/aem-page/aem-model-provider/aem-responsivegrid/div[2]/aem-responsivegrid/div[1]/app-enel-debtcontrol/div/div[3]/div[1]/div/div[2]/app-enel-button/button'))).click()
            
            
            time.sleep(3)
            driver.execute_script("document.body.style.zoom='25%'")
            
        except Exception as e:
            driver.back() 
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="spa-root"]/div/app-main/aem-page/aem-model-provider/aem-responsivegrid/div[2]/aem-responsivegrid/div[1]/app-enel-debtcontrol/div/div[3]/div[1]/div/div[2]/app-enel-button/button'))).click()
    quit()
if __name__ == ("__main__"):
    Config()
    
