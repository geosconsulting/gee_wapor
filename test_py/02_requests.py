from urllib2 import urlopen

# Add your code here!
website = urlopen("http://repubblica.it/")
kittens = website.read()

print(kittens)