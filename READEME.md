## **使用说明**
####环境配置
#####1、 chrome驱动下载`http://npm.taobao.org/mirrors/chromedriver/`，自己谷歌浏览器必须使用对应驱动，驱动放在工程目录drivers下
#####2、安装python环境，并安装所需依赖库：pip install -r requirments.txt -i https://pypi.doubanio.com/simple
#####3、本地安装：npm install -g anywhere，提前安装好node环境
#####4、allure-commandline-2.13.3，下载后，配置环境变量，才能运行allure报告

####执行测试
#####1、运行run.py文件，等结束后，在report/result/目录下，直接浏览器中预览index.html文件，显示测试结果
#####2、用例编写位置在testcase下，具体用例参考pytest官方文档进行：`https://docs.pytest.org/en/stable/

