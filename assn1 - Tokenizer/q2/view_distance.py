def distance(target, source, insertcost, deletecost, replacecost):
    n = len(target) + 1
    m = len(source) + 1
    # set up dist and initialize values
    dist = [[0 for j in range(m)] for i in range(n)]
    for i in range(1, n):
        dist[i][0] = dist[i-1][0] + insertcost
    for j in range(1,m):
        dist[0][j] = dist[0][j-1] + deletecost
    # align source and target strings
    for j in range(1,m):
        for i in range(1,n):
            inscost = insertcost + dist[i - 1][j]
            delcost = deletecost + dist[i][j - 1]
            if (source[j - 1] == target[i - 1]): add = 0
            else: add = replacecost
            substcost = add + dist[i - 1][j - 1]
            dist[i][j] = min(inscost, delcost, substcost)
# return min edit distance
    return dist[n - 1][m - 1]


def generatearray(target, source):
    partialsource = []
    partialtarget = []
    si = 1
    ti = 1
    array1 = []
    array2 = []
    array1.append(range(0, len(target)+1))
    for sletter in source:
        partialsource.append(sletter)
        array2.append(ti)
        for tletter in target:
            partialtarget.append(tletter)
            array2.append(distance((''.join(partialtarget)), (''.join(partialsource)), 1, 1, 2))
        array1.append(array2)
        array2 = []
        partialtarget = []
        ti += 1
    return array1


def plot(target, source, inarray):
    row = len(source)
    column = len(target)
    changelog = []
    chart = [(row,column)]
    while True:
        if row == 0:
            if column == 0:
                break
            else:
                chart.insert(0, (row, column-1))
                changelog.insert(0, "insert")
                column -= 1
        elif column == 0:
            chart.insert(0, (row-1,column))
            changelog.insert(0, "delete")
            row -= 1

        elif source[row-1] == target[column-1]:
            if (inarray[row][column-1] + 1) <= (inarray[row-1][column] + 1):
                if (inarray[row][column-1] + 1) < inarray[row-1][column-1]:
                    chart.insert(0, (row,column-1))
                    changelog.insert(0, "insert")
                    column -= 1
                else:
                    chart.insert(0, (row-1,column-1))
                    changelog.insert(0, "no change")
                    row -= 1
                    column -= 1
            else:
                    chart.insert(0, (row-1,column))
                    changelog.insert(0, "delete")
                    row -= 1
        else:
            if (inarray[row][column-1] + 1) <= (inarray[row-1][column] + 1):
                if (inarray[row][column-1] + 1) < (inarray[row-1][column-1] + 2):
                    chart.insert(0, (row,column-1))
                    changelog.insert(0, "insert")
                    column -= 1
                else:
                    chart.insert(0, (row-1,column-1))
                    changelog.insert(0, "substitution")
                    row -= 1
                    column -= 1
            else:
                    chart.insert(0, (row-1,column))
                    changelog.insert(0, "delete")
                    row -= 1
    return changelog


def output(target, source, key):
    tartracker = 0
    srctracker = 0
    prettyprintarray = []
    print(distance(target, source, 1, 1, 2))
    for operator in key:
        if operator == "insert":
            prettyprintarray.append("_ ")
        else:
            prettyprintarray.append("{0} ".format(str(source[srctracker])))
            srctracker += 1
    print("{0}\n".format(''.join(prettyprintarray)))
    prettyprintarray = []
    for operator in key:
        if operator == "no change":
            prettyprintarray.append("| ")
        else:
            prettyprintarray.append("  ")
    print("{0}\n".format(''.join(prettyprintarray)))
    prettyprintarray = []
    for operator in key:
        if operator == "delete":
            prettyprintarray.append("_ ")
        else:
            prettyprintarray.append("{0} ".format(str(target[tartracker])))
            tartracker += 1
    print("{0}\n".format(''.join(prettyprintarray)))
    return

def view_distance(source, target):
    alignmentarray = generatearray(target, source)
    map=plot(target, source, alignmentarray)
    output(target, source, map)
    return


if __name__=="__main__":
    from sys import argv
    if len(argv) > 2:
        print "levenshtein distance =", view_distance(argv[1], argv[2])