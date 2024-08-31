import requests

def download_photo(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {file_name}")
    else:
        print(f"Failed to download {file_name}")

# URL parameters
base_url = 'http://172.16.1.19/sarahome/photos/'
file_extension = '.jpg'

# Loop to download photos
for i in range(244001, 244065):  # Adjust the range according to the number of photos
    file_number = f'{i:05d}'  # Pad the number with leading zeros (e.g., 00001, 00002, ...)
    file_name = file_number + file_extension
    photo_url = base_url + file_name
    download_photo(photo_url, file_name)
