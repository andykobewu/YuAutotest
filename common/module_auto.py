"""
@File    :   new_context_parse.py
@Contact :   https://www.toutiao.com/c/user/token/MS4wLjABAAAAakx_PBJsQXpljEkaBcc0pEteSDMYxTbbBrlQ6F4p3yQ/

@Modify Time      @Author           @Version    @Desciption
------------      -------           --------    -----------
2021/3/22 00:47   软件测试开发技术栈    1.0         None
"""

import ast
import re
import yaml
import os
import sys
import types
import importlib
from collections import defaultdict
from collections import OrderedDict


class MyBaseError(Exception):
    pass


class FileFormatError(MyBaseError):
    pass


class ParamsError(MyBaseError):
    pass


class NotFoundError(MyBaseError):
    pass


class FileNotFound(FileNotFoundError, NotFoundError):
    pass


class FunctionNotFound(NotFoundError):
    pass


class VariableNotFound(NotFoundError):
    pass


class LoadModule:

    def __init__(self):

        self.custom_module_info = {
            "variables": {},
            "functions": {}
        }

        self.project_working_directory = ""

    @staticmethod
    def is_function(_type: types) -> bool:
        """
        判断对象是否为函数
        Args:
            _type: 对象实际类型

        Returns:

        """
        return isinstance(_type, types.FunctionType)

    @staticmethod
    def is_variable(name: str, _type: types) -> bool:
        """
        判断对象是否为变量，不含私有变量
        Args:
            name:
            _type:

        Returns:

        """
        if callable(_type):
            return False

        if isinstance(_type, types.ModuleType):
            return False

        if name.startswith("_"):
            return False

        return True

    @staticmethod
    def locate_file(start_file_or_dir_path: str, file_name: str) -> str:
        """
        递归查询，返回文件绝对路径
        Args:
            start_file_or_dir_path: 起始目录
            file_name: 文件名称,包含文件类型后缀

        Returns: 不存在时,抛出异常

        Raises:
            exceptions.FileNotFound: 文件不存在

        """

        if os.path.isfile(start_file_or_dir_path):
            start_dir_path = os.path.dirname(start_file_or_dir_path)

        elif os.path.isdir(start_file_or_dir_path):
            start_dir_path = start_file_or_dir_path

        else:
            raise FileNotFound("invalid path: {}".format(start_file_or_dir_path))

        file_path = os.path.join(start_dir_path, file_name)

        if os.path.isfile(file_path):
            return file_path

        # 当前工作目录
        if os.path.abspath(start_dir_path) in [os.getcwd(), os.path.abspath(os.sep)]:
            raise FileNotFound("{} not found in {}".format(file_name, start_file_or_dir_path))

        # 递归向上查找
        return LoadModule.locate_file(os.path.dirname(start_dir_path), file_name)

    @staticmethod
    def locate_py(start_path, module_file_name) -> str or None:
        """
        递归查询，返回文件绝对路径
        Args:
            start_file_or_dir_path: 起始目录
            file_name: 文件名称,包含文件类型后缀

        Returns: 不存在时,返回 None

        Raises:
            exceptions.FileNotFound: 文件不存在

        """
        try:
            path = LoadModule.locate_file(start_path, module_file_name)
            return os.path.abspath(path)

        except FileNotFound:
            return None

    @staticmethod
    def load_module_with_object(module_object: types.ModuleType) -> dict:
        """
        通过模块对象的方式 加载 Python指定模块.获取函数与变量信息。

        Args:
            module_object (Object): python module 对象, module_object = importlib.import_module(module_name)

        Returns:
            dict: 指定python模块的变量和函数字典，字典格式:

                {
                    "variables": {},
                    "functions": {}
                }

        """
        _custom_module_info = defaultdict(dict)

        for _name, _type in vars(module_object).items():

            if LoadModule.is_function(_type):
                _custom_module_info["functions"][_name] = _type

            elif LoadModule.is_variable(_name, _type):
                if isinstance(_type, tuple):
                    continue
                _custom_module_info["variables"][_name] = _type

            else:
                # 过滤掉私有变量、模块等
                pass

        return _custom_module_info

    def load_module_with_name(self, module_name: str) -> None:
        """
           通过模块名字(不含)的方式 加载 Python指定模块.获取函数与变量信息。应该位于项目工作目录中
        Args:
            module_name: 模块名称, 不含后缀

        Returns:
            dict: 指定python模块的变量和函数字典，字典格式:
                {
                    "variables": {},
                    "functions": {}
                }

        """

        imported_module = importlib.import_module(module_name)

        _custom_module_info = LoadModule.load_module_with_object(imported_module)
        # 更新
        self.custom_module_info.update(_custom_module_info)

    def load_specified_path_module(self, start_path: str, module_file_name_with_py: str) -> None:
        """
        通过模块名字（含后缀）的方式 加载 Python指定模块.获取函数与变量信息。
        Args:
            start_path:
            module_file_name_with_py: 模块名字（含后缀）

        Returns:

        """

        """ load  .env, .py.
            api/testcases folder is relative to project_working_directory

        Args:
            module_file_name_with_py: 
            start_path (str):
            module_file_name(str):
        """

        module_path = LoadModule.locate_py(start_path, module_file_name_with_py)

        # 模块工作目录.
        if module_path:

            self.project_working_directory = os.path.dirname(module_path)
        else:
            # 当前目录兜底
            self.project_working_directory = os.getcwd()

        if module_path:
            # 将当前目录作为最优加载目录
            sys.path.insert(0, self.project_working_directory)

            module_name = os.path.splitext(module_file_name_with_py)[0]

            self.load_module_with_name(module_name)


class Utils:
    """
    工具类
    """

    @staticmethod
    def load_yaml(yaml_file_path: str) -> dict:
        """
        加载 yaml文件
        Args:
            yaml_file_path: yaml文件路径,绝对或相对路径

        Returns:
            dict

        """
        # 将yaml格式内容 转换成 dict类型
        with open(yaml_file_path, encoding="utf-8") as read_yaml:
            yaml_context_dict = yaml.load(read_yaml.read(), Loader=yaml.Loader)

        return yaml_context_dict

    @staticmethod
    def string_value_number(possible_number: str) -> int or float or str:
        """
        将允许为数字的字符串，解析为数字
        Args:
            possible_number: 可能为数字的字符串

        Returns:

        Examples:
             "9527" => 9527
             "9527.2" => 9527.3
             "abc" => "abc"
             "$name" => "$name"
        """

        try:
            return ast.literal_eval(possible_number)

        except ValueError:
            return possible_number

        except SyntaxError:
            return possible_number

    @staticmethod
    def convert_list_to_dict(mapping_list: list) -> dict:
        """ 将列表转换为有序字典

        Args:
            mapping_list: 列表
                [
                    {"a": 1},
                    {"b": 2}
                ]

        Returns:
            OrderedDict:

                {
                    "a": 1,
                    "b": 2
                }


        """
        ordered_dict = OrderedDict()

        for map_dict in mapping_list:
            ordered_dict.update(map_dict)

        return ordered_dict

    @staticmethod
    def extract_functions(content: str) -> list:
        """ 从字符串内容中提取所有函数，格式为${fun()}

        Args:
            content : 字符串的内容

        Returns:
            list: functions list extracted from string content

        Examples:
            >>> Utils.extract_functions("${func(1)}")
            ["func(1)"]

            >>> Utils.extract_functions("${func(a=1, b=2)}")
            ["func(a=1, b=2)"]

            >>> Utils.extract_functions("/api/${func(1, 2)}")
            ["func(1, 2)"]

            >>> Utils.extract_functions("/api/${func(1, 2)}?_s=${func2()}")
            ["func(1, 2)", "func2()"]

        """
        try:
            return re.findall(StaticVariable.FUNCTION_REGEXP, content)
        except TypeError:
            return []

    @staticmethod
    def extract_variables(content: str) -> list:
        """ 从字符串内容中提取所有变量名，格式为$variable

        Args:
            content : 字符串的内容

        Returns:
            list: 从字符串内容中提取的变量列表

        Examples:
            >>> Utils.extract_variables("$phone")
            ["phone"]

            >>> Utils.extract_variables("/api/$phone")
            ["phone"]

            >>> Utils.extract_variables("/$phone/$name")
            ["phone", "name"]

        """
        try:
            return re.findall(StaticVariable.VARIABLE_REGEXP, content)
        except TypeError:
            return []

    @staticmethod
    def parse_string_variables(content: str, variables_mapping: dict) -> str:
        """ 用变量映射,替换出字符串内容中提取所有变量名。

        Args:
            content : 字符串的内容
            variables_mapping : 变量映射.

        Returns:
            str: 解析字符串内容。

        Examples:
            >>> content = '$TERMINAL_NAME'
            >>> variables_mapping = {"$TERMINAL_NAME": "alibaba"}
            >>> Utils.parse_string_variables(content, variables_mapping)
                "alibaba"

        """

        def get_mapping_variable(__variable_name: str):
            """ 从 variable_mapping 中获取变量。
            Args:
                __variable_name: 变量名称

            Returns:
                变量值.

            Raises:
                exceptions.VariableNotFound: 变量不存在

            """
            try:
                return variables_mapping[__variable_name]
            except KeyError:
                # print variable_name
                raise VariableNotFound("{} is not found.".format(__variable_name))

        variables_list = Utils.extract_variables(content)
        for variable_name in variables_list:

            variable_value = get_mapping_variable(variable_name)

            if "${}".format(variable_name) == content:
                content = variable_value
            else:
                if not isinstance(variable_value, str):
                    variable_value = str(variable_value)

                content = content.replace(
                    "${}".format(variable_name),
                    variable_value, 1
                )

        return content

    @staticmethod
    def parse_function(content: str) -> dict:
        """ 从字符串内容中解析函数名和参数。

        Args:
            content : 字符串的内容

        Returns:
            dict:
                {
                    "func_name": "xxx",
                    "func_args": [],
                    "func_kwargs": {}
                }

        Examples:
            >>> Utils.parse_function("func()")
            {'func_name': 'func', 'func_args': [], 'func_kwargs': {}}

            >>> Utils.parse_function("func(1)")
            {'func_name': 'func', 'func_args': [1], 'func_kwargs': {}}

            >>> Utils.parse_function("func(1, 2)")
            {'func_name': 'func', 'func_args': [1, 2], 'func_kwargs': {}}

            >>> Utils.parse_function("func(a=1, b=2)")
            {'func_name': 'func', 'func_args': [], 'func_kwargs': {'a': 1, 'b': 2}}

            >>> Utils.parse_function("func(1, 2, a=3, b=4)")
            {'func_name': 'func', 'func_args': [1, 2], 'func_kwargs': {'a':3, 'b':4}}

        """
        matched = StaticVariable.FUNCTION_REGEXP_COMPILE.match(content)
        if not matched:
            raise FunctionNotFound("{} not found!".format(content))

        function_meta = {
            "func_name": matched.group(1),
            "func_args": [],
            "func_kwargs": {}
        }

        args_str = matched.group(2).strip()
        if args_str == "":
            return function_meta

        args_list = args_str.split(',')
        for arg in args_list:
            arg = arg.strip()
            if '=' in arg:
                key, value = arg.split('=')
                function_meta["func_kwargs"][key.strip()] = Utils.string_value_number(value.strip())
            else:
                function_meta["func_args"].append(Utils.string_value_number(arg))

        return function_meta

    @staticmethod
    def get_mapping_function(function_name: str, functions_mapping: dict) -> types.FunctionType or None:
        """ 从functions_mapping中获取函数，如果没有找到，那么尝试检查是否内置函数。

        Args:
            function_name: 函数名称
            functions_mapping: 函数映射


        Returns:
                函数对象
        Raises:
            exceptions.FunctionNotFound: 函数没有定义

        """
        if function_name in functions_mapping:
            return functions_mapping[function_name]

        try:
            # 判断是否是内置函数
            item_func = eval(function_name)
            if callable(item_func):
                return item_func
        except (NameError, TypeError):
            raise FunctionNotFound("{} is not found.".format(function_name))


class StaticVariable:
    # 变量正则规则
    VARIABLE_REGEXP = r"\$([\w_.]+)"
    # 函数正则规则
    FUNCTION_REGEXP = r"\$\{([\w_]+\([\$\w\.\-/_ =,]*\))\}"
    # 函数正则规则
    FUNCTION_REGEXP_COMPILE = re.compile(r"^([\w_]+)\(([$\w.\-/_ =,]*)\)$")


class ParseContent:
    def __init__(self):

        self.variables_mapping = {}
        self.functions_mapping = {}

    def parse(self, content: (str, dict, list, int, float, bool, type)) -> list or dict or str:

        """ 解析变量|函数映射值

        Args:
            content :
            variables_mapping : 变量映射
            functions_mapping : 函数映射

        Returns:
            parsed content.

        Examples:
            >>> content = {
                    'SignMap':
                        [
                            {'TIME': '${now_time()}'},
                            { 'PHONE': '${phone($MODULE)}'},
                            {'TERMINALNAME': '$TERMINAL_NAME'}
                        ]
                    }

            >>> variables_mapping = {'MODULE': '2', 'TERMINAL_NAME': 'alibaba'}
            >>> functions_mapping = {'now_time': '<function now_time at 0x00000142659A8C18>', 'phone': '<function phone at 0x00000142659B9AF8>', }
            >>> self.parse(content, variables_mapping)
                {
                    'SignMap':
                        [
                            {'TIME': '2021-03-20'},
                            { 'PHONE': '0532-819109210'},
                            {'TERMINALNAME': 'alibaba'}
                        ]
                    }
                }

        """

        if content is None or isinstance(content, (int, float, bool, type)):
            return content

        if isinstance(content, (list, set, tuple)):
            return [
                self.parse(item, )
                for item in content
            ]

        if isinstance(content, dict):
            parsed_content = {}
            for key, value in content.items():
                parsed_key = self.parse(key)
                parsed_value = self.parse(value)
                parsed_content[parsed_key] = parsed_value
            return parsed_content

        if isinstance(content, (str, bytes)):
            _variables_mapping = self.variables_mapping or {}
            _functions_mapping = self.functions_mapping or {}
            content = content.strip()

            # 用求值替换函数
            content = self.parse_string_functions(content)
            # 用绑定值替换变量
            content = Utils.parse_string_variables(content, _variables_mapping)

        return content

    def update_original_context_var_func(self, _variables_mapping: dict, _functions_mapping: dict) -> None:
        """
        将模块原始函数、变量更新到对象属性中
        Args:
            _variables_mapping:
            _functions_mapping:

        Returns:

        """
        self.variables_mapping.update(_variables_mapping)
        self.functions_mapping.update(_functions_mapping)

    def update_context_variables(self, _variables: (str, list, dict)) -> None:
        """
        更新上下文中的变量
        Args:
            _variables:

        Returns:

        """

        if isinstance(_variables, list) or isinstance(_variables, dict):

            if isinstance(_variables, list):
                _variables = Utils.convert_list_to_dict(_variables)

            for variable_name, variable_value in _variables.items():
                variable_eval_value = self.parse(variable_value)

                self.variables_mapping[variable_name] = variable_eval_value
        else:
            variable_eval_value = self.parse(_variables)
            self.variables_mapping[_variables] = variable_eval_value

    def parse_string_functions(self, content: str) -> str:
        """ 用函数映射解析字符串内容。

        Args:
            content : 要解析的字符串内容。

        Returns:
            str: 解析字符串内容。

        Examples:
            >>> content = '${now_time()}'
            >>> self.parse_string_functions(content)
                '2021-03-20'

        """
        functions_list = Utils.extract_functions(content)

        for func_content in functions_list:

            function_meta = Utils.parse_function(func_content)
            func_name = function_meta["func_name"]
            args = function_meta.get("func_args", [])
            kwargs = function_meta.get("func_kwargs", {})
            args = self.parse(args)
            kwargs = self.parse(kwargs)

            func = Utils.get_mapping_function(func_name, self.functions_mapping)
            eval_value = func(*args, **kwargs)
            func_content = "${" + func_content + "}"
            if func_content == content:
                content = eval_value
            else:
                # 字符串包含一个或多个函数或其他内容
                content = content.replace(
                    func_content,
                    str(eval_value), 1
                )

        return content

    def add_module_variables_functions(self, module_dirname, module_file_name) -> None:
        """
        添加模块属性、函数
        Args:
            module_dirname:
            module_file_name:
            context:

        Returns:

        """

        load_module = LoadModule()

        load_module.load_specified_path_module(module_dirname, module_file_name)

        custom_module_info = load_module.custom_module_info

        _variables_mapping = custom_module_info["variables"]

        _functions_mapping = custom_module_info["functions"]

        self.update_original_context_var_func(_variables_mapping, _functions_mapping)

    def parse_content(self, context):
        """
        解析内容
        Args:
            context:

        Returns:

        """
        self.update_context_variables(context)

        return self.parse(context)


if __name__ == '__main__':
    parse_context = ParseContent()

    # 加载 yaml 内容 ,如下
    yaml_context = Utils.load_yaml(r'E:\FrontWebAutotest\YuAutotest\data\DataJob.yml')

    # 加载指定 built_in 模块
    parse_context.add_module_variables_functions(
        module_dirname=r"E:\FrontWebAutotest\YuAutotest\common",
        module_file_name="built_in.py")

    # 加载指定 common 模块
    parse_context.add_module_variables_functions(
        module_dirname=r"E:\PythonCode\MOC",
        module_file_name="common.py")

    # 解析 yaml 中数据
    result = parse_context.parse_content(yaml_context)
    print(result)
    # {'SignMap': [{'TIME': '2021-03-23'}, {'PHONE': '0532-819109210'}, {'TERMINALNAME': 'alibaba'}]}

    # 解析字符串
    result_str = parse_context.parse_content("TIME: ${now_time()}")
    print(result_str)
    # TIME: 2021-03-23