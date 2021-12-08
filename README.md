# toolbox
## 1. chooseImage
运行环境：建议在linux环境下运行，也可用windows。

运行要求：Python3 + cv2

运行方法：直接运行chooseImage.py

标注方法：
1. 成功运行程序会显示待标注图片，其中左上角子图为source image，其余子图是方法1-7裁剪得到的图片（crop）。
2. 键盘输入你认为的best crop（1-7中的任意一个数字），自动显示下一张；输入其他数字或按键会被忽略。
3. 标注失误按上键或左键返回上一张图重新标注，输入下键或右键进入下一张。
4. 输入q或者ESC退出标注，程序会自动保存标注到同一文件夹下annotation.json文件，下次标注直接从断点开始。输入S可保存结果并继续标注。
5. 左上角显示当前已完成/总的图片数量。
6. 完成所有标注之后程序自动退出，再次运行会直接退出，删除json文件可重新标注。

注意事项：
1. 按键不要太快，否则程序容易崩溃，特别是在windows上。
1. 如果是远程服务器+ssh运行，参考https://blog.csdn.net/qq_28888837/article/details/102865139进行配置。推荐ssh使用MobaXterm.
2. 如果运行程序发现显示的图片很小，建议关闭程序多试两次。
3. 标注过程命令窗口会打印信息，不过可以忽略。如果按键没反应，可能是图片窗口没在最前。
