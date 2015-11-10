import random

def cross(a, b):
	cross_point = random.randint(0, len(a)-1)
	#TODO should this return one or two children? as in, should it return just one kid or that kid and it's inverse
	x = a[:cross_point] + b[cross_point:]
	y = b[:cross_point] + a[cross_point:]
	return (x,y)

'''/**
	 * Crosses a and b at a randomly selected crossover point.
	 * 
	 * @param a
	 * @param b
	 * @return
	 */
	public static String cross(String a, String b) {
		int crossoverPoint = (int) (Math.random() * a.length());
		return a.substring(0, crossoverPoint)
				+ b.substring(crossoverPoint, b.length());
	}

	/**
	 * Flips each bit in the string with the give probability.
	 * 
	 * @param individual
	 * @param rate
	 * @return
	 */
	public static String mutate(String individual, double rate) {
		String result = "";
		for (int i = 0; i < individual.length(); i++) {
			if (Math.random() <= rate) {
				if (individual.charAt(i) == '0') {
					result += "1";
				} else {
					result += "0";
				}
			} else {
				result += individual.charAt(i);
			}
		}
		return result;
	}

	/**
	 * Generates a random string of the given length.
	 * 
	 * @param length
	 * @return
	 */
	public static String random(int length) {
		String result = "";
		for (int i = 0; i < length; i++) {
			if (Math.random() <= .5) {
				result += "1";
			} else {
				result += "0";
			}
		}
		return result;
	}

}'''
