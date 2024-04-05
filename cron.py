import re
import logging
from cron_descriptor import get_description


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# def get_description(quartz_cron_expression):
#     # Simulated implementation to return dummy schedule descriptions
#     descriptions = {
#         "0 0 * * *": "Every day at midnight",
#         "0 0/30 6-19 ? * MON-SUN": "Every 30 minutes, between 06:00 AM and 07:59 PM, Monday through Sunday",
#         "0 12 * * MON-FRI": "Every Monday to Friday at noon",
#         "30 8 * * *": "Every day at 8:30 AM",
#         "0 18 * * SUN": "Every Sunday at 6:00 PM",
#         "": None,  # Empty cron expression
#     }
#     return descriptions.get(quartz_cron_expression)

class CronParser:

    def _parse_cron(self, quartz_cron_expression):
        
        if not quartz_cron_expression:
            return None, None, None
        DAYS_OF_WEEK = (
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        )
        schedule_desc = get_description(quartz_cron_expression) or None
        print(schedule_desc)

        schedule_year = 0
        schedule_month_of_year = 0  
        schedule_day_of_month = 0
        schedule_day_of_week = "NA"
        schedule_hour_of_day = 0
        schedule_min_of_hour = 0
        schedule_sec_of_min = 0
        
        if schedule_desc is not None:
            sch_list = schedule_desc.split(" ")
            time = ""
            am_pm = ""
            index = 0
            for index in range(0, len(sch_list)):
                if sch_list[index] == "At" and sch_list[index + 2] in ["AM", "PM", "AM,", "PM,"]:
                    time = sch_list[index + 1] 
                    am_pm = sch_list[index + 2]
                    time_list = time.split(":")
                    schedule_hour_of_day = int(time_list[0])
                    schedule_min_of_hour = int(time_list[1])
                    try: 
                        schedule_sec_of_min = int(time_list[2])
                    except:
                        pass
                    if am_pm in ["PM," ,"PM"] and schedule_hour_of_day < 12:
                        schedule_hour_of_day = schedule_hour_of_day + 12
                        
                if sch_list[index] in ["At", "at"] and sch_list[index + 2] in ["minutes", "minute"]:
                    schedule_min_of_hour = sch_list[index + 1]
                    
                elif sch_list[index] == "between":
                    start_hour_number = -1
                    end_hour_number = -1
                    start_hour = sch_list[index + 1]
                    start_hour_system = sch_list[index + 2]
                    end_hour = sch_list[index + 4]
                    end_hour_system = sch_list[index + 5]
                    split_start = start_hour.split(":")
                    if(start_hour_system) in ["PM", "PM,"] and int(split_start[0]) < 12:
                        start_hour_number = int(split_start[0]) + 12
                        start_hour_min = int(split_start[1])
                    else: 
                        start_hour_number = int(split_start[0])
                        start_hour_min = int(split_start[1])
                    
                    split_end = end_hour.split(":")
                    
                    if(end_hour_system) in ["PM,", "PM"] and int(split_end[0]) < 12:
                        end_hour_number = int(split_end[0]) + 12
                        end_hour_min = int(split_start[1])
                        if start_hour_number == end_hour_number:
                            schedule_hour_of_day= f"{start_hour_number}"
                        else: 
                            schedule_hour_of_day= f"{start_hour_number}-{end_hour_number}"
                        if(schedule_min_of_hour==0):
                            schedule_min_of_hour = "Every Minute"
                    
                elif sch_list[index] in ["every", "Every"] and sch_list[index + 2] in ["seconds", "seconds,"]:
                    schedule_sec_of_min = f"{sch_list[index]} {sch_list[index + 1]} {sch_list[index + 2]}"

                elif sch_list[index] in ["At"] and sch_list[index + 2] in ["seconds", "seconds,"]:
                    schedule_sec_of_min = sch_list[index + 1]

                elif sch_list[index] in ["every", "Every"] and sch_list[index + 2] in ["minutes", "minutes,"]:
                    schedule_min_of_hour = f"{sch_list[index]} {sch_list[index + 1]} {sch_list[index + 2]}"
                    
                elif sch_list[index] in ["every", "Every"] and sch_list[index + 2] in ["hours", "hours,"]:
                    schedule_hour_of_day = f"{sch_list[index]} {sch_list[index + 1]} {sch_list[index + 2]}"
                
                elif sch_list[index] in ["past"] and sch_list[index + 2] in ["hour,"]:
                    schedule_hour_of_day = "Every Hour"
                    
                elif sch_list[index] == "only" and sch_list[index + 1] == "on":
                    try: 
                        if sch_list[index + 3] == "and":
                            schedule_day_of_week = f"{sch_list[index + 2]} and {sch_list[index + 4]}"
                    except:
                        schedule_day_of_week = sch_list[index + 2]
                
                elif sch_list[index] == "through":
                    if sch_list[index - 1].isdigit() and sch_list[index + 1].isdigit():
                        print("digit wala")
                        schedule_year = f"{sch_list[index - 1]} through {sch_list[index + 1]}"
                    elif not re.search(r"(day$|days)", sch_list[index - 1]):
                        print("day wala")
                        schedule_month_of_year = f"{sch_list[index - 1]} through {sch_list[index + 1]}"
                    else:
                        print("month wala")
                        schedule_day_of_week = f"{sch_list[index - 1]} through {sch_list[index + 1]}"

                elif sch_list[index] == "only" and sch_list[index + 1] == "in":
                    if sch_list[index + 2].isdigit():
                        schedule_year = sch_list[index + 2]
                    else: 
                        schedule_month_of_year = sch_list[index + 2]

                elif sch_list[index] in ["month", "month,"]:
                    schedule_day_of_month = sch_list[index - 3]
                    schedule_day_of_week = "NA"
                
                elif sch_list[index] in ["every", "Every"] and sch_list[index + 2] in ["day", "days", "days,"]:
                    schedule_day_of_month = f"{sch_list[index]} {sch_list[index + 1]} {sch_list[index + 2]}"
                    schedule_day_of_week = "NA"

                elif schedule_day_of_week in ["NA"]: 
                    if schedule_day_of_month == 0 and not re.search(r"\b\w*day,\b", sch_list[index]):
                        schedule_day_of_week = "Every Day"
                        flag = 1
                    elif flag != 1:
                        schedule_day_of_week = "NA"
                
            return schedule_year, schedule_month_of_year, schedule_day_of_month, schedule_day_of_week, schedule_hour_of_day, schedule_min_of_hour, schedule_sec_of_min
            return schedule_day_of_week, schedule_hour_of_day, schedule_min_of_hour
        else:
            return None, None, None

# Testing the code
if __name__ == "__main__":
    parser = CronParser()
    inputs = [
        # "0 1 * * *",
        # "0 10 1 * * *",
        # "0 59 23 * * MON-FRI",
        # "0 12 * * MON-FRI",
        # "30 8 * * *",
        # "0 18 * * SUN",
        # "0 0/30 6-19 ? * MON-SUN",
        #  "0 0 0/6 1/1 * ? *",
        # "0 0 2 15 * ?",
        # "0 0 2 ? * 2",
        # "0 0 2 15 * ?",
        # "0 0 2 ? * 2",
        # "0 0 2 ? * 2-6",
        # "0 0/15 * 1/1 * ? *",
        # "0 0/30 6-19 ? * MON-SUN",
        # "0/30 * * * * ?",
        # "1 45 16 ? * Wed",
        # "22 1 * * *",
        # "22 1 * * * ?",
        # "0 11 11 11 11 ?",
        # "0 0 10,18/12 * *",
        # "29 53 15 ? * Mon",
        # "0 0 2/2 2/2 * ?",
        # "1 * 1/2 * *",
        # "1 1 * * 1",
        # "0 0 * * 1,3",
        # "41 31 3 1 1-2 ?", # error
        # "0 0/30 6-19 ? * MON-SUN",
        # "0 0 2 15 * ?",
        # "22 * * * * ?",
        # "0 0 23 * * ?",
        # "0 15 13 ? * *",
        # "0 15 10 * * ?",
        # "0 15 10 * * ? *",
        # "0 * 14 * * ?",
        # "0 0/5 14 * * ?",    
        # "0 0-5 14 * * ?" ,  
        # "0 10,44 14 ? 3 WED" 
        # "0 15 10 * * ? 2005"
        # "0 15 10 ? * 6L 2002-2005"
        # "22 * * * * ?"
        "0/30 * * * * ?"
    ]
    for input_expr in inputs:
        year, month_year, day_month, day_week, hour, minute, sec = parser._parse_cron(input_expr)
        print(f"Input: {input_expr} \nOutput:\nschedule_year={year}\nschedule_month_of_year={month_year}\nschedule_day_of_month={day_month}\nschedule_day_of_week={day_week}\nschedule_hour_of_day={hour}\nschedule_min_of_hour={minute}\nschedule_sec_of_min={sec}\n")

