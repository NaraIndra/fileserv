from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from django.http import FileResponse
import os
from PIL import Image

TOKEN = 'kahhbcdbksjhbvksjhcbalkh;qpipopoiyiuyrytrrwqeqdz..khlis,fvs8168765§1876239'

def prove_directory(dir_name):
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)

def read_file(filename, attributes):
	open_file = open(filename, attributes)
	read_file = open_file.read()
	open_file.close()
	return read_file

def write_file(filename, text, attributes):
	wfile = open(filename, attributes)
	wfile.write(text)
	wfile.close()

def get_file_name(filename_string):
	strings = filename_string.split(b';')
	filename = (strings[len(strings) - 1].split(b'"'))[1]
	return filename

def cut_request_file(request_body):
	file_strings = request_body.split(b'\n')
	file_name = get_file_name(file_strings[1])
	lenth = len(file_strings)
	index = 0
	result = b''
	for string in file_strings:
		if index != lenth - 1 and index > 2:
			result += string
			if index != lenth - 2:
				result += b'\n'
		index += 1
	return file_name + b'\n' + result

def last_file():
	if not os.path.exists('last_file'):
		write_file('last_file', '0', 'w')
	next = str(int(read_file('last_file', 'r')) + 1)
	write_file('last_file', next, 'w')
	return next

def write_new_file(file, filename):
	prove_directory('files')
	write_file('files/' + filename, file, 'wb+')

def to_temp_file(file_strings, filename):
	index = 0
	len_strings = len(file_strings)
	temp_bytes = b''
	for string in file_strings:
		if index > 0:
			if index != len_strings - 1:
				temp_bytes += string + b'\n'
			else:
				temp_bytes += string
		index += 1
	prove_directory('temp_files')
	write_file('temp_files/' + filename, temp_bytes, 'wb+')

def mini_create(file_id):
	clean_cash()
	prove_directory('minis')
	file = read_file('files/' + file_id, 'rb').split(b'\n')
	to_temp_file(file, file_id)
	os.rename('temp_files/' + file_id, 'temp_files/' + file_id + '.jpg')
	size = (50, 50)
	img = Image.open('temp_files/' + file_id + '.jpg')
	img.thumbnail(size)
	img.save('minis/' + 'mini' + file_id + '.jpg')

def clean_cash():
	prove_directory('temp_files')
	files = os.listdir('temp_files')
	if files:
		for file in files:
			os.remove("temp_files/" + file)

@csrf_exempt
def file_save(request):
	if request.method == 'POST':
		content = cut_request_file(request.body)
		file_id = last_file()
		write_new_file(content, file_id)
		return HttpResponse(json.dumps({'file_id': file_id}), content_type="application/json")
	else:
		return HttpResponse(json.dumps({'error': 400}), content_type="application/json")

@csrf_exempt
def get_file(request, file_id):
	if not os.path.exists('/Users/mstygg/Desktop/fileserv/files/' + file_id):
		return HttpResponse(json.dumps({'error': 404}), content_type="application/json")
	clean_cash()
	file = read_file('/Users/mstygg/Desktop/fileserv/files/' + file_id, 'rb').split(b'\n')
	print("file_found")
	filename = str(file[0]).split("'")[1]
	to_temp_file(file, file_id)
	response = FileResponse(open('temp_files/' + file_id, 'rb'), content_type='application/octet-stream')
	response['Content-Disposition'] = 'attachment; filename=' + filename
	return response

@csrf_exempt
def delete_file(request, file_id):
	if request.method == 'DELETE':
		token = (json.loads(request.body))['token']
		if token != TOKEN:
			return HttpResponse(json.dumps({'error': 401, 'explanation': 'the token is invalid'}), content_type="application/json")
		prove_directory('files')
		if os.path.exists('files/' + file_id):
			os.remove('files/' + file_id)
			if os.path.exists('minis/' + file_id):
				os.remove('minis/' + file_id)
			return HttpResponse(json.dumps({'success': 200}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({'error': 204}), content_type="application/json")
	else:
		return HttpResponse(json.dumps({'error': 400}), content_type="application/json")

@csrf_exempt
def get_mini(request, file_id):
	if not os.path.exists('files/' + file_id):
		return HttpResponse(json.dumps({'error': 404}), content_type="application/json")
	mini_exist = os.path.exists('minis/' + 'mini' + file_id + '.jpg')
	if not mini_exist:
		mini_create(file_id)
	filename = file_id
	response = FileResponse(open('minis/' + 'mini' + file_id + '.jpg', 'rb'), content_type='application/octet-stream')
	response['Content-Disposition'] = 'attachment; filename=' + filename
	return response
