import json
import os
from datetime import datetime
import requests
import sys
import time

json_file = "mina.json"

def get_filePath():
    return os.path.abspath(json_file)


if not os.path.exists(json_file):
    with open(json_file, 'w') as file:
        json.dump([], file)

def save_cache(port, origin, response):
    with open(json_file, 'r') as file:
        requests = json.load(file)
    
    request = {
        'port': port,
        'origin': origin,
        'response': response
    }
        
    requests.append(request)
    
    with open(json_file, 'w') as file:
        json.dump(requests, file, indent=4)


def search_cache(port, origin):
    with open(json_file, 'r') as file:
        requests = json.load(file)
        
    for request in requests:
        if request['port'] == port and request['origin'] == origin:
            return request['response']
    return None


def ask_origin(port, origin):
    url = origin
    
    # headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    # 'Accept': 'application/json',
    # 'Accept-Language': 'en-US,en;q=0.9',
    # 'Connection': 'keep-alive'
    # }
    
    response = requests.get(url)
    print(F"Status code: {response.status_code}")
    # print(response)

    data = response.json()
    products = data['products']
    save_cache(port, origin, products)
    for product in products:
        print(f"ID: {product['id']}, Name: {product['title']}")
        
        
def clear_cache():
    with open(json_file, 'w') as file:
        json.dump([], file)
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("please enter valid requests!")
        sys.exit(1)
        
        # caching-proxy --port <number> --origin <url>
    if sys.argv[1] == "--port" and sys.argv[3] == "--origin":
        port = sys.argv[2]
        origin = sys.argv[4]
        
        start_time = time.time()
        responses =  search_cache(port, origin)
        
        if responses != None:
            
            for response in responses:
                print(f"ID: {response['id']}, Name: {response['title']}")
                
            end_time = time.time()     
            elipse_time = end_time - start_time  
            print(f"Response --X-Cache: HIT-- : at {elipse_time}")  
            print(f"JSON file path: {get_filePath()}")
        
        else:
            start_time = time.time()
            ask_origin(port, origin)
            end_time = time.time()
            elipse_time = end_time - start_time
            print(f"Response --X-Cache: MISS-- : at {elipse_time}")
            print(f"JSON file path: {get_filePath()}")
            
        # caching-proxy --clear-cache
    elif sys.argv[1] == "--clear-cache":
        clear_cache()
        print("Cache Cleared")
    else:
        print("Unknown command!")

    # python proxy.py --port 3000 --origin http://dummyjson.com/products
    # python proxy.py --clear-cache
    # python -u "c:\Users\micheal.MICHOOL\Desktop\caching proxy\proxy.py" --clear-cache
    # python -u "c:\Users\micheal.MICHOOL\Desktop\caching proxy\proxy.py" --port 3000 --origin http://dummyjson.com/products
            