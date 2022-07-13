from torch import image
import lpips

class MetricCalculator():
    def __init__(self):
        pass

    def msssim(X, Y, data_range=255, size_average=True, win_size=11, win_sigma=1.5, win=None, K=(0.01, 0.03), nonnegative_ssim=False,):
        return image.ssim(X, Y, data_range, size_average, win_size, win_sigma, win, K, nonnegative_ssim)

    def lpips(img1, img2, net):
        
        loss_fn_alex = lpips.LPIPS(net='alex')
        loss_fn_vgg = lpips.LPIPS(net='vgg') 

        if net == "alex":
            return loss_fn_alex(img1, img2)

        return loss_fn_vgg(img1, img2)