from proxy_handler import *
import requests
from requests.exceptions import *


def grab_code_from_page(page_url, ip_address="0"):
    """
    Function to get the source code of the url provided

    :param ip_address: Proxy IP Address
    :param page_url: URL of the page
    :returns: string formatted source code
    """

    # print("In code grabber")
    # Acting as mozilla browser while requesting data from server
    user_agent = "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"

    # Making a connection along with proxy handling
    try:
        if ip_address != "0":
            my_proxy = get_proxy(ip_address)
            response = requests.get(page_url, headers={'User-Agent': user_agent}, proxies=my_proxy)
        else:
            response = requests.get(page_url, headers={'User-Agent': user_agent})

        if response.status_code == requests.codes.ok:
            response.close()
            return response.text
        else:
            print("Error {} this is".format(response.status_code))
            log_file = open("logs.txt", 'a')
            log_file.write("\nError {} while retrieving {}\n".format(response.status_code, page_url))
            log_file.close()
            return 0

    except ProxyError as e:
        print("Unable to connect to {}\n".format(ip_address))
        log_file = open("logs.txt", 'a')
        log_file.write("\nException occurred while getting {}\nException: {}\n".format(page_url, e))
        log_file.close()
        exit()

    except Exception as e:
        print(e)
        log_file = open("logs.txt", 'a')
        log_file.write("\nException occurred while getting {}\nException: {}\n".format(page_url, e))
        log_file.close()
        exit()
