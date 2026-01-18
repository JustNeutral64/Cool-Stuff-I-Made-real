rows, cols = (5, 5)
arr = [[0]*cols]*rows
print(arr, "before")

arr[0][0] = 1 # update only one element
print(arr, "after")