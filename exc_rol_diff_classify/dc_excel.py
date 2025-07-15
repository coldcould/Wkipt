import pandas as pd
import re

def classify_columns_by_keywords(df, keyword_categories):
    """
    根据关键词将数据框的列分类到不同的类别
    
    参数:
    df (pd.DataFrame): 输入数据框
    keyword_categories (dict): 分类字典，格式为 {类别名: [关键词列表]}
    
    返回:
    dict: 包含分类结果的字典，键为类别名，值为对应的数据框
    """
    # 初始化结果字典
    classified_dfs = {}
    
    # 创建未分类列的副本
    remaining_cols = set(df.columns)
    
    # 按照优先级处理每个类别（从最具体的关键词开始）
    # 这里按照关键词长度降序排序，确保先匹配更长的关键词
    sorted_categories = sorted(keyword_categories.items(), 
                              key=lambda x: max(len(kw) for kw in x[1]), 
                              reverse=True)

    print(sorted_categories)
    
    for category, keywords in sorted_categories:
        # 为每个类别创建正则表达式模式
        pattern = re.compile(r'(' + '|'.join(keywords) + r')', re.IGNORECASE)
        
        # 查找匹配的列
        matched_cols = [col for col in remaining_cols if pattern.search(str(col))]
        
        # 如果有匹配的列
        if matched_cols:
            # 创建子数据框
            classified_dfs[category] = df[matched_cols].copy()
            
            # 从剩余列中移除已匹配的列
            remaining_cols -= set(matched_cols)

    print(classified_dfs)
    
    # 添加未分类的列到单独类别
    if remaining_cols:
        classified_dfs['Other'] = df[list(remaining_cols)].copy()
    
    return classified_dfs


def dcEx(file_path, group_cols=None): 
  if group_cols is not None:
    keyword_categories = {col: [col] for col in group_cols}
  else:
    keyword_categories = {}

  df = pd.read_excel(file_path)

  print(f"原始数据形状：{df.shape}")

  # 选择数值列（排除如 时间列、文本列等）
  numeric_cols = df.select_dtypes(include=['int', 'float']).columns.tolist()
  non_numeric_cols = [col for col in df.columns if col not in numeric_cols]

  print(f"数值列({len(numeric_cols)}):{numeric_cols}")
  print(f"非数值列({len(non_numeric_cols)}):{non_numeric_cols}")

  # 计算差值
  if numeric_cols: 
    df_numeric = df[numeric_cols].copy()
    df_diff = df_numeric.diff()
    
    classified_dfs = classify_columns_by_keywords(df_diff, keyword_categories)

    output_file = "classified_result.xlsx"
    with pd.ExcelWriter(output_file) as writer:
      df_diff.to_excel(writer, sheet_name='Original', index=False)

      for category, sub_df in classified_dfs.items():
        sheet_name = category[:31]
        sub_df.to_excel(writer, sheet_name=sheet_name, index=False)