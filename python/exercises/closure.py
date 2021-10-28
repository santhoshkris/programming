
# def outer(tag):
#     def inner(msg):
#         print("<"+tag+">"+msg+"</"+tag+">")
#     return inner

# p = outer("p")
# q = outer("a")
# p("hello")
# q("how")
# p("wonderful")
# q("howisit")
#

def incrementor(num):
    info = {"count": num}
    def number():
        info["count"] += 1
        return info["count"]
    return number

counter100 = incrementor(100)
print(counter100())
print(counter100())
