import itertools
import pandas as pd

class RuleMiner(object):
	"""RuleMiner implements methods to get association rules 
	using the market-basket model. This code is heavily based off of
	the rule miner featured in Notebook 7.
	"""

	def __init__(self, support_threshold: int, confidence_threshold: int) -> None:
		"""Constructor for the RuleMiner object.
		Arguments:
			support {int}: Support threshold for the dataset.
			confidence {int}: Confidence threshold for the dataset.
		"""
		self.support_threshold: int = support_threshold
		self.confidence_thershold: int = confidence_threshold

	def get_support(self, data: pd.DataFrame, itemset: list) -> int:
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

	def get_rules(self, itemset: list) -> list:
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

	def get_confidence(self, data: pd.DataFrame, rule: list) -> float:
		"""Returns the confidence value for a rule.
		The confidence value of a rule measures the frequency of occurrences
		between X and Y, relative to X alone.
		Arguments:
			data {pd.DataFrame}: Dataset to get confidence values of rule from.
			rule {list}: List that contains two values. A rule of X -> y is
			represented as [X, y].
		Returns:
			float: Confidence value for rule in the dataset.
		"""
  
		# Create a combined rule [X, y].
		combined_set = rule[0] + rule[1]
  
		# The formula for getting the confidence value of X -> y is:
		# Support of X -> y divided by Support of X.
		return self.get_support(data, combined_set) / self.get_support(data, rule[0])

	def merge_itemsets(self, itemsets: list) -> list:
		"""Returns a list of merged itemsets.
		These itemsets cannot have duplicate items.
		Arguments:
			itemsets {list}: List that contains itemsets to merge.
		Returns:
			list: List of merged itemsets.
		"""

		# Store merged itemsets.
		new_itemsets = []

		# Get the current number of items for the first itemset in the list.
		item_count = len(itemsets[0])
	
		if item_count == 1:
			new_itemsets = [list(set(itemsets[i]) | set(itemsets[j])) for i in range(len(itemsets)) for j in range(i + 1)]
		else:
			for i in range(len(itemsets)):
				for j in range(i + 1, len(itemsets)):
					combined_list = list(set(itemsets[i]) | set(itemsets[j]))
					combined_list.sort()
					if len(combined_list) == item_count + 1 and combined_list not in new_itemsets:
						new_itemsets.append(combined_list)
		return new_itemsets

	def get_frequent_itemsets(self, data: pd.DataFrame) -> list:
		"""Returns a list of frequent itemsets in the datasets.
		The support of a "frequent" itemset should be >= to the support.
		Arguments:
			data {pd.DataFrame}: Dataset to get frequent itemsets from.
		Returns:
			list: List of frequent itemsets in the dataset.
		"""
  
		itemsets = [[i] for i in data.columns]
		old_itemsets = []
		new_itemset_not_empty = True
  
		while new_itemset_not_empty:
			new_itemsets = []
			for itemset in itemsets:
				if (self.get_support(data, itemset) >= self.support_t):
					new_itemsets.append(itemset)

			if len(new_itemsets) != 0:
				old_itemsets = new_itemsets
				itemsets = self.merge_itemsets(new_itemsets)
			else:
				new_itemset_not_empty = False
				itemsets = old_itemsets

		return itemsets

	def get_association_rules(self, data: pd.DataFrame):
		"""Returns a list of association rules with a support value >= to the
		support threshold and confidence >= to the confidence threshold.
		Arguments:
			data {pd.DataFrame}: Dataset to get association rules from.
		Returns:
			list: List of association rules.
		"""
  
		# Get frequent itemsets from the given data.
		itemsets = self.get_frequent_itemsets(data)
  
		# Get rules for each itemset in the list of itemsets.
		rules = [self.get_rules(itemset) for itemset in itemsets]
  
		# For each item in each rule, check if its confidence value is greater
		# than the threshold.
		association_rules = [i for rule in rules for i in rule if self.get_confidence(data, i) >= self.confidence_thershold]
		return association_rules