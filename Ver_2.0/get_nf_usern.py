import ast
from instabot import Bot
from time import sleep
from random import randint

bot=Bot()

bot.login(username="calcutta_blog",password="upsisoumya")
print("LOGGEDIN")
sleep(2)

nfollowers=[]

f=open("non_followers.txt","r")
if f.mode=='r':
    nfollowers=f.read()
f.close()

nfollowers = ast.literal_eval(nfollowers)
print("No of non followers : {}".format(len(nfollowers)))
print("Getting username ")
don=[]
f=open("non_folls.txt","w+")
for i in range(300):
    s=bot.get_username_from_user_id(nfollowers[i])
    print("{}".format(s))
    f.write(s+"\n")
    don.append(nfollowers[i])
    sleep(randint(0,2))
f.close()
to_unfoll=[]
to_unfoll=list(set(nfollowers)-set(don))

f=open("to_unfollow.txt","w")
f.write(str(to_unfoll))
f.close()