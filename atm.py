#!/usr/bin/python
import getpass
import string
import platform
import mysql.connector
import MySQLdb
import re

#Database connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ATM"
)

mycursor = mydb.cursor()

#mycursor.execute("SELECT * FROM users")
#vin = mycursor.fetchall()
#i=1
#print("Details")				
#for a, b, c in vin:
#	print("{}\t{}\t\t{}\t{}".format(i, a, b, c))
#	i=i+1

count = 0
# while loop checks existance of the enterd username
while True:
	user = input('\nENTER USER NAME: ')
	user = user.lower()
	mycursor.execute("(SELECT count(1) FROM users WHERE uname = %(name)s )",{'name':user})
	if mycursor.fetchone()[0]:
		break
	else:
		print('----------------')
		print('****************')
		print('INVALID USERNAME')
		print('****************')
		print('----------------')

# comparing pin
while count < 3:
	print('------------------')
	print('******************')
	pinno = str(getpass.getpass('PLEASE ENTER PIN: '))
	print('******************')
	print('------------------')
	if pinno.isdigit():
		mycursor.execute("(SELECT count(1) FROM users WHERE uname = %(name)s AND pin = %(pinn)s)",{'name':user, 'pinn':pinno})
		if mycursor.fetchone()[0]:
			break
		else:
			count += 1
			print('-----------')
			print('***********')
			print('INVALID PIN')
			print('***********')
			print('-----------')
			print()
	else:
		print('------------------------')
		print('************************')
		print('PIN CONSISTS OF 4 DIGITS')
		print('************************')
		print('------------------------')
		count += 1
	
# in case of a valid pin- continuing, or exiting
if count == 3:
	print('-----------------------------------')
	print('***********************************')
	print('3 UNSUCCESFUL PIN ATTEMPTS, EXITING')
	print('!!!!!YOUR CARD HAS BEEN LOCKED!!!!!')
	print('***********************************')
	print('-----------------------------------')
	exit()

print('-------------------------')
print('*************************')
print('LOGIN SUCCESFUL, CONTINUE')
print('*************************')
print('-------------------------')
print()
print('--------------------------')
print('**************************')	
print(str.capitalize(user), 'welcome to ATM')
print('**************************')
print('----------ATM SYSTEM-----------')
# Main menu
while True:
	#os.system('clear')
	print('-------------------------------')
	print('*******************************')
	response = input('SELECT FROM FOLLOWING OPTIONS: \nStatement__(S) \nWithdraw___(W) \nDeposit____(D)  \nChange PIN_(P)  \nQuit_______(Q) \n: ').lower()
	print('*******************************')
	print('-------------------------------')
	valid_responses = ['s', 'w', 'd', 'p', 'q']
	response = response.lower()
	if response == 's':
		mycursor.execute("(SELECT amount FROM users WHERE uname = %(uname)s AND pin = %(pin)s)",{'uname':user, 'pin':pinno})
		vin = mycursor.fetchone()
		print('---------------------------------------------')
		print('*********************************************')
		print('{} YOU HAVE {} Rupees ON YOUR ACCOUNT.'.format(user, vin))
		print('*********************************************')
		print('---------------------------------------------')
		
	elif response == 'w':
		print('---------------------------------------------')
		print('*********************************************')
		cash_out = int(input('ENTER AMOUNT YOU WOULD LIKE TO WITHDRAW: '))
		print('*********************************************')
		print('---------------------------------------------')
		mycursor.execute("(SELECT amount FROM users WHERE uname = %(name)s AND pin = %(pinn)s)",{'name':user, 'pinn':pinno})
		vin = mycursor.fetchone()
		vin = int(vin[0])
		if cash_out%10 != 0:
			print('------------------------------------------------------')
			print('******************************************************')
			print('AMOUNT YOU WANT TO WITHDRAW MUST TO MATCH 10 Rupees NOTES')
			print('******************************************************')
			print('------------------------------------------------------')
		elif cash_out > vin:
			print('-----------------------------')
			print('*****************************')
			print('YOU HAVE INSUFFICIENT BALANCE')
			print('*****************************')
			print('-----------------------------')
		else:
			vin = vin - cash_out
			print('-----------------------------------')
			print('***********************************')
			print('YOUR NEW BALANCE IS: {} Rupees'.format(vin))
			print('***********************************')
			print('-----------------------------------')
			mycursor.execute("UPDATE users SET amount = %(amount)s WHERE uname = %(name)s AND pin = %(pinn)s",{'amount':vin,'name':user, 'pinn':pinno})
			mydb.commit()
			
	elif response == 'd':
		print()
		print('---------------------------------------------')
		print('*********************************************')
		cash_in = int(input('ENTER AMOUNT YOU WANT TO DEPOSIT: '))
		print('*********************************************')
		print('---------------------------------------------')
		print()
		mycursor.execute("SELECT amount FROM users WHERE uname = %(name)s AND pin = %(pinn)s",{'name':user, 'pinn':pinno})
		vin = mycursor.fetchone()
		vin = int(vin[0])
		if cash_in%10 != 0:
			print('----------------------------------------------------')
			print('****************************************************')
			print('AMOUNT YOU WANT TO DEPOSIT MUST TO MATCH 10 Rupees NOTES')
			print('****************************************************')
			print('----------------------------------------------------')
		else:
			vin = vin + cash_in
			print('----------------------------------------')
			print('****************************************')
			print('YOUR NEW BALANCE IS: {} Rupees'.format(vin))
			print('***********************************')
			print('-----------------------------------')
			mycursor.execute("UPDATE users SET amount = %(amount)s WHERE uname = %(name)s AND pin = %(pinn)s",{'amount':vin,'name':user, 'pinn':pinno})
			mydb.commit()
	elif response == 'p':
		print('-----------------------------')
		print('*****************************')
		new_pin = str(getpass.getpass('ENTER A NEW PIN: '))
		print('*****************************')
		print('-----------------------------')
		if new_pin.isdigit() and new_pin != pinno and len(new_pin) == 4:
			print('------------------')
			print('******************')
			new_ppin = str(getpass.getpass('CONFIRM NEW PIN: '))
			print('*******************')
			print('-------------------')
			if new_ppin != new_pin:
				print('------------')
				print('************')
				print('PIN MISMATCH')
				print('************')
				print('------------')
			else:
				pinn = new_pin
				print('NEW PIN SAVED')
				mycursor.execute("UPDATE users SET pin = %(newpin)s WHERE uname = %(name)s AND pin = %(pinn)s",{'newpin':new_pin,'name':user, 'pinn':pinno})
				mydb.commit()
		else:
			print('-------------------------------------')
			print('*************************************')
			print('   NEW PIN MUST CONSIST OF 4 DIGITS \nAND MUST BE DIFFERENT TO PREVIOUS PIN')
			print('*************************************')
			print('-------------------------------------')
	elif response == 'q':
		exit()
	else:
		print('------------------')
		print('******************')
		print('RESPONSE NOT VALID')
		print('******************')
		print('------------------')
