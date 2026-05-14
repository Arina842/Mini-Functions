
a=np.array([1,3,4,5,6,7,8])

# вывод обычного массива
print(f"a=[{', '.join(map(str,a[:10]))}]")

# вывод numpy массива
print(f"a=np.array([{', '.join(map(str, a[:10]))}])")
