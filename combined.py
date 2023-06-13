from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import random
from utils import userAgent

app = Flask(__name__)


def amazonDataScrapper(prod_type, prod_count) :
    def get_title_amazon(soup) :
        try :
            # Outer Taging Object
            title = soup.find("span", attrs={"id" : "productTitle"})
            title_value = title.string
            title_string = title_value.strip()
        except AttributeError :
            title_string = "NA"
        return title_string


    def get_price_amazon(soup) :
        try :
            price = soup.find("span", attrs={"class" : "a-price aok-align-center"}).find(
                "span", attrs={"class" : "a-offscreen"}
            ).text.strip()
            if len(price) >= 10 :
                price = "NA"
        except AttributeError :
            try :
                # Trying for some deal price
                price = soup.find("span", attrs={"class" : "a-offscreen"}).string.strip()
                if len(price) >= 10 :
                    price = "NA"
            except :
                price = "NA"
        return price


    def get_rating_amazon(soup) :
        try :
            rating = soup.find("i", attrs={"class" : "a-icon a-icon-star a-star-4-5"}).string.strip()
        except AttributeError :
            try :
                rating = soup.find("span", attrs={"class" : "a-icon-alt"}).string.strip()
            except :
                rating = "NA"
        return rating


    def get_review_count_amazon(soup) :
        try :
            review_count = soup.find("span", attrs={"id" : "acrCustomerReviewText"}).string.strip()
        except AttributeError :
            review_count = "NA"
        return review_count


    def get_availability_amazon(soup) :
        try :
            available = soup.find("div", attrs={"id" : "availability"})
            available = available.find("span").string.strip()
        except AttributeError :
            available = "NA"
        return available
    
    # Code calling begins here......
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language' : 'en-US'
    }
    url = f"https://www.amazon.com/s?k={prod_type}"
    webpage = requests.get(url, headers=headers)

    soup = BeautifulSoup(webpage.content, "lxml")

    links = soup.find_all("a", attrs={"class" : "a-link-normal s-no-outline"})
    links_list = []
    for link in links :
        links_list.append(link.get("href"))

    product_details_amazon = []

    for link in links_list[:prod_count] :
        new_webpage = requests.get("https://www.amazon.com" + link, headers=headers)
        new_soup = BeautifulSoup(new_webpage.content, "lxml")

        title = get_title_amazon(new_soup)
        price = get_price_amazon(new_soup)
        rating = get_rating_amazon(new_soup)
        review_count = get_review_count_amazon(new_soup)
        availability = get_availability_amazon(new_soup)

        product_details_amazon.append({
            "title" : title,
            "price" : price,
            "rating" : rating,
            "review_count" : review_count,
            "availability" : availability,
        })
        
    return product_details_amazon


def flipkartDataScrapper(prod_type, prod_count) :

    def get_title_flipkart(soup):
        try:
            # Outer Tag Object
            title = soup.find("span", attrs={"class":'B_NuCI'})
            print(title.text)
            # Inner NavigatableString Object
            # title_value = title.string
            title_value = title.text

            # Title as a string value
            title_string = title_value.strip()
            print(title_string)
            
        except AttributeError:
            title_string = ""	
            
        return title_string
    
    # Function to extract Product Price
    def get_price_flipkart(soup):
        try:
            price = soup.find("div", attrs={"class": "_25b18c"}).find(
                    "div", attrs={"class": "_30jeq3 _16Jk6d"}
                ).text.strip()
            if len(price) >= 10 :
                price = "NA"
        except AttributeError:

            try:
                # If there is some deal price
                price = soup.find("span", attrs={"class": "a-offscreen"}).string.strip()
                if len(price) >= 10 :
                    price = "NA"
            except:
                price = ""

        return price
    
    # Function to extract Product Rating
    def get_rating_flipkart(soup):
        try:
            rating = soup.find("span", attrs={'class':'_2_R_DZ'}).find("span").find("span").string.strip()
            
            # print(rating)
        except AttributeError:
            
            try:
                rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
            except:
                rating = ""	

        return rating
    
    # Function to extract Number of User Reviews
    def get_review_count_flipkart(soup):
        try:
            review_count = soup.find("span", attrs={'class':'_2_R_DZ'}).find("span").find_all("span")[2].string.strip()
            
        except AttributeError:
            review_count = ""	

        return review_count
    
    # Function to extract Availability Status
    def get_availability_flipkart(soup):
        try:
            available = soup.find("span", attrs={'class': '_1TPvTK'}).string.strip()
            # available = available.find("span").string.strip()

        except AttributeError:
            available = "Not Available"	

        return available

    # Code calling begins here.....	
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language' : 'en-US'
    }

    # The webpage URL
    url = f"https://www.flipkart.com/search?q={prod_type}"

    # HTTP Request
    webpage = requests.get(url, headers=headers)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class': '_1fQZEK'})
    # print(links[0])

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
        links_list.append(link.get('href'))
    
    # print(links_list[0])

    product_details_flipkart = []

    # Loop for extracting product details from each link
    for link in links_list[:prod_count]:
        new_webpage = requests.get("https://www.flipkart.com" + link, headers=headers)
        
        new_soup = BeautifulSoup(new_webpage.content, "lxml")

        # Extract product details
        title = get_title_flipkart(new_soup)
        price = get_price_flipkart(new_soup)
        rating = get_rating_flipkart(new_soup)
        review_count = get_review_count_flipkart(new_soup)
        availability = get_availability_flipkart(new_soup)

        # Append details to the list
        product_details_flipkart.append({
            "title": title,
            "price": price,
            "rating": rating,
            "review_count": review_count,
            "availability": availability
        })

    return product_details_flipkart


@app.route("/", methods=["GET", "POST"])
def index() :
    if request.method == "POST" :
        product_type = request.form["productType"]
        count = int(request.form['count'])
        website_choice = request.form["websiteChoice"]
        
        if website_choice == "Amazon" :
            amazon_data_json = amazonDataScrapper(product_type, count)
            if amazon_data_json is not None :
                return render_template('product.html', product_details=amazon_data_json)
        elif website_choice == "Flipkart" :
            flipkart_data_json = flipkartDataScrapper(product_type, count)
            if flipkart_data_json is not None :
                return render_template('product.html', product_details=flipkart_data_json)
    return render_template("index.html")


if __name__ == "__main__" :
    app.run(debug=True)