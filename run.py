import pytest,os,time
import shutil


if __name__ =="__main__":

    #清空allure中间结果
    tmp_path = os.path.dirname(__file__)+"/report/"
    test_path = os.path.dirname(__file__)+"/report/test"
    print(os.listdir(tmp_path))
    for fp in os.listdir(tmp_path):
        if fp == "test":
            print("allure临时文件目录：",test_path)
            shutil.rmtree(test_path)
        else:
            pass
    pytest.main(["-s","--alluredir=report"])  # 存放allure生成的xml文件的目录
    os.system("py.test -q testcase/ --alluredir ./report/test")
    time.sleep(10)
    os.system("allure generate ./report/test/ -o ./report/result --clean")
    os.system("cd report/result && anywhere")
