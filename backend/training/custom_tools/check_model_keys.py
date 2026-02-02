import paddle

# Load the parameters
states = paddle.load("./output/rec_ppv5_vi_server/best_model/best_model.pdparams")

# Print the first 10 keys to see the structure
print("Model Structure Keys:")
for i, key in enumerate(states.keys()):
    if i < 10:
        print(key)