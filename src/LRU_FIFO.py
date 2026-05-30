from collections import deque
from random import randrange
class LRU:
	def __init__(self, n, p):
		self.n=n
		self.p=p
		self.f=0
		self.h=0
		self.pj=0.0
		self.r=0.0
		self.s=""
		self.mp={}
		self.build()
		self.iniz()
		self.debug()
	def build(self):
		aux=0;
		for i in range(0,self.n):
			aux=randrange(0,10)
			self.s+=str(aux)
	def iniz(self):
		for i in range(0,self.n):
			print(self.s[i])
			for key,val in self.mp.items():
				self.mp[key]+=1
			if self.s[i] not in self.mp and	len(self.mp)==self.p:
				ind="0"
				it=-1
				for key,val in self.mp.items():
					if val>=it:
						it=val
						ind=key
				if ind in self.mp:
					del self.mp[ind]
				self.f+=1;
			else:
				self.h+=1;
			self.mp[self.s[i]]=0
			for key,val in self.mp.items():
				print(key," ",val)
		self.r=self.f/self.p
		self.pg=(self.h*100.0)/self.n
	def debug(self):
		print("LRU")
		print(self.s)
		print("nivel de fallos de pagina ",self.r)
		print("porcentaje ",self.pg)
		print("numero de fallos ",self.f)
		print("hits ",self.h)
lru=LRU(10,4)
class FIFO:
	def __init__(self, n, p):
		self.n=n
		self.p=p
		self.f=0
		self.h=0
		self.pj=0.0
		self.r=0.0
		self.s=""
		self.q=deque([])
		self.st={}
		self.build()
		self.iniz()
		self.debug()
	def build(self):
		aux=0;
		for i in range(0,self.n):
			aux=randrange(0,10)
			self.s+=str(aux)
	def iniz(self):
		for i in range(0,self.n):
			print(self.s[i])
			if self.s[i] not in self.st and	len(self.st)==self.p:
				if(len(self.q)>=1):
					del self.st[self.q[0]]
					self.q.popleft()
				self.f+=1
			else:
				self.h+=1
			if self.s[i] not in self.st:
				self.q.append(self.s[i])
			self.st[self.s[i]]=0
			for i in range(0,len(self.q)):
				print(self.q[i],end=" ")
			print();
		self.r=self.f/self.p
		self.pg=(self.h*100.0)/self.n
	def debug(self):
		print("FIFO")
		print(self.s)
		print("nivel de fallos de pagina ",self.r)
		print("porcentaje ",self.pg)
		print("numero de fallos ",self.f)
		print("hits ",self.h)
fifo=FIFO(10,4)
