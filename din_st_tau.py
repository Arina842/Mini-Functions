import numpy as np
def din_st_tau(num,c,fi_degrees,sigma_3,u_ex):
    print()
    print('for',num)
    c = c
    fi_degrees = fi_degrees  #  Градусы
    sigma_3 = sigma_3 # КПА
    sigma_3_MPA = sigma_3/1000 # MПА
    u_ex = u_ex # МПА

    # Преобразуем градусы в радианы
    fi_radians = np.radians(fi_degrees)

    # Вычисляем выражение, используя радианы
    result_din= c+(sigma_3_MPA-u_ex)*np.tan(fi_radians)
    result_st= c+sigma_3_MPA*np.tan(fi_radians)

    print('st', round(result_st, 3))
    print('din', round(result_din, 3))

#Примеры
din_st_tau(num=102,c = 0.003,fi_degrees = 32 ,sigma_3 = 62 ,u_ex = 0.036)
din_st_tau(num=99,c = 0.002,fi_degrees = 39 ,sigma_3 = 30,u_ex = 0.02)
din_st_tau(num=56,c = 0.05, fi_degrees = 42, sigma_3 = 42, u_ex = 0.028)
din_st_tau(num=66, c = 0.009, fi_degrees = 40, sigma_3 = 10, u_ex=0.092)
