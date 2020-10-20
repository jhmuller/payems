import os
import pandas as pd
from fredapi import Fred

def get_children_categories(cid,
                            fred):
    url = "https://api.stlouisfed.org/fred/"
    url += "category/children?category_id=%d&api_key=%s" % (cid, fred.api_key)
    res = fred.category_children_search(url=url)
    if res.shape[0] > 0:
        res['category_id'] = res['category_id'].apply(int)
        res.sort_values(by='category_id', inplace=True)
        res.set_index(keys='category_id', inplace=True)
    return res

def get_all_categories(api_key_file='fred_api.key'):
    fred = Fred(api_key_file=api_key_file)
    cid = 0
    res = get_children_categories(cid=cid,
                                  fred=fred)
    i = 0
    while True:
        cid = res.index[i]
        df = get_children_categories(cid=cid,
                                     fred=fred)
        msg = "cat %s had %d children\n" % (str(cid),
                                          df.shape[0])
        msg += "i=%d, res.rows=%d" % (i, res.shape[0])
        print (msg)
        res = pd.concat([res, df])
        i += 1
        if i > res.shape[0] - 1:
            break
        if res.shape[0] >= 5091:
            res.to_csv("fred_cats.csv")
            break
    return res


def get_popular_fred(num2get=100, api_key_file='fred_api.key'):
    fred = Fred(api_key_file=api_key_file)
    cid = 0
    num_fetched = 0
    res = pd.DataFrame()
    while num_fetched < num2get:
        try:
            df = fred.search_by_category(category_id=cid, order_by='popularity')
            if df.shape[0] > 0:
                df['popularity'] = df['popularity'].apply(float)
                df = df[df.popularity > 10]
        except Exception as exc:
            msg = " searching for cid = %d" % (cid,)
            msg += str(exc)
            print (msg)
        else:
            res = (df if res.shape[0] == 0
                   else pd.concat([res, df]))
            num_fetched += 1
        cid += 1
        msg = "CID= %d" % (cid,)
        print(msg)
        if cid > 2000:
            break
    res.sort_values(by='popularity', inplace=True)
    return res

def main():
    df = get_all_categories()
    #df = get_popular_fred(num2get=300)
    df.to_csv("fred_categories.csv")
    print ("done")

if __name__ == "__main__":
        main()