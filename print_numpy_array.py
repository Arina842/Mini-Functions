
a=np.array([1,3,4,5,6,7,8])

# вывод обычного массива
print('a=[')
print(', '.join(map(str, a)))
print(']')

# вывод numpy массива
print('a=np.array([')
print(', '.join(map(str, a)))
print('])')
