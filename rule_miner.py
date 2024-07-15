import itertools
import pandas as pd

class RuleMiner(object):

    def __init__(self, support_t: int, confidence_t: int) -> None:
        """Class constructor for RuleMiner
        Arguments:
            support_t {int} -- support threshold for the dataset
            confidence_t {int} -- confidence threshold for the dataset
        """
        self.support_t = support_t
        self.confidence_t = confidence_t

    def get_support(self, data: pd.DataFrame, itemset: list) -> int:
        """Returns the support for an itemset. The support of an itemset
        refers to the number of baskets wherein the itemset is present.
        Arguments:
            data {pd.DataFrame} -- DataFrame containing the dataset represented
            as a matrix
            itemset {list} -- list of items to check in each observation
            in the dataset
        Returns:
            int -- support for itemset in data
        """
        itemset = list(itemset)

        mask = data[itemset].all(axis=1)
        support = mask.sum()

        return support

    def merge_itemsets(self, itemsets: list) -> list:
        """Returns a list of merged itemsets. If one itemset of size 2
        from itemsets contains one item in another itemset of size 2 from
        itemsets, the function merges these itemsets to produce an itemset of
        size 3.
        Arguments:
            itemsets {list} -- list which contains itemsets to merge.
        Returns:
            list -- list of merged itemsets
        """

        new_itemsets = []

        cur_num_items = len(itemsets[0])

        if cur_num_items == 1:
            for i in range(len(itemsets)):
                for j in range(i + 1, len(itemsets)):
                    new_itemsets.append(list(set(itemsets[i]) | set(itemsets[j])))

        else:
            for i in range(len(itemsets)):
                for j in range(i + 1, len(itemsets)):
                    combined_list = list(set(itemsets[i]) | set(itemsets[j]))
                    combined_list.sort()
                    if len(combined_list) == cur_num_items + 1 and combined_list not in new_itemsets:
                        new_itemsets.append(combined_list)

        return new_itemsets

    def get_rules(self, itemset: list) -> list:
        """Returns a list of rules produced from an itemset.
        Arguments:
            itemset {list} -- list which contains items.
        Returns:
            list -- list of rules produced from an itemset.
        """

        combinations = itertools.combinations(itemset, len(itemset) - 1)
        combinations = [list(combination) for combination in combinations]

        rules = []
        for combination in combinations:
            diff = set(itemset) - set(combination)
            rules.append([combination, list(diff)])
            rules.append([list(diff), combination])

        return rules

    def get_frequent_itemsets(self, data: pd.DataFrame) -> list:
        """Returns a list frequent itemsets in the dataset. The support of each
        frequent itemset should be greater than or equal to the support
        threshold.
        Arguments:
            data {pd.DataFrame} -- DataFrame containing the dataset represented
            as a matrix
        Returns:
            list -- list of frequent itemsets in the dataset.
        """

        itemsets = [[i] for i in data.columns]
        old_itemsets = []
        flag = True

        while flag:
            new_itemsets = []
            for itemset in itemsets:
                if (self.get_support(data, itemset) >= self.support_t):
                    new_itemsets.append(itemset)

            if len(new_itemsets) != 0:
                old_itemsets = new_itemsets
                itemsets = self.merge_itemsets(new_itemsets)
            else:
                flag = False
                itemsets = old_itemsets

        return itemsets

    def get_confidence(self, data: pd.DataFrame, rule: list) -> float:
        """Returns the confidence for a rule. Suppose the rule is X -> y, then
        the confidence for the rule is the support of the concatenated list of
        X and y divided by the support of X.
        Arguments:
            data {pd.DataFrame} -- DataFrame containing the dataset represented
            as a matrix
            rule {list} -- list which contains two values. If the rule is
            X -> y, then a rule is a list containing [X, y].
        Returns:
            float -- confidence for rule in data
        """
        combined_set = rule[0] + rule[1]
        return self.get_support(data, combined_set) / self.get_support(data, rule[0])

    def get_association_rules(self, data: pd.DataFrame) -> list:
        """Returns a list of association rules with support greater than or
        equal to the support threshold support_t and confidence greater than or
        equal to the confidence threshold confidence_t.
        Arguments:
            data {pd.DataFrame} -- DataFrame containing the dataset represented
            as a matrix
        Returns:
            list -- list of association rules. If the rule is X -> y, then each
            rule is a list containing [X, y].
        """
        itemsets = self.get_frequent_itemsets(data)

        rules = []
        for itemset in itemsets:
            rules.append(self.get_rules(itemset))

        association_rules = []
        for rule in rules:
            for i in rule:
                if (self.get_confidence(data, i) >= self.confidence_t):
                    association_rules.append(i)

        return association_rules
