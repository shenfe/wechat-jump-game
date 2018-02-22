# 微信小游戏“跳一跳”autoplay程序

<p align="center">
<img src="https://raw.githubusercontent.com/shenfe/wechat-jump-game/master/readme_assets/game.png">
<img src="https://raw.githubusercontent.com/shenfe/wechat-jump-game/master/readme_assets/score.jpg">
</p>

1. 电脑[安装adb](https://www.xda-developers.com/install-adb-windows-macos-linux/)并加入path
1. Android手机usb连接电脑并允许usb调试、模拟点击
1. 执行`pip install -r requirements.txt`安装依赖
1. 在data目录下确保存在screenshot文件夹
1. 执行`python src/main.py`运行自动模式

*程序适配1280x720屏幕的安卓手机，其余分辨率请自行调整代码中相关数值。*

## 命令

### 运行自动模式

```commandline
$ python src/main.py
```

### 运行手动模式

将`src/config.py`中`test`设为`True`后，

```commandline
$ python src/hand.py
```

### 截图预览

```commandline
$ python src/preview.py
```

### 公式系数

见`src/distance_time.py`。

## 原理

* Adb连接设备执行命令
* Opencv图像识别和处理
* 统计分析得出“距离-时间”线性公式
* 特殊情况特殊处理

## 建议

自己动手，丰衣足食。无暇回应关于本程序的一切问题。
