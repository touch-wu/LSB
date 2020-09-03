from PIL import Image
import random

#fulfil the string with "0" to 8 bits 
def mod(x,y):
	return x%y

def plus(str):
	return str.zfill(8)

def toasc(strr):
	return int(strr, 2)

def get_key(strr):
	#获取要隐藏的文件内容
	tmp = strr
	f = open(tmp,"rb")
	str = ""
	s = f.read()
	global text_len
	text_len = len(s)
	for i in range(len(s)):
		#code.interact(local=locals())
		str = str+plus(bin(s[i]).replace('0b',''))
		#逐个字节将要隐藏的文件内容转换为二进制，并拼接起来
		#1.先用ord()函数将s的内容逐个转换为ascii码
		#2.使用bin()函数将十进制的ascii码转换为二进制
		#3.由于bin()函数转换二进制后，二进制字符串的前面会有"0b"来表示这个字符串是二进制形式，所以用replace()替换为空
		#4.又由于ascii码转换二进制后是七位，而正常情况下每个字符由8位二进制组成，所以使用自定义函数plus将其填充为8位
		#print str
	f.closed
	return str
def q_converto_wh(q,width):
	w = q//width
	h = q%width
	return w,h 

#input: image, watermark, watermarked image
def func_LSB_yinxie(str1,str2,str3):
	im = Image.open(str1)
	#获取图片的宽和高
	global width,height
	width = im.size[0]
	print("width:" + str(width)+"\n")
	height = im.size[1]
	print("height:"+str(height)+"\n")
	count = 0
	#获取需要隐藏的信息
	key = get_key(str2)
	print('key: ',key)
	keylen = len(key)
	print('keylen: ',keylen)


	for h in range(0,height):
		for w in range(0,width):
			pixel = im.getpixel((w,h))
			#code.interact(local=locals())
			a=pixel[0]
			b=pixel[1]
			c=pixel[2]
			if count == keylen:
				break
			#下面的操作是将信息隐藏进去
			#分别将每个像素点的RGB值余2，这样可以去掉最低位的值
			#再从需要隐藏的信息中取出一位，转换为整型
			#两值相加，就把信息隐藏起来了
			a= a-mod(a,2)+int(key[count])
			count+=1
			if count == keylen:
				im.putpixel((w,h),(a,b,c))
				break
			b =b-mod(b,2)+int(key[count])
			count+=1
			if count == keylen:
				im.putpixel((w,h),(a,b,c))
				break
			c= c-mod(c,2)+int(key[count])
			count+=1
			if count == keylen:
				im.putpixel((w,h),(a,b,c))
				break
			if count % 3 == 0:
				im.putpixel((w,h),(a,b,c))
	im.save(str3)
	print("")


#le为所要提取的watermark大小单位bit，str1为加密载体图片的路径，str2为提取文件的保存路径，suffix为watermark文件类型后缀
def func_LSB_tiqu(le,str1,str2,suffix):
	a=""
	b=""
	im = Image.open(str1) 
	str2 = str2 + 'watermark.' + suffix
	#lenth = le*8
	lenth = le
	width = im.size[0]
	height = im.size[1]
	count = 0
	for h in range(0, height):
		for w in range(0, width):
			#获得(w,h)点像素的值
			pixel = im.getpixel((w, h))
			#此处余3，依次从R、G、B三个颜色通道获得最低位的隐藏信息
			if count%3==0:
				count+=1
				b=b+str((mod(int(pixel[0]),2)))
				if count ==lenth:
					break
			if count%3==1:
				count+=1
				b=b+str((mod(int(pixel[1]),2)))
				if count ==lenth:
					break
			if count%3==2:
				count+=1
				b=b+str((mod(int(pixel[2]),2)))
				if count ==lenth:
					break
		if count == lenth:
			break
	
	print(b)

	with open(str2,"wb") as f:
		for i in range(0,len(b),8):
			#以每8位为一组二进制，转换为十进制
			stra = toasc(b[i:i+8])
			#stra = b[i:i+8]
			#将转换后的十进制数视为ascii码，再转换为字符串写入到文件中
			stra = chr(stra)
			sb = bytes(stra, encoding = "utf8")
			#print(sb)
			#f.write(chr(stra))
			f.write(sb)
			stra =""
	f.closed

def func_LSB_suijijiange_yinxie(str1,str2,str3,step):
	im = Image.open(str1)
	global width,height
	width = im.size[0]
	print("width:" + str(width)+"\n")
	height = im.size[1]
	print("height:"+str(height)+"\n")
	count = 0
    #获取需要隐藏的信息
	global keylen
	key = get_key(str2)
	keylen = len(key)
	print(key)
	print(keylen)

	random.seed(2)
	global LSB_suijijiange_step
	step_max = int(width*height/keylen)
	print('step: ',step)
	print('step_max: ',step_max)
	LSB_suijijiange_step = int(step)
	if LSB_suijijiange_step > step_max:
		print('err: step is too large!')
		return

	step=LSB_suijijiange_step
	random_seq = [0]*keylen
	for i in range(0,keylen):
		random_seq[i] = int(random.random()*step+1)
		#print(random_seq[i])

	q=1
    
	for count in range(keylen):
	    w,h = q_converto_wh(q,width)
	    pixel = im.getpixel((w,h))
	    a=pixel[0]
	    a = a-mod(a,2)+int(key[count])
	    q=q+random_seq[count]
	    im.putpixel((w,h),(a,pixel[1],pixel[2]))
	
	im.save(str3)

def func_LSB_suijijiange_tiqu(le,str1,str2,step,suffix):
	a=""
	b=""
	im = Image.open(str1)

	
	global width
	global height
	width = im.size[0]
	height = im.size[1]
	print(width,',',height)
	len_total = le
	count = 0
	#print(len_total)
	random.seed(2)
	#step = int(width*height/len_total)
	#step = int(LSB_suijijiange_step)
	random_seq = [0]*len_total
	for i in range(0,len_total):
		random_seq[i] = int(random.random()*step+1)


	q=1
	count = 0


	for count in range(len_total):
		
		w,h = q_converto_wh(q,width)
		pixel = im.getpixel((w, h))
		#print(q,'-----',w,',',h)
		b=b+str(mod(pixel[0],2))
		#print(count)
		q = q + random_seq[count]
		count+=1

	print(b)
	str2=str2+'watermark.'+suffix

	with open(str2,"wb") as f:
		for i in range(0,len(b),8):
			#以每8位为一组二进制，转换为十进制
			stra = toasc(b[i:i+8])
			#stra = b[i:i+8]
			#将转换后的十进制数视为ascii码，再转换为字符串写入到文件中
			stra = chr(stra)
			sb = bytes(stra, encoding = "utf8")
			#print(sb)
			#f.write(chr(stra))
			f.write(sb)
			stra =""
	f.closed


