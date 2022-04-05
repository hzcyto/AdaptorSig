import sys

def analyzyer(l, sip):
    box = l.split(" ")
    rbox = []
    for data in box:
        if data == '':
            continue
        if data[0].isdigit() and "." in data and not sip in data:
            rbox.append(data)
    if len(rbox) == 1:
        return rbox[0].rstrip(":")
    else:
        rstr = ""
        for d in rbox:
            rstr += d + ", "
        return None
    


def ipchecker(data):
    box = data.rstrip(":").split(".")
    if len(box) == 5 and box[4].isdigit():
        ip = ""
        for i in range(4):
            ip += f"{box[i]}."
        return ip.rstrip("."), int(box[4])
    return None, -1


fname = sys.argv[1]
sip = sys.argv[2]

ouputs = []
inputs = []

datanum = {}
safeport = [22, 53, 443, 5353]


data = ""
with open(fname, "r") as f:
    for line in f:
        #print(line)
        if "> " + sip in line:
            data = analyzyer(line, sip)
            if not data in inputs and not data is None:
                inputs.append(data)
                if not data in datanum.keys():
                    datanum[data] = 0
            elif data in inputs:
                datanum[data] += 1
        elif sip in line and ">" in line:
            data = analyzyer(line, sip)
            if not data in ouputs and not data is None:
                ouputs.append(data)
                if not data in datanum.keys():
                    datanum[data] = 0
            elif data in ouputs:
                datanum[data] += 1

print("output")
for d in ouputs:
    print(d)
print("-"*150)
print("input")
for d in inputs:
    print(d)
print("-"*150)
print("amounts of it")
for k in datanum.keys():
    print(f"{k} : {datanum[k]}")



with open("wl.sh", "w") as f:
    for d in ouputs:
        ip, port = ipchecker(d)
        if (datanum[d] > 20 or port in safeport) and not ip is None and port != -1:
            f.write(f"sudo iptables -A OUTPUT -d {ip} --dport {port} -j ACCEPT\n")
    for d in inputs:
        ip, port = ipchecker(d)
        if (datanum[d] > 20 or port in safeport) and not ip is None and port != -1:
            f.write(f"sudo iptables -A INPUT -s {ip} --sport {port} -j ACCEPT\n")
    


