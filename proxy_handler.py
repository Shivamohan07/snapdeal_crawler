def get_proxy(my_proxy):
    """
    Function to set proxy

    :param my_proxy: Proxy IP Address
    :returns: dictionary
    """

    http_proxy = "http://edcguest:edcguest@{}:3128".format(my_proxy)
    https_proxy = "https://edcguest:edcguest@{}:3128".format(my_proxy)

    # Proxy dictionary definition
    proxy = {
        "http": http_proxy,
        "https": https_proxy
    }
    return proxy
