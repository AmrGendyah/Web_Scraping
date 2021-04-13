from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs, urlencode
import json

URL= "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22usersSearchTerm%22%3A%22Miami%2C%20FL%22%2C%22mapBounds%22%3A%7B%22west%22%3A-80.54059341902641%2C%22east%22%3A-79.96147658097354%2C%22south%22%3A25.491795827322694%2C%22north%22%3A26.052877951724916%7D%2C%22mapZoom%22%3A11%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12700%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%2C%22sortSelection%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%7D&wants={%22cat1%22:[%22listResults%22,%22mapResults%22],%22cat2%22:[%22total%22]}&requestId=4"
Api_Cookies='zguid=23|%245f3f8e67-b493-4453-b338-2f7355a0ee81; zgsession=1|02aff571-3750-4662-a44b-5073709d23a5; _ga=GA1.2.2054106970.1616541032; zjs_user_id=null; _pxvid=f75a15ab-8c2c-11eb-9604-0242ac120010; _gcl_au=1.1.2055763478.1616541033; DoubleClickSession=true; _fbp=fb.1.1616541032833.1003257010; _pin_unauth=dWlkPU5EUTFOamcwTldJdE9UVXpZeTAwT0RJNExXSTJPRE10T0RjNU5URTFORGcwWmpJMw; _uetvid=f7bdf0908c2c11ebb5ed1f48f8629f8d; zjs_anonymous_id=%225f3f8e67-b493-4453-b338-2f7355a0ee81%22; g_state={"i_p":1617378755690,"i_l":3}; KruxPixel=true; JSESSIONID=6B1758F53ADD7409E0EEAC3EB53D7C6E; _gid=GA1.2.318303111.1616906004; utag_main=v_id:017868ed27b5001e7e7d3b92df8c03072001d06a00c98$_sn:4$_se:1$_ss:1$_st:1616907806984$dc_visit:4$ses_id:1616906006984%3Bexp-session$_pn:1%3Bexp-session$tdsyncran:1%3Bexp-session$dc_event:1%3Bexp-session$dc_region:eu-central-1%3Bexp-session$ttd_uuid:c818b067-f46e-4f07-aa51-8285a21efe9a%3Bexp-session; KruxAddition=true; _pxff_bsco=1; _uetsid=bd4582e08f7e11eb83f985220eb3308c; _px3=1603b3f0283fa10816c7e6b9fe930d8a1565bfb37a0de5c7aacc2741e6d27a6d:ckZfnrjexky8bhGKRbwMSNGtlUfEUHVjAzWNh1jltBi5/rssLEEAXgLUaDATzIQ7MqjZT+ecaVSd+HCbsgwp7A==:1000:T6xzFW5z3vvXwZjXRB+U+9BLTUPZE65RRyK6QAGgjw9nIMqaE8sRTDdFcGwjsIdHtvLQT6uQpK3th9QTjpyEfaXNCzBDHFLRAIuVR8UPGlovcIXFIaFNF6fxjOP8HDBVKAMA3OwY8DLVg/4sSnjmPaz5WjeQejA/F6OXWnQB9Lg=; _gat=1; AWSALB=tp3ZwNTpPXx2wm7mWv5GdMD0ZBoQQaDXI+XWuDJloXHsNUYp90sAknbAy+Xke0HwaYYEsHGbxHa4TLRqHqfVyOP0Ii7yrM/m0TkLmX6UQWIyNN05lGhxAKP2gilP; AWSALBCORS=tp3ZwNTpPXx2wm7mWv5GdMD0ZBoQQaDXI+XWuDJloXHsNUYp90sAknbAy+Xke0HwaYYEsHGbxHa4TLRqHqfVyOP0Ii7yrM/m0TkLmX6UQWIyNN05lGhxAKP2gilP; search=6|1619498729869%7Crect%3D25.855607%252C-80.142305%252C25.689672%252C-80.359765%26rid%3D12700%26disp%3Dmap%26mdm%3Dauto%26p%3D2%26z%3D1%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%0912700%09%09%09%09%09%09'


def cookie_parser():
    cookie_string = Api_Cookies
    cookie = SimpleCookie()
    cookie.load(cookie_string)
    cookies_dic = {}
    for key, morsel in cookie.items():
        cookies_dic[key] = morsel.value

    return cookies_dic


def parse_new_url(url, pg_num):
    url_parsed = urlparse(url)

    ### to get the link/url for next page, use.query
    ### use parse_qs to parse/inject it as a python dictionary not a string
    query_string = parse_qs(url_parsed.query)

    srch_query_state = json.loads(query_string.get('searchQueryState')[0])

    ### Inject page number
    srch_query_state['pagination'] = {'currentPage': pg_num}

    ### Update query_string to the next page/page number
    query_string.get('searchQueryState')[0] = srch_query_state

    ### Encode new query_string to constructe a URL
    ### Set doseq=1 to prevent convertion of query_string's values to string
    encoded_qs = urlencode(query_string, doseq=1)
    new_url= f"https://www.zillow.com/search/GetSearchPageState.htm?{encoded_qs}"
    
    return (new_url)
