import os
import yaml
import warnings

class readerYml:
    def __init__(self):
        warnings.simplefilter('ignore',ResourceWarning)
        self.path = r'application.yml'
    def get_data(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        yaml_path = os.path.join(BASE_DIR,self.path)
        f = open(yaml_path,'r',encoding='utf-8')
        result = f.read()
        return yaml.load(result,Loader=yaml.FullLoader)
    def get_url(self):
        test_url = self.get_data()['web']['url']
        return test_url
    def get_path(self):
        driver_path = self.get_data()['ChromeDriver']['path']
        return driver_path
# testdata =  readerYaml().get_router()
# print("配置文件路径为：",testdata)

