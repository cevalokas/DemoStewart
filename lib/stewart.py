from vpython import *
import numpy as np
from scipy.spatial.transform import Rotation as R
from math import *

class Kinematics:
	def __init__(self, 		   #Parameters needed for kinematics
				 r: np.float64, #Radius of inscribed circle in inner triangle
				 s: np.float64, #Radius of inscribed circle in outer triangle
				 d: np.float64, #Rod length
				 h: np.float64, #Servo Horn Length 
				 ):
		self.r = r
		self.s = s
		self.origin = vec(0,0,0)
		self.T0 = np.array([0,0,0])# Home position translation from base to plate origin
		self.pk = np.zeros((6,3))# Corners of the plate in plate's frame
		self.Pk_solved = np.zeros((6,3))# Corners of the plate in the base frame with desired pose
		self.bk = np.zeros((6,3))# Points of servo axis
		self.beta_k = np.zeros(6)# Angles of the servo horns in XY plane
		self.alpha_k = np.zeros(6)# Angles of the servo axis
		self.T = np.zeros(3)
		self.Rot = R.from_euler('x', 0, degrees=True)
		self.a = (2*self.r-self.s)/sqrt(3) #Side of the pyramidion
		self.d = d # Length of the rods
		self.h = h# Length of servo horns
		self.lk = np.array((6,3))# Vector from bk to ek in base frame
		self.calculateInitialPlatePoints()
		self.calculateServoAxisPoints()
		self.calculateBetaK()
		self.lineUpIndices()
		self.calculateZ0()
		self.solveIK(np.array([0,0,0]), self.Rot)

	def calculateInitialPlatePoints(self):
		for i,e in enumerate(self.pk):
			k = i+1
			ang = 2*pi/3*(k)/2
			self.pk[i,0] = self.s*cos(ang)+self.a/2*((-1)**k)*sin(ang)
			self.pk[i,1] = self.s*sin(ang)+self.a/2*((-1)**k)*-cos(ang)
			self.pk[i,2] = 0

	def calculateZ0(self):
		self.T0[2] = sqrt(d**2 + h**2 - (self.pk[0,0] - self.bk[0,0])**2 - (self.pk[0,1] - self.bk[0,1])**2)

	def calculateServoAxisPoints(self):
		for i,e in enumerate(self.bk):
			k = i+1
			ang = 2*pi/3*(k)/2 + pi/3
			self.bk[i,0] = (self.s+10)*cos(ang)+self.a/4*((-1)**k)*sin(ang)
			self.bk[i,1] = (self.s+10)*sin(ang)+self.a/4*((-1)**k)*-cos(ang)

	def calculateBetaK(self):
		i=0
		while i < len(self.bk):
			curr_idx = i % len(self.bk)
			next_idx = (i+1) % len(self.bk)
			v_side = self.pk[next_idx] - self.pk[curr_idx]
			self.beta_k[i] = atan2(v_side[1], v_side[0])+pi/3
			self.beta_k[i+1] = atan2(-v_side[1], -v_side[0])+pi/3
			i += 2
		# print("Initial Beta K")
		# print(self.beta_k)
		# print("Initial bk")
		# print(self.bk)
		# print("")

	def lineUpIndices(self):
		temp_bk = np.copy(self.bk)
		temp_beta_k = np.copy(self.beta_k)
		for i in range(len(self.bk)):
			idx = (i+1) % len(self.bk)
			self.bk[idx] = temp_bk[i]
			self.beta_k[idx] = temp_beta_k[i]
		# print("Corrected Indices Beta K")
		# print(self.beta_k)
		# print("Corrected Indices bk")
		# print(self.bk)
		# print("")


	def solveIK(self, T_rel, rot):
		T_prev = np.copy(self.T)
		Rot_prev = np.copy(self.Rot)
		Pk_solved_prev = np.copy(self.Pk_solved)
		self.T = self.T0 + T_rel
		self.Rot = rot
		self.lk = np.tile(self.T, (6,1)) + self.Rot.apply(self.pk) - self.bk
		self.Pk_solved = np.tile(self.T, (6,1)) + self.Rot.apply(self.pk)
		# print("Kinematics: lk")
		# print(self.lk)
		self.e_k = 2*self.h*self.lk[:,2] # shape is 6
		# print("Kinematics: e_k")
		# print(self.e_k)
		self.fk = 2*self.h*(np.cos(self.beta_k)*self.lk[:,0] + np.sin(self.beta_k)*self.lk[:,1])
		# print("Kinematics: f_k")
		# print(self.fk)
		self.gk = np.linalg.norm(self.lk, axis=1)**2 - (self.d**2 - self.h**2)
		# print("Kinematics: g_k")
		# print(self.gk)
		# print("Input to Arcsin")
		# print(self.gk/np.sqrt(self.e_k**2 + self.fk**2))
		try:
			self.alpha_k = np.arcsin(self.gk/np.sqrt(self.e_k**2 + self.fk**2)) - np.arctan2(self.fk, self.e_k)
			successful = True
		except:
			print("Kinematically unfeasible")
			self.T = T_prev
			self.Rot = Rot_prev
			self.Pk_solved = Pk_solved_prev
			successful = False

		return successful
		# print("Kinematics: Alpha K")
		# print(self.alpha_k)
		#Solve inverse kinematics, solves for alpha k

if __name__ == "__main__":
	ro = 60
	ri = 50
	d = 50
	h = 10
	np.seterr(all='raise')
	kine = Kinematics(ri, ro, d, h)
	T = np.array([0,0,0])
	r = R.from_euler('x', 0, degrees=True)
	print("T0")
	print(kine.T0)
	print("T")
	print(T)
	print("R")
	print(r.as_euler('xyz'))
	x_rot=0
	y_rot=0
	z_rot=0
	x=0
	y=0
	z=0
	x_rot_prev=0
	y_rot_prev=0
	z_rot_prev=0
	x_prev=0
	y_prev=0
	z_prev=0
	dpos = 0.1
	drot = 0.1
	dlength = 0.1
	increment = True
	decrement = False