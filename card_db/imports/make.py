f = open("this.json", "r+")
new = open("new.json", "w")

newobj = ''
for line in f.readlines():
    newln = line.strip()
    newobj += newln

new.write(newobj)

f.close()
new.close()

