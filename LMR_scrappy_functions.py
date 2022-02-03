import requests
from bs4 import BeautifulSoup as sopa
import csv
import time

'''
Enviorment:
    BeautifulSoup
    request
    csv
    time
'''



def get_product_links(url):
    '''
    Must be a level above the product.

    ie url = "https://www.uprproducts.com/ford-vehicles/mustang/1979-1993-mustang/suspension/anti-roll-bars/?limit=30"
    '''

    page = requests.get(url)
    soup = sopa(page.content, "html.parser")
    product_listing = soup.find_all("li", class_ = "product")
    links = []

    for product in product_listing:
        a_container = product.find('a')
        links.append(a_container.get("href"))
    return links


def trim_product_decription():
    '''
    test for trimimgn text

    this is not used any where and i dont remember what this was for.... to trim the product description!
    
    '''


    url = "https://www.uprproducts.com/79-04-ford-mustang-front-motor-plate/"
    page = requests.get(url)
    soup = sopa(page.content, "html.parser")

    product_desc_raw = soup.find_all("div", class_ = "caption-display")

    product_desc = ''

    for plain_text in product_desc_raw:
        product_desc += plain_text.get_text() + "\n"

    product_desc = product_desc.replace("»", "")

    return product_desc




def get_product_info(url):
    '''
    get url from product catagory page. parent of the product it self.
    ie url = "https://www.uprproducts.com/79-04-ford-mustang-front-motor-plate/"
    this is in the wordpress format. the array

    *** need to implement a check for items that addtional options. ***    
    '''
    
    #product_img = (get img)
    #README :: Get the img url to give godaddy as they can use url to get image.

    page = requests.get(url)
    soup = sopa(page.content, "html.parser")
    
    product_name = soup.find("h1").get_text()
    product_price = soup.find("span" , class_ = "price price--withoutTax").get_text()
    product_sale_price = ''
    product_sku = soup.find_all("dd", class_ = "productView-info-value")[0].get_text()

    # this need to filter out an char that might throw of the import to a word press doc
    product_desc_raw = soup.find_all("div", class_ = "caption-display")
    product_desc = ''

    for plain_text in product_desc_raw:
        product_desc += plain_text.get_text() + "\n"

    product_desc = product_desc.replace('»', '\n')
    product_desc = product_desc.replace('\xa0', '')
    product_desc = product_desc.replace('&', 'and')

    #this is to get the url of the imag but i dont think word press uses this. i think this was for wix...
    product_img_url = soup.find_all("img")[3].get("data-src")

    product_track_inventory = "FALSE"
    product_qty = ''
    product_sale_price = ''
    product_backorder = ''
    product_weight = ''
    product_lenght = ''
    product_width = ''
    product_height = ''
    product_tax_catagory = ''
    product_hidden = 'FALSE'
    product_catagory = ''
    product_seo_title = ''
    product_seo_desc = ''
    product_option1_name = ''
    product_option1_val = ''
    product_option2_name = ''
    product_option2_val = ''
    product_option3_name = ''
    product_option3_val = ''
    product_addon1_name = ''
    product_addon1_type = ''
    product_addon1_req = ''
    product_addon1_val = ''
    product_addon2_name = ''
    product_addon2_type = ''
    product_addon2_req = ''
    product_addon2_val = ''
    product_addon3_name = ''
    product_addon3_type = ''
    product_addon3_req = ''
    product_addon3_val = ''

    product_details = [product_name, product_sku, product_price, product_sale_price, product_desc, product_track_inventory, product_qty, product_backorder, product_weight, product_lenght, product_width, product_height, product_tax_catagory, product_hidden, product_catagory, product_img_url, product_seo_title, product_seo_desc, product_option1_name, product_option1_val, product_option2_name, product_option2_val, product_option3_name, product_option3_val, product_addon1_name, product_addon1_type, product_addon1_req, product_addon1_val, product_addon2_name, product_addon2_type, product_addon2_req, product_addon2_val, product_addon3_name, product_addon3_type, product_addon3_req, product_addon3_val]

    return product_details


def LMR_scrapper(product_catagory_url, file_name):

    # set the column names in word press format
    col_title = ['Product Name', 'SKU', 'Price', 'Sale Price', 'Description', 'Track Inventory', 'QTY', 'Backorder', 'Weight	Length', 'Width', 'Height', 'Tax Category', 'Hidden', 'Category', 'Image URL', 'SEO Title', 'SEO Desc', 'Option1 Name', 'Option1 Values', 'Option2 Name', 'Option2 Values', 'Option3 Name', 'Option3 Values', 'Add-on1 Name', 'Add-on1 Type', 'Add-on1 Required', 'Add-on1 Values', 'Add-on2 Name', 'Add-on2 Type', 'Add-on2 Required', 'Add-on2 Values', 'Add-on3 Name', 'Add-on3 Type', 'Add-on3 Required', 'Add-on3 Values']

    #product_catagory_url = "https://www.uprproducts.com/1979-1993/suspension/a-arms/"


    #this site does not have more than 100 items per category
    product_catagory_url += "?limit=100"
    
    single_product_url_list = []

    single_product_url_list = get_product_links(product_catagory_url)
    my_file = open (file_name+'.csv', mode = 'w')

    product_writer = csv.writer(my_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL, lineterminator = '\n')
    product_writer.writerow(col_title)
    
    number_of_urls = len(single_product_url_list)
    print (number_of_urls)
    count = 1
    count_fail = 0
    
    for product in single_product_url_list:
        try:
            # time delay as not inavertly DoS.
            time.sleep(1)

            info = get_product_info(product)
            product_writer.writerow(info)
            print(str(count) + "    " + product)
            count += 1

        except:
                fail_file = open (file_name+"_FAIL.txt", 'a')
                fail_file.write("FAIL AT: " + product +"\n")
                fail_file.close()
                count_fail +=1

    my_file.close()

    return f" *** DONE *** fail_count{count_fail} *** "



#url = "https://www.uprproducts.com/79-04-ford-mustang-front-motor-plate/"
#print(get_product_info(url))
