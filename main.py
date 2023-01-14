from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

option = Options()
option.headless = False
driver = webdriver.Firefox(options=option)
driver.implicitly_wait(7)
baseurl = "https://www.flipkart.com/"
keyword = "iphone 14 max pro"

driver.get(f"{baseurl}search?q={keyword}")
time.sleep(3)
phone_list=list(driver.find_elements(By.CSS_SELECTOR,"#container div div._36fx1h._6t1WkM._3HqJxg div._1YokD2._2GoDe3 div._1YokD2._3Mn1Gg div._1AtVbE.col-12-12 div._13oc-S div div._2kHMtA a._1fQZEK"))
name_list = driver.find_elements(By.CSS_SELECTOR,"#container div div._36fx1h._6t1WkM._3HqJxg div._1YokD2._2GoDe3 div._1YokD2._3Mn1Gg div._1AtVbE.col-12-12 div._13oc-S div div._2kHMtA a._1fQZEK div.MIXNux div._2QcLo- div div.CXW8mj img._396cs4")

phone_url = list(map(lambda a: a.get_attribute('href'),phone_list))
phone_title = list(map(lambda a: a.get_attribute('alt'),name_list))

def GetRatings(phone_url,phone_title):
    phone_detail = list()

    for i in range(0,len(phone_url)):
        url = phone_url[i]
        title = phone_title[i]
        driver.get(f"{url}")
        time.sleep(3)

        overall_rating = driver.find_element(By.CSS_SELECTOR,"#container div div._2c7YLP.UtUXW0._6t1WkM._3HqJxg div._1YokD2._2GoDe3 div._1YokD2._3Mn1Gg.col-8-12 div._1YokD2._3Mn1Gg div._1AtVbE.col-12-12 div.col.JOpGWq div.row._3AjFsn._2c2kV- div._2e3Uck div.row div.col-4-12 div.col div.row div.col-12-12._1azcI6 div._2d4LTz").text
        #total_noof_rating = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[3]/div[1]/div[2]/div[9]/div[6]/div/div[2]/div[1]/div/div[1]/div/div[2]/div/span").text.replace("Ratings &","")
        star_rating_obj = list(driver.find_elements(By.CSS_SELECTOR,"#container div div._2c7YLP.UtUXW0._6t1WkM._3HqJxg div._1YokD2._2GoDe3 div._1YokD2._3Mn1Gg.col-8-12 div._1YokD2._3Mn1Gg div._1AtVbE.col-12-12 div.col.JOpGWq div.row._3AjFsn._2c2kV- div._2e3Uck div.row div.col-8-12._3qpj74._31DkEZ div._13sFCC.miQW6D ul._36LmXx li._28Xb_u div._1uJVNT"))
        star_rating =  list(map(lambda a: a.text,star_rating_obj))

        five_star_rating = star_rating[0]
        four_star_rating = star_rating[1]
        three_star_rating = star_rating[2]
        two_star_rating = star_rating[3]
        one_star_rating = star_rating[4]

        feature_ratingObj = list(driver.find_elements(By.CSS_SELECTOR,"#container div div._2c7YLP.UtUXW0._6t1WkM._3HqJxg div._1YokD2._2GoDe3 div._1YokD2._3Mn1Gg.col-8-12 div._1YokD2._3Mn1Gg div._1AtVbE.col-12-12 div.col.JOpGWq div.row._3AjFsn._2c2kV- div._2LE14f div.row a.col-3-12.hXkZu-._1pxF-h div._2a78PX div._2aWUii svg.HTdwVj text._2Ix0io"))
        feature_rating =  list(map(lambda a: a.text,feature_ratingObj))

        camera_rating = feature_rating[0]
        batter_rating = feature_rating[1]
        display_rating = feature_rating[2]
        design_rating = feature_rating[3]

        feature_rating = {
            'camera_rating' : camera_rating,
            'batter_rating' : batter_rating,
            'display_rating' : display_rating,
            'design_rating' : design_rating
        }

        rating_obj = {
            'five_star_rating':five_star_rating,
            'four_star_rating':four_star_rating,
            'three_star_rating':three_star_rating,
            'two_star_rating':two_star_rating,
            'one_star_rating':one_star_rating
        }

        dict_obj={
            'id':i+1,
            'Title':title,
            'overall_ratings':overall_rating,
            'total_ratings':(int(five_star_rating) + int(four_star_rating) + int(three_star_rating) + int(two_star_rating) + int(one_star_rating)),
            'ratings':rating_obj,
            'feature_ratings':feature_rating
        }

        phone_detail.append(dict_obj)

    print(phone_detail)

def GetReviews(phone_url,phone_title):
    phone_reviews = list()
    page_count = 0
    review_pages = 1
    
    url = phone_url

    title = phone_title
    driver.get(f"{url}")
    time.sleep(3)
    allreview_obj = driver.find_elements(By.CSS_SELECTOR,"#container div div._2c7YLP.UtUXW0._6t1WkM._3HqJxg div._1YokD2._2GoDe3 div._1YokD2._3Mn1Gg.col-8-12 div._1YokD2._3Mn1Gg div._1AtVbE.col-12-12 div.col.JOpGWq a")
    all_review_url=list(map(lambda a: a.get_attribute('href'),list(allreview_obj)))[0].split('aid=')[0] + "aid=overall"

    
    driver.get(f"{all_review_url}")
    time.sleep(3)

    review_pages = int(driver.find_element(By.CSS_SELECTOR,"#container div div._2tsNFb div._6t1WkM._3HqJxg div._1YokD2._2GoDe3.col-12-12 div._1YokD2._3Mn1Gg.col-9-12 div._1AtVbE.col-12-12 div div._2MImiq._1Qnn1K").text.split(' ')[-1].split('\n')[0])

    for i in range(1,review_pages+1):
        if page_count > 0:
            allreview_url = f"{all_review_url}&page={i}"
            driver.get(f"{allreview_url}")
            time.sleep(3)
            print(allreview_url)

        page_count = page_count+1

        Review_obj = list(driver.find_elements(By.CSS_SELECTOR,"#container div div._2tsNFb div._6t1WkM._3HqJxg div._1YokD2._2GoDe3.col-12-12 div._1YokD2._3Mn1Gg.col-9-12 div._1AtVbE.col-12-12 div._27M-vq div.col div.col._2wzgFH.K0kLPL div.row div._3LWZlK._1BLPMq"))
        
        Review_Star = list()
        for item in Review_obj:
            Review_Star.append(item.text)

        ReviewText_obj = list(driver.find_elements(By.CSS_SELECTOR,"#container div div._2tsNFb div._6t1WkM._3HqJxg div._1YokD2._2GoDe3.col-12-12 div._1YokD2._3Mn1Gg.col-9-12 div._1AtVbE.col-12-12 div._27M-vq div.col div.col._2wzgFH.K0kLPL div.row p._2-N8zT"))
        

        Review_Text = list()
        for item in ReviewText_obj:
            Review_Text.append(item.text)


        Review_like_dislike_obj = list(driver.find_elements(By.CSS_SELECTOR,"#container div div._2tsNFb div._6t1WkM._3HqJxg div._1YokD2._2GoDe3.col-12-12 div._1YokD2._3Mn1Gg.col-9-12 div._1AtVbE.col-12-12 div._27M-vq div.col div.col._2wzgFH.K0kLPL div.row._3n8db9 div._1e9_Zu div.row div._27aTsS div._1LmwT9"))

        review_dec_obj = list(driver.find_elements(By.CSS_SELECTOR,"#container div div._2tsNFb div._6t1WkM._3HqJxg div._1YokD2._2GoDe3.col-12-12 div._1YokD2._3Mn1Gg.col-9-12 div._1AtVbE.col-12-12 div._27M-vq div.col div.col._2wzgFH.K0kLPL div.row div.t-ZTKy"))
        
        Review_Desc = list()
        for item in review_dec_obj:
            Review_Desc.append(item.text)

        
        
        
        for i in range(0,len(Review_Star)):
            review={
                'star':Review_Star[i],
                'review_text':Review_Text[i],
                'review_description':Review_Desc[i],
                'likes':Review_like_dislike_obj[i].text,
                'dislikes':Review_like_dislike_obj[i+1].text
            }

            phone_reviews.append(review)
        #['Page', '1', 'of', '5\n1\n2\n3\n4\n5\nNEXT']
        #print(allreview_url)

    return phone_reviews
    
    '''
    overall_url = driver.find_element(By.CSS_SELECTOR,"#container div div._2tsNFb div._6t1WkM._3HqJxg div._1YokD2._2GoDe3.col-12-12 div._1YokD2._3Mn1Gg.col-9-12 div._1YokD2._3Mn1Gg.col-12-12 div._1AtVbE.col-12-12 div._33iqLu div a._203_Tp").get_attribute("href")
   
    print(overall_url)

    driver.get(f"{overall_url}")
    time.sleep(3)
    '''
    

if __name__ == "__main__":
    #GetReviews(phone_url[0],phone_title[0])
    print(GetReviews(phone_url[0],phone_title[0]))