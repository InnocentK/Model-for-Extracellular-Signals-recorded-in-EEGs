

import numpy as np
import pickle
import matplotlib.pyplot as plt

resultsRoot = "mazzoni_example/results/"
plotsDir = "./"

def loadResults(fname):
	file = open(resultsRoot + fname, "rb" )
	data = pickle.load(file, encoding='latin1')
	file.close()
	return data


def graphLFP(lfpProxy, show_plot=True):
	plt.plot(np.mean(lfpProxy, axis=0))
	# plt.title("LFP")
	plt.xlabel('Time (ms)')
	plt.ylabel('LFP (mV)')

	if show_plot:
		plt.show()
	else:
		plt.savefig(plotsDir + '_DSurface' + ".png", bbox_inches='tight')
		print('\n', 'DSurface', "| Plot Saved")
		plt.close()
	return 0

def main():
	fname = "input15_output_data_rank0.p15"
	data = loadResults(fname)

	print(data.keys())
	lfpDict = data['LFP']

	print(lfpDict.keys())

	gaba_weight = 1.65
	lfpProxy = lfpDict[0]
	for i in range(1, len(lfpDict.keys())):
		if i < 40:
			lfpProxy += lfpDict[i] # Excititory neurons add to the signal
		else:
			# lfpProxy -= lfpDict[i] # Inhibitory take away from the signal
			lfpProxyT = np.transpose(lfpProxy)
			for j, data_t in enumerate( np.transpose(lfpDict[i]) ):
				time_delay = 6
				if j >= time_delay:
					lfpProxyT[j - time_delay] -= np.multiply(gaba_weight, data_t)
			lfpProxy = np.transpose(lfpProxyT)



	return 0
main()