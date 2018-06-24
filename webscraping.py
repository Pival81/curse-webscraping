from bs4 import BeautifulSoup
from requests import get
from json import dumps

class getFiles():
	cont = 1
	
	data = []

	def getfileDetails(self, url):
		html = get(url).text
		soup = BeautifulSoup(html, "html.parser")
		file_info = soup.body.find_all("div", class_="details-info")[0].find_all("li")

		self.filename = file_info[0].find_all("div")[1].text
		self.uploader = file_info[1].find_all("a")[1].text
		self.upload_date = file_info[2].find_all("abbr")[0].text
		self.size = file_info[3].find_all("div")[1].text
		self.downloads = file_info[4].find_all("div")[1].text
		self.md5 = file_info[5].find_all("span")[0].text

	
	def init(self, html):
		soup = BeautifulSoup(html, "html.parser")

		rows = soup.body.table.tbody.find_all("tr")

		for row in rows:
			row_content = row.find_all("a")
			
			name = row_content[1].text
			url = "https://minecraft.curseforge.com" + row_content[1]["href"]
			download_url = "https://minecraft.curseforge.com" + row_content[0]["href"]
			self.getfileDetails(url)
			mc_version = row.find_all("span")[0].text
			if len(row_content) == 3:
				add_files = True
			else:
				add_files = False
			self.data.append({
								"name": name,
								"filename": self.filename,
								"uploader": self.uploader,
								"upload_date": self.upload_date,
								"size": self.size,
								"downloads": self.downloads,
								"download_url": download_url,
								"number": self.cont,
								"additional_files": add_files,
								"mc_version": mc_version,
								"md5": self.md5
							})
			self.cont+= 1

class generateJson():
	def init(self, arg1: str, arg2: bool):		
		html = get(arg1 + "/files").text

		soup = BeautifulSoup(html, "html.parser")
		
		pages = len(soup.body.find_all("div", class_="b-pagination b-pagination-a")[1].find_all("li")) - 1
		pages = int(soup.body.find_all("div", class_="b-pagination b-pagination-a")[1].find_all("li")[pages-1].text)
		
		if pages == -1:
			pages = 1

		getfiles = getFiles()

		for num in range(pages):
			html = get(arg1 + "/files", params={ "page": num+1 } )
			getfiles.init(html.text)
		
		if arg2 == True:
			with open("output.json", "w") as file:
				file.write(dumps(getfiles.data, indent=4, sort_keys=True, separators=(',', ': ')))
				
if __name__ == "__main__":
	import sys
	
	start = generateJson()
	start.init(sys.argv[1], True)