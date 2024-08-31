import csv
def add_student_information(student_info):
    with open('StudentInformation.csv','a',newline='')as f:
        writer=csv.writer(f)
        writer.writerow(student_info)
for student_number in range(1,66):
    print(f"Enter information for Student {student_number}:")

    student_name=input("Enter student name:")
    student_id=input("Enter student ID:")
    student_email=input("Enter student Email:")

    student_info=[student_name,student_id,student_email]
    add_student_information(student_info)
    print("Student information for 65 students has been saved to StudentInformation.csv.")