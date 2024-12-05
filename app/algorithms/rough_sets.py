import pandas as pd

def equivalence_classes(df, attributes):
    if not set(attributes).issubset(df.columns):
        raise ValueError("Một số thuộc tính trong B không tồn tại trong DataFrame.")
    equivalence_classes = df.groupby(attributes).groups
    result = []
    for group, indices in equivalence_classes.items():
        result.append(set(df.loc[indices, 'ID']))
    return result

def b_lower_approximation_for_X(df, X, attributes):
    if 'ID' not in df.columns:
        raise ValueError("DataFrame phải chứa cột 'ID'.")
    equivalence_classes = df.groupby(attributes).groups
    b_lower = []
    for group, indices in equivalence_classes.items():
        if set(df.loc[indices, 'ID']).issubset(X):
            b_lower.extend(indices)
    return df.loc[b_lower]

def b_upper_approximation_for_X(df, X, attributes):
    if 'ID' not in df.columns:
        raise ValueError("DataFrame phải chứa cột 'ID'.")
    equivalence_classes = df.groupby(attributes).groups
    b_upper = []
    for group, indices in equivalence_classes.items():
        if set(df.loc[indices, 'ID']).intersection(X):
            b_upper.extend(indices)
    return df.loc[b_upper]

def positive_region(df, decision_attribute, condition_attributes):
    if decision_attribute not in df.columns:
        raise ValueError(f"Cột '{decision_attribute}' không tồn tại trong DataFrame.")
    equivalence_classes = df.groupby(condition_attributes).groups
    pos_b_c = set()
    for group, indices in equivalence_classes.items():
        if len(df.loc[indices, decision_attribute].unique()) == 1:
            pos_b_c.update(indices)
    return pos_b_c

def dependency_degree(df, decision_attribute, condition_attributes):
    if len(df) == 0:
        raise ValueError("DataFrame không có dữ liệu, không thể tính gamma(B, C).")
    pos_b_c = positive_region(df, decision_attribute, condition_attributes)
    total_objects = len(df)
    gamma_bc = len(pos_b_c) / total_objects
    return gamma_bc

def boundary_region(df, b_lower, b_upper):
    return set(b_upper) - set(b_lower)

def outside_region(df, b_upper):
    if 'ID' not in df.columns:
        raise ValueError("DataFrame phải chứa cột 'ID'.")
    all_objects = set(df['ID'])
    return all_objects - set(b_upper)


def calculate_rough_set_properties(df, X, attributes, decision_attribute):
    if not isinstance(X, list):
        raise TypeError("Tập X phải là một danh sách.")
    if not set(attributes).issubset(df.columns):
        raise ValueError("Một số thuộc tính trong B không tồn tại trong DataFrame.")
    if decision_attribute not in df.columns:
        raise ValueError(f"Cột mục tiêu '{decision_attribute}' không tồn tại.")
    
    b_lower = b_lower_approximation_for_X(df, X, attributes)
    b_upper = b_upper_approximation_for_X(df, X, attributes)
    gamma = dependency_degree(df, decision_attribute, attributes)
    boundary = boundary_region(df, b_lower, b_upper)
    outside = outside_region(df, b_upper)

    return {
        "Lower(B, X)": set(b_lower['ID']),
        "Upper(B, X)": set(b_upper['ID']),
        "Boundary(B, X)": boundary,
        "Outside(B, X)": outside,
        "Gamma(B, C)": gamma
    }
