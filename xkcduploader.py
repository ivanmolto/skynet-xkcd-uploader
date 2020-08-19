import siaskynet
import requests
import webbrowser
import os
import bs4

blurb_description = 'This is the Skylink that you can share with anyone to retrieve your comic image on any Skynet Webportal:'
blurb_url = 'Please check at the follow link: '
blurb_host = 'https://siasky.net/'

url = 'http://xkcd.com'
while not url.endswith('#'):
    print(f'Downloading page {url}...')
    response = requests.get(url)
    response.raise_for_status()
    soup_object = bs4.BeautifulSoup(response.text, 'html.parser')
    comic_img_element = soup_object.select('#comic img')
    if comic_img_element == []:
        print('Sorry a comic image was not found.')
    else:
        comic_url = 'http:' + comic_img_element[0].get('src')
        print(f'Downloading image {comic_url} to your current directory...')
        response = requests.get(comic_url)
        response.raise_for_status()
        imageFile = open(os.path.basename(comic_url), 'wb')
        for chunk in response.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

    prevLink = soup_object.select('a[rel="prev"]')[0]
    url = 'http://xkcd.com' + prevLink.get('href')
    if url.endswith('/1/'):
        break

for root, dirs, files in os.walk("."):
    for filename in files:
        if "png" in filename:
            comic_download_image = filename
            print(
                f'Now uploading your comic image {comic_download_image} to Skynet...')
            print(blurb_description)
            skylink = siaskynet.upload_file(comic_download_image)
            print(skylink)
            url_link = blurb_host + skylink[6:]
            print(blurb_url + url_link)
            webbrowser.open_new(url_link)
            print()
