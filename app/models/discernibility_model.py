import pandas as pd

class DiscernibilityModel:
    def __init__(self, data: pd.DataFrame, criteria: list, target_column: str):
        self.data = data
        self.criteria = criteria
        self.target_column = target_column

    def generate_discernibility_matrix(self):
        """Tạo ma trận phân biệt từ dữ liệu."""
        n = len(self.data)
        matrix = pd.DataFrame('Ø', index=self.data.index, columns=self.data.index)

        for i in range(n):
            for j in range(i + 1, n):
                if self.data.iloc[i][self.target_column] == self.data.iloc[j][self.target_column]:
                    matrix.iloc[i, j] = 'Ø'
                    matrix.iloc[j, i] = 'Ø'
                else:
                    differences = [
                        criterion[0].lower()
                        for criterion in self.criteria
                        if self.data.iloc[i][criterion] != self.data.iloc[j][criterion]
                    ]
                    if differences:
                        value = ','.join(differences)
                        matrix.iloc[i, j] = value
                        matrix.iloc[j, i] = value

        return matrix

    def optimize_discernibility_matrix(self, matrix):
        """Tối ưu ma trận phân biệt thành biểu thức đơn giản."""
        final_terms = []
        used_elements = set()

        # Xử lý các ô chứa 1 phần tử
        for i in matrix.index:
            for j in matrix.columns:
                current_cell = matrix.loc[i, j].strip()
                if current_cell != 'Ø' and len(current_cell.split(',')) == 1:
                    element = current_cell.strip()
                    if element not in used_elements:
                        final_terms.append(f"{element}")
                        used_elements.add(element)

        # Xử lý các ô còn lại
        for i in matrix.index:
            for j in matrix.columns:
                current_cell = matrix.loc[i, j].strip()
                if current_cell != 'Ø' and not any(el in used_elements for el in current_cell.split(',')):
                    remaining_elements = [el for el in current_cell.split(',') if el not in used_elements]
                    if remaining_elements:
                        or_expression = ' ∨ '.join(sorted(set(remaining_elements)))
                        final_terms.append(f"({or_expression})")

        simplified_expression = ' ∧ '.join(sorted(set(final_terms)))
        return simplified_expression
