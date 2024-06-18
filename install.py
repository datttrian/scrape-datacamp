from rpy2.robjects.packages import importr

utils = importr('utils')
utils.install_packages('rvest')
