#import instabot
from instabot import Bot
from time import sleep

bot=Bot()

bot.login(username="calcutta_blog",password="upsisoumya")
sleep(2)

followers = bot.get_user_followers("calcutta_bloggers")
f=open("Followers.txt","w")
f.write(str(followers))
f.close()

sleep(1)

following = bot.get_user_following("calcutta_bloggers")
f=open("Following.txt","w")
f.write(str(following))
f.close()

print("Complete")
