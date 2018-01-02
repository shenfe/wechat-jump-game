# 微信小游戏“跳一跳”autoplay程序

1. 电脑安装adb并加入path
1. Android手机usb连接电脑并允许usb调试、模拟点击
1. 执行`python src/main.py`

## 命令

### 运行

```commandline
python src/main.py
```

### 截图

```commandline
python src/screenshot.py
```

### 检测

```commandline
python src/detect.py
```

### 手动模式

```commandline
python src/hand.py
```

## 原理

* Adb连接设备执行命令
* Opencv图像识别和处理
* 统计分析得出“距离-时间”线性公式
* 特殊情况特殊处理

## 建议

自己动手，丰衣足食。无暇回应关于本程序的一切问题。
