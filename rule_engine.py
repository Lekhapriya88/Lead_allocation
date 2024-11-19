import json
import logging

class RuleEngine:
    def __init__(self, rules):
        self.rules = rules

    def calculate_scorex(self, lead, counsellor):
        total_score = 0
        for rule in self.rules:
            rule_score = self.evaluate_rule(rule, lead, counsellor)
            total_score += rule_score
        return total_score
    
    def calculate_score(self, lead, counsellor):
        total_score = 0
        rule_contributions = {}
        for rule in self.rules:
            print("************** rule: ", rule)
            rule_score = self.evaluate_rule(rule, lead, counsellor)
            print("---- ", rule_score)
            total_score += rule_score
            # Use the rule's description as the key
            rule_desc = rule.get('description', f"Rule_{self.rules.index(rule)+1}")
            rule_contributions[rule_desc] = rule_score
        return total_score, rule_contributions

    def evaluate_rule(self, rule, lead, counsellor):
        result = self.evaluate_conditions(rule['conditions'], rule['logic'], lead, counsellor)
        weight = rule.get('weight', 1)
        return weight if result else 0

    def evaluate_conditions(self, conditions, logic, lead, counsellor):
        results = []
        for condition in conditions:
            if 'conditions' in condition:
                # Nested conditions
                result = self.evaluate_conditions(
                    condition['conditions'],
                    condition['logic'],
                    lead,
                    counsellor
                )
            else:
                left_value = self.get_attribute_value(condition['left'], lead, counsellor)
                print("left = ", left_value)
                right_value = self.get_attribute_value(condition['right'], lead, counsellor)
                print("right =", right_value)
                operator = condition['operator']
                result = self.compare_values(left_value, right_value, operator)
            results.append(result)
        if logic == 'AND':
            return all(results)
        elif logic == 'OR':
            return any(results)
        else:
            return False

    def get_attribute_value(self, side, lead, counsellor):
        if 'value' in side:
            return side['value']
        elif 'attribute' in side and 'entity' in side:
            entity = side['entity']
            attribute = side['attribute']
            if entity == 'lead':
                return getattr(lead, attribute, None)
            elif entity == 'counsellor':
                return getattr(counsellor, attribute, None)
        return None

    def compare_values(self, left, right, operator):
        try:
            if left is None or right is None:
                return False
            left_value = self.parse_value(left)
            right_value = self.parse_value(right)
            # Handle list comparisons
            if operator == 'in':
                return left_value in right_value if isinstance(right_value, list) else left_value in [right_value]
            elif operator == 'not in':
                return left_value not in right_value if isinstance(right_value, list) else left_value not in [right_value]
            else:
                # Handle other operators
                if operator == '==':
                    return left_value == right_value
                elif operator == '!=':
                    return left_value != right_value
                elif operator == '>':
                    return left_value > right_value
                elif operator == '<':
                    return left_value < right_value
                elif operator == '>=':
                    return left_value >= right_value
                elif operator == '<=':
                    return left_value <= right_value
            return False
        except (TypeError, ValueError) as e:
            logging.error(f"Error comparing values: {e}")
            return False

    def parse_value(self, value):
        # Attempt to parse numbers
        try:
            return float(value)
        except (ValueError, TypeError):
            pass
        # Attempt to parse JSON arrays
        if isinstance(value, str) and value.startswith('[') and value.endswith(']'):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        # Return the value as is
        return value