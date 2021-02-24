import numpy as np

x = np.eye(3)

print(x)
print(x.shape)
y = x[0,:]
z = np.reshape(y,(1,3))
print(y)
print(z)
print(y.shape)
y_t = np.transpose(y)
print("y_t: ",y_t)
print(z.shape)
z_t = np.transpose(z)
print("z_t: ",z_t)
print(len(y))