import cloudinary
from downloadImg import KeywordNameDownloader,KeywordGoogleImageCrawler
from pymongo import MongoClient
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

cloudinary.config(
    cloud_name = "yourname",
    api_key = "youkey_api",
    api_secret = "yoursecret_api",
    secure = True
)


client = MongoClient('YOUR MONGODB CONECTION')

db = client.get_database()
collection = db['cars']
cursor = collection.find({},{'_id': 0,'ToyNum': 0,'Series': 0,'SeriesNum': 0})
cars = []

for document in cursor:
    #format data
    name = document['Brand'] + " " + document['ModelName'] + " " + str(document['Year']) + " " + str(document['ColNum']) + " " + document['Version']
    model = name.replace("/","",1)
    modelN = document['ModelName'].replace("/","",1)
    cars.append(model)
    #download images from google
    google_crawler = KeywordGoogleImageCrawler(downloader_cls=KeywordNameDownloader, storage={'root_dir': 'image_downloads'})
    google_crawler.crawl(keyword=document, max_num=1)
    #upload images in cloudinary
    result = upload("./Folder/" + model + ".jpg",
                    public_id=modelN + " " + document['Version'] + " " + str(document['ColNum']))
    collection.update_one({'ModelName': document['ModelName'], 'Version':document['Version'], 'ColNum': str(document['ColNum'])},{'$set': {'Img':result['url']}})

print(cars)

