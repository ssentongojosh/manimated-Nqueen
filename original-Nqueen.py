threatened_columns_set = set()
threatened_negative_diagonals_set = set()
threatened_positive_diagonals_set = set()

N = 8

result = []

x = [["."] * N for i in range(N) ]

def print_board():
    y = result
    for sub_list in y:
        print("\n")
        for group in sub_list:
            print("\n")
            for item in group:
                print(item,end="    ")

def solution(N,row):
    if row == N:
        copy = ["".join(row) for row in x]
        result.append(copy)
        return 
    
    for column in range(N):
        if column in threatened_columns_set or (row - column) in threatened_negative_diagonals_set or (row + column) in threatened_positive_diagonals_set:
            continue
        x[row][column] = "Q"
        threatened_columns_set.add(column)
        threatened_negative_diagonals_set.add(row - column)
        threatened_positive_diagonals_set.add(row + column)
        solution(N,row + 1)
        threatened_columns_set.remove(column)
        threatened_negative_diagonals_set.remove(row - column)
        threatened_positive_diagonals_set.remove(row + column)
        x[row][column] = "."


solution(8,0)


print_board()
print(f"\n\nnumber of arrangements = {len(result)}")


