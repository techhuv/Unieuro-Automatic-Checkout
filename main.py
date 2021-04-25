# %%
# %%
import re
import pandas as pd
import multiprocessing


# %%
"""
### df
"""

# %%
# import webbrowser

# from bs4 import BeautifulSoup, NavigableString, Tag 
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import  os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
chrome_options = Options()
import time
from selenium.webdriver.common.action_chains import ActionChains
# coding=utf-8



class Scrape:
	def __init__(self):
		self.df = pd.read_csv('unieuro.csv')
		password=[]
		email=[]
		for i in self.df['EMAIL']:
			a=re.split(":", i)
			password.append(a[1])
			email.append(a[0])
		self.df['EMAIL'] = email
		self.df['password'] = password
		prefs = {"profile.default_content_setting_values.notifications" : 2}  #block notifications
		chrome_options.add_experimental_option("prefs",prefs)
		chrome_options.add_argument("--no-sandbox")
		# chrome_options.add_argument("--headless")
		chrome_options.add_argument("--disable-setuid-sandbox")
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument('--disable-features=VizDisplayCompositor')
		self.chrome_options=chrome_options

		# %%
	
	def try_again(self,a):
		print(a)

# %%
	
	def final_checkout(self,driver):
		try:
			driver.implicitly_wait(30)
			cod = '/html/body/div[1]/div/div[2]/div[2]/div/section[1]/div[3]/div/div[1]/span[2]'
			address = '/html/body/div[1]/div/div[2]/div[2]/div/section[3]/article/section[1]/div[2]/div[2]/div/div/span[1]/label'
			endgame = '/html/body/div[1]/div/div[2]/div[2]/div/section[3]/article/form/section/div[2]/font[1]/font/font/font/input'

			driver.find_element_by_xpath(cod).click()
			driver.implicitly_wait(5)
			driver.find_element_by_xpath(address).click()
			driver.implicitly_wait(3)
			#         driver.find_element_by_xpath(endgame).click() <-- dont uncomment this

			driver.close()

		except:
			try_again("final_check")

	def login(self,e,p,driver):
		try:
				mail = '/html/body/div[1]/div/div[2]/div[1]/div/section/div[1]/form/div[1]/input'
				passw = '/html/body/div[1]/div/div[2]/div[1]/div/section/div[1]/form/div[2]/input'
				enter = '/html/body/div[1]/div/div[2]/div[1]/div/section/div[1]/form/div[3]/input'

				driver.find_element_by_xpath(mail).send_keys(e)
				driver.find_element_by_xpath(passw).send_keys(p)
				driver.find_element_by_xpath(enter).click()

				driver.implicitly_wait(30)

				check = driver.find_element_by_link_text("Vai alla cassa")
				resp = check.is_displayed()
				if(resp):
				    check.click()

				self.final_checkout(driver)

		except:
			pass

	
	def check_out(self,e,p,driver):
		try:
			element = driver.find_element_by_link_text("No, grazie")
			thanks = element.is_displayed()
			if(thanks):
				element.click()

			driver.implicitly_wait(20)   

			final = driver.find_element_by_link_text("Vai alla cassa")
			resp = final.is_displayed()
			if(resp):
				final.click()

			self.login(e,p,driver)
		except:
				pass

	def available(self,e,p,driver):
		time.sleep(5)
		try:
			accept = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
			yes=accept.is_displayed()
			if(yes):
				accept.click()
		except:
			pass 
		try:
			
			element = driver.find_element_by_link_text("Aggiungi al carrello")
			# print value
			yes=element.is_displayed()
			if(yes):
				print('Adding to the cart')
				element.click()
				time.sleep(1)
				self.check_out(e,p,driver)
		except:

			print('Again checking for unavailable product')
			self.available(e,p,driver)

	def run(self,i):
		print( multiprocessing.current_process().name)
		# print(type(df))

		driver = webdriver.Chrome(ChromeDriverManager().install(),options=self.chrome_options)
		print(f"Opening the {i} th link")
		print("---------",str(i))
		driver.get(self.df['PRODUCT'][i])
		self.available(self.df['EMAIL'][i],self.df['password'][i],driver)
		# driver.close()
		time.sleep(3)

if __name__=='__main__':
	obj=Scrape()
	# first_args=obj.df
	# second_args=obj.df
	#import pdb;pdb.set_trace()

	i=0
	while i<len(obj.df):
		time.sleep(2)
		service = multiprocessing.Process(name='my_service', target=obj.run,args=(i,))
		service.start()

		i+=1
		if i<len(obj.df):
			service1 = multiprocessing.Process(name='my_service', target=obj.run,args=(i,))
			service1.start()
		
		i+=1
		if i<len(obj.df):
			service2 = multiprocessing.Process(name='my_service', target=obj.run,args=(i,))
			service2.start()
		
		i+=1

	#




# %%


# %%
# driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)


# %%

        
# final_checkout()

# %%


# %%

    


# %%


# %%
  
    
    

# %%


# %%


# %%


# %%


# %%

#     login = '/html/body/div[1]/header/section[2]/span[2]/div[2]/a'
# mail = '/html/body/div[1]/div[2]/div[2]/section[1]/div[1]/form/div[1]/input'
# passw = '/html/body/div[1]/divcheck = driver.find_element_by_link_text("RITIRA IN")


#     driver.find_element_by_xpath(login).send_keys(df['EMAIL'][i])
#     driver.find_element_by_xpath(passw).send_keys(df['PASSWORD'][i])
#     //*[@id="features"]/div[2]/section[3]/article[2]/div/div/div[2]/a[1]



# %%
# https://realpython.com/modern-web-automation-with-python-and-selenium/
# https://stackoverflow.com/questions/66303178/python-selenium-headless-threading
# https://testdriven.io/blog/building-a-concurrent-web-scraper-with-python-and-selenium/
# https://python-forum.io/Thread-How-to-run-multiple-threads-with-selenium
# https://stackoverflow.com/questions/62007674/multi-thread-requests-python3

# %%

        
        

# %%
