from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from account import *
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class Bird(object):
    # Define Bird
    def __init__(self, target:str):
        self.target = target
        self.driver = webdriver.Chrome()

    #Login System
    def login(self):

        print("Logging in...")
        self.driver.get("https://twitter.com/i/flow/login") #Login Page

        time.sleep(2 + random.uniform(0, 1)) #Sleeping so it can let page refresh and open / make twitter think we user
        #Username input
        time.sleep(random.uniform(0, 1))
        textbox = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
        for letter in username:
            textbox.send_keys(letter)
        textbox.send_keys(Keys.ENTER)

        time.sleep(1 + random.uniform(0, 1))
        #Password input
        textbox = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        for letter in password:
            textbox.send_keys(letter)
        textbox.send_keys(Keys.ENTER)
        time.sleep(1 + random.uniform(0, 1))

        print("Logged in!")

        self.driver.get(self.target)

    def bio(self):
        bio = Bird.__waitforelement(self.driver, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[3]/div/div/span')
        return bio.text

    
    def following(self):
        f = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span').text
        return f

    def followers(self):
        f = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span').text
        return f
    
    def link(self):
        f = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[4]/div/a/span').text
        return f
    
    def location(self):
        f = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[4]/div/span[1]/span/span').text
        return f
    
    
    def recent(self):
        target = Bird.__checkpinned(self.driver)
        time.sleep(1)
        f = self.driver.find_element(By.XPATH, target+'/div/div[1]/div/div')
        f.click()


        def find_id(): #This searches for the ID. it turns out that there are seperate ids for seperate things
            mainframe = Bird.__waitforelement(self.driver, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]')
            x = mainframe
            while True:
                x = x.find_element(By.XPATH, './/*')
                print(x.get_attribute('id'))
                if "id__" in x.get_attribute('id'):
                    return x.get_attribute('id')

        # Get recent ID
        id = find_id()

        result_string = ''

        for elm in self.driver.find_elements(By.XPATH, '//*[@id="'+id+'"]'):
            if elm.text:
                result_string += elm.text+ " "



        status_id = self.driver.current_url.split("/")[-1]

        return {"twitter_post_id":status_id, "twitter_link":self.target+"/status/1708142894895571418", "content":result_string}
    
    def __checkpinned(driver):
        mainframe = Bird.__waitforelement(driver, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div[1]/div/div/article/div')

        x = mainframe.find_elements(By.XPATH, '//span[text()]')
        for y in x:
            if "Pinn" in y.text:
                return '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div[2]/div/div/article/div'
        
        return '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div[1]/div/div/article/div'
    
    def __waitforelement(driver, target):
        while True:
            try:
                mainframe = driver.find_element(By.XPATH, target)
                return mainframe
            except:
                continue