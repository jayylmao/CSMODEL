import itertools
import pandas as pd

class RuleMiner(object):
	"""RuleMiner implements methods to get association rules using the market-basket model.
	This code is heavily based off of the rule miner featured in Notebook 7.
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
		Returns:
			int: Support of itemset in dataset.
		"""

		# Create a boolean mask for each row in the dataset
		# where it returns True if all items in the itemset are in the row.
		mask = data[itemset].all(axis = 1)

		# Add all the 'True' values from the mask to get the number of
		# rows that meet the condition specified above.
		support = mask.sum()
		return support

	def getRules(self, itemset: list) -> list:
		"""Returns a list of rules from an itemset.
		Arguments:
			itemset {list}: Items to generate rules from.
		Returns:
			list: List of rules generated from an itemset.
		"""
  
		# Generate combinations of lists from the input itemset.
		combinations = itertools.combinations(itemset, len(itemset) - 1)

		# List comprehension to create a list of lists.
		combinations = [list(combination) for combination in combinations]
  
		# Declare empty list to store rules in.
		rules = []
  
		# Get the difference between the itemset and the combination,
		# and add two association rules that represent:
		# - Combination that implies the existence of the items in the difference list.
		# - The reverse rule, where the absence of items in the difference list implies the presence of combination.
		for combination in combinations:
			diff = set(itemset) - set(combination)
			rules.append([combination, list(diff)])
			rules.append([list(diff), combination])
		return rules

