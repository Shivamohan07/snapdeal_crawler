"""
Python code to grab reviews of mobiles from www.snapdeal.com
Python version required: 3 or above

Link: "http://www.snapdeal.com/products/mobiles-mobile-phones?sort=plrty"
Equivalent link of ajax request (Grabbed by monitoring from dev tools in browser):
"http://www.snapdeal.com/acors/json/product/get/search/175/x/48"

The 'x' in the above given url is replaced with a value to get result of x to x+48 mobiles

"""
from review_grabber import *

# Getting proxy IP address
ip_address = (str(input("Enter proxy IP address (for Direct connection enter 0):"))).strip(' ')

# Creating Reviews directory
os.makedirs("reviews", 0o777, exist_ok=True)

# Creating a log file
log_file = open("logs.txt", 'w')
log_file.write("Caught Exceptions\n")
log_file.close()

base_url = "http://www.snapdeal.com/acors/json/product/get/search/175/{}/48"
product_num = 0
while True:
    url = base_url.format(product_num)
    print("Processing products {}-{}".format(product_num, product_num+47))
    source_code = grab_code_from_page(url, ip_address)
    if source_code != 0:
        make_reviews(source_code, ip_address)
    product_num += 48   # Snapdeal server sends 48 products per one GET request
