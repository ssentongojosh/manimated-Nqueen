x = []

def function(N,r):
    if r == N:
        print(f"value of r : {r}")
        print(f"returning from function({N},{r})\n This is time {r}")
        return
    for i in range(N):
        print(f"{i = }")
        if i in x:
            print(x)
            print("preparing to continue...")
            continue
        print(f"adding {i = } to set x")
        x.append(i)
        print(f"set x is now {x}")
        print(f"recursively calling function({N},{r + 1})\nThis is time {r + 1 } of calling function")
        function(N,r + 1)
        print(f"removing {i = } from set x")
        print(F'value of r after return : {r}')
        x.remove(i)
        print(f"set x is now {x}")
print(f"calling function(3,0)")
function(4,0)
print("returned from function(5,0)")
