import pandas as pd
from unicodedata import normalize
import re

# CSVファイルを読み込む
df = pd.read_csv('input.csv')

# 'instruction', 'input', 'output'列のテキストを正規化します
for column in ['instruction', 'input', 'output']:
    df[column] = df[column].apply(lambda x: normalize("NFKC", str(x)))

# 'instruction', 'input', 'output'列に正規表現を適用して数値の注釈のみを削除し、結果を新しい列に保存します
df['cleaned_input'] = df['input'].apply(lambda x: re.sub(r'\[\d+\]', '', str(x)))
df['cleaned_instruction'] = df['instruction'].apply(lambda x: re.sub(r'\[\d+\]', '', str(x)))
df['cleaned_output'] = df['output'].apply(lambda x: re.sub(r'\[\d+\]', '', str(x)))

# 元のテキストと注釈を除去したテキストが一致するかどうかを比較し、その結果を新たな列に保存する
df['input_is_changed'] = df['input'] != df['cleaned_input']
df['instruction_is_changed'] = df['instruction'] != df['cleaned_instruction']
df['output_is_changed'] = df['output'] != df['cleaned_output']

# cleaned_input, cleaned_instruction, cleaned_output列で、_is_changedがFalseの場合は何も表示しないようにします
df.loc[df['input_is_changed'] == False, 'cleaned_input'] = ''
df.loc[df['instruction_is_changed'] == False, 'cleaned_instruction'] = ''
df.loc[df['output_is_changed'] == False, 'cleaned_output'] = ''

# 'nan'も表示しないようにします
df = df.replace('nan', '', regex=True)

# CSVファイルへ書き込む
df.to_csv('output_edit_RevA.csv', index=False, encoding='utf-8-sig')

# 確認のため、DataFrameの最初の数行を返します
df.head()