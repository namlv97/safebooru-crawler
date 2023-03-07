from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import os
import re
import argparse

chrome_options = Options()
# chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option('detach',True)
chrome_options.add_experimental_option("prefs",{
    "download.default_directory":"C:\Documents",
    # "download.prompt_for_download":False,
    # "download.directory_upgrade":True,
})

parser = argparse.ArgumentParser()
parser.add_argument("--tags",type=str)

chrome_options.add_argument("--profile.default_content_settings.popups")
chrome_options.add_argument("--profile.content_settings.exceptions.automatic_downloads.*.setting")


driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver.exe",)


def main(args):
    _tags=args.tags
    url = f"https://safebooru.org/index.php?page=post&s=list&tags={_tags}"
    driver.get(url)
    time.sleep(1)
    while True:
        try:
            posts=driver.find_elements(By.CSS_SELECTOR,"span.thumb")
            for post in posts:
                _id=post.get_attribute('id')
                img=post.find_element(By.CSS_SELECTOR,'img')
                image_url=img.get_attribute('src')
                href=post.find_element(By.CSS_SELECTOR,"a")
                driver.execute_script(f"window.open('{href.get_attribute('href')}');")
                
                driver.switch_to.window(driver.window_handles[1])
                tags_sidebar=driver.find_element(By.ID,'tag-sidebar')
                
                tags=tags_sidebar.find_elements(By.XPATH,"//li[@class='tag-type-general tag']/a")
                tags=",".join([tag.text for tag in tags])
                with open(os.path.join('dataset',f'{_tags}.tsv'),'a') as f:
                    content=f'{_id}\t{tags}\t{image_url}\n'
                    
                    f.write(content)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            next_page=driver.find_element(By.XPATH,"//div/div/a[@alt='next']")
            next_page.click()
            time.sleep(1)
        except:
            driver.get(driver.current_url)
            time.sleep(1)


if __name__=="__main__":
    args = parser.parse_args()
    print(args)
    main(args)
            