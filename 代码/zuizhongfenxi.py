from PIL import Image, ImageFilter
import tensorflow as tf
import os
from array import array
def imageprepare(file_name):
    """
    This function returns the pixel values.
    The imput is a png file location.
    """
    #file_name='image/vpn_youtube.pcap._10-8-8-138__131-202-244-3_.png'#导入自己的图片地址
    #in terminal 'mogrify -format png *.jpg' convert jpg to png
    tv = array('B')
    Im = Image.open(file_name)
    pixel = Im.load()
    width, height = Im.size
    for x in range(0, width):
        for y in range(0, height):
            tv.append(pixel[x, y])
    #im = Image.open(file_name).convert('L')
    #tv = list(im.getdata()) #get pixel values

    #normalize pixels to 0 and 1. 0 is pure white, 1 is pure black.



    #print(tva)
    return tv
NUM = 2
num0 = 0
num1 = 0
for file in os.listdir('image'):
    result = imageprepare('image'+ '/'+ str(file))
    tf.reset_default_graph()
    CLASS_NUM = NUM
    x = tf.placeholder("float", [None, 784])
    y_ = tf.placeholder("float", [None, NUM])


    def find_element_in_list(element, list_element):
        try:
            index_element = list_element.index(element)
            return index_element
        except ValueError:
            return -1


    # weight initialization
    def weight_variable(shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)


    def bias_variable(shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)


    # convolution
    def conv2d(x, W):
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


    # pooling
    def max_pool_2x2(x):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


    # Create the model
    # placeholder
    x = tf.placeholder("float", [None, 784])
    y_ = tf.placeholder("float", [None, CLASS_NUM])

    # first convolutinal layer
    w_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])

    x_image = tf.reshape(x, [-1, 28, 28, 1])

    h_conv1 = tf.nn.relu(conv2d(x_image, w_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    # second convolutional layer
    w_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])

    h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    # densely connected layer
    w_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1) + b_fc1)

    # dropout
    keep_prob = tf.placeholder("float")
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # readout layer
    w_fc2 = weight_variable([1024, CLASS_NUM])
    b_fc2 = bias_variable([CLASS_NUM])

    y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, w_fc2) + b_fc2)

    init_op = tf.global_variables_initializer()
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(init_op)
        saver.restore(sess, "/home/sqWang/liuliang/model_2class_liuliang/model_2class_liuliang.ckpt")  # 这里使用了之前保存的模型参数
        # print ("Model restored.")

        prediction = tf.argmax(y_conv, 1)
        predint = prediction.eval(feed_dict={x: [result], keep_prob: 1.0}, session=sess)
        with open('resule.txt', 'a') as f:
            if predint[0] == 0:
                num0 = num0 + 1
                f.write(os.path.splitext(file)[0]+':'+'w'+ "\n\n")
            else:
                num1 = num1 + 1
                f.write(os.path.splitext(file)[0]+':'+'o'+ "\n\n")
            print('recognize result:')
            print(predint[0],num0,num1)
