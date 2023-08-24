
def particion(arr, ini, final):
    pivote = arr[final]
    i = ini-1
    for j in range(ini, final):
        if(arr[j] <= pivote):
            i=i+1
            (arr[i],arr[j]) = (arr[j],arr[i])
            
    (arr[i+1], arr[final]) = (arr[final], arr[i+1])
    return i + 1
    
def quickSort(arr, ini, final):
    if(ini < final):
        pivote = particion(arr, ini, final)
        quickSort(arr, ini, pivote-1)
        quickSort(arr, pivote+1, final)

def main():
    import random
    arr = []
    for i in range(10000):
        arr.append(random.randint(1,100))
    lenArr = len(arr)
    quickSort(arr, 0, lenArr - 1)
main()
