#!/usr/bin/env python3
"""
Modularity boxplot with sector-specific shapes and trip colors
Matching your R script style:
- Shapes: different for each sector (circle, triangle, diamond, square, etc.)
- Colors: based on sampling trip (indianred, indianred4, red3, slateblue)
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
import logging
from pathlib import Path

matplotlib.rcParams['font.family'] = 'DejaVu Sans'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Colors matching your R script (based on sampling trip)
TRIP_COLORS = {
    '01_Cape_Grenville': '#CD5C5C',      # indianred (Trip 1)
    '02_Princess_Charlotte_bay': '#CD5C5C',  # indianred (Trip 1)
    '06_Swains': '#8B3A3A',              # indianred4 (Trip 2)
    '03_Cairns': '#CD3700',              # red3 (Trip 3)
    '07_Capricorn_Bunker': '#8B3A3A',    # indianred4 (Trip 2)
    '05_Townsville': '#6A5ACD',          # slateblue (Trip 4)
    '04_Innisfail': '#CD3700'            # red3 (Trip 3)
}

# Shapes for each sector (matching R: 1=circle, 2=triangle, 3=square, 4=cross, 5=plus, 6=diamond, 7=solid circle)
SECTOR_SHAPES = {
    '01_Cape_Grenville': 'o',        # circle (R shape 1)
    '02_Princess_Charlotte_bay': '^', # triangle (R shape 2)
    '06_Swains': 'D',                 # diamond (R shape 6)
    '03_Cairns': 's',                 # square (R shape 3)
    '07_Capricorn_Bunker': 'o',       # circle (R shape 7)
    '05_Townsville': '+',             # plus (R shape 5)
    '04_Innisfail': 'x'               # cross (R shape 4)
}

def main():
    # Load results
    results_df = pd.read_csv("results/modularity/binary_modularity_hernandez.csv")
    
    # Add sector short name for display
    results_df['sector_short'] = results_df['sector'].str.split('_').str[1]
    
    # Assign colors and shapes based on sector
    results_df['trip_color'] = results_df['sector'].map(TRIP_COLORS)
    results_df['shape'] = results_df['sector'].map(SECTOR_SHAPES)
    
    # Separate NTMR and Fished
    ntmr_df = results_df[results_df['zone'] == 'NTMR']
    fished_df = results_df[results_df['zone'] == 'Fished']
    
    ntmr_mod = ntmr_df['modularity'].values
    fished_mod = fished_df['modularity'].values
    
    # Create figure with two subplots: boxplot and scatter
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # ============================================================
    # LEFT PANEL: Boxplot with points
    # ============================================================
    ax1 = axes[0]
    
    data_to_plot = [ntmr_mod, fished_mod]
    
    # Boxplot
    bp = ax1.boxplot(data_to_plot, tick_labels=['NTMR', 'Fished'], patch_artist=True, widths=0.5)
    bp['boxes'][0].set_facecolor('#2E8B57')  # seagreen3
    bp['boxes'][1].set_facecolor('#4682B4')  # steelblue4
    bp['boxes'][0].set_alpha(0.5)
    bp['boxes'][1].set_alpha(0.5)
    bp['medians'][0].set_color('black')
    bp['medians'][1].set_color('black')
    bp['medians'][0].set_linewidth(2)
    bp['medians'][1].set_linewidth(2)
    
    # Add points with sector-specific colors and shapes
    # NTMR points
    for _, row in ntmr_df.iterrows():
        x = 1 + np.random.normal(0, 0.04)
        ax1.scatter(x, row['modularity'], 
                   s=100, 
                   facecolor=row['trip_color'], 
                   edgecolor='black', 
                   linewidth=1,
                   marker=row['shape'],
                   zorder=3,
                   alpha=0.9)
    
    # Fished points
    for _, row in fished_df.iterrows():
        x = 2 + np.random.normal(0, 0.04)
        ax1.scatter(x, row['modularity'], 
                   s=100, 
                   facecolor=row['trip_color'], 
                   edgecolor='black', 
                   linewidth=1,
                   marker=row['shape'],
                   zorder=3,
                   alpha=0.9)
    
    ax1.set_ylabel('Modularity', fontsize=12)
    ax1.set_title('Binary Modularity by Zone', fontsize=14, fontweight='bold')
    ax1.set_ylim(0.7, 1.05)
    ax1.set_xlim(0.5, 2.5)
    
    # Add statistics
    stat, pval = stats.mannwhitneyu(ntmr_mod, fished_mod)
    
    if pval < 0.001:
        p_text = 'p < 0.001'
    else:
        p_text = f'p = {pval:.4f}'
    
    textstr = f'NTMR: {ntmr_mod.mean():.3f} ± {ntmr_mod.std():.3f}\nFished: {fished_mod.mean():.3f} ± {fished_mod.std():.3f}\n{p_text}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax1.text(0.05, 0.95, textstr, transform=ax1.transAxes, fontsize=9,
            verticalalignment='top', bbox=props)
    
    # ============================================================
    # RIGHT PANEL: Scatter plot by sector order
    # ============================================================
    ax2 = axes[1]
    
    # Sort by sector number
    results_df['sector_num'] = results_df['sector'].str.extract(r'(\d+)').astype(int)
    results_df = results_df.sort_values(['sector_num', 'zone'])
    
    # Plot NTMR and Fished with lines connecting
    ntmr_sorted = results_df[results_df['zone'] == 'NTMR'].sort_values('sector_num')
    fished_sorted = results_df[results_df['zone'] == 'Fished'].sort_values('sector_num')
    
    ax2.plot(ntmr_sorted['sector_num'], ntmr_sorted['modularity'], 'o-', 
             color='#2E8B57', linewidth=2, markersize=8, label='NTMR', alpha=0.8)
    ax2.plot(fished_sorted['sector_num'], fished_sorted['modularity'], 's-', 
             color='#4682B4', linewidth=2, markersize=8, label='Fished', alpha=0.8)
    
    # Add points with sector-specific colors
    for _, row in ntmr_sorted.iterrows():
        ax2.scatter(row['sector_num'], row['modularity'], 
                   s=100, 
                   facecolor=row['trip_color'], 
                   edgecolor='black', 
                   linewidth=1,
                   marker=SECTOR_SHAPES[row['sector']],
                   zorder=3)
    
    for _, row in fished_sorted.iterrows():
        ax2.scatter(row['sector_num'], row['modularity'], 
                   s=100, 
                   facecolor=row['trip_color'], 
                   edgecolor='black', 
                   linewidth=1,
                   marker=SECTOR_SHAPES[row['sector']],
                   zorder=3)
    
    ax2.set_xlabel('Sector (North to South)', fontsize=12)
    ax2.set_ylabel('Modularity', fontsize=12)
    ax2.set_title('Modularity by Sector Order', fontsize=14, fontweight='bold')
    ax2.set_xticks(range(1, 8))
    ax2.set_xticklabels(['Cape\nGrenville', 'Princess\nCharlotte Bay', 'Cairns', 
                         'Innisfail', 'Townsville', 'Swains', 'Capricorn\nBunker'])
    ax2.set_ylim(0.7, 1.05)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    
    # Save figures
    output_dir = Path("results/figures")
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / "Fig_modularity_with_sector_shapes.png", dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / "Fig_modularity_with_sector_shapes.pdf", bbox_inches='tight')
    
    # Also save individual panels
    fig_boxplot, ax_box = plt.subplots(figsize=(6, 8))
    # Recreate boxplot alone
    bp = ax_box.boxplot(data_to_plot, tick_labels=['NTMR', 'Fished'], patch_artist=True, widths=0.5)
    bp['boxes'][0].set_facecolor('#2E8B57')
    bp['boxes'][1].set_facecolor('#4682B4')
    bp['boxes'][0].set_alpha(0.5)
    bp['boxes'][1].set_alpha(0.5)
    bp['medians'][0].set_color('black')
    bp['medians'][1].set_color('black')
    bp['medians'][0].set_linewidth(2)
    bp['medians'][1].set_linewidth(2)
    
    for _, row in ntmr_df.iterrows():
        x = 1 + np.random.normal(0, 0.04)
        ax_box.scatter(x, row['modularity'], s=100, facecolor=row['trip_color'], 
                      edgecolor='black', linewidth=1, marker=row['shape'], zorder=3, alpha=0.9)
    for _, row in fished_df.iterrows():
        x = 2 + np.random.normal(0, 0.04)
        ax_box.scatter(x, row['modularity'], s=100, facecolor=row['trip_color'], 
                      edgecolor='black', linewidth=1, marker=row['shape'], zorder=3, alpha=0.9)
    
    ax_box.set_ylabel('Modularity', fontsize=12)
    ax_box.set_title('Binary Modularity by Zone', fontsize=14, fontweight='bold')
    ax_box.set_ylim(0.7, 1.05)
    ax_box.set_xlim(0.5, 2.5)
    ax_box.text(0.05, 0.95, textstr, transform=ax_box.transAxes, fontsize=9,
               verticalalignment='top', bbox=props)
    plt.tight_layout()
    plt.savefig(output_dir / "Fig_modularity_boxplot_only.png", dpi=300, bbox_inches='tight')
    
    # Print summary
    logger.info("\n" + "="*70)
    logger.info("SUMMARY STATISTICS")
    logger.info("="*70)
    logger.info(f"\nNTMR (n={len(ntmr_mod)}):")
    logger.info(f"  Mean: {ntmr_mod.mean():.4f}")
    logger.info(f"  SD: {ntmr_mod.std():.4f}")
    logger.info(f"  Values: {', '.join([f'{x:.4f}' for x in sorted(ntmr_mod)])}")
    
    logger.info(f"\nFished (n={len(fished_mod)}):")
    logger.info(f"  Mean: {fished_mod.mean():.4f}")
    logger.info(f"  SD: {fished_mod.std():.4f}")
    logger.info(f"  Values: {', '.join([f'{x:.4f}' for x in sorted(fished_mod)])}")
    
    logger.info(f"\nMann-Whitney U test: p = {pval:.6f}")
    
    logger.info(f"\nFigures saved to: {output_dir}")
    logger.info("  Fig_modularity_with_sector_shapes.png/pdf (combined)")
    logger.info("  Fig_modularity_boxplot_only.png (boxplot only)")

if __name__ == "__main__":
    main()
