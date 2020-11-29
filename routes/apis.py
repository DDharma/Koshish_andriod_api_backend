from routes import app,request,cross_origin
from modules.connection import sql_connection


@app.route("/")
def hello():
    return "hello koshish"

@app.route("/get_member_name",methods=["GET"])
@cross_origin()
def get_member_name():
    """[Retrive th NAME from table ]

    Returns:
        [JSON]: [Array of all the name]
    """
    #Caling function to connecting database
    mydb = sql_connection()
    try:
        if request.method == "GET":
            mycursor = mydb.cursor()
            get_member_query = "SHOW COLUMNS FROM koshish_member_attendance"
            mycursor.execute(get_member_query)
            member_list = []
            for i in mycursor: 
                member_list.append(i[0])

            member_data_json = {
                "member_data_json":member_list[1:]
            }
            mydb.commit()
            mycursor.close()
            mydb.close()
    except Exception as e:
        return e

    return member_data_json
    
@app.route("/add_new_member",methods=["POST"])
@cross_origin()
def add_new_member():


    #Caling function to connecting database
    mydb = sql_connection()

    try:
        if request.method == "POST":
            print(1)
            add_member_json_data = request.get_json()

            NAME            = add_member_json_data["NAME"].replace(" ","_")
            YEAR_OF_JOINING = add_member_json_data["YEAR_OF_JOINING"]
            EMAIL           = add_member_json_data["EMAIL"]
            PHONE           = add_member_json_data["PHONE"]
            LOCATION        = add_member_json_data["LOCATION"]
            IS_ADMIN        = add_member_json_data["IS_ADMIN"]
            RESPONSIBILITY  = add_member_json_data["RESPONSIBILITY"]
            SUNDAY          = add_member_json_data["SUNDAY"]
            MONDAY          = add_member_json_data["MONDAY"]
            TUESDAY         = add_member_json_data["TUESDAY"]
            WEDNESDAY       = add_member_json_data["WEDNESDAY"]
            THURSDAY        = add_member_json_data["THURSDAY"]
            FRIDAY          = add_member_json_data["FRIDAY"]
            SATURDAY        = add_member_json_data["SATURDAY"]

            print(YEAR_OF_JOINING,type(YEAR_OF_JOINING))
            print(SUNDAY,type(SUNDAY))
            print(NAME,type(NAME))
            
            #print(NAME, YEAR_OF_JOINING, EMAIL, PHONE, LOCATION, IS_ADMIN, RESPONSIBILITY, SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY)

            mycursor = mydb.cursor()
            add_member_query = "INSERT INTO koshish_member_details (NAME, YEAR_OF_JOINING, EMAIL, PHONE, LOCATION, IS_ADMIN, RESPONSIBILITY, SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"

            print(1)
            add_member_data = (NAME, YEAR_OF_JOINING, EMAIL, PHONE, LOCATION, IS_ADMIN, RESPONSIBILITY, SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY)

            print(2)
            mycursor.execute(add_member_query, add_member_data)
            print(3)
            mydb.commit()
            mycursor.close()

            print(4)
            mycursor = mydb.cursor()
            add_member_for_attendace = "ALTER TABLE koshish_member_attendance ADD "+NAME+" int(1)"
            mycursor.execute(add_member_for_attendace)

            print(5)
            mydb.close()
            print("value_added")
            return "Value added"

    except Exception as e:
        return str(e)

@app.route("/set_time_table",methods=["POST"])
@cross_origin()
def set_time_table():
    #Caling function to connecting database
    mydb = sql_connection()
    #print("-----------------------------------")

    try:
        if request.method == "POST":
            set_time_table_json_data = request.get_json()
            NAME            = set_time_table_json_data["NAME"]
            SUNDAY          = set_time_table_json_data["SUNDAY"]
            MONDAY          = set_time_table_json_data["MONDAY"]
            TUESDAY         = set_time_table_json_data["TUESDAY"]
            WEDNESDAY       = set_time_table_json_data["WEDNESDAY"]
            THURSDAY        = set_time_table_json_data["THURSDAY"]
            FRIDAY          = set_time_table_json_data["FRIDAY"]
            SATURDAY        = set_time_table_json_data["SATURDAY"]

            print(NAME, SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY)


            mycursor = mydb.cursor()
            set_time_table_query = "UPDATE koshish_member_details SET SUNDAY = %s, MONDAY = %s,TUESDAY = %s,WEDNESDAY = %s,THURSDAY = %s,FRIDAY = %s,SATURDAY = %s WHERE NAME = %s"

            set_time_table_data = (SUNDAY,MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY,NAME) 

            mycursor.execute(set_time_table_query, set_time_table_data)

            mydb.commit()
            mycursor.close()
            mydb.close()

            return "TIME TABLE UPDATED SUCCESSFULLY "

    except Exception as e:
        return str(e)
   
@app.route("/check_date",methods=["POST"])
@cross_origin()
def check_date():
    #Caling function to connecting database
    mydb = sql_connection()
    #print("-----------------------------------")

    try:
        if request.method == "POST":
            date_json_data  = request.get_json()
            ATTENDANCE_DATE = date_json_data["ATTENDANCE_DATE"]
        
            print(ATTENDANCE_DATE,type(ATTENDANCE_DATE  ))

            mycursor = mydb.cursor()
            check_date_query = "SELECT COUNT(Attendance_Date)FROM koshish_member_attendance WHERE Attendance_Date = %s"

            check_date_data = (ATTENDANCE_DATE,) 
            mycursor.execute(check_date_query,check_date_data)
            
            date_check = {}
            for i in mycursor: 
                date_check["return"] = i[0]

            if date_check["return"] == 0:
                
                add_date_query = "INSERT INTO koshish_member_attendance (Attendance_Date) VALUES (%s)"

                add_date_data = (ATTENDANCE_DATE,)
                
                mycursor.execute(add_date_query,add_date_data)
                
                mydb.commit()
                mycursor.close()
                mydb.close()
                return "True"
            else:
                mycursor.close()
                mydb.close()
                return "False"

    except Exception as e:
        return str(e)

@app.route("/mark_attendance",methods=["POST"])
@cross_origin()
def mark_attendance():
    #Caling function to connecting database
    mydb = sql_connection()

    try:
        if request.method == "POST":
            mark_attendance_json_data = request.get_json()

            NAME  = mark_attendance_json_data["NAME"]
            DATE  =  mark_attendance_json_data["DATE"]
            VALUE = mark_attendance_json_data["VALUE"]
            
            print(NAME,DATE,VALUE)

            #Checking the date for marking the attendance
            mycursor = mydb.cursor()
            check_date_query = "SELECT COUNT(Attendance_Date)FROM koshish_member_attendance WHERE Attendance_Date = %s"

            check_date_data = (DATE,) 
            mycursor.execute(check_date_query,check_date_data)
            date_check = {}
            for i in mycursor: 
                date_check["return"] = i[0]
            mycursor.close()

            #if the date is exist then direct update the attendance or if not exist then first add the date then update
            
            if date_check["return"] == 0:
                mycursor = mydb.cursor()
                add_date_query = "INSERT INTO koshish_member_attendance (Attendance_Date) VALUES (%s)"

                add_date_data = (DATE,)
                mycursor.execute(add_date_query,add_date_data)
                mydb.commit()
                mycursor.close()

                mycursor = mydb.cursor()
                mark_attendance_query = "UPDATE koshish_member_attendance SET "+NAME+" = %s WHERE Attendance_Date = %s"
                
                mark_attendace_data = (VALUE,DATE)
                mycursor.execute(mark_attendance_query, mark_attendace_data)
                mydb.commit()


            else:
                mycursor = mydb.cursor()
                mark_attendance_query = "UPDATE koshish_member_attendance SET "+NAME+" = %s WHERE Attendance_Date = %s"
                mark_attendace_data = (VALUE,DATE)
                mycursor.execute(mark_attendance_query, mark_attendace_data)
                mydb.commit()
            

            
            print(mycursor.rowcount, "record(s) affected")
            mycursor.close()
            mydb.close()
            MARKS = ""
            if VALUE == 0:
                MARKS = "ABSENT "
            elif VALUE == 1:
                MARKS = "PRESENT"
            else:
                MARKS = "INFORMED ABSENT"

            return "{} is {} on {}".format(NAME,MARKS,DATE)

    except Exception as e:
        return str(e)

@app.route("/show_attendance",methods=["POST"])
@cross_origin()
def show_attendance():

    #Caling function to connecting database
    mydb = sql_connection()

    try:
        if request.method == "POST":
            show_attendance_json_data = request.get_json()
            
            NAME = show_attendance_json_data["NAME"]
            END_DATE = show_attendance_json_data["END_DATE"]
            START_DATE = show_attendance_json_data["START_DATE"]

            show_attendance_query           = "SELECT COUNT("+NAME+") FROM koshish_member_attendance WHERE Attendance_Date BETWEEN %s AND %s AND " +NAME+ "= %s"
            absent_attendance_data          = (START_DATE,END_DATE,0)
            present_attendance_data         = (START_DATE,END_DATE,1)
            informed_absend_attendance_data = (START_DATE,END_DATE,2)
            extra_present_attendance_data   = (START_DATE,END_DATE,3)

            mycursor = mydb.cursor()
            mycursor.execute(show_attendance_query,absent_attendance_data)
            for i in mycursor:
                ABSENT = i[0]

            mycursor.execute(show_attendance_query,present_attendance_data)
            for i in mycursor:
                PRESENT = i[0]
            
            mycursor.execute(show_attendance_query,informed_absend_attendance_data)
            for i in mycursor:
                INFORMED_ABSENT = i[0]
            
            mycursor.execute(show_attendance_query,extra_present_attendance_data)
            for i in mycursor:
                EXTRA_PRESENT = i[0]




            attendane_details = {
                                    "NAME"            :NAME,
                                    "START_DATE"      :START_DATE,
                                    "END_DATE"        :END_DATE,
                                    "PRESENT"         :PRESENT,
                                    "ABSENT"          :ABSENT,
                                    "INFORMED_ABSENT" :INFORMED_ABSENT,
                                    "EXTRA_PRESENT"   :EXTRA_PRESENT,
                                    "TOTAL_NO_OF_TURN":PRESENT+ABSENT+INFORMED_ABSENT,
             
                                }
            return attendane_details

    except Exception as e:
        return str(e)
            