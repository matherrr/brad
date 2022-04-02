from selenium import webdriver

class insta:

    ChromeOptions ={

    }

    def __init__(self) : 
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.__driver = webdriver.Chrome('chromedriver',options=self.options)
        
    @property
    def driver(self):
        if not (self.__driver):
            self.__driver = webdriver.Chrome('chromedriver',options=self.options)
        return self.__driver


    def chrome(self,url,keyword,add=''):

        return self.driver.get(url+'/'+keyword+'/'+add)


    def js_excute(self,url,keyword,js):

        self.chrome(url,keyword)
        print('return '+js)
        try:        
            return self.driver.execute_script('return '+js)
        except:
            return 'excute error'

    def __exit__(self, *args) :  
        self.driver.quit()