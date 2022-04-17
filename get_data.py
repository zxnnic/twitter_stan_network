import requests
import json
from secret import *
import pandas as pd


def create_url(id):
    # Replace with user ID below
    # user_id = 884378714 # SMTOWNGLOBAL
    max_results = 'max_results=1000'
    return "https://api.twitter.com/2/users/{}/following?{}".format(id, max_results)

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2FollowingLookupPython"
    return r

def get_params():
    return {"user.fields": "created_at"}

def connect_to_endpoint(url, params=None, next_token=None):
    if params is not None:
        params['next_token'] = next_token   #params object received from create_url function
        response = requests.request("GET", url, params = params, auth=bearer_oauth,)
    else:
        response = requests.request("GET", url, auth=bearer_oauth,)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

    return response.json()

def create_json(f_name, json_response):
    f = open('./data/'+f_name+'.json', 'w')
    json.dump(json_response, f, sort_keys=True)
    f.close()

def pretty_txt(f_name, json_response):
    f = open('./data/'+f_name+'_followers.txt', 'w')
    json.dump(json_response, f, indent=4, sort_keys=True)
    f.close()
    
def get_sm_data():
    # get 3000 people that follow SMTOWNGLOBAL
    url = create_url()
    params = get_params()
    json_response = None
    for n in range(2):
        json_response = connect_to_endpoint(url, params)
        # print(json.dumps(json_response, indent=4, sort_keys=True))
        create_json('SMTOWNGLOBAL_'+str(n), json_response)
    
def get_stan_data(f):
    with open(f, encoding='utf-8') as f_obj:
        data = json.load(f_obj)['data']
    
    acc_un = ['rvsmtown', 'girlsgeneration', 'nctsmtown', 'shinee', 'sjofficial', 'aespa_official', 'weareoneexo']
    for entry in data:
        id = entry['id']
        url = create_url(id)
        params = get_params()
        # get max 1000 following
        json_response = connect_to_endpoint(url, params)
        if 'errors' in json_response.keys():
            print(id, 'private acc')
        else:
            print(id)
            create_json('following/i_'+id,json_response)
        # check if acc is following more than 10 accounts
        if 'errors' not in json_response.keys() and json_response['meta']["result_count"] > 10:
            # first store obtained data into all
            # convert json_response to dataframe
            df = pd.DataFrame.from_dict(json_response['data'])
            # get all usernames they are following
            following_list = df['username'].tolist()
            following_list =(map(lambda x: x.lower(), following_list))
            # check if they follow one of the other accounts
            found = False
            n = 0
            while not found and n < len(acc_un):
                if acc_un[n].lower() in following_list:
                    found = True
                else:
                    n += 1
            if found:
                create_json('following/i_'+id, json_response)
                

if __name__ == "__main__":
    # get_sm_data()
    get_stan_data('./data/SMTOWNGLOBAL_followers.json')


