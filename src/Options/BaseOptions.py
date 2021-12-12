import argparse


class BaseOptions:
    _parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    initialized = False

    @staticmethod
    def parse():
        BaseOptions.initialized = True
        BaseOptions._parser.add_argument('--ib-gateway-port', type=int, default=7496, help="Specify port for IB gateway. Use -1 to disable.")
        BaseOptions._parser.add_argument('--ib-gateway-readonly', type=bool, default=False, help="If true the connection to IB will be established as readonly.")
        BaseOptions._parser.add_argument('--external-portfolio', type=str, default='', help="Specify path .json file containing portfolio")
        BaseOptions._parser.add_argument('--dry-run', action='store_true', default=False, help="If set to true, no orders will be submitted.")

        return BaseOptions._parser

    @staticmethod
    def get_args():
        if BaseOptions.initialized:
            return BaseOptions._parser.parse_args()
        else:
            raise ValueError("Parser uninitialized")

    @staticmethod
    def print_options(opt):
        """Print and save options
        Taken from pytorch-CycleGAN-and-pix2pix repo
        It will print both current options and default values(if different).
        It will save options into a text file / [checkpoints_dir] / opt.txt
        """
        message = ''
        message += '----------------- Options ---------------\n'
        for k, v in sorted(vars(opt).items()):
            comment = ''
            default = BaseOptions._parser.get_default(k)
            if v != default:
                comment = '\t[default: %s]' % str(default)
            message += '{:>25}: {:<30}{}\n'.format(str(k), str(v), comment)
        message += '----------------- End -------------------'
        print(message)
