import argparse

print("""
                    _ _
   __ _  __ _ _   _(_) | __ _
  / _` |/ _` | | | | | |/ _` |
 | (_| | (_| | |_| | | | (_| |
  \__,_|\__, |\__,_|_|_|\__,_|
           |_|

""")

parser = argparse.ArgumentParser()
parser.add_argument('pre', type=str, nargs='?',
                    help='path to pre disaster image')
parser.add_argument('post', type=str, nargs='?',
                    help='path to post disaster image')
parser.add_argument('--theia', type=str,
                    default='./theia/model/theia.pth', help='path to theia model')
parser.add_argument('--threshhold', type=float, default=0.10,
                    help='threshhold value for theia segmentation maps')
parser.add_argument('--perses', type=str,
                    default='./perses/model/perses.pt', help='path to perses model')
parser.add_argument('--no-cuda', action='store_true', help='disables cuda')
parser.add_argument('--time', action='store_true',
                    help='measure performance time')
parser.add_argument('--save', type=str, default='',
                    help='filename to save output file to')

opt = parser.parse_args()
