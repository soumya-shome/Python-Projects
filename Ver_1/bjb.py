from igramscraper.instagram import Instagram
import datetime
from pytz import timezone
from os import path
from time import sleep
import ast
import sys
insta_username =''
insta_password = ''
FOLLOWER_LIMIT = 10**6

FOLLOWER_LIMIT = 10**6


insta_username = 'randompy21'


insta_password = 'xyz123'

#username = 'calcutta_bongs'
username = 'calcutta_bloggers'

MINS_TO_SLEEP = 40

def non_followers(following,followers):
	return list(set(following) - set(followers))

print("iter")
instagram = Instagram()
instagram.with_credentials(insta_username, insta_password)
instagram.login(force=False,two_step_verificator=True)
sleep(2) # Delay to mimic user
followers = []
account = instagram.get_account(username)
sleep(1)
curr_time = datetime.datetime.now(timezone('Asia/Kolkata'))
curr_time = curr_time.strftime("%b %d, %Y - %H:%M:%S")
followers = instagram.get_followers(account.identifier, FOLLOWER_LIMIT, 100, delayed=True) # Get 150 followers of 'kevin', 100 a time with random delay between requests
#print(followers)

followings = instagram.get_following(account.identifier, FOLLOWER_LIMIT, 100, delayed=True) # Get 150 followers of 'kevin', 100 a time with random delay between requests

current_followers = []
for follower in followers['accounts']:
	current_followers.append(follower.username)

current_following = []
for following in followings['accounts']:
	current_following.append(following.username)
#print (current_followers)
#print (current_following)
del followers
del followings
nonfollowers = non_followers(current_following,current_followers)
f=open("List.txt","w")
for i in nonfollowers:
	s=i+","
	f.write(s)
f.close()
print("Non Folowers : ",nonfollowers)
#f=open("List.txt","w")
#f.write(nonfollowers)
#f.close()
#if not path.exists("follower_list.txt"):
#	f = open("follower_list.txt","w")
#	f.write(str(current_followers))
#	f.close()
#else:
#	f = open("follower_list.txt","r+")
#	old_followers = f.read()
#	f.close()
#old_followers = ast.literal_eval(old_followers)
#unfollowers = check_unfollowers(current_followers,old_followers)
#followers = check_followers(current_followers,old_followers)
#follower_change  = len(current_followers)-len(old_followers)
#follow_count = len(followers)
#unfollow_count = len(unfollowers)
#f = open("follower_list.txt","w")
#f.write(str(current_followers))
#f.close()