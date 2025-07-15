### 一个用于将表格 每行的差值 分类的工具。
#### 功能：
- 输入：一个包含表格数据的Excel文件，以及一个分类标准。
#### 处理当前目录下的目标excel文件
- 输出：一个包含分类结果的Excel文件。# classified_result.xlsx

#### 使用方法：
``` python
>>> from dc_excel import dcEx
>>>  dcEx('dhd.xlsx', ['ch','cwp']) # 目标excel文件路径 用于分类字符串数组
```