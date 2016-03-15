from bs4 import BeautifulSoup
from code_grabber import *
import os
import re


def make_reviews(source_code, ip_address):
    """
    Function to write review details.
    If no more products exits, the program halts.

    :param ip_address: Proxy IP Address
    :param source_code: source code of web page to crawl,
    get links of mobiles and iterate over each link to get the reviews
    """

    try:
        dom = BeautifulSoup(source_code, "html.parser")
    except TypeError:
        return

    # Check if received page contains any products
    # Snapdeal server sends empty with a '0' in it if there are no more products
    if dom.select("div.jsNumberFound.hidden")[0].string == "0":
        print("No more products\nTask completed!")
        exit(0)
    else:
        a_tags = dom.select("div.product-desc-rating.title-section-expand a")
        for tag in a_tags:
            mobile_link = tag["href"]
            print(mobile_link)
            page_num = 0
            review_no = 0

            while True:
                page_num += 1
                print("--Review page {}".format(page_num))
                review_link = "{}/reviews?page={}".format(mobile_link, page_num)
                try:
                    # Get link from parent page (Page containing all 48 links)
                    mobile_code = grab_code_from_page(review_link, ip_address)

                    if mobile_code != 0:
                        # If reviews are found
                        mobile_dom = BeautifulSoup(mobile_code, "html.parser")

                        # Get name of mobile from it's page
                        mobile_name = str(mobile_dom.select("span.section-head.customer_review_tab")[0].string)

                        # mobile_name = "Mobile"
                        mobile_name = re.sub(r'[\r\n\t]', '', mobile_name)
                        mobile_name = mobile_name.strip(' ')

                        # Replacing path separator from filename with '-' if any
                        mobile_name = str(mobile_name).replace(os.path.sep, "-")

                        file_name = mobile_name + ".txt"

                        try:
                            if page_num == 1:
                                # Creating a file with mobile name (Clear data if file already exists)
                                review_file = open(os.path.join("reviews", file_name), 'w')
                                review_file.write("{}\t{}\t{}\t{}\t{}\t{}\n".format('Review No.', 'Reviewer Name', 'Date', 'Verified Buyer', 'Title', 'Review'))
                                review_file.close()

                            # Opening file to write reviews
                            comment_list = mobile_dom.select("div.commentlist.first")
                            no_of_comments = len(comment_list)

                            # Break out of infinite loop if no more reviews are found
                            if no_of_comments == 0:
                                break

                            review_file = open(os.path.join("reviews", file_name), 'a')
                            for i in range(0, no_of_comments):
                                review_no += 1
                                review_file.write("{}\t".format(review_no))

                                # Reviewer name
                                name = (comment_list[i].select("span._reviewUserName"))[0].string
                                name = re.sub(r'[\n\t\r]', ' ', name)
                                review_file.write("{}\t".format(name))

                                # Review Date
                                date = (comment_list[0].select("div.date.LTgray"))[0].string
                                date = re.sub(r'[\n\t\r]', ' ', date)
                                review_file.write("{}\t".format(date))

                                # Verified User
                                try:
                                    if (comment_list[i].select("div.LTgray.light-font"))[0].contents[1] == "Verified Buyer":
                                        review_file.write("Yes\t")
                                except:
                                    review_file.write("No\t")

                                # Review Title:
                                title = (comment_list[i].select("div.head"))[0].string
                                title = re.sub(r'[\n\t\r]', ' ', title)
                                review_file.write("{}\t".format(title))

                                # Review
                                review = (comment_list[i].select("div.user-review p"))[0].string
                                review = re.sub(r'[\t\n\r]', ' ', review)
                                review_file.write("{}\n".format(review))
                            review_file.close()

                        except FileNotFoundError as e:
                            print("Couldn't open file {}. Skipping...".format(file_name))
                            log_file = open("logs.txt", 'a')
                            log_file.write("\nCouldn't open file {}. Skipped writing reviews\nException: {}".format(file_name, e))
                            log_file.close()

                    else:
                        # If no reviews are found a product, writing No reviews to file
                        no_reviews(mobile_link, ip_address)

                        # Break out of loop
                        break
                except Exception as e:
                    print(e)
                    log_file = open("logs.txt", 'a')
                    log_file.write("\nException while processing: {}\nException: {}\n".format(review_link, e))


def no_reviews(mobile_link, ip_address):
    """
    If no reviews are found, write no reviews in the file

    :param mobile_link: Link to mobile page
    :param ip_address: Proxy IP Address
    :return:
    """

    source_code = grab_code_from_page(mobile_link, ip_address)
    mobile_dom = BeautifulSoup(source_code, 'html.parser')
    mobile_name = mobile_dom.select("h1.pdp-e-i-head")[0].string
    file_name = mobile_name + ".txt"

    try:
        # Creating a file with mobile name (Clear data if file already exists)
        review_file = open(os.path.join("reviews", file_name), 'w')
        review_file.close()

        # Opening file to write reviews
        review_file = open(os.path.join("reviews", file_name), 'a')
        review_file.write("{}\nLink: {}\n\n".format(mobile_name, mobile_link))
        review_file.write("{:-^50}\n".format("Reviews"))
        review_file.write("No Reviews Found")

    except FileNotFoundError as e:
        print("Couldn't open file {}. Skipping...".format(file_name))
        log_file = open("logs.txt", 'a')
        log_file.write("\nCouldn't open file {}. Skipped writing reviews\nException: {}".format(file_name, e))
        log_file.close()
