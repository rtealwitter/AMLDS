import numpy as np

def readfile(filename="code/UScities.txt"):
    names = []
    D = []
    with open(filename, "r") as f:
        for line in f:
            lstrow = line.replace("\n", "").split(sep=" ")
            for j in range(len(lstrow)):
                if lstrow[j].isnumeric():
                    break
            if j == 1:
                names += [lstrow[0]]
            else:
                names += [" ".join(lstrow[:2])]
            D += [[np.float64(dist)**2 for dist in lstrow[j:]]]
    return names, np.matrix(D)

def norms(D):
    n=len(D)
    rowsums = D.sum(axis=0)
    normlst = []
    for i in range(n):
        total = 0
        for k in range(n):
            total += D[i,k] + (rowsums[0,i]-rowsums[0,k])/n
        normlst += [total/(2* n)]
    return normlst

def crossmatrix(D):
    n=len(D)
    normlst = norms(D)
    G = []
    for i in range(n):
        row = []
        for j in range(n):
            row += [(normlst[i]+normlst[j]-D[i,j])/2]
        G += [row[:]]
    return np.matrix(G)

names, D = readfile()
normlst = norms(D)
print(D.sum()/(2*len(D)))
print(sum(normlst))

G = crossmatrix(D)
u, s, vh = np.linalg.svd(G, full_matrices=True)
w, v = np.linalg.eig(G)
print(s)
print(w)

