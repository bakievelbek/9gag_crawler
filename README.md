# 9Gag Module assignment description


### 9Gag module scraper is created to crawl the posts of a specific user.
### Input parameters are: Username, number of posts (default = 100) and the output format (json, csv, pdf)


#### Ways to run:

1. Using API:
   - Run command in the command line: 
      ```bash
      uvicorn api.app:app --reload
   from the project directory (It starts FastAPI)
   - Open browser page [localhost:8000/docs]()
   - Insert username, limit and the output format

2. Using Command line:
   - Simply paste 
      ```bash
      scrapy crawl ninegag_user_posts -a user={username} -a limit={limit} -s OUTPUT_FORMAT={output format} 
   in the command line

3. Results can be found in the ***items/*** folder. New files will appear directly in a root folder


Example of the datastructure that was chosen:


```json
{
        "id": "aoy02ew",
        "title": "If true, this is a brilliant idea! - 9GAG",
        "url": "https://9gag.com/gag/aoy02ew",
        "images": {
            "image700": {
                "width": 526,
                "height": 526,
                "url": "https://img-9gag-fun.9cache.com/photo/aoy02ew_700b.jpg",
                "webpUrl": "https://img-9gag-fun.9cache.com/photo/aoy02ew_700bwp.webp"
            },
            "image460": {
                "width": 460,
                "height": 460,
                "url": "https://img-9gag-fun.9cache.com/photo/aoy02ew_460s.jpg",
                "webpUrl": "https://img-9gag-fun.9cache.com/photo/aoy02ew_460swp.webp"
            },
            "imageFbThumbnail": {
                "width": 220,
                "height": 220,
                "url": "https://img-9gag-fun.9cache.com/photo/aoy02ew_fbthumbnail.jpg"
            }
        },
        "interaction_statistics": {
            "likes": 0,
            "dislikes": 0,
            "comments": 0
        },
        "created_at": "2024-05-29 19:59:44"
    }