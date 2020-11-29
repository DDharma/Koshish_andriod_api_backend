from modules.connection import sql_connection

mydb = sql_connection()

def new_member():
    mycursor = mydb.cursor()
    add_member_query = "INSERT INTO koshish_member_details (NAME, YEAR_OF_JOINING, EMAIL, PHONE, LOCATION, IS_ADMIN, RESPONSIBILITY, SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"

    add_member_data = (NAME, YEAR_OF_JOINING, EMAIL, PHONE, LOCATION, IS_ADMIN, RESPONSIBILITY, SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY)

    mycursor.execute(add_member_query, add_member_data)
    mydb.commit()
    mycursor.close()

    mycursor = mydb.cursor()
    add_member_for_attendace = "ALTER TABLE koshish_member_attendance ADD "+NAME+" int(1)"
    mycursor.execute(add_member_for_attendace)

    mydb.commit()
    mycursor.close()

    mydb.close()