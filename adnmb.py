import requests
import re
import os
import time
#串号错误 -1
#路径占用 -2
#网络错误 -3
#路径错误 -4


def crawler(num):
	page = 1
	counter = 1
	path_head = 'https://adnmb2.com/t/'
	page_head = '?page='
	pic_pattern_1 = 'https://nmbimg.fastmirror.org/image/(.*?)jpg'
	pic_pattern_2 = 'https://nmbimg.fastmirror.org/image/(.*?)png'
	pic_head = 'https://nmbimg.fastmirror.org/image/'
	pic_type_1 = 'jpg'
	pic_type_2 = 'png'
	block_list = ['https://nmbimg.fastmirror.org/image/2019-08-24/5d60c60501fd3.jpg',
					'https://nmbimg.fastmirror.org/image/2020-03-31/5e8364b9c8730.jpg',
					'https://nmbimg.fastmirror.org/image/2020-03-31/5e836499efff9.jpg',
					'https://nmbimg.fastmirror.org/image/2020-03-31/5e8364adc9ce7.jpg',
					'https://nmbimg.fastmirror.org/image/2018-09-01/5b8a4c0a233c7.jpg',
					'https://nmbimg.fastmirror.org/image/2020-03-07/5e63c24a69a79.jpg',
					'https://nmbimg.fastmirror.org/image/2020-05-05/5eb177be55d97.png',
					'https://nmbimg.fastmirror.org/image/2016-06-15/576132a9e3482.png',
					'https://nmbimg.fastmirror.org/image/2020-02-12/5e4368849c7f3.png']
	pic_url = []
	headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'zh-CN,zh;q=0.9',
		'cache-control': 'max-age=0',
		'cookie': '_ga=GA1.2.811084631.1587126690; __dtsu=6D00158962713577F4B4A3DA0F435CE2; PHPSESSID=nqsvv8b18m2mk5cs1c3spl1p44; _gid=GA1.2.1508843656.1592573987; Hm_lvt_e6d1419842221a8d451e9a89cabbcba6=1591802627,1592573987; Hm_lpvt_e6d1419842221a8d451e9a89cabbcba6=1592590321',
		'sec-fetch-dest': 'document',
		'sec-fetch-mode': 'navigate',
		'sec-fetch-site': 'none',
		'sec-fetch-user': '?1',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
	page_pattern_1 = r'''page=[0-9]+">末页'''
	page_pattern_2 = r'''[0-9]+</a></li> <li><a [a-z]+="(.+)">下一页'''
	check_pattern = '该主题不存在'
	check_p = re.compile(check_pattern)
	retry = 0
	while(True):
		try:
			html = requests.get(path_head + num, headers).text
			break
		except:
			if retry < 3:
				print('连接失败，重试中(' + str(retry + 1) + '/3)')
				retry += 1
				time.sleep(3)
				continue
			else:
				print('连接失败！')
				return -3

	check_result = check_p.search(html)
	#串号错误
	if check_result != None:
		print('串号错误！')
		return -1
	#正确串号，拿到html
	page_1 = re.compile(page_pattern_1)
	page_2 = re.compile(page_pattern_2)
	#末页
	p_1 = page_1.search(html)
	#下一页
	p_2 = page_2.search(html)
	#拿取页数
	if p_1 != None:
		total_page = re.search('[0-9]+',p_1.group())
		page = int(total_page.group())
	elif p_2 != None:
		total_page = re.search('\\A[0-9]+', p_2.group())
		page = int(total_page.group())
	#匹配jpg与png
	temp_1 = re.findall(pic_pattern_1, html)
	temp_2 = re.findall(pic_pattern_2, html)
	for i in temp_1:
		full_link = pic_head + i + pic_type_1
		if full_link not in block_list:
			if full_link not in pic_url:
				pic_url.append(full_link)
				print('页数:1/' + str(page) + ' 发现图片数:' + str(len(pic_url)) + '\r', end='')
	for i in temp_2:
		full_link = pic_head + i + pic_type_2
		if full_link not in block_list:
			if full_link not in pic_url:
				pic_url.append(full_link)
				print('页数:1/' + str(page) + ' 发现图片数:' + str(len(pic_url)) + '\r', end='')
	#更多页数的图片url
	time.sleep(3)
	for i in range(2, page + 1):
		retry = 0
		while(True):
			try:
				html = requests.get(path_head + num + page_head + str(i), headers).text
				break
			except:
				if retry < 3:
					print('连接失败，重试中(' + str(retry + 1) + '/3)')
					retry += 1
					time.sleep(3)
					continue
				else:
					print('连接失败！')
					return -3
		temp_1 = re.findall(pic_pattern_1, html)
		temp_2 = re.findall(pic_pattern_2, html)
		for j in temp_1:
			full_link = pic_head + j + pic_type_1
			if full_link not in block_list:
				if full_link not in pic_url:
					pic_url.append(full_link)
					print('页数:' + str(i) + '/' + str(page) + ' 发现图片数:' + str(len(pic_url)) + '\r', end='')
		for j in temp_2:
			full_link = pic_head + j + pic_type_2
			if full_link not in block_list:
				if full_link not in pic_url:
					pic_url.append(full_link)
					print('页数:' + str(i) + '/' + str(page) + ' 发现图片数:' + str(len(pic_url)) + '\r', end='')
		time.sleep(3)
	print('')
	#创建存储文件夹，以串号命名
	try:
		print('创建文件夹./' + num + '中...')
		os.makedirs('./' + num)
	except OSError:
		if num in os.listdir('./'):
			print('路径已存在')
			while(True):
				a = input('是否继续向./' + num + '中写入图片(y/n):')
				if a == 'n':
					return -2
				elif a == 'y':
					break
				else:
					print('输入错误！')
					continue
		else:
			print('存储路径错误！')
			return -4
	#log，存储编号和地址
	f_log = open('./'+num+'/log.txt', 'w')
	#拿图片
	for i in pic_url:
		retry = 0
		while(True):
			try:
				pic_cache = requests.get(i, headers).content
				break
			except:
				if retry < 3:
					print('连接失败，重试中(' + str(retry + 1) + '/3)')
					retry += 1
					time.sleep(3)
					continue
				else:
					print('连接失败！')
					return -3
		pic = open('./' + num + '/' + str(counter) + i[len(i) - 4:], 'wb')
		pic.write(pic_cache)
		pic.close()
		f_log.write(str(counter) + "	" + i + '\n')
		print('写入完成:' + str(counter) + '/' + str(len(pic_url)) + '\r', end='')
		counter += 1
		time.sleep(3)
	print('')
	print('串号' + num + '已爬取完毕')
	f_log.close()
	return 0

if __name__ == '__main__':
	while(True):
		num = input('请输入串号:')
		crawler(num)
		while(True):
			next = input('是否继续爬取新的串(y/n):')
			if next == 'n':
				os._exit(0)
			elif next == 'y':
				break
			else:
				print('输入错误！')
				continue