text = ""
	job_title = ""
	location = ""
	Organization = ""
	Contact =""
	Date = ""
	if request.method == "POST":
		image = request.FILES.get('img')
		img_data = image.read()
		nparr = np.fromstring(img_data, np.uint8)
		img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply thresholding
		(thresh, binary) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Find contours
		(contours, _) = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours
		areas = [cv2.contourArea(c) for c in contours]
		max_index = np.argmax(areas)
		cnt = contours[max_index]

        # Draw bounding box
		x, y, w, h = cv2.boundingRect(cnt)
		cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Crop the table
		table_img = img[y:y+h, x:x+w]

        # Preprocess the image
		gray = cv2.cvtColor(table_img, cv2.COLOR_RGB2GRAY)
		(thresh, binary) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		kernel = np.ones((3,3), np.uint8)
		binary = cv2.erode(binary, kernel, iterations=1)
		coords = np.column_stack(np.where(binary > 0))
		angle = cv2.minAreaRect(coords)[-1]
		if angle < -45:
			angle = -(90 + angle)
		else:
			angle = -angle
		(h, w) = binary.shape[:2]
		center = (w // 2, h // 2)
		M = cv2.getRotationMatrix2D(center, angle, 1.0)
		binary = cv2.warpAffine(binary, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        # Perform OCR
		text = pytesseract.image_to_string(binary, lang='eng', config='--psm 6')
		print(text)
		# job_title = text.split('JOB TITLE:')[1].split('\n')[0].strip()
		# location = text.split('LOCATION:')[1].split('\n')[0].strip()
		# Organization = text.split('ORGANIZATION:')[1].split('\n')[0].strip()
		# Contact = text.split('CONTACT:')[1].split('\n')[0].strip()
		# Date = text.split('DATE:')[1].split(',')[0].strip()
		# date_section = text.split('DATE:')[1].split('\n')[0].strip()
		# values = date_section.split(',')

		# value_before_comma = values[0].strip()
		# if len(values) > 1:
		#     value_after_comma = values[1].strip()
		# else:
		#     value_after_comma = "No value after comma"

		# print("Value before comma:", value_before_comma)
		# print("Value after comma:", value_after_comma)

		# print("Title:" , job_title)
		# print("location:" ,location)
		# print("Organization:", Organization)
		# print("Contact:", Contact)
		# print("Date:", Date)
        # Display image
        # cv2.imshow('Table Detection', img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	context ={'Title':job_title,'Location':location,'Organization':Organization,'Contact':Contact,'Date':Date}