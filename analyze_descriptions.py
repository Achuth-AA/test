import pandas as pd
import re
from collections import Counter, defaultdict
import numpy as np

def analyze_csv_descriptions(file_path, file_name):
    print(f"\n{'='*60}")
    print(f"Analyzing: {file_name}")
    print(f"{'='*60}")
    
    # Read CSV
    df = pd.read_csv(file_path)
    
    # Basic statistics
    print(f"\nTotal rows: {len(df)}")
    
    if 'Description' in df.columns:
        desc_col = df['Description']
        
        # Handle missing values
        non_null_count = desc_col.notna().sum()
        null_count = desc_col.isna().sum()
        
        print(f"Non-null descriptions: {non_null_count}")
        print(f"Null/empty descriptions: {null_count}")
        
        # Filter non-null descriptions
        descriptions = desc_col.dropna().astype(str)
        
        if len(descriptions) > 0:
            # Length statistics
            desc_lengths = descriptions.str.len()
            print(f"\nDescription length statistics:")
            print(f"  Min length: {desc_lengths.min()}")
            print(f"  Max length: {desc_lengths.max()}")
            print(f"  Average length: {desc_lengths.mean():.2f}")
            print(f"  Median length: {desc_lengths.median():.2f}")
            
            # Unique descriptions
            unique_count = descriptions.nunique()
            print(f"\nUnique descriptions: {unique_count}")
            print(f"Duplicate rate: {((len(descriptions) - unique_count) / len(descriptions) * 100):.2f}%")
            
            # Most common descriptions (top 10)
            value_counts = descriptions.value_counts()
            print(f"\nTop 10 most common descriptions:")
            for i, (desc, count) in enumerate(value_counts.head(10).items(), 1):
                truncated = desc[:100] + "..." if len(desc) > 100 else desc
                print(f"  {i}. '{truncated}' - {count} occurrences")
            
            # Pattern analysis
            print(f"\nPattern analysis:")
            
            # Count descriptions with numbers
            with_numbers = descriptions.str.contains(r'\d').sum()
            print(f"  Descriptions containing numbers: {with_numbers} ({with_numbers/len(descriptions)*100:.2f}%)")
            
            # Count descriptions with special characters
            with_special = descriptions.str.contains(r'[^a-zA-Z0-9\s]').sum()
            print(f"  Descriptions with special characters: {with_special} ({with_special/len(descriptions)*100:.2f}%)")
            
            # Count all uppercase descriptions
            all_upper = descriptions.str.isupper().sum()
            print(f"  All uppercase descriptions: {all_upper} ({all_upper/len(descriptions)*100:.2f}%)")
            
            # Count all lowercase descriptions
            all_lower = descriptions.str.islower().sum()
            print(f"  All lowercase descriptions: {all_lower} ({all_lower/len(descriptions)*100:.2f}%)")
            
            # Word frequency analysis
            print(f"\nTop 20 most common words:")
            all_words = []
            for desc in descriptions:
                # Split by whitespace and common delimiters
                words = re.findall(r'\b[a-zA-Z]+\b', desc.lower())
                all_words.extend(words)
            
            word_counts = Counter(all_words)
            # Filter out common stop words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'was', 'are', 'were'}
            filtered_words = {word: count for word, count in word_counts.items() if word not in stop_words and len(word) > 2}
            
            for i, (word, count) in enumerate(Counter(filtered_words).most_common(20), 1):
                print(f"  {i}. '{word}' - {count} occurrences")
            
            # Category detection (if patterns suggest categories)
            print(f"\nPotential categories/themes:")
            
            # Look for common prefixes or patterns
            prefix_counter = defaultdict(int)
            for desc in descriptions:
                # Extract first few words as potential category
                words = desc.split()
                if len(words) >= 2:
                    prefix = ' '.join(words[:2])
                    prefix_counter[prefix] += 1
            
            # Show prefixes that appear more than 5 times
            common_prefixes = [(prefix, count) for prefix, count in prefix_counter.items() if count > 5]
            common_prefixes.sort(key=lambda x: x[1], reverse=True)
            
            if common_prefixes:
                for i, (prefix, count) in enumerate(common_prefixes[:10], 1):
                    print(f"  {i}. '{prefix}...' - {count} occurrences")
            else:
                print("  No clear category patterns detected")
            
            # Sample of random descriptions
            print(f"\nRandom sample of 5 descriptions:")
            sample = descriptions.sample(min(5, len(descriptions)), random_state=42)
            for i, desc in enumerate(sample, 1):
                truncated = desc[:150] + "..." if len(desc) > 150 else desc
                print(f"  {i}. '{truncated}'")
                
    else:
        print("No 'Description' column found in the CSV file!")
        print(f"Available columns: {list(df.columns)}")

# Analyze all three files
files = [
    ('test_data_comms_data.csv', 'Communications Data'),
    ('test_data_hot_data.csv', 'Hot Data'),
    ('test_data_prod_data.csv', 'Production Data')
]

for file_name, display_name in files:
    try:
        analyze_csv_descriptions(file_name, display_name)
    except Exception as e:
        print(f"\nError analyzing {display_name}: {str(e)}")

print(f"\n{'='*60}")
print("Analysis Complete")
print(f"{'='*60}")