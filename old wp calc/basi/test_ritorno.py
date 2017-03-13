def f(in_str):
    out_str = in_str.upper()
    return True, out_str # Creates tuple automatically

succeeded, b = f("a") # Automatic tuple unpacking

print b

