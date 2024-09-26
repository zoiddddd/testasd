from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time,sys,concurrent.futures
edgedriver_path=Path(__file__).parent/'msedgedriver.exe'
extension_folder=Path(__file__).parent/'1.14.2_0'
def load_roblosecurity_from_file(filename):
	A=Path(__file__).parent/filename
	try:
		with open(A,'r')as B:C=B.read().strip();return C
	except FileNotFoundError:print(f"File not found: {A}");return
roblosecurity=load_roblosecurity_from_file('roblox_cookies.txt')
if not roblosecurity:print('roblox_cookies.txt not found or is empty. Please create the file with your ROBLOSECURITY cookie.');sys.exit()
def load_group_urls(filename):
	A=Path(__file__).parent/filename
	try:
		with open(A,'r')as B:C=[A.strip()for A in B if A.strip()and not A.startswith('#')]
		return C
	except FileNotFoundError:print(f"File not found: {A}");return[]
def load_message_from_file(filename):
	A=Path(__file__).parent/filename
	try:
		with open(A,'r',encoding='utf-8')as B:C=B.read().strip();return C
	except FileNotFoundError:print(f"File not found: {A}");return
def post_message_to_group(group_url,message,roblosecurity,edgedriver_path,extension_folder):
	G='Message sent successfully!';F="textarea[placeholder='Say something...']";E='value';B=Options();B.add_argument(f"--load-extension={extension_folder}");B.add_argument('--disable-background-timer-throttling');B.add_argument('--disable-backgrounding-occluded-windows');B.add_argument('--disable-renderer-backgrounding');H=Service(edgedriver_path);A=webdriver.Edge(service=H,options=B);A.get('https://www.roblox.com');A.add_cookie({'name':'.ROBLOSECURITY',E:roblosecurity,'domain':'.roblox.com','path':'/'});A.get(group_url);time.sleep(5);A.execute_script("window.onfocus = () => {document.title = 'Active';};")
	try:
		C=A.find_element(By.CSS_SELECTOR,F);C.click();A.execute_script('arguments[0].value = arguments[1];',C,message);A.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",C)
		while True:
			try:
				I=A.find_element(By.XPATH,"//button[contains(text(), 'Post')]");A.execute_script('arguments[0].click();',I);print('Sending Message');time.sleep(5)
				if A.find_element(By.CSS_SELECTOR,F).get_attribute(E)=='':print(G);break
				else:print('Message not sent, checking again...');time.sleep(5)
			except Exception as D:
				print(f"Post button click intercepted or another error: {D}. Checking textarea...")
				if A.find_element(By.CSS_SELECTOR,F).get_attribute(E)=='':print(G);break
				else:print('Solving Captcha/Pasting Message');time.sleep(5)
	except Exception as D:print(f"Error finding elements: {D}")
	finally:A.quit()
def main(total_messages):
	A=total_messages;E=load_group_urls('groups.txt')
	if not E:print('No groups to process. Exiting.');return
	F=load_message_from_file('message.txt')
	if not F:print('message.txt not found or is empty. Please create the file with your message.');return
	B=0
	with concurrent.futures.ThreadPoolExecutor(max_workers=3)as G:
		C=[]
		while B<A or A==-1:
			for D in E:
				if B>=A and A!=-1:break
				print(f"Opening group {D}");H=G.submit(post_message_to_group,D,F,roblosecurity,edgedriver_path,extension_folder);C.append(H);B+=1;print(f"Message sent to group {D} - {B}/{A}")
				if B>=A and A!=-1:break
			concurrent.futures.wait(C,return_when=concurrent.futures.FIRST_COMPLETED);C=[A for A in C if not A.done()]
		concurrent.futures.wait(C)
if __name__=='__main__':total_messages=int(input('How many messages do you want to send? If infinite, enter -1: '));main(total_messages)
