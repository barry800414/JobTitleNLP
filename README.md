
#### This project is to relieve the job title matching problem using 104 data and NLP techniques

* [104 Company](www.104.com.tw) 
* [104 Job Category](http://www.104.com.tw/i/api_doc/jobsearch/documentation.cfm#fld_cat)
* [104 API](http://www.104.com.tw/i/api_doc/jobsearch/)
* Please notice that, all the rights of data belong to 104 Company. Please follow the liscence of 104 Company. 


## Procedure

#### Get 104 job Category from 104 website 
	`python3 ./104API/getCat.py categoryFile`
#### Get Job-category to job-title data from 104 API 
	`python3 ./104API/104API.py categoryFile outJsonFile`
#### Preprocess job titles (removing punctuation, normalize space) 
	`python3 ./preprocess/rmPunctuation.py inJsonFile PunctuationFile outJsonFile`
#### Jieba word segmentation 
	`cd ./preprocess/jieba/; python3 jieba_segment.py inJsonFile outJsonFile; cd ../..`
#### Minimize data 
	`python3 ./preprocess/minimizeData.py inJobJsonFile outJobJsonFile`
#### Calculate TF-IDF 
	`python3 tfidf.py Cat2TitleJsonFile outTFIDFJsonFile`
#### Filtering some impossible terms 
	`python3 filterTFIDF.py < inJson > outJson`
#### Get final term candidate 
	`python3 getCandidate.py webSiteData apiData outJson outTxt [[[topPercent] min] max]`