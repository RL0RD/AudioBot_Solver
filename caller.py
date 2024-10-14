from DrissionPage import ChromiumPage 
from AudioBot_Solver import Captcha_Atack
import time


driver = ChromiumPage()
recaptchaSolver = Captcha_Atack(driver)

driver.get("https://www.google.com/recaptcha/api2/demo")


t0 = time.time()
recaptchaSolver.solveCaptcha()
print(f"tiempo de solución captcha: {time.time()-t0:.2f} segundos")

driver.ele("#recaptcha-demo-submit").click()

driver.get("https://drive.google.com/file/d/1K1QS6Hcnd5Dppf2bIzu45wYKYcEL7tkf/view?usp=sharing")
time.sleep(25)

driver.close()

