# coding=gbk
import base64
# with open("./imgs/users.jpg","rb") as f:#转为二进制格式    b'/9j
#     base64_data = base64.b64encode(f.read())#使用base64进行加密
#     print(base64_data)
    # file=open('1.txt','wt',encoding=)#写成文本格式
    # file.write(base64_data)
    # file.close()

with open("./imgs/users.jpg","rb") as f:                  #9j
    image = f.read()
    image_base64 = str(base64.b64encode(image), encoding='utf-8')  # image_base64即是对图像进行base64编码后的内容
    print(image_base64)