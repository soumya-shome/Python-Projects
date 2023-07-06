import ast
def check_unfollowers(current,old):
	return list(set(old) - set(current))

def check_followers(current,old):
	return list(set(current) - set(old))

old_followers = []
current_followers = []
f1 = open("follower_list.txt","r+")
current_followers = f1.read()
f1.close()
current_followers = ast.literal_eval(current_followers)

f2 = open("old_follower_list.txt","r+")
old_followers = f2.read()
f2.close()
old_followers = ast.literal_eval(old_followers)

unfollowers = check_unfollowers(current_followers,old_followers)
followers = check_followers(current_followers,old_followers)

follower_change  = len(current_followers)-len(old_followers)

follow_count = len(followers)
unfollow_count = len(unfollowers)

print("Followers Change : ",follower_change)
print()
print("Followers Change : ",follow_count)
print()
print("Unfollower Count : ",unfollow_count)
print()
print("Unfollowers : ",unfollowers)
print()
print("Followers : ",followers)