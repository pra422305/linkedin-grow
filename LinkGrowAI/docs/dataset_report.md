# Dataset Report

## initial
{'records': 258, 'columns': ['Post title', 'Post link', 'Post type', 'Posted by', 'Created date', 'Audience', 'Impressions', 'Clicks', 'Click through rate (CTR)', 'Likes', 'Comments', 'Reposts', 'Engagement rate'], 'dtypes': {'Post title': 'object', 'Post link': 'object', 'Post type': 'object', 'Posted by': 'object', 'Created date': 'object', 'Audience': 'object', 'Impressions': 'int64', 'Clicks': 'int64', 'Click through rate (CTR)': 'float64', 'Likes': 'int64', 'Comments': 'int64', 'Reposts': 'int64', 'Engagement rate': 'float64'}, 'missing': {'Post title': 0, 'Post link': 0, 'Post type': 0, 'Posted by': 0, 'Created date': 0, 'Audience': 0, 'Impressions': 0, 'Clicks': 0, 'Click through rate (CTR)': 0, 'Likes': 0, 'Comments': 0, 'Reposts': 0, 'Engagement rate': 0}, 'duplicates': 0}

## removed_empty_text
0

## removed_duplicates
0

## final
{'records': 258, 'columns': ['post_id', 'post_text', 'creator_or_page_id', 'topic', 'hook_type', 'post_format', 'publication_date', 'impressions', 'reactions', 'comments', 'reposts', 'engagement_rate', 'source', 'license_or_permission_reference'], 'dtypes': {'post_id': 'object', 'post_text': 'object', 'creator_or_page_id': 'object', 'topic': 'object', 'hook_type': 'object', 'post_format': 'object', 'publication_date': 'datetime64[ns]', 'impressions': 'float64', 'reactions': 'float64', 'comments': 'float64', 'reposts': 'float64', 'engagement_rate': 'float64', 'source': 'object', 'license_or_permission_reference': 'object'}, 'missing': {'post_id': 0, 'post_text': 0, 'creator_or_page_id': 0, 'topic': 258, 'hook_type': 258, 'post_format': 0, 'publication_date': 0, 'impressions': 0, 'reactions': 0, 'comments': 0, 'reposts': 0, 'engagement_rate': 0, 'source': 0, 'license_or_permission_reference': 0}, 'duplicates': 0}

## numeric_summary
{'impressions': {'count': 258.0, 'mean': 773.1821705426356, 'std': 741.0364138723311, 'min': 136.0, '25%': 403.75, '50%': 540.0, '75%': 849.75, 'max': 7202.0}, 'reactions': {'count': 258.0, 'mean': 9.151162790697674, 'std': 10.270865570949166, 'min': 1.0, '25%': 3.0, '50%': 6.0, '75%': 11.0, 'max': 81.0}, 'comments': {'count': 258.0, 'mean': 0.686046511627907, 'std': 1.6569271726348744, 'min': 0.0, '25%': 0.0, '50%': 0.0, '75%': 1.0, 'max': 15.0}, 'reposts': {'count': 258.0, 'mean': 1.4651162790697674, 'std': 0.9298048967173927, 'min': 0.0, '25%': 1.0, '50%': 1.0, '75%': 2.0, 'max': 7.0}, 'engagement_rate': {'count': 258.0, 'mean': 0.04892914694582303, 'std': 0.023031593295421066, 'min': 0.0096286106854677, '25%': 0.032555972225964, '50%': 0.04642989672720425, '75%': 0.060522868297994054, 'max': 0.1836327314376831}}

## limitations
This dataset is small and appears to represent posts from one creator/page. Use results as exploratory patterns, not proof of causal LinkedIn growth.
