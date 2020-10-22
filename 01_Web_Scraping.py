# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import re
from tqdm import tqdm
import time
#import IPython
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

# %%
chrome_options = webdriver.ChromeOptions()
#Disable loading of images
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

# %%
urls = [
"https://www.instagram.com/matiamubysofia/",
"https://www.instagram.com/starkstromhippie/",
"https://www.instagram.com/juleslw/",
"https://www.instagram.com/juliahlm/",
"https://www.instagram.com/melaniekroll/",
"https://www.instagram.com/theocarow/",
"https://www.instagram.com/riccardosimonetti/",
"https://www.instagram.com/california.89/",
"https://www.instagram.com/andrehellmundt/",
"https://www.instagram.com/jonnyfoe/",
"https://www.instagram.com/philipp_stehler/",
"https://www.instagram.com/tobiaswolf/",
"https://www.instagram.com/justusf_hansen/",
"https://www.instagram.com/marcelfloruss/",
"https://www.instagram.com/sandro/",
"https://www.instagram.com/kosta_williams/",
"https://www.instagram.com/isek___/",
"https://www.instagram.com/ibdansch",
"https://www.instagram.com/andi.woehle",
"https://www.instagram.com/klaus_grillt",
"https://www.instagram.com/nickjann/",
"https://www.instagram.com/lukaszgler/",
"https://www.instagram.com/wowa_valentino/",
"https://www.instagram.com/lanmandragoran9/",
"https://www.instagram.com/maxisanchezz",
"https://www.instagram.com/ayla.eulalia/",
"https://www.instagram.com/laratolksdorf/",
"https://www.instagram.com/dianazurloewen/",
"https://www.instagram.com/dariadaria/",
"https://www.instagram.com/jesswayoflife/",
"https://www.instagram.com/emilylouise.i/",
"https://www.instagram.com/lea/",
"https://www.instagram.com/leonieyoung/",
"https://www.instagram.com/jileileen/",
"https://www.instagram.com/lizkaeber/",
"https://www.instagram.com/hannah.hofinger/",
"https://www.instagram.com/lolaweippert/",
"https://www.instagram.com/frankly.alina/",
"https://www.instagram.com/putsch.i/"
"https://www.instagram.com/lisaandlena",
"https://www.instagram.com/bibisbeautypalace",
"https://www.instagram.com/dagibee",
"https://www.instagram.com/pamela_rf",
"https://www.instagram.com/julienco_",
"https://www.instagram.com/julienbam",
"https://www.instagram.com/paola",
"https://www.instagram.com/stefaniegiesinger",
"https://www.instagram.com/melinasophie",
"https://www.instagram.com/lenameyerlandrut",
"https://www.instagram.com/marcusbutler",
"https://www.instagram.com/laserluca",
"https://www.instagram.com/juliabeautx",
"https://www.instagram.com/lenagercke",
"https://www.instagram.com/felixladen",
"https://www.instagram.com/sarah.harrison.official",
"https://www.instagram.com/carodaur",
"https://www.instagram.com/xlaeta",
"https://www.instagram.com/simondesue",
"https://www.instagram.com/magic_fox",
"https://www.instagram.com/lionttv",
"https://www.instagram.com/mrjade",
"https://www.instagram.com/mrsbella",
"https://www.instagram.com/rewinstagram",
"https://www.instagram.com/danielakatzenberger",
"https://www.instagram.com/inscopenico",
"https://www.instagram.com/andreschiebler",
"https://www.instagram.com/lorena",
"https://www.instagram.com/ivana.santacruz",
"https://www.instagram.com/dimakoslowski",
"https://www.instagram.com/annamariadamm",
"https://www.instagram.com/heikolochmann",
"https://www.instagram.com/romanlochmann",
"https://www.instagram.com/caroeinhoff/",
"https://www.instagram.com/marenwolf",
"https://www.instagram.com/xeniaadonts",
"https://www.instagram.com/sarellax3",
"https://www.instagram.com/samislimani",
"https://www.instagram.com/joyceilg",
"https://www.instagram.com/ischtarisik",
"https://www.instagram.com/ksfreak",
"https://www.instagram.com/leoobalys",
"https://www.instagram.com/iblali"
]

# %%
#Show next url and open website. First image needs to be selected manually.
#This needs to be executed for each url
driver.get(urls[0])
url = urls[0] 
print(url)

# %%
#This needs to be executed for each url
#Remove the url from the list 
del urls[0]

df = pd.DataFrame(columns=["user","timestamp","description","likes1","likes2","video_views"])

#Placeholders. Later: Check whether this list is full of duplicates
duplicate_detection = ["First","Second","Third","Fourth","Fifth"]

#At most 2000 posts per profile
for x in tqdm(range(2000)):
    
    html_source = driver.page_source
       
    current_timestamp = ""
    
    try:
        description = re.search('(<\/div><\/h2><span class="")([\s\S]*)(<\/span>)',html_source).group(2).split('</span>')[0] 
    except:
        description = "Error"
    try:
        timestamp = re.search('( datetime=\")([\s\S]*)( title=)',re.search('(<\/div><\/h2><span class="")([\s\S]*)(<\/span>)',html_source).group(2)).group(2).split('\" title=')[0]
    except:
        timestamp = "Error"
    try:
        likes1 = re.search('(type="button"><span>)([\d\.]+)',html_source).group(2)
    except:
        likes1 = "Error"
    try:
        likes2 = re.search('([\d\.]+)(</span> Mal</button>)',html_source).group(1)
    except:
        likes2 = "Error"
    try:
        video_views = re.search('(span>)([\d\.]+)(</span> Aufrufe</span>)',html_source).group(2)        
    except:
        video_views = "Error"
        
    #"|"" should be used as delimiter for the csv. If users use it in there captions, it is replaced with "I"
    description = description.replace("|","I")    

    df = df.append({
        "user": url,
        "description": description,
        "timestamp":  timestamp,
        "likes1": likes1,
        "likes2": likes2,
        "video_views": video_views
          }, ignore_index=True)

    duplicate_detection.append(timestamp)
    current_timestamp = timestamp
     
    #Break if duplicate_detection elements are all equal    
    if duplicate_detection.count(duplicate_detection[0]) == len(duplicate_detection):
        break
        
    #Remove first element of duplicate detection
    del duplicate_detection[0]
    
    #Stop webscraping when post was published before 01 March 2019
    if '2019-03-01T00:00:00.000Z' > current_timestamp:   
        break
    
    #Simulate button press to switch to the next post
    driver.find_element_by_tag_name('body').send_keys(Keys.RIGHT)
    time.sleep(3)
    
    #If last post resulted in an error, additonal time is provided. Note that error is not scraped again.
    if timestamp == "Error":
        driver.find_element_by_tag_name('body').send_keys(Keys.LEFT)
        time.sleep(7)
        driver.find_element_by_tag_name('body').send_keys(Keys.RIGHT)
        time.sleep(3)
        
 
df.to_csv('scraping-output/results.csv', mode='a', sep="|", header=False)

#Audio notification
#IPython.display.Audio("finished.wav", autoplay=True)

# %%
#Control amount of error in timestamps
df.timestamp.value_counts().head(5)

# %%
df
