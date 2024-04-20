## 一个HDSky签到脚本
# 思路
通过抓包获取到签到接口的请求参数，然后通过requests库发送请求，完成签到。  
通过抓包可知，HDSky站点签到大致分为了三步
![第一步.png](https://img2.imgtp.com/2024/04/20/IBG1e94K.png)
![第二步.png](https://img2.imgtp.com/2024/04/20/TzfuFXiS.png)
![第三步.png](https://img2.imgtp.com/2024/04/20/iORluzj6.png)
通过带有cookies的请求发送到签到接口，使用ddddocr识别验证码，完成签到。
## 使用方式
1. 获取cookie  
在浏览器中打开签到页面，在开发者工具中查看请求头，找到cookie字段，将cookie复制到config.ini文件中。  
2. 运行脚本  
在终端中运行脚本，即可完成签到。（建议通过crontab定时执行）  
3. 获取签到结果  
在终端中查看签到结果。  

## 注意事项
1. 请确保文件中的cookie是正确的。  
2. 请勿频繁运行脚本，否则可能会被封禁。  
3. 请勿将cookie泄露给其他人。