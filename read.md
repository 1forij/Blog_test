# 2021年12月1日 js的flash自动隐藏+token的初识
~~~js
// flash自动隐藏
setTimeout  +  $("").hide()
~~~
~~~python
'''
如果我们将已验证的用户的信息保存在Session中，则每次请求都需要用户向已验证的服务器发送验证信息(称为Session亲和性)。用户量大时，可能会造成  一些拥堵。
'''
# session 
每个人只需要保存自己的session id，而服务器要保存所有人的session id ！  如果访问服务器多了， 就得由成千上万，甚至几十万个#text "这对服务器说是一个巨大的开销 ， 严重的限制了服务器扩展能力， 比如说我用两个机器组成了一个集群， 小F通过机器A登录了系统，  那session id会保存在机器A上，  假设小F的下一次请求被转发到机器B怎么办？  机器B可没有小F的 session id啊。"


~~~




# 2021年12月2日22:22:59 @property的介绍与使用 笔记
<h4>摘抄自知乎用户
~~~python

'''
作用：
    使用@property装饰器来创建只读属性----(有点类似c++的const)
    @property装饰器会将方法转换为相同名称的只读属性,可以与所定义的属性配合使用，这样可以防止属性被修改。
'''


# 一.修饰方法，使方法可以像属性一样访问
class DataSet(object):
  @property
  def method_with_property(self): # 含有@property
      return 15
  def method_without_property(self): # 不含@property
      return 15

l = DataSet()
print(l.method_with_property) # 加了@property后，当作属性来调用方法,不需要加（）。
print(l.method_without_property())  #没有加@property , 就是在调用方法，故后面加()
# 结果均为15


# 二.与所定义的属性配合使用，这样可以防止属性被修改。(防止密码被用户修改)
class DataSet(object):
    def __init__(self):
        self._images = 1#定义属性的名称
        self._labels = 2 #定义属性的名称
    @property
    def images(self): #方法加入@property后，使方法相当于一个属性，这个属性可以让用户进行使用，而且用户有没办法随意修改。
        return self._images 
    @property
    def labels(self):
        return self._labels
l = DataSet()
#用户进行属性调用的时候，直接调用images即可，而不用知道属性名_images，因此用户无法更改属性，从而保护了类的属性。
print(l.images) # 加了@property后，可以用调用属性的形式来调用方法,后面不需要加（）。
~~~

# 2021年12月3日18:02:40 使用werkzeug.security时的一些理解
~~~python
'''
User类表中
    @property
    def password(self):#    用户调用密码,能看(哈希值)不能改   使得password == self._password_hash
        return self._password_hash

    @password.setter#   存储密码于db  and  修改密码
    def password(self, in_word):
        self._password_hash = generate_password_hash(in_word)

    关于 上述两函数名一样的理解:
    记@property def password(self):      为 a
    记@password.setter  def password(self, in_word):     为 b
    以及 views/fun_register  new_user=User(username=in_name,password=in_word,phonenum=in_phone)
    
    a 存在的作用:   使得 password == self._password_hash   (两者等价)
    b 存在的作用:   password 同是也是函数 将in_word作为参数执行了 b
    
    简单来说:   
        password        "一语双关"
        self._hash_word / property(类似const) / 机密 / 让用户无权修改
        a 在查(用户只能查看)    查看 self._hash_word
        b 在写()              修改 self._hash_word
    
    当然 b 也可以改名为 def set_password(self, in_word):

'''
~~~
<h3> "一语双关"
<h4> a 在查(用户只能查看)    查看 self._hash_word
<h4> b 在写()              修改 self._hash_word