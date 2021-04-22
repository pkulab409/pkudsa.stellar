from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

LOCAL_DIR = os.path.dirname(__file__)

class SeleniumClass:
    def __init__(self):
        self.__url = 'https://mi.js.org/dsa21vis/battleground.html'
        self.__driverPath = os.path.join(LOCAL_DIR, 'chromedriver.exe')

        self.JS_DROP_FILE ="""
    var target = arguments[0],
        offsetX = arguments[1],
        offsetY = arguments[2],
        document = target.ownerDocument || document,
        window = document.defaultView || window;

    var input = document.createElement('INPUT');
    input.type = 'file';
    input.onchange = function () {
      var rect = target.getBoundingClientRect(),
          x = rect.left + (offsetX || (rect.width >> 1)),
          y = rect.top + (offsetY || (rect.height >> 1)),
          dataTransfer = { files: this.files };

      ['dragenter', 'dragover', 'drop'].forEach(function (name) {
        var evt = document.createEvent('MouseEvent');
        evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
        evt.dataTransfer = dataTransfer;
        target.dispatchEvent(evt);
      });

      setTimeout(function () { document.body.removeChild(input); }, 25);
    };
    document.body.appendChild(input);
    return input;
"""
        self.__option = webdriver.ChromeOptions()
        self.__option.add_experimental_option("detach", False)

        self.__web = webdriver.Chrome(self.__driverPath)
        self.__web.get(self.__url)
        wait = WebDriverWait(self.__web, 10)
        try:
            test = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/p')))
        except:
            raise RuntimeError('TimeOut')

    def openJson(self, fileName):
        target = self.__web.find_element_by_xpath('//*[@id="help"]')
        drop = self.__web.execute_script(self.JS_DROP_FILE, target, 0, 0)
        drop.send_keys(os.path.join(LOCAL_DIR, fileName))

    def click(self):
        button = self.__web.find_element_by_xpath('/html/body/div[6]/span[2]/i')
        button.click()


