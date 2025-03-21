# dataset_new = []
# dataset_res = []

# scaler = StandardScaler()
# # dataset = np.load("n_body_ml/data-np/-0.9_0.6.npy")
# # dataset[:,1:] = scaler.fit_transform(dataset[:,1:])

# total_num = 5
# for i in tqdm(range(-total_num, total_num)):
#   for j in range(-total_num, total_num):
#     v1 = 1.5 * i / total_num
#     v2 = 1.5 * j / total_num

#     try:
#       dataset = np.load("n_body_ml/data-np/"+str(v1)+"_"+str(v2)+".npy")
#     except:
#       continue
#     dataset = np.array(dataset, dtype=float)

#     how_much = 1000
#     dataset = dataset[:how_much]

#     dataset[:,0] = np.linspace(0,1,1000)[:how_much]
#     # dataset[:,1:] = scaler.transform(dataset[:,1:])

#     for i in range(len(dataset)):
#         for j in range(i+1,len(dataset)):
#               if np.amax(np.abs(dataset[j,1:])) <= 4:
#                 dataset_new.append([*dataset[i,1:], dataset[j,0]-dataset[i,0]])

#                 dataset_res.append(dataset[j,1:])



# dataset_new = np.array(dataset_new)
# dataset_res = np.array(dataset_res)

# print(np.shape(dataset_new))

# dataset_new[:,:-1] = scaler.fit_transform(dataset_new[:,:-1])
# dataset_res = scaler.transform(dataset_res)

# data_x = torch.tensor(dataset_new.tolist(), dtype=torch.float32)
# data_y = torch.tensor(dataset_res.tolist(), dtype=torch.float32)
# # sklearn.MinMaxScalar

# x_train, x_valid, y_train, y_valid = train_test_split(data_x, data_y, test_size=0.2, shuffle=True)

# print('x_train:', x_train.shape)
# print('y_train:', y_train.shape)
# print('x_valid:', x_valid.shape)
# print('y_valid:', y_valid.shape)










# def run_infer(scaler, model_data=None):
#   dataset = np.load("n_body_ml/test-data/-0.9_0.6.npy")
#   dataset = np.array(dataset, dtype=float)
#   dataset = dataset[:4000]
#   dataset_saver = dataset.copy()

#   dataset_0 = scaler.transform([dataset[0,1:]])

#   dataset_new = []
#   dataset_res = []
#   # for i in range(1,len(dataset)):
#   for i in np.linspace(0,4,8000):
#       dataset_new.append([*dataset_0[0], i])

#   dataset_new = np.array(dataset_new)
#   example_input = torch.tensor(dataset_new, dtype=torch.float32)

#   # Load the entire model (architecture + state)
#   if model_data == None:
#     model = torch.load('test.pth')
#   else:
#     model = model_data

#   # Set the model to evaluation mode before inference
#   model.eval()

#   device = 'cuda' if torch.cuda.is_available() else 'cpu'


#   all_pred = []
#   with torch.inference_mode():
#         example_input = example_input.to(device)
#         prediction = model(example_input)
#         predicted_values = prediction.detach().cpu().numpy()

#   all_pred = np.array(predicted_values)
#   all_pred = scaler.inverse_transform(all_pred)

#   return all_pred, dataset_saver















# epoch_count, train_loss_values, valid_loss_values = [], [], []

# last_loss = np.inf
# for epoch in range(epochs):

#     # Put the model in training mode
#     model.train()

#     y_pred = model(x_train) # forward pass to get predictions; squeeze the logits into the same shape as the labels
#     # print(y_logits)
#     # y_pred = (y_logits) # convert logits into prediction probabilities

#     loss = loss_fn(y_pred, y_train) # compute the loss
#     acc = accuracy_fn(y_train, y_pred)

#     optimizer.zero_grad() # reset the gradients so they don't accumulate each iteration
#     loss.backward() # backward pass: backpropagate the prediction loss
#     optimizer.step() # gradient descent: adjust the parameters by the gradients collected in the backward pass



#     if epoch % int(epochs / 50) == 0 and epoch != 0:
#         model.eval()

#         with torch.inference_mode():
#             valid_pred = model(x_valid)

#             valid_loss = loss_fn(valid_pred, y_valid)
#             valid_acc = accuracy_fn(y_valid, valid_pred)



#         epoch_count.append(epoch)
#         train_loss_values.append(loss.detach().cpu().numpy())
#         valid_loss_values.append(valid_loss.detach().cpu().numpy())

#         if valid_loss < last_loss:
#             torch.save(model, 'test.pth')
#             last_loss = valid_loss
#             all_pred, dataset_saver = run_infer(scaler, model)


#         display.display(plt.gcf())
#         display.clear_output(wait=True)

#         print(f'Epoch: {epoch:4.0f} | Train Loss: {loss:.5f}, MSE: {acc:.2f}% | Validation Loss: {valid_loss:.5f}, MSE: {valid_acc:.2f}%')



#         splitter = 2000

#         plt.plot(dataset_saver[1:,1], dataset_saver[1:,2], c="black")
#         plt.plot(dataset_saver[1:,3], dataset_saver[1:,4], c="black")
#         plt.plot(dataset_saver[1:,5], dataset_saver[1:,6], c="black")


#         plt.plot(all_pred[:splitter,0], all_pred[:splitter,1], c="green")
#         plt.plot(all_pred[:splitter,2], all_pred[:splitter,3], c="green")
#         plt.plot(all_pred[:splitter,4], all_pred[:splitter,5], c="green")
#         print(len(all_pred))

#         plt.plot(all_pred[splitter:,0], all_pred[splitter:,1], c="red")
#         plt.plot(all_pred[splitter:,2], all_pred[splitter:,3], c="red")
#         plt.plot(all_pred[splitter:,4], all_pred[splitter:,5], c="red")


#         # for i in range(5):
#         #     print("Pred:", all_pred[i,:6])
#         #     print("Real:", dataset_saver[1+i,1:7])
#         #     print()

#         plt.gca().axis('equal')
#         # plt.plot(train_loss_values, c="blue")
#         # plt.plot(valid_loss_values, c="green")
#         # plt.yscale("log")

#         plt.show()
#         # plt.savefig("loss.png")
#         # plt.clf()

# if valid_loss < last_loss:
#     torch.save(model, 'test.pth')
#     last_loss = valid_loss












# def run_infer_jump(scaler, model_data=None):
#   dataset = np.load("n_body_ml/test-data/-0.9_0.6.npy")
#   dataset = np.array(dataset, dtype=float)
#   dataset = dataset[:8000]
#   dataset_saver = dataset.copy()

#   initial = []
#   initial.append(dataset[0,1:].copy())

#   # scaler = StandardScaler()
#   dataset_0 = scaler.transform([dataset[0,1:]])


#   dataset_new = []
#   dataset_new.append([*dataset_0[0], 0.1])

#   dataset_new = np.array(dataset_new)
#   example_input = torch.tensor(dataset_new, dtype=torch.float32)

#   # Load the entire model (architecture + state)
#   if model_data == None:
#     model = torch.load('test.pth')
#   else:
#     model = model_data

#   # Set the model to evaluation mode before inference
#   model.eval()

#   device = 'cuda' if torch.cuda.is_available() else 'cpu'


#   all_pred = []
#   with torch.inference_mode():
#         example_input = example_input.to(device)
#         prediction = model(example_input)
#         predicted_values = prediction.detach().cpu().numpy()

#   all_pred = np.array(predicted_values)
#   all_pred = scaler.inverse_transform(all_pred)
#   initial.append(np.array(all_pred[0]).copy())

#   # Extra steps
#   for i in range(5):

#     # Step 2
#     dataset_0 = np.array(predicted_values)

#     dataset_new = []

#     dataset_new.append([*dataset_0[0], 0.1])

#     dataset_new = np.array(dataset_new)
#     example_input = torch.tensor(dataset_new, dtype=torch.float32)

#     # Load the entire model (architecture + state)
#     if model_data == None:
#       model = torch.load('test.pth')
#     else:
#       model = model_data

#     # Set the model to evaluation mode before inference
#     model.eval()

#     device = 'cuda' if torch.cuda.is_available() else 'cpu'


#     all_pred = []
#     with torch.inference_mode():
#           example_input = example_input.to(device)
#           prediction = model(example_input)
#           predicted_values = prediction.detach().cpu().numpy()

#     all_pred = np.array(predicted_values)
#     all_pred = scaler.inverse_transform(all_pred)
#     initial.append(np.array(all_pred[0]).copy())

#   return np.array(initial), dataset_saver

















# epoch_count, train_loss_values, valid_loss_values = [], [], []

# last_loss = np.inf
# for epoch in range(epochs):

#     # Put the model in training mode
#     model.train()

#     y_pred = model(x_train) # forward pass to get predictions; squeeze the logits into the same shape as the labels
#     # print(y_logits)
#     # y_pred = (y_logits) # convert logits into prediction probabilities

#     loss = loss_fn(y_pred, y_train) # compute the loss
#     acc = accuracy_fn(y_train, y_pred)

#     optimizer.zero_grad() # reset the gradients so they don't accumulate each iteration
#     loss.backward() # backward pass: backpropagate the prediction loss
#     optimizer.step() # gradient descent: adjust the parameters by the gradients collected in the backward pass



#     if epoch % int(epochs / 50) == 0 and epoch != 0:
#         model.eval()

#         with torch.inference_mode():
#             valid_pred = model(x_valid)

#             valid_loss = loss_fn(valid_pred, y_valid)
#             valid_acc = accuracy_fn(y_valid, valid_pred)



#         epoch_count.append(epoch)
#         train_loss_values.append(loss.detach().cpu().numpy())
#         valid_loss_values.append(valid_loss.detach().cpu().numpy())

#         if valid_loss < last_loss:
#             torch.save(model, 'test.pth')
#             last_loss = valid_loss

#             display.display(plt.gcf())
#             display.clear_output(wait=True)

#             all_pred, dataset_saver = run_infer_jump(scaler, model)

#             splitter = 2000

#             plt.plot(dataset_saver[1:,1], dataset_saver[1:,2], c="black")
#             plt.plot(dataset_saver[1:,3], dataset_saver[1:,4], c="black")
#             plt.plot(dataset_saver[1:,5], dataset_saver[1:,6], c="black")

#             # print(all_pred)
#             plt.scatter(all_pred[:,0], all_pred[:,1], c="blue")
#             plt.scatter(all_pred[:,2], all_pred[:,3], c="green")
#             plt.scatter(all_pred[:,4], all_pred[:,5], c="purple")

#             plt.gca().axis('equal')

#             # print(np.around(all_pred[:,:6]))

#             plt.show()

#         print(f'Epoch: {epoch:4.0f} | Train Loss: {loss:.5f}, MSE: {acc:.2f}% | Validation Loss: {valid_loss:.5f}, MSE: {valid_acc:.2f}%')





# if valid_loss < last_loss:
#     torch.save(model, 'test.pth')
#     last_loss = valid_loss