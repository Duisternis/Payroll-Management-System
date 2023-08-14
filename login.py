def pdf_maker(month):
    cur.execute(f"select * from personal_details where ID='{userID_salary.get()}'")
    info = list(list(cur)[0])

    html = f"""
    <h1><center>Pay Slip - {company_name}</center></h1>
    <h3><center>{month} - 2021</center></h3>

    <table border="0" align="center" width="100%">
    <thead><tr><th width="25%">&nbsp;</th><th width="25%">&nbsp;</th><th width="25%">&nbsp;</th><th width="25%">&nbsp;</th></tr></thead>
    <tbody>

    <tr><td><b>User ID: </b></td><td> {userID_salary.get()}</td> <td><b>Username: </b></td><td>{info[1]}</td></tr>
    <tr><td><b>PAN: </b></td><td> {info[13]}</td> <td><b>Bank Account Number: </b></td><td>{info[14]}</td></tr>

    </tbody>
    </table>

    <table border="0" align="center" width="100%">
    <thead><tr><th width="25%"><center>Earnings</center></th><th width="25%"><center>Amount</center></th><th width="25%"><center>Extra</center></th><th width="25%"><center>Amount</center></th></tr></thead>
    <tbody>

    <tr><td>Basic </td><td>{basic_salary}</td> <td>Deduction </td><td>{deduction}</td></tr>
    <tr><td>Conveyance </td><td>{conveyance}</td> <td>PF (yearly) </td><td>{PF}</td></tr>
    <tr><td>House Rent </td><td>{house_rent}</td> <td>&nbsp;</td><td>&nbsp;</td></tr>
    <tr><td>Medical </td><td>{medical}</td> <td>&nbsp;</td><td>&nbsp;</td></tr>
    <tr><td><b>Gross Salary (monthly) </b></td><td>{gross_salary}</td><td><b>Net Salary</b></td><td>{((gross_salary*12)-PF)/12}</td></tr>
    <tr><td>&nbsp;</td><td>&nbsp;</td> <td><b>TDS (monthly)</b></td><td>{(salary_slab((gross_salary*12)-deduction))/12}</td></tr>

    </tbody>
    </table>
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
    <p>
        <b>Address:</b> Company's address, line 1 <br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        Company's address, line 2<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        Company's address, line 3<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        Company's address, line 4<br>
    </p>
    <br>
    <p><i> Employee Signature __________________________ (Date of print: {str(datetime.datetime.now())}) </i></p>
    """

    class MyFPDF(FPDF, HTMLMixin):
        pass

    pdf = FPDF()
    pdf.add_page()
    pdf.write_html(html)
    pdf.output(f'{userID_salary.get()}-{month}-payslip.pdf', 'F')

def display_all_tables():
    main = Tk()

    main_display = Frame(main)
    main_display.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(main_display)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    _Y = Scrollbar(main_display, orient=VERTICAL, command=my_canvas.yview)
    _Y.pack(side=RIGHT, fill=Y)
    _X = Scrollbar(main_display, orient=HORIZONTAL, command=my_canvas.xview)
    _X.pack(side=BOTTOM, fill=X)

    my_canvas.configure(xscrollcommand=_X.set, yscrollcommand=_Y.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    display = Frame(my_canvas)

    my_canvas.create_window((0, 0), window=display, anchor="nw")

    cur.execute("show tables")
    table_list = list(cur)

    i = 0
    for _ in table_list:
        k = 0
        cur.execute(f"desc {_[0]}")
        header = list(cur)
        for header_name in header:
            e = Label(display, text=header_name[0], height=2, fg="dark blue")
            e.grid(row=i, column=k, pady=(20, 0), padx=20)
            k = k + 1

        i = i + 1

        cur.execute(f"select * from {_[0]}")
        info = cur

        for record in info:
            for j in range(len(record)):
                e = Label(display, text=record[j])
                e.grid(row=i, column=j, padx=20)
            i = i + 1

    main.mainloop()

def deduction_changes(deduction_details):
    cur.execute(f"delete from deduction_details where ID = '{deduction_details[0]}'")
    cur.execute(f"insert into deduction_details values {tuple(deduction_details)}")
    myconn.commit()

def deduction_entry_panel(info):
    salary = Tk()

    Label(salary, text="Deduction Panel").grid(row=0, column=0, columnspan=2, pady=(10, 10))

    Label(salary, text="PF", width=20, height=2, bg="light blue").grid(row=1, column=0)
    PF_salary = Entry(salary, width=15)
    PF_salary.grid(row=1, column=1)
    PF_salary.insert(END, info[1])

    Label(salary, text="PPF", width=20, height=2, bg="light blue").grid(row=2, column=0)
    PPF_salary = Entry(salary, width=15)
    PPF_salary.grid(row=2, column=1)
    PPF_salary.insert(END, info[2])

    Label(salary, text="NSC/FD", width=20, height=2, bg="light blue").grid(row=3, column=0)
    NSC_FD_salary = Entry(salary, width=15)
    NSC_FD_salary.grid(row=3, column=1)
    NSC_FD_salary.insert(END, info[3])

    Label(salary, text="Tuition Fees", width=20, height=2, bg="light blue").grid(row=4, column=0)
    tuition_fees_salary = Entry(salary, width=15)
    tuition_fees_salary.grid(row=4, column=1)
    tuition_fees_salary.insert(END, info[4])

    Label(salary, text="Home Loan", width=20, height=2, bg="light blue").grid(row=5, column=0)
    home_loan_salary = Entry(salary, width=15)
    home_loan_salary.grid(row=5, column=1)
    home_loan_salary.insert(END, info[5])

    Label(salary, text="Life Insurance", width=20, height=2, bg="light blue").grid(row=6, column=0)
    life_ins_salary = Entry(salary, width=15)
    life_ins_salary.grid(row=6, column=1)
    life_ins_salary.insert(END, info[6])

    Label(salary, text="Medical Insurance", width=20, height=2, bg="light blue").grid(row=7, column=0)
    medi_ins_salary = Entry(salary, width=15)
    medi_ins_salary.grid(row=7, column=1)
    medi_ins_salary.insert(END, info[7])

    if adminPerms == 1: Button(salary, text="Commit changes", width=15, command=lambda: deduction_changes((info[0], PF_salary.get(), PPF_salary.get(), NSC_FD_salary.get(), tuition_fees_salary.get(), home_loan_salary.get(), life_ins_salary.get(), medi_ins_salary.get()))).grid(row=8, column=1, pady=(20, 20), padx=(10, 10))

    salary.mainloop()


def salary_slab(gross_salary):
    if gross_salary<250000: return 0
    elif 250000 <= gross_salary<500000: return ((5/100)*gross_salary)/12
    elif 500000 <= gross_salary < 750000: return ((10 / 100) * gross_salary) / 12
    elif 750000 <= gross_salary < 1000000: return ((15 / 100) * gross_salary) / 12
    elif 1000000 <= gross_salary < 1250000: return ((20 / 100) * gross_salary) / 12
    elif 1250000 <= gross_salary < 1500000: return ((25 / 100) * gross_salary) / 12
    else: return ((30 / 100) * gross_salary) / 12

def salary_changes(salary_details):
    cur.execute(f"delete from salary_details where ID = '{salary_details[0]}'")
    cur.execute(f"insert into salary_details values {tuple(salary_details)}")
    myconn.commit()

def admin_salary_commands(salary):
    Button(salary, text="Fetch Records", width=15, command=lambda: salary_page_setup(salary, userID_salary.get())).grid(row=3, column=2)
    Button(salary, text="Commit Changes", width=15, command=lambda: salary_changes((userID_salary.get(), SPH_salary.get(), hours_salary.get()))).grid(row=3, column=3)

def salary_page_setup(salary, USER_ID_salary):
    global userID_salary, SPH_salary, hours_salary
    global conveyance, house_rent, medical, deduction, gross_salary, basic_salary, PF

    cur.execute(f"select * from salary_details where ID = '{USER_ID_salary}'")
    info = list(list(cur)[0])
    cur.execute(f"select * from deduction_details where ID = '{USER_ID_salary}'")
    info2 = list(list(cur)[0])

    PF = info2[2]

    basic_salary = float(info[1])*float(info[2]*28)
    conveyance, house_rent, medical = basic_salary * 0.05, basic_salary*0.25, basic_salary*0.2
    deduction = sum(float(i) for i in info2[1:])
    gross_salary = basic_salary+conveyance+house_rent+medical

    Label(salary, text="USER_ID:", width=20, height=2).grid(row=0, column=0)
    userID_salary = Entry(salary, width=20)
    userID_salary.grid(row=0, column=1)
    userID_salary.insert(END, info[0])

    month = Entry(salary, width=20)
    month.grid(row=0, column=3)
    month.insert(END, str(datetime.datetime.now().strftime('%B')))
    Button(salary, text="Print Payslip", width=20, command=lambda: pdf_maker(month.get())).grid(row=1, column=3)

    Label(salary, text="Salary/hour:", width=20, height=2).grid(row=1, column=0)
    SPH_salary = Entry(salary, width=20)
    SPH_salary.grid(row=1, column=1)
    SPH_salary.insert(END, info[1])

    Label(salary, text="Hours worked: ", width=20, height=2).grid(row=2, column=0)
    hours_salary = Entry(salary, width=20)
    hours_salary.grid(row=2, column=1)
    hours_salary.insert(END, info[2])

    Label(salary, text="Basic Salary", width=20, height=2).grid(row=3, column=0)
    Label(salary, text=basic_salary, width=20, height=2).grid(row=3, column=1)

    Label(salary, text="Conveyance", width=40, height=2, bg="light blue").grid(row=4, column=0, columnspan=2, pady=(30,0))
    Label(salary, text=conveyance, width=40, height=2).grid(row=4, column=2, columnspan=2, pady=(30,0))
    Label(salary, text="House Rent", width=40, height=2, bg="light blue").grid(row=5, column=0, columnspan=2)
    Label(salary, text=house_rent, width=40, height=2).grid(row=5, column=2, columnspan=2)
    Label(salary, text="Medical", width=40, height=2, bg="light blue").grid(row=6, column=0, columnspan=2)
    Label(salary, text=medical, width=40, height=2).grid(row=6, column=2, columnspan=2)

    Label(salary, text="Gross Salary (monthly)", width=19, height=2, bg="light blue").grid(row=7, column=0)
    Label(salary, text=gross_salary, width=19, height=2).grid(row=7, column=1)
    Label(salary, text="Deduction (yearly)", width=19, height=2, bg="light blue").grid(row=8, column=0)
    Label(salary, text=deduction, width=19, height=2).grid(row=8, column=1)

    Label(salary, text="Tax (yearly)", width=19, height=2, bg="light blue").grid(row=9, column=0)
    Label(salary, text=salary_slab((gross_salary*12)-deduction), width=19, height=2).grid(row=9, column=1)

    Button(salary, text="Deduction", width=15, command=lambda: deduction_entry_panel(info2)).grid(row=9, column=3)
    if adminPerms == 1: Button(salary, text="EDIT", width=15, command=lambda: admin_salary_commands(salary)).grid(row=9, column=2)

def delete_records(ID):
    cur.execute(f"delete from personal_details where ID = '{ID}'")
    cur.execute(f"delete from salary_details where ID = '{ID}'")
    cur.execute(f"delete from deduction_details where ID = '{ID}'")
    cur.execute(f"delete from login_details where ID = '{ID}'")

    myconn.commit()

def reset_system():
    cur.execute("drop database payroll_forms")
    myconn.commit()
    sys.exit()

def command_palette_setup():
    cp = Tk()
    Label(cp, text="COMMAND PALETTE").grid(row=0, column=0, columnspan=2, pady=20)
    Button(cp, text="Fetch Records", width=20, height=10, command=fetch_records).grid(row=1, column=0)
    Button(cp, text="Add/Edit Record", width=20, height=10, command=lambda: edit_records([USER_ID.get(), USER_NAME.get(), GENDER.get(), FATHERS_NAME.get(), marital_Button.get(), DESIGNATION.get(), DEPARTMENT.get(), DOB.get(), DOJ.get(), DOC.get(), DOE.get(), QUALIFICATIONS.get(), ADDRESS.get(), PAN.get(), BANK_ACCOUNT_NUMBER.get(), MANAGER_ID.get(), MANAGER_NAME.get(), LOCATION.get(), STATUS.get(), EMAIL.get()], [USER_ID.get(), SET_PASSWORD.get(), ADMIN_PERMS.get()], [USER_ID, USER_NAME, GENDER, FATHERS_NAME, marital_Button_check, DESIGNATION, DEPARTMENT, DOB, DOJ, DOC, DOE, QUALIFICATIONS, ADDRESS, PAN, BANK_ACCOUNT_NUMBER, MANAGER_ID, MANAGER_NAME, LOCATION, STATUS, EMAIL, USER_ID, SET_PASSWORD, ADMIN_PERMS_check])).grid(row=1, column=1)
    Button(cp, text="Delete Record", width=20, height=10, command=lambda: delete_records(USER_ID.get())).grid(row=2, column=0)
    Button(cp, text="Reset System", width=20, height=10, command=reset_system).grid(row=2, column=1)

    cp.mainloop()

def fetch_records():
    cur.execute(f'select * from personal_details where ID = "{USER_ID.get()}"')
    info = list(list(cur)[0])
    print(info)
    cur.execute(f'select * from login_details where ID = "{USER_ID.get()}"')
    info_ = list(list(cur)[0])
    print(info_)
    delete_from_entry()
    USER_ID.insert(END, info[0])
    USER_NAME.insert(END, info[1])
    GENDER.insert(END, info[2])
    FATHERS_NAME.insert(END, info[3])
    DESIGNATION.insert(END, info[5])
    DEPARTMENT.insert(END, info[6])
    DOB.insert(END, str(info[7]))
    DOJ.insert(END, str(info[8]))
    DOC.insert(END, str(info[9]))
    DOE.insert(END, str(info[10]))
    QUALIFICATIONS.insert(END, info[11])
    ADDRESS.insert(END, info[12])
    PAN.insert(END, info[13])
    BANK_ACCOUNT_NUMBER.insert(END, info[14])
    MANAGER_ID.insert(END, info[15])
    MANAGER_NAME.insert(END, info[16])
    LOCATION.insert(END, info[17])
    STATUS.insert(END, info[18])
    EMAIL.insert(END, info[19])
    SET_PASSWORD.insert(END, info_[1])

    if info[4] == 1: marital_Button_check.select()
    if info_[2] == 1: ADMIN_PERMS_check.select()

def delete_from_entry():
    variables_list = [USER_ID, USER_NAME, GENDER, FATHERS_NAME, DESIGNATION, DEPARTMENT, DOB, DOJ, DOC, DOE, QUALIFICATIONS, ADDRESS, PAN, BANK_ACCOUNT_NUMBER, MANAGER_ID, MANAGER_NAME, LOCATION, STATUS, EMAIL, SET_PASSWORD]
    for i in variables_list: exec("i.delete(0, END)")
    marital_Button_check.deselect()
    ADMIN_PERMS_check.deselect()

def edit_records(personal_details, login_details, variables_list):
    cur.execute(f"delete from login_details where ID = '{login_details[0]}'")
    cur.execute(f"insert into login_details values {tuple(login_details)}")
    cur.execute(f"delete from personal_details where ID = '{personal_details[0]}'")
    cur.execute(f"insert into personal_details values {tuple(personal_details)}")

    cur.execute(f"select * from deduction_details where ID = '{personal_details[0]}'")
    try:
        info = list(list(cur)[0])
        cur.execute(f"delete from deduction_details where ID = '{info[0]}'")
        cur.execute(f"insert into deduction_details values ('{info[0]}')")
    except:
        cur.execute(f"insert into deduction_details(ID) values('{personal_details[0]}')")

    cur.execute(f"select * from salary_details where ID = '{personal_details[0]}'")
    try:
        info = list(list(cur)[0])
        cur.execute(f"delete from salary_details where ID = '{info[0]}'")
        cur.execute(f"insert into salary_details values ('{info[0]}', {float(info[1])}, {float(info[2])})")
    except:
        cur.execute(f"insert into salary_details(ID) values('{personal_details[0]}')")

    myconn.commit()
    delete_from_entry()
    print("Done")

def admin_page_setup(admin):
    global USER_ID, USER_NAME, GENDER, FATHERS_NAME, DESIGNATION, DEPARTMENT, DOB, DOJ, DOC, DOE, QUALIFICATIONS, ADDRESS, PAN, BANK_ACCOUNT_NUMBER, MANAGER_ID, MANAGER_NAME, LOCATION, STATUS, EMAIL, SET_PASSWORD, marital_Button_check, ADMIN_PERMS_check, ADMIN_PERMS, marital_Button
    Label(admin, text="USER ID:").grid(row=0, column=0)
    USER_ID = Entry(admin)
    USER_ID.grid(row=0, column=1)

    Button(admin, text="All info", width=20, command=display_all_tables).grid(row=0, column=2)
    Button(admin, text="Open Command Palette", command=command_palette_setup).grid(row=0, column=3)

    Label(admin, text="USER NAME:", width=20, height=2).grid(row=1, column=0)
    USER_NAME = Entry(admin, width=20)
    USER_NAME.grid(row=1, column=1)
    Label(admin, text="SET PASSWORD:", width=20, height=2).grid(row=1, column=2)
    SET_PASSWORD = Entry(admin, width=20)
    SET_PASSWORD.grid(row=1, column=3)

    Label(admin, text="Martial Status: ", width=20, height=2).grid(row=2, column=2)
    marital_Button = IntVar()
    marital_Button_check = Checkbutton(admin, variable=marital_Button, onvalue=1, offvalue=0, width=17)
    marital_Button_check.grid(row=2, column=3)
    Label(admin, text="Father's Name: ", width=20, height=2).grid(row=2, column=0)
    FATHERS_NAME = Entry(admin, width=20)
    FATHERS_NAME.grid(row=2, column=1)

    Label(admin, text="Designation: ", width=20, height=2).grid(row=3, column=0)
    DESIGNATION = Entry(admin, width=20)
    DESIGNATION.grid(row=3, column=1)
    Label(admin, text="Department: ", width=20, height=2).grid(row=3, column=2)
    DEPARTMENT = Entry(admin, width=20)
    DEPARTMENT.grid(row=3, column=3)

    Label(admin, text="DOB: ", width=20, height=2).grid(row=4, column=0)
    DOB = Entry(admin, width=20)
    DOB.grid(row=4, column=1)
    Label(admin, text="DOJ: ", width=20, height=2).grid(row=4, column=2)
    DOJ = Entry(admin, width=20)
    DOJ.grid(row=4, column=3)
    Label(admin, text="DOC: ", width=20).grid(row=5, column=0)
    DOC = Entry(admin, width=20)
    DOC.grid(row=5, column=1)
    Label(admin, text="DOE: ", width=20, height=2).grid(row=5, column=2)
    DOE = Entry(admin, width=20)
    DOE.grid(row=5, column=3)

    Label(admin, text="Qualifications: ", width=20, height=2).grid(row=6, column=0)
    QUALIFICATIONS = Entry(admin, width=20)
    QUALIFICATIONS.grid(row=6, column=1)
    Label(admin, text="Admin perms: ", width=20, height=2).grid(row=6, column=2)
    ADMIN_PERMS = IntVar()
    ADMIN_PERMS_check = Checkbutton(admin, variable=ADMIN_PERMS, onvalue=1, offvalue=0, width=17)
    ADMIN_PERMS_check.grid(row=6, column=3)
    Label(admin, text="Address: ", width=20, height=2).grid(row=7, column=0)
    ADDRESS = Entry(admin, width=20)
    ADDRESS.grid(row=7, column=1)

    Label(admin, text="PAN: ", width=20, height=2).grid(row=8, column=0)
    PAN = Entry(admin, width=20)
    PAN.grid(row=8, column=1)
    Label(admin, text="Bank Account Number: ", width=20, height=2).grid(row=8, column=2)
    BANK_ACCOUNT_NUMBER = Entry(admin, width=20)
    BANK_ACCOUNT_NUMBER.grid(row=8, column=3)

    Label(admin, text="Manager ID: ", width=20, height=2).grid(row=9, column=0)
    MANAGER_ID = Entry(admin, width=20)
    MANAGER_ID.grid(row=9, column=1)
    Label(admin, text="Manager Name: ", width=20, height=2).grid(row=9, column=2)
    MANAGER_NAME = Entry(admin, width=20)
    MANAGER_NAME.grid(row=9, column=3)

    Label(admin, text="Location: ", width=20, height=2).grid(row=10, column=0)
    LOCATION = Entry(admin, width=20)
    LOCATION.grid(row=10, column=1)
    Label(admin, text="Status: ", width=20, height=2).grid(row=10, column=2)
    STATUS = Entry(admin, width=20)
    STATUS.grid(row=10, column=3)

    Label(admin, text="E-mail: ", width=20, height=2).grid(row=11, column=0)
    EMAIL = Entry(admin, width=20)
    EMAIL.grid(row=11, column=1)
    Label(admin, text="Gender: ", width=20, height=2).grid(row=11, column=2)
    GENDER = Entry(admin, width=20)
    GENDER.grid(row=11, column=3)


def personal_page_setup(personal_page):
    cur.execute(f"select * from personal_details where ID = '{userID}'")
    info = list(list(cur)[0])
    Label(personal_page, text="USER ID:", font=("Arial Bold", 9)).grid(row=0, column=0)
    Label(personal_page, text="USERNAME:", font=("Arial Bold", 9)).grid(row=1, column=0, pady=(0, 20))
    Label(personal_page, text="GENDER:", font=("Arial Bold", 9)).grid(row=1, column=2, pady=(0, 20))
    Label(personal_page, text=info[0]).grid(row=0, column=1)
    Label(personal_page, text=info[1]).grid(row=1, column=1, pady=(0, 20))
    Label(personal_page, text=info[2]).grid(row=1, column=3, pady=(0, 20))

    Label(personal_page, text="Martial Status: ", bg="light blue", width=20, height=2).grid(row=2, column=2)
    maritalButton = Checkbutton(personal_page, width=17)
    if info[4] == 1: maritalButton.select()
    else: maritalButton.deselect()
    maritalButton.grid(row=2, column=3)
    Label(personal_page, text="Father's Name: ", bg="light blue", width=20, height=2).grid(row=2, column=0)
    Label(personal_page, text=info[3], width=20, height=2).grid(row=2, column=1)

    Label(personal_page, text="Designation: ", bg="light blue", width=20, height=2).grid(row=3, column=0)
    Label(personal_page, text=info[5], width=20, height=2).grid(row=3, column=1)
    Label(personal_page, text="Department: ", bg="light blue", width=20, height=2).grid(row=3, column=2)
    Label(personal_page, text=info[6], width=20, height=2).grid(row=3, column=3)

    Label(personal_page, text="DOB: ", bg="light blue", width=20, height=2).grid(row=4, column=0)
    Label(personal_page, text=info[7], width=20, height=2).grid(row=4, column=1)
    Label(personal_page, text="DOJ: ", bg="light blue", width=20, height=2).grid(row=4, column=2)
    Label(personal_page, text=info[8], width=20, height=2).grid(row=4, column=3)
    Label(personal_page, text="DOC: ", bg="light blue", width=20, height=2).grid(row=5, column=0)
    Label(personal_page, text=info[9], width=20, height=2).grid(row=5, column=1)
    Label(personal_page, text="DOE: ", bg="light blue", width=20, height=2).grid(row=5, column=2)
    Label(personal_page, text=info[10], width=20, height=2).grid(row=5, column=3)

    Label(personal_page, text="Qualifications: ", bg="light blue", width=20, height=2).grid(row=6, column=0)
    Label(personal_page, text=info[11], width=20, height=2).grid(row=6, column=1, columnspan=3)
    Label(personal_page, text="Address: ", bg="light blue", width=20, height=2).grid(row=7, column=0)
    Label(personal_page, text=info[12], height=2).grid(row=7, column=1, columnspan=3)

    Label(personal_page, text="PAN: ", bg="light blue", width=20, height=2).grid(row=8, column=0)
    Label(personal_page, text=info[13], width=20, height=2).grid(row=8, column=1)
    Label(personal_page, text="Bank Account Number: ", bg="light blue", width=20, height=2).grid(row=8, column=2)
    Label(personal_page, text=info[14], width=20, height=2).grid(row=8, column=3)

    Label(personal_page, text="Manager ID: ", bg="light blue", width=20, height=2).grid(row=9, column=0)
    Label(personal_page, text=info[15], width=20, height=2).grid(row=9, column=1)
    Label(personal_page, text="Manager Name: ", bg="light blue", width=20, height=2).grid(row=9, column=2)
    Label(personal_page, text=info[16], width=20, height=2).grid(row=9, column=3)

    Label(personal_page, text="Location: ", bg="light blue", width=20, height=2).grid(row=10, column=0)
    Label(personal_page, text=info[17], width=20, height=2).grid(row=10, column=1)
    Label(personal_page, text="Status: ", bg="light blue", width=20, height=2).grid(row=10, column=2)
    Label(personal_page, text=info[18], width=20, height=2).grid(row=10, column=3)

    Label(personal_page, text="E-mail: ", bg="light blue", width=20, height=2).grid(row=11, column=0)
    Label(personal_page, text=info[19], height=2).grid(row=11, column=1, columnspan=3)

    print(info)

def main_page():
    Label(root, text=f"USERPAGE - {userID}").pack()

    tabControl = ttk.Notebook(root)
    personal_page = Frame(tabControl)
    salary = Frame(tabControl)
    admin = Frame(tabControl)

    tabControl.add(personal_page, text="PERSONAL PAGE")
    tabControl.add(salary, text="SALARY PAGE")
    if adminPerms == 1: tabControl.add(admin, text="ADMIN")
    else: tabControl.add(admin, text="ADMIN", state=DISABLED)
    tabControl.pack()

    personal_page_setup(personal_page)
    admin_page_setup(admin)
    salary_page_setup(salary, userID)

def create_environment():
    cur.execute("create table login_details(ID varchar(20) primary key, password varchar(20), perms int)")
    cur.execute("insert into login_details values('0A00', 'pass@123', 1)")
    cur.execute("CREATE TABLE `personal_details` ( `ID` VARCHAR(20) NOT NULL, `Name` VARCHAR(20), `Gender` VARCHAR(6), `F_Name` VARCHAR(20), `Marital_Status` INT, `Designation` VARCHAR(20), `Department` VARCHAR(20), `DOB` DATE, `DOJ` DATE, `DOC` DATE, `DOE` DATE, `Qualification` VARCHAR(100), `Address` VARCHAR(100), `PAN` CHAR(10), `Bank_Account_Number` INT, `Manager_ID` VARCHAR(20), `Manager_Name` VARCHAR(20), `Location` VARCHAR(20), `Status` VARCHAR(6), `EMail_ID` VARCHAR(50), PRIMARY KEY (`ID`) );")
    cur.execute("insert into personal_details(ID) values('0A00')")
    cur.execute("CREATE TABLE `salary_details` (`ID` VARCHAR(20) NOT NULL, `SPH` INT DEFAULT '0', `hours` INT DEFAULT '0', PRIMARY KEY (`ID`));")
    cur.execute("insert into salary_details(ID) values('0A00')")
    cur.execute("CREATE TABLE `deduction_details` (`ID` VARCHAR(20) NOT NULL, `PF` INT DEFAULT '0', `PPF` INT DEFAULT '0', `NSC_FD` INT DEFAULT '0', `tuition_fees` INT DEFAULT '0',	`home_loan` INT DEFAULT '0', `life_ins` INT DEFAULT '0', `medi_ins` INT DEFAULT '0', PRIMARY KEY (`ID`));")
    cur.execute("insert into deduction_details(ID) values('0A00')")
    myconn.commit()

def connect():
    global myconn
    global cur
    myconn = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, database="payroll_forms")
    cur = myconn.cursor(buffered=True)

def new_connect():
    tempMyconn = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD)
    tempCur = tempMyconn.cursor()
    tempCur.execute("create database payroll_forms")
    tempMyconn.close()
    connect()
    create_environment()

def check():
    global userID, adminPerms
    userID = ID.get()
    userPassword = password.get()
    try:
        connect()
    except mysql.connector.errors.ProgrammingError:
        new_connect()
    try:
        cur.execute(f"select * from login_details where ID = '{userID}'")
        tempList = list(cur)[0]
        realpassword = tempList[1]
        adminPerms = tempList[2]
        if realpassword == userPassword: return True
    except:
        Label(login, text="Please enter correct details.").grid(row=3, column=1)
        return False

def main():
    global root
    if check() == True:
        login.destroy()

        root = Tk()
        root.title("Payroll Forms - USER DASHBOARD")
        root.resizable(width=False, height=False)
        root.iconbitmap("logo.ico")

        main_page()
        root.mainloop()

def login_page():
    global ID
    global password
    Label(login, text="Python Project: Payroll", font=("Arial", 30)).grid(row=0, column=0, columnspan=4, padx=50, pady=25)

    Label(login, text="UsernameID: ").grid(row=1, column=1)
    Label(login, text="Password: ").grid(row=2, column=1)
    ID = Entry(login)
    password = Entry(login, show="*")
    ID.grid(row=1, column=2)
    password.grid(row=2, column=2)

    login_btn = Button(login, text="LOGIN", width=10, command=main).grid(row=3, column=2, pady=(10,50), padx=(50,0))

from tkinter import *
import mysql.connector
import datetime
from tkinter import ttk
from fpdf import FPDF, HTMLMixin
from settings import HOST, USER, PASSWD, company_name

login = Tk()
login.title("Payroll Forms - LOGIN PAGE")
login.resizable(width=False, height=False)
login.iconbitmap("logo.ico")

login_page()

login.mainloop()
cur.close()
