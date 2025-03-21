from datasets import load_dataset
import matplotlib.pyplot as plt
import numpy as np



dataset = load_dataset("0x365/stable-orbits", split="part_00000")


print(dataset)
# for i in iter(dataset):
#     print(i)



# plt.savefig("test.png")

# plt.clf()