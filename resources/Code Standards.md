# 1、安装

```
pip install autopep8
```

# 2、配置

文件（file）-设置（settings）-工具(tools)-外部工具(external-tools)-添加

- 名称：autopep8（随便）

- 程序：autopep8

- 实参：--in-place --aggressive --aggressive $FilePath$

- 工作目录：$ProjectFileDir$

- 输出筛选器：$FILE_PATH$\:$LINE$\:$COLUMN$\:.*

# 3、使用

选中文件右击选择 External Tools 中的 autopep8，即可自动规范化代码

# 4、其他

## （1）类型注解

注：通过“函数名.\__annotations__”显示函数的注释（两下划线）

### ① 函数注解

```python
def classify_by_level1(typeof4: str) -> list
```

### ② 变量注解

```python
a: int = 1
```

## （2）参数注解

注：通过“函数名.\__doc__”显示函数的注释（两下划线）

```python
def show(x: int, y: int) -> int:
	"""
	展示函数
	:param x: lalala
	:param y: bababa
	:return: hahaha
	"""
    return x*y
```

