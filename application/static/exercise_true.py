# coding=gbk
import base64
# with open("./imgs/users.jpg","rb") as f:#תΪ�����Ƹ�ʽ    b'/9j
#     base64_data = base64.b64encode(f.read())#ʹ��base64���м���
#     print(base64_data)
    # file=open('1.txt','wt',encoding=)#д���ı���ʽ
    # file.write(base64_data)
    # file.close()

with open("./imgs/users.jpg","rb") as f:                  #9j
    image = f.read()
    image_base64 = str(base64.b64encode(image), encoding='utf-8')  # image_base64���Ƕ�ͼ�����base64����������
    print(image_base64)