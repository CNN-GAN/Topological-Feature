import tensorflow as tf

def defaultParam():

    flags = tf.app.flags
    flags.DEFINE_integer("epoch", 35, "Epoch to train [25]")
    flags.DEFINE_integer("c_epoch", 16, "current Epoch")
    flags.DEFINE_integer("enhance", 5, "Enhancement for different matrix")
    flags.DEFINE_float("learning_rate", 0.0002, "Learning rate of for adam [0.0002]")
    flags.DEFINE_float("beta1", 0.5, "Momentum term of adam [0.5]")
    flags.DEFINE_float("side_dic", 1.0, "side discriminator for cycle updating")
    flags.DEFINE_float("lamda", 0.5, "lamda for cycle updating")
    
    flags.DEFINE_float("v_ds", 10, "seqslam distance")
    flags.DEFINE_float("vmin", 0.8, "min velocity of seqslam")
    flags.DEFINE_float("vskip", 0.1, "velocity gap")
    flags.DEFINE_float("vmax", 1.2, "max velocity of seqslam")
    flags.DEFINE_integer("Rwindow", 10, "rainbow")
    
    flags.DEFINE_integer("train_size", np.inf, "The size of train images [np.inf]")
    flags.DEFINE_integer("batch_size", 64, "The number of batch images [64]")
    flags.DEFINE_integer("image_size", 500, "The size of image to use (will be center cropped) [108]")
    flags.DEFINE_integer("output_size", 64, "The size of the output images to produce [64]")
    flags.DEFINE_integer("sample_size", 64, "The number of sample images [64]")
    flags.DEFINE_integer("c_dim", 3, "Dimension of image color. [3]")
    flags.DEFINE_integer("sample_step", 2, "The interval of generating sample. [500]")
    flags.DEFINE_integer("save_step", 100, "The interval of saveing checkpoints. [500]")
    flags.DEFINE_string("dataset", "loam", "The name of dataset [celebA, mnist, loam, lsun]")
    flags.DEFINE_string("checkpoint_dir", "checkpoint", "Directory name to save the checkpoints [checkpoint]")
    flags.DEFINE_string("sample_dir", "samples", "Directory name to save the image samples [samples]")
    flags.DEFINE_boolean("is_train", False, "True for training, False for testing [False]")
    flags.DEFINE_boolean("is_crop", True, "True for training, False for testing [False]")
    flags.DEFINE_boolean("is_restore", True, "restore from pre trained")
    flags.DEFINE_boolean("visualize", False, "True for visualizing, False for nothing [False]")

    return flags.FLAGS