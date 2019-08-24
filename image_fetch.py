# importing google_images_download module 
from google_images_download import google_images_download 
import sys

# creating object 
response = google_images_download.googleimagesdownload() 

search_queries = []

f = open("keyword.txt", "r")
if f.mode=="r":
	contents = f.read()
	search_queries.append(contents)



def downloadimages(query): 
	# keywords is the search query 
	# format is the image file format 
	# limit is the number of images to be downloaded 
	# print urs is to print the image file url 
	# size is the image size which can 
	# be specified manually ("large, medium, icon") 
	# aspect ratio denotes the height width ratio 
	# of images to download. ("tall, square, wide, panoramic") 
	arguments = {"keywords": query, 
				"format": "jpg", 
				"limit":1, 
				"print_urls":True, 
				"size": "medium", 
				"aspect_ratio": "panoramic"} 
	try: 
		response.download(arguments) 
	
	# Handling File NotFound Error	 
	except FileNotFoundError: 
		arguments = {"keywords": query, 
					"format": "jpg", 
					"limit":1, 
					"print_urls":True, 
					"size": "medium"} 
					
		# Providing arguments for the searched query 
		try: 
			# Downloading the photos based 
			# on the given arguments 
			response.download(arguments)
		except: 
			pass

# Driver Code 
# orig_stdout = sys.stdout
# f = open('URLS.txt', 'w+')
# sys.stdout = f

for query in search_queries:
	downloadimages(query)
	#f.write(",")
	#print("==============================================================")

# sys.stdout = orig_stdout
# f.close()
