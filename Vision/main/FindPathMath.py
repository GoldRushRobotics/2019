'''

Math behind the path finding.

'''
import math

Const = 1.0

def findTurn(x, y, maxY, maxX, objgrav):
	halfX = .5*maxX

	if (x < halfX):
		xsqr = -((x-halfX)/halfX *(x-halfX)/halfX)
	else:
		xsqr = (x-halfX)/halfX * (x-halfX)/halfX

	ysqr = y/maxY * y/maxY

	turn = xsqr * ysqr * objgrav * Const

	return turn


def findPow(turn):
	bpow = (1-(turn*turn)**.5
	#theta = math.asin(turn)
	theta = (turn + (1/6 * turn**3) + (3/40 * turn**5) + (15/336 * turn**7)) * 180/math.pi #approximation of arcsin(runs quicker) probably?
	return (bpow*255, theta)
