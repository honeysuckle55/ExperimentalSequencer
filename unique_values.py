import pandas as pd
from glob import glob
import numpy as np
from scipy.special import erf
import io
import matplotlib.pyplot as plt

def get_unique_values(date, meas_num, param_name, threshold, roi="Cam4_AllTraps_Sum", binarize=False):
  yyyy, mm, dd = date  
  directory = '\\\\treqs_camera.local\\d\\images\\'+yyyy+'\\'+mm+'\\'+dd+'\\'
  #directory = 'M:\\data_backup\\images\\'+yyyy+'\\'+mm+'\\'+dd+'\\'
  meas_name = yyyy+'-'+mm+'-'+dd+'_meas{0:04d}'.format(meas_num)
  info_loc = glob(directory + meas_name+'*')[0]
  info = pd.read_csv(info_loc)

  info_roi = info[roi]
  
  if binarize:
      info_roi[info_roi <= threshold] = 0
      info_roi[info_roi > threshold] = 1  
  
  data_param = info[param_name].to_numpy()  
  unique_param = info[param_name].unique()
  num_unique_param = len(unique_param)
  
  fluoresc_avg = np.zeros((len(unique_param)))
  fluoresc_err = np.zeros((len(unique_param)))
  
  for i in range(num_unique_param):
    loc = np.where(data_param == unique_param[i])[0]
    #n_max = 50  # to select only the first 20 y values to average
    #loc = loc[:n_max]  #comment this line and the one above to select all data
    fluoresc_avg[i] = np.average(info_roi.to_numpy()[loc])
    fluoresc_err[i] = np.std(info_roi.to_numpy()[loc])/np.sqrt(len(loc))
    
  return [unique_param, fluoresc_avg, fluoresc_err]  


def get_unique_values2d(date, meas_num, param_name, param_scan_name, param_scan_ind, roi='Cam4_Trap1_Sum',
                        binarize=False, threshold=0):
  yyyy, mm, dd = date  
  directory = '\\\\treqs_camera.local\\d\\images\\'+yyyy+'\\'+mm+'\\'+dd+'\\'
  meas_name = yyyy+'-'+mm+'-'+dd+'_meas{0:04d}'.format(meas_num)
  info_loc = glob(directory + meas_name+'*')[0]
  info = pd.read_csv(info_loc)

  info_roi = info[roi]

  if binarize:
      info_roi[info_roi <= threshold] = 0
      info_roi[info_roi > threshold] = 1
  
  p = param_scan_ind
  param_scan = np.unique(info[param_scan_name].to_numpy())  
  locs = info.loc[info[param_scan_name] == param_scan[p]]
  
  # print(locs.keys())
  
  data_param = locs[param_name].to_numpy()  
  unique_param = locs[param_name].unique()
  num_unique_param = len(unique_param)
  
  fluoresc_avg = np.zeros((len(unique_param)))
  fluoresc_err = np.zeros((len(unique_param)))
  
  for i in range(num_unique_param):
    loc = np.where(data_param == unique_param[i])[0]
    fluoresc_avg[i] = np.average(locs[roi].to_numpy()[loc])
    fluoresc_err[i] = np.std(locs[roi].to_numpy()[loc])/np.sqrt(len(loc))
    
  return [unique_param, fluoresc_avg, fluoresc_err, param_scan[p]]      


def get_unique_values2d_df(df, param_name, param_scan_name, param_scan_ind):

  info = df
  
  p = param_scan_ind
  param_scan = np.unique(info[param_scan_name].to_numpy())  
  locs = info.loc[info[param_scan_name] == param_scan[p]]
  
  data_param = locs[param_name].to_numpy()  
  unique_param = locs[param_name].unique()
  num_unique_param = len(unique_param)
  
  fluoresc_avg = np.zeros((len(unique_param)))
  fluoresc_err = np.zeros((len(unique_param)))
  
  for i in range(num_unique_param):
    loc = np.where(data_param == unique_param[i])[0]
    fluoresc_avg[i] = np.average(locs['Cam4_Trap_Sum'].to_numpy()[loc])
    fluoresc_err[i] = np.std(locs['Cam4_Trap_Sum'].to_numpy()[loc])/np.sqrt(len(loc))
    
  return [unique_param, fluoresc_avg, fluoresc_err, param_scan[p]]


def get_df(date, meas_num):
  yyyy, mm, dd = date
  directory = '\\\\treqs_camera.local\\d\\images\\'+yyyy+'\\'+mm+'\\'+dd+'\\'
  meas_name = yyyy+'-'+mm+'-'+dd+'_meas{0:04d}'.format(meas_num)
  info_loc = glob(directory + meas_name+'*')[0]
  info = pd.read_csv(info_loc) 
  
  return [info, info_loc]


def GaussianFunction(x, x0, sigma):
    return np.exp(-(x-x0)**2/(2*sigma**2))

def GaussianCumulative(x, x0, sigma, alpha):
    return 1/2*(1+erf(alpha*(x-x0)/sigma))

def skewedFunction(x,const,amp,x0,sigma,alpha):
    return const + amp*GaussianFunction(x,x0,sigma)*GaussianCumulative(x,x0,sigma,alpha)


