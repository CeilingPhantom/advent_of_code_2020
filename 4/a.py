import re

def a(lines):
    nValid = 0
    passport = {}
    for line in lines:
        line = line.strip()
        if not line:
            if len(passport) == 8 or \
               "cid" not in passport and len(passport) == 7:
                nValid += 1
            passport.clear()
            continue
        fields = line.split()
        for field in fields:
            kv = field.split(":")
            passport[kv[0]] = kv[1]
    # check last passport
    if len(passport) == 8 or \
        "cid" not in passport and len(passport) == 7:
        nValid += 1
    return nValid

def b(lines):
    nValid = 0
    passport = {}
    for line in lines:
        line = line.strip()
        if not line:
            nValid += 1 * validPassport(passport)
            passport.clear()
            continue
        fields = line.split()
        for field in fields:
            kv = field.split(":")
            passport[kv[0]] = kv[1]
    # check last passport
    nValid += 1 * validPassport(passport)
    return nValid

def validPassport(passport):
    return (len(passport) == 8 or "cid" not in passport and len(passport) == 7) and \
           validRange(int(passport["byr"]), 1920, 2002) and \
           validRange(int(passport["iyr"]), 2010, 2020) and \
           validRange(int(passport["eyr"]), 2020, 2030) and \
           validHgt(passport["hgt"]) and \
           validHcl(passport["hcl"]) and \
           validEcl(passport["ecl"]) and \
           validPid(passport["pid"])

def validRange(x, lo, hi):
    return x >= lo and x <= hi

def validHgt(hgt):
    return hgt[-2:] == "cm" and validRange(int(hgt[:-2]), 150, 193) or \
           hgt[-2:] == "in" and validRange(int(hgt[:-2]), 59, 76)

def validHcl(hcl):
    return bool(re.match(r"^#[0-9a-f]{6}$", hcl))

def validEcl(ecl):
    return ecl in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

def validPid(pid):
    return bool(re.match(r"^[0-9]{9}$", pid))

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.readlines()
    print(b(lines))
