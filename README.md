OMM
===

Option Market Maker

1> 安装软件
*) 安装Wind资讯，路径[C:\Wind]
*）安装WinPython3，路径[D:\Program Files\WinPython3]

2> 配置环境
*) 使用Wind量化接口,将WindPy.pth文件复制到[WinPython3\python-3.3.5\Lib\site-packages]，注意WindPy.pth中的路径要和Wind安装路径吻合
*) 运行程序需要开启Wind终端

3> 配置策略
*) gvar.py 配置段，设置Wind帐户；设置程序轮询速度，默认值为0.1秒一个合约；
*) marketmaker.py，class MarketMaker1，设置交易价差和交易量

4> 运行
*) 打开main.py，运行；程序未设置自动退出，请使用Ctrl+C退出
*) 察看委托成交信息：打开Wind终端，进入模拟交易（WTTS），选择期权交易的衍生品帐户，选择查询功能

5> 当前问题
*) 由于是在非交易时间开发的，还没有测试实时盘口跳动时程序运行的状况，也没有测试成交回报