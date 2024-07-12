import itertools
import pandas as pd

class RuleMiner(object):
	"""RuleMiner implements methods to get association rules
 	   using the market-basket model.
	"""

	def __init__(self, support: int, confidence: int) -> None:
		"""Constructor for the RuleMiner object.
		Arguments:
			support {int}: Support threshold for the dataset.
			confidence {int}: Confidence threshold for the dataset.
		"""
		self.support: int = support
		self.confidence: int = confidence

	def getSupport(self, data: pd.DataFrame, itemset: list) -> int:
		"""Returns the support for a given dataset.
		The support of a dataset is the number of baskets where a given itemset
		is present.
		Arguments:
			data {pd.DataFrame}: Dataset to search.
			itemset {list}: Items to get support of in dataset.
		"""
		mask = data[itemset].all(axis = 1)
		support = mask.sum()
		return support

	def getRules() -> list:
		""""""
		pass