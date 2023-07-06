import ast

def non_followers(following,followers):
	return list(set(following) - set(followers))

followers=[]
following=[]

f=open("Followers.txt","r")
if f.mode=='r':
    followers=f.read()
f.close()
print("Got Followers")

f=open("Following.txt","r")
if f.mode=='r':
    following=f.read()
f.close()
print("Got Followings")

followers = ast.literal_eval(followers)
following=ast.literal_eval(following)

nonfollowers = non_followers(following,followers)
f=open("non_followers.txt","w")
f.write(str(nonfollowers))
f.close()
print("Completed")