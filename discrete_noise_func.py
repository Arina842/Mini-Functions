    @staticmethod
    def discrete_noise_func(len, discrete_step):
        size = len
        random_numbers = np.random.rand(size)

        # Преобразование в дискретный шум (0 или 1)
        discrete_noise = np.where(random_numbers < 0.5, 0, discrete_step)
        return discrete_noise
