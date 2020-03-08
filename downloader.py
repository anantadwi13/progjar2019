import logging
import requests
import os
import threading



def download_gambar(id, url=None):
    if (url is None):
        return False
    ff = requests.get(url)
    tipe = dict()
    tipe['image/png']='png'
    tipe['image/jpg']='jpg'
    tipe['image/jpeg']='jpg'

    content_type = ff.headers['Content-Type']
    logging.warning(content_type)
    if (content_type in list(tipe.keys())):
        namafile = os.path.basename(url)
        ekstensi = tipe[content_type]
        logging.warning(f"writing {namafile}.{ekstensi}")
        fp = open(f"{id}_{namafile}.{ekstensi}","wb")
        fp.write(ff.content)
        fp.close()
    else:
        return False


url_gambars = [
    'https://www.its.ac.id/wp-content/uploads/sites/2/2020/02/WhatsApp-Image-2020-02-12-at-16.02.13-1024x683.jpeg',
    'https://www.its.ac.id/wp-content/uploads/sites/2/2020/02/WhatsApp-Image-2020-02-12-at-16.02.13-1024x683.jpeg',
]

threads = []

if __name__=='__main__':
    for id, url in enumerate(url_gambars):
        t = threading.Thread(target=download_gambar,args=(id, url,))
        threads.append(t)
        t.start()
