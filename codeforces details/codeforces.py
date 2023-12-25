from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

url = "https://codeforces.com"

driver = webdriver.Chrome()

def reverseStr(str):
  str = list(str)
  for i in range(len(str)//2):
    str[i], str[len(str)-i-1] = str[len(str)-i-1], str[i]
  return ''.join(str)

def separateProblemIdAndContestId(id):
  contestId = ""
  problemId = ""
  
  isOrNot = False
  for j in range(len(id)):
    j = len(id)-j-1
    if not isOrNot:
      problemId += id[j]
    else: 
      contestId += id[j]
      
    if id[j].isalpha():
      isOrNot = True
  return contestId, problemId

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
  if i!= 1: break
  driver.get(url + f'/problemset/page/{i}')
  element = driver.find_elements(By.CSS_SELECTOR, 'table.problems tbody tr')
  problemList.extend(getProblems(element))
  try:
    inactiveArrow = driver.find_element(By.CSS_SELECTOR, 'span.inactive')
    if inactiveArrow and inactiveArrow.text == '→':
      break
  except: pass
  i += 1
  

for i, item in enumerate(problemList):
  id = ''.join(item['id'].split(' '))
  
  problemId, contestId = separateProblemIdAndContestId(id)
  
  problemId = reverseStr(problemId)
  contestId = reverseStr(contestId)

  problemUrl = f'{url}/problemset/problem/{contestId}/{problemId}'

  print(problemUrl)
  driver.get(problemUrl) 
  
  # try:
  #   # problemList[i]['time'] = problemDetails.find_element(By.CSS_SELECTOR, '.time-limit').text
  #   print(problemDetails.find_element(By.CSS_SELECTOR, '.time-limit').text)
  #   print(driver.find_element(By.CSS_SELECTOR, '.time-limit').text)
  # except:
  #   pass

  
# problemListFrame = pd.DataFrame(problemList)
# problemListFrame.to_csv('./codeforcesDetails.csv', index=False)

driver.quit()