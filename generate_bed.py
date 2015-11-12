import tools
import matplotlib.pyplot as mp

nodes = 58s

def generate_bed(parameters):
	return np.zeros(58)


def main():
	test = generate_bed(parameters)
	real = tools.load_nolan_bedrock()
	mp.plot(range(58), real, 'green')
	mp.plot(range(58), test, 'red')



if __name__=='__main__':
    main()