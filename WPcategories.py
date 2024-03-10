
import requests

def get_category_ids (category_slugs = '', include_children = '', url_base = 'https://www.ktoo.org' ):


    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        'Connection': "keep-alive",
        'Accept-Encoding': "gzip, deflate",
        'Postman-Token': "0,4eef3916-2e17-4176-81a5-1c5ade2848bc",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "www.ktoo.org",
        'cache-control': "no-cache"
        }



    ###############
    # Turn the slugs into IDs
    category_ids = []

    #print (category_slugs)
    url = url_base + '/wp-json/wp/v2/categories?slug=' + category_slugs + '&per_page=100'

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print ("error: ", resp.status_code)
        print (url)
    else:
        #print (resp.headers['X-WP-Total'])
        for category in resp.json():
            category_ids.append(category['id'])
            #print(category)

    if (not include_children):
        return (','.join(str(x) for x in category_ids))

    else:
        def get_children_by_id (id):

            url = 'https://www.ktoo.org/wp-json/wp/v2/categories?parent=' + str(id) + '&per_page=100'

            response = requests.get (url, headers=headers)

            child_categories = []

            for category in response.json():
                child_categories = child_categories + get_children_by_id(category['id'])
                #print(child_categories)
            return child_categories + [id]

        all_ids = []

        for category in category_ids:
            all_ids = all_ids + get_children_by_id(category)

        return (','.join(str(x) for x in all_ids))
