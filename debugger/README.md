# 本地调试用代码

## TL;DR
* 跑`debuggerCmd.py`
    * 成功运行: 获得记录json
    * 报错: 自行debug
* 跑`debugVisualizer.py`
    * 成功运行: 看可视化记录
    * 报错: 回到`debuggerCmd.py`debug

## 文件列表
* `debuggerCmd.py`: 命令行调试工具
* `debugVisualizer.py`: Flask可视化调试工具（需安装`flask`）
    * `server.py`: 其运行内核

## 使用步骤
### 0. 配置比赛内核位置
`debuggerCmd.py`中的全局参数`SRC_PATH`指定了源代码目录`src`的相对路径；  
若需移动该文件夹则需相应修改此路径
### 1. 启动方式 & 加载双方代码
调试代码有2种运行方式：直接启动（IDLE、PyCharm、VSCODE等）或命令行启动（`python ***.py`）  
其需要接收两个主要参数，分别为双方参赛代码的文件路径（可相同）  

双方代码路径分别从`预设输入`与`用户输入`中获取  
若`预设输入`没有输入，将会进入`用户输入`；  
若`预设输入`或`用户输入`没有获取到有效文件（路径不存在、无法解析为python代码、缺失必要对象定义）则会展示报错内容，并循环尝试`用户输入`

#### 1) 预设输入
预设输入来源于以下方式（按优先级由高至低）：
1. 直接修改`debuggerCmd.py`中的全局参数`PLAYER1_PATH`与`PLAYER2_PATH`
1. 启动时包含的命令行参数（`python ***.py player1_path player2_path`）

#### 2) 用户输入
程序将按顺序获取先手与后手玩家中未指定合法预设输入的代码路径  
根据`debuggerCmd.py`中的全局参数`USE_DIALOG`决定输入方式：
1. （若为True，默认）打开文件选择窗口选取对应文件
1. （若为False）直接使用`input()`输入代码路径

### 2. 运行结果
#### a) 运行失败
与实际游戏规则不同，调试用代码在任一参赛者出现异常时将直接中止比赛，包括代码报错与超时的情况  

`debuggerCmd.py`可使用Python调试工具运行，若发生此类情况可使用异常捕捉、断点调试等功能自行处理  
由于`debugVisualizer.py`使用Flask作为后端，不建议使用该文件进行后续调试工作  

运行失败后不会保存比赛记录

#### b) 运行成功
`debuggerCmd.py`将保存成功的比赛记录至全局变量`OUTPUT_DIR`配置的位置（默认为同目录`output.json`），随后退出程序  
`debugVisualizer.py`将打开可视化窗口展示该局运行结果，不会保存比赛记录；此时可刷新该页面使相同对战双方进行一局新的比赛，或手动关闭Flask后台结束程序