import matplotlib.pyplot as plt
import sys

#Lcolors, markers, and line styles definition
lines=[
"s-k",
"^--k",
"+-.k",
"x:k",
"o--k",
]

input_file=sys.argv[1]
f=open(input_file)

title=f.readline().strip()

labels=[i.strip() for i in f.readline().split("	")]
labels.pop(0)

data=[[float(j) for j in i.split("	")] for i in f]
#Transpose the matrix
data=list(zip(*data))

x_axis=data.pop(0)
x_axis=[int(i) for i in x_axis]

plt.figure(figsize=(18, 9), dpi=400)

plt.ylabel('Time log scale (sec)', fontsize=16, labelpad=15)
plt.xlabel('Input size log scale', fontsize=16, labelpad=15)

for i in range(len(labels)):
	plt.plot(x_axis, data[i], lines[i], fillstyle="none", markersize=8, linewidth=0.8, label=labels[i])

plt.yscale("log")
plt.xscale("log")

#Removing automatic ticks and labels
plt.tick_params(axis='x', which='minor', bottom=False, labelbottom=False)
plt.tick_params(axis='both', labelsize=14)

#Custom ticks and labels
plt.xticks(x_axis, [str(i) for i in x_axis])

plt.legend(prop={"size":20})

plt.title(title, pad=20, fontdict={"fontsize":20})

plt.savefig(input_file)

#plt.show()
