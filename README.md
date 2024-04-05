# cron-parser


Here's a sample code output:
```
(venv) zriyansh@Priyanshs-MacBook-Air misc % python cron.py          
Every 30 seconds
Input: 0/30 * * * * ? 
Output:
schedule_year=0
schedule_month_of_year=0
schedule_day_of_month=0
schedule_day_of_week=Every Day
schedule_hour_of_day=0
schedule_min_of_hour=0
schedule_sec_of_min=Every 30 seconds
```

Given a cron job input, lets say `0/30 * * * * ?`, the parser will try to separate the components of time in a separate variable. 

Here's a list of cron's you can test out the code with:

```
  "0 1 * * *",
  "0 10 1 * * *",
  "0 59 23 * * MON-FRI",
  "0 12 * * MON-FRI",
  "30 8 * * *",
  "0 18 * * SUN",
  "0 0/30 6-19 ? * MON-SUN",
  "0 0 0/6 1/1 * ? *",
  "0 0 2 15 * ?",
  "0 0 2 ? * 2",
  "0 0 2 15 * ?",
  "0 0 2 ? * 2",
  "0 0 2 ? * 2-6",
  "0 0/15 * 1/1 * ? *",
  "0 0/30 6-19 ? * MON-SUN",
  "0/30 * * * * ?",
  "1 45 16 ? * Wed",
  "22 1 * * *",
  "22 1 * * * ?",
  "0 11 11 11 11 ?",
  "0 0 10,18/12 * *",
  "29 53 15 ? * Mon",
  "0 0 2/2 2/2 * ?",
  "1 * 1/2 * *",
  "1 1 * * 1",
  "0 0 * * 1,3",
  "41 31 3 1 1-2 ?", # error
  "0 0/30 6-19 ? * MON-SUN",
  "0 0 2 15 * ?",
  "22 * * * * ?",
  "0 0 23 * * ?",
  "0 15 13 ? * *",
  "0 15 10 * * ?",
  "0 15 10 * * ? *",
  "0 * 14 * * ?",
  "0 0/5 14 * * ?",    
  "0 0-5 14 * * ?" ,  
  "0 10,44 14 ? 3 WED" 
  "0 15 10 * * ? 2005"
  "0 15 10 ? * 6L 2002-2005"
  "22 * * * * ?"
```
