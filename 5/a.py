def a(lines):
    hi = 0
    for line in lines:
        (_, _, seat) = seatId(line)
        hi = seat if seat > hi else hi
    return hi

def seatId(line):
    row = 0
    col = 0
    for i in range(7):
        if line[i] == "B":
            row += 2**(7-1-i)
    for i in range(3):
        if line[7+i] == "R":
            col += 2**(3-1-i)
    return (row, col, row * 8 + col)

def b(lines):
    rowLo = 127
    rowLoSeats = []
    rowHi = 0
    rowHiSeats = []
    seatSum = 0
    for line in lines:
        (row, _, seat) = seatId(line)
        seatSum += seat
        if row < rowLo:
            rowLo = row
            rowLoSeats = [seat]
        elif row == rowLo:
            rowLoSeats.append(seat)
        elif row > rowHi:
            rowHi = row
            rowHiSeats = [seat]
        elif row == rowHi:
            rowHiSeats.append(seat)
    print(rowLo, rowHi)
    print(rowLoSeats)
    print(rowHiSeats)
    return sum(range((rowLo+1)*8, rowHi*8)) - (seatSum - sum(rowLoSeats) - sum(rowHiSeats))

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.readlines()
    print(b(lines))
