from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv
import pandas as pd

url = "https://codeforces.com/problemset"

driver = webdriver.Chrome()

def getProblems(element):
  problemList = []
  for i, item  in enumerate(element):
    if not i: continue
    data = {}
    keywords = []
    
    try:
      data['id'] = item.find_element(By.CSS_SELECTOR, '.id.left').text
      if data['id'].find('E'):
        data['id'] = 'E '.join(data['id'].split('E'))
    except: 
      pass
    
    try:
      data['title'] = item.find_element(By.CSS_SELECTOR, 'div[style="float: left;"]').text
    except: pass
    
    try:
      keywordsElement = item.find_elements(By.CSS_SELECTOR, 'a.notice')
      for key in keywordsElement:
        keywords.append(key.text)
      data['keywords'] = ', '.join(keywords)
    except:
      data['keywords'] = None
    
    try:
      data['rating'] = item.find_element(By.CSS_SELECTOR, '.ProblemRating').text
    except: 
      data['rating'] = None
    
    try:
      data['solved'] = int(item.find_element(By.CSS_SELECTOR, '.right').text.split('x')[1])
    except:
      data['solved'] = 0
    
    problemList.append(data)
    if not data['title']: continue
  
  return problemList


i = 1;
problemList = [];
while True:
  driver.get(url + f'/page/{i}')
  element = driver.find_elements(By.CSS_SELECTOR, 'table.problems tbody tr')
  problemList.extend(getProblems(element))
  try:
    inactiveArrow = driver.find_element(By.CSS_SELECTOR, 'span.inactive')
    if inactiveArrow and inactiveArrow.text == '→':
      break
  except: pass
  i += 1
  
  
problemListFrame = pd.DataFrame(problemList)
problemListFrame.to_csv('./codeforces.csv', index=False)

driver.quit()