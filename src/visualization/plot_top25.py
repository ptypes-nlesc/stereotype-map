import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 11)
plt.rcParams['font.size'] = 11

# ====================== DATA ======================
gender_data = {
    'term': ['Cock', 'Girl', 'Tit', 'Dick', 'Babe', 'Wife', 'Guy', 'Pussi', 'Slut', 
             'Boob', 'Man', 'Girlfriend', 'Blond', 'Mom', 'Chick', 'Bitch', 'Stud',
             'Woman', 'Women', 'Whore', 'Breast', 'Redhead', 'Boy', 'Dude', 'Men'],
    'count': [8030, 4800, 2969, 1745, 1741, 1112, 1109, 1086, 1029, 802, 766, 726,
              661, 445, 414, 322, 292, 284, 265, 253, 245, 233, 230, 223, 192]
}

ethno_data = {
    'term': ['Black', 'Asian', 'Eboni', 'White', 'Latina', 'German', 'French', 'Russian',
             'Spanish', 'Italian', 'Indian', 'Dark', 'British', 'Brazilian', 'Korean',
             'European', 'Brown', 'Thai', 'African', 'Orient', 'Arab', 'English',
             'Muslim', 'Canadian', 'Hungarian'],
    'count': [5921, 1694, 1244, 1178, 797, 668, 557, 520, 301, 164, 151, 144, 130,
              126, 108, 82, 79, 72, 65, 54, 51, 46, 43, 40, 38]
}

df_gender = pd.DataFrame(gender_data)
df_ethno = pd.DataFrame(ethno_data)

# Calculate percentage
df_gender['percentage'] = (df_gender['count'] / df_gender['count'].sum()) * 100
df_ethno['percentage']  = (df_ethno['count']  / df_ethno['count'].sum())  * 100

# ====================== PLOT ======================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 11))

sns.barplot(data=df_gender.head(25), y='term', x='percentage', ax=ax1, color='#d62728')
# ax1.set_title('Top 25 Most Frequent Gender Nouns\n(as % of all gender nouns)', 
            #   fontsize=14, pad=15)
ax1.set_xlabel('Percentage of Total (%)')
ax1.set_ylabel('')

sns.barplot(data=df_ethno.head(25), y='term', x='percentage', ax=ax2, color='#1f77b4')
# ax2.set_title('Top 25 Most Frequent Ethno-Racial Adjectives\n(as % of all ethno-racial adjectives)', 
            #   fontsize=14, pad=15)
ax2.set_xlabel('Percentage of Total (%)')
ax2.set_ylabel('')

# Add value labels
for ax in [ax1, ax2]:
    for i, v in enumerate(ax.patches):
        width = v.get_width()
        ax.text(width + 0.4, v.get_y() + v.get_height()/2, 
                f'{width:.1f}%', va='center', fontsize=10)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig('plots/top_25_terms_comparison.png', dpi=300, bbox_inches='tight')
plt.show()


