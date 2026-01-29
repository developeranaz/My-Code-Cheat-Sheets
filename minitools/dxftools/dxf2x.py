#!/usr/bin/env python3
import ezdxf
import numpy as np
from scipy.interpolate import LinearNDInterpolator, CloughTocher2DInterpolator
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import argparse
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# ARGUMENT PARSER FOR COMMAND LINE FLAGS
# ============================================================================
parser = argparse.ArgumentParser(description='DXF Volume Calculator - Earthwork Cut & Fill Analysis (Termux Edition)')
parser.add_argument('-i', '--input', type=str, default='cloud_boundary_all.dxf', 
                    help='Input DXF file path (default: cloud_boundary_all.dxf)')
parser.add_argument('-f', '--formation', type=float, default=56.0, 
                    help='Formation level in meters (default: 56.0)')
parser.add_argument('-g', '--grid', type=float, default=0.5, 
                    help='Grid cell size in meters (default: 0.5)')
parser.add_argument('-xmin', '--xrange-min', type=float, default=None, 
                    help='X-range minimum for analysis (default: None)')
parser.add_argument('-xmax', '--xrange-max', type=float, default=None, 
                    help='X-range maximum for analysis (default: None)')
parser.add_argument('-p', '--pdf', type=lambda x: x.lower() == 'true', default=True, 
                    help='Generate PDF report (true/false, default: true)')
parser.add_argument('-o', '--output', type=str, default='earthwork_volume_report_grid.pdf', 
                    help='Output PDF file path (default: earthwork_volume_report_grid.pdf)')
parser.add_argument('-ox', '--output-xrange', type=str, default='earthwork_volume_report_grid_xrange.pdf', 
                    help='Output X-range PDF file path (default: earthwork_volume_report_grid_xrange.pdf)')

args = parser.parse_args()

# ============================================================================
# CONFIGURATION FROM ARGUMENTS
# ============================================================================
INPUT_DXF = args.input
FORMATION_LEVEL = args.formation
GRID_SIZE = args.grid
X_RANGE_MIN = args.xrange_min
X_RANGE_MAX = args.xrange_max
GENERATE_PDF = args.pdf
OUTPUT_PDF = args.output
OUTPUT_PDF_XRANGE = args.output_xrange

print("="*60)
print("DXF VOLUME CALCULATOR - TERMUX EDITION")
print("="*60)
print(f"Input DXF:       {INPUT_DXF}")
print(f"Formation Level: {FORMATION_LEVEL} m")
print(f"Grid Size:       {GRID_SIZE} m × {GRID_SIZE} m")
print(f"X Range:         {X_RANGE_MIN} - {X_RANGE_MAX}" if X_RANGE_MIN is not None else "X Range:         Full site")
print(f"Generate PDF:    {GENERATE_PDF}")
print("="*60)

# ============================================================================
# STEP 1: READ DXF AND EXTRACT DATA
# ============================================================================
print("\nReading DXF file...")
doc = ezdxf.readfile(INPUT_DXF)
msp = doc.modelspace()

# Extract spot levels from TEXT and MTEXT entities (boundary points only)
boundary_spot_levels = []
for entity in msp:
    if entity.dxftype() == 'TEXT':
        try:
            x = entity.dxf.insert.x
            y = entity.dxf.insert.y
            z = float(entity.dxf.text.strip())
            boundary_spot_levels.append((x, y, z))
        except:
            pass
    elif entity.dxftype() == 'MTEXT':
        try:
            x = entity.dxf.insert.x
            y = entity.dxf.insert.y
            text = entity.text.strip()
            z = float(text)
            boundary_spot_levels.append((x, y, z))
        except:
            pass

print(f"Found {len(boundary_spot_levels)} boundary spot levels")

# Extract boundary from POLYLINE or LWPOLYLINE
boundary_points = []
for entity in msp:
    if entity.dxftype() in ['POLYLINE', 'LWPOLYLINE']:
        try:
            points = [(p[0], p[1]) for p in entity.get_points()]
            if len(points) > len(boundary_points):
                boundary_points = points
        except:
            pass

# If no polyline found, try to find connected LINE entities
if len(boundary_points) == 0:
    lines = [e for e in msp if e.dxftype() == 'LINE']
    if lines:
        boundary_points = []
        current_line = lines[0]
        boundary_points.append((current_line.dxf.start.x, current_line.dxf.start.y))
        boundary_points.append((current_line.dxf.end.x, current_line.dxf.end.y))
        used = {0}
        
        while len(used) < len(lines):
            last_point = boundary_points[-1]
            found = False
            for i, line in enumerate(lines):
                if i in used:
                    continue
                start = (line.dxf.start.x, line.dxf.start.y)
                end = (line.dxf.end.x, line.dxf.end.y)
                
                if np.allclose(start, last_point, atol=0.1):
                    boundary_points.append(end)
                    used.add(i)
                    found = True
                    break
                elif np.allclose(end, last_point, atol=0.1):
                    boundary_points.append(start)
                    used.add(i)
                    found = True
                    break
            
            if not found:
                break

print(f"Found boundary with {len(boundary_points)} points")

# ============================================================================
# STEP 2: CLEAN AND PREPARE BOUNDARY DATA
# ============================================================================
print("Cleaning boundary data...")

# Remove duplicate spot levels
spot_levels_unique = []
seen = set()
for x, y, z in boundary_spot_levels:
    key = (round(x, 2), round(y, 2))
    if key not in seen:
        seen.add(key)
        spot_levels_unique.append((x, y, z))

boundary_spot_levels = spot_levels_unique

# Remove outliers (Z values beyond 3 standard deviations)
if len(boundary_spot_levels) > 0:
    z_values = [z for _, _, z in boundary_spot_levels]
    z_mean = np.mean(z_values)
    z_std = np.std(z_values)
    boundary_spot_levels = [(x, y, z) for x, y, z in boundary_spot_levels 
                           if abs(z - z_mean) <= 3 * z_std]

print(f"After cleaning: {len(boundary_spot_levels)} boundary spot levels")

# Create boundary polygon
boundary_polygon = Polygon(boundary_points)

# ============================================================================
# STEP 3: CREATE GRID POINTS
# ============================================================================
print(f"Creating grid with cell size {GRID_SIZE}m x {GRID_SIZE}m...")

# Get boundary extents
boundary_array = np.array(boundary_points)
x_min, x_max = boundary_array[:, 0].min(), boundary_array[:, 0].max()
y_min, y_max = boundary_array[:, 1].min(), boundary_array[:, 1].max()

# Create grid
x_grid = np.arange(x_min, x_max + GRID_SIZE, GRID_SIZE)
y_grid = np.arange(y_min, y_max + GRID_SIZE, GRID_SIZE)

print(f"Grid dimensions: {len(x_grid)} x {len(y_grid)} = {len(x_grid) * len(y_grid)} potential grid points")

# Create grid corner points (we'll calculate volumes cell by cell)
grid_corners = []
for i in range(len(x_grid)):
    for j in range(len(y_grid)):
        x = x_grid[i]
        y = y_grid[j]
        
        # Check if point is inside boundary
        if boundary_polygon.contains(Point(x, y)):
            grid_corners.append((x, y))

print(f"Grid corners inside boundary: {len(grid_corners)}")

# ============================================================================
# STEP 4: INTERPOLATE Z VALUES FOR GRID CORNERS
# ============================================================================
print("Interpolating elevations for grid corners using advanced methods...")
print("This may take time for accuracy - please wait...")

# Prepare boundary spot level data
if len(boundary_spot_levels) > 0:
    spot_array = np.array(boundary_spot_levels)
    spot_xy = spot_array[:, :2]
    spot_z = spot_array[:, 2]
    
    # Use multiple interpolation methods and combine for better accuracy
    print("  - Using Clough-Tocher cubic interpolation...")
    ct_interp = CloughTocher2DInterpolator(spot_xy, spot_z)
    
    print("  - Using Linear interpolation...")
    linear_interp = LinearNDInterpolator(spot_xy, spot_z)
    
    # Interpolate for each grid corner
    grid_points_with_z = []
    
    for idx, (x, y) in enumerate(grid_corners):
        if (idx + 1) % 1000 == 0:
            print(f"  - Processed {idx + 1}/{len(grid_corners)} grid points...")
        
        # Get elevation using cubic interpolation (primary method)
        z_ct = ct_interp(x, y)
        
        # If cubic fails (returns nan), use linear interpolation
        if np.isnan(z_ct):
            z_linear = linear_interp(x, y)
            if np.isnan(z_linear):
                # Last resort: use inverse distance weighting of 5 nearest points
                distances = np.sqrt((spot_xy[:, 0] - x)**2 + (spot_xy[:, 1] - y)**2)
                nearest_indices = np.argsort(distances)[:5]
                nearest_distances = distances[nearest_indices]
                nearest_z = spot_z[nearest_indices]
                
                # Avoid division by zero
                nearest_distances = np.maximum(nearest_distances, 1e-10)
                
                # Inverse distance weighting
                weights = 1.0 / nearest_distances
                z_est = np.sum(weights * nearest_z) / np.sum(weights)
            else:
                z_est = z_linear
        else:
            z_est = z_ct
        
        grid_points_with_z.append((x, y, float(z_est)))
    
    print(f"Successfully interpolated elevations for {len(grid_points_with_z)} grid corners")

# ============================================================================
# STEP 5: CREATE GRID CELLS AND CALCULATE VOLUMES
# ============================================================================
print("Creating grid cells and calculating volumes...")

# Create a dictionary for quick lookup of grid point elevations
grid_elevation_dict = {(round(x, 6), round(y, 6)): z for x, y, z in grid_points_with_z}

def get_elevation(x, y):
    """Get elevation for a grid point"""
    key = (round(x, 6), round(y, 6))
    return grid_elevation_dict.get(key, None)

# Create grid cells
grid_cells = []
cut_volume = 0.0
fill_volume = 0.0
total_area = 0.0

for i in range(len(x_grid) - 1):
    for j in range(len(y_grid) - 1):
        # Define cell corners
        x1, x2 = x_grid[i], x_grid[i + 1]
        y1, y2 = y_grid[j], y_grid[j + 1]
        
        # Cell corners (bottom-left, bottom-right, top-right, top-left)
        corners = [
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2)
        ]
        
        # Check if cell center is inside boundary
        cell_center = Point((x1 + x2) / 2, (y1 + y2) / 2)
        if not boundary_polygon.contains(cell_center):
            continue
        
        # Get elevations for all corners
        elevations = []
        valid_cell = True
        for cx, cy in corners:
            elev = get_elevation(cx, cy)
            if elev is None:
                valid_cell = False
                break
            elevations.append(elev)
        
        if not valid_cell:
            continue
        
        # Calculate average elevation of cell
        avg_elevation = np.mean(elevations)
        
        # Cell area
        cell_area = GRID_SIZE * GRID_SIZE
        
        # Volume calculation
        height_diff = avg_elevation - FORMATION_LEVEL
        cell_volume = cell_area * height_diff
        
        # Classify as cut or fill
        if cell_volume > 0:
            cell_type = 'cut'
            cut_volume += cell_volume
        else:
            cell_type = 'fill'
            fill_volume += abs(cell_volume)
        
        total_area += cell_area
        
        grid_cells.append({
            'corners': corners,
            'elevations': elevations,
            'avg_elevation': avg_elevation,
            'type': cell_type,
            'volume': abs(cell_volume),
            'area': cell_area
        })

net_volume = cut_volume - fill_volume

print(f"\nTotal grid cells created: {len(grid_cells)}")
print(f"\n{'='*60}")
print(f"GRID-BASED VOLUME RESULTS")
print(f"{'='*60}")
print(f"Grid Size:   {GRID_SIZE}m x {GRID_SIZE}m")
print(f"Cut Volume:  {cut_volume:,.2f} m³")
print(f"Fill Volume: {fill_volume:,.2f} m³")
print(f"Net Volume:  {net_volume:,.2f} m³ ({'CUT' if net_volume > 0 else 'FILL'})")
print(f"Total Area:  {total_area:,.2f} m²")
print(f"Grid Cells:  {len(grid_cells):,}")
print(f"{'='*60}\n")

# ============================================================================
# STEP 6: GENERATE 2D CUT/FILL MAP (PDF)
# ============================================================================
if GENERATE_PDF:
    print("Generating 2D grid-based cut/fill map...")

    # Set matplotlib to use Agg backend for Termux compatibility
    plt.switch_backend('Agg')
    
    fig = plt.figure(figsize=(24, 18))
    ax = fig.add_subplot(111)

    # Plot cut cells in red
    cut_patches = []
    for cell in grid_cells:
        if cell['type'] == 'cut':
            polygon_coords = np.array(cell['corners'])
            polygon = plt.Polygon(polygon_coords, closed=True)
            cut_patches.append(polygon)

    if cut_patches:
        cut_collection = PatchCollection(cut_patches, facecolor='red', alpha=0.6, edgecolor='darkred', linewidth=0.3)
        ax.add_collection(cut_collection)

    # Plot fill cells in blue
    fill_patches = []
    for cell in grid_cells:
        if cell['type'] == 'fill':
            polygon_coords = np.array(cell['corners'])
            polygon = plt.Polygon(polygon_coords, closed=True)
            fill_patches.append(polygon)

    if fill_patches:
        fill_collection = PatchCollection(fill_patches, facecolor='blue', alpha=0.6, edgecolor='darkblue', linewidth=0.3)
        ax.add_collection(fill_collection)

    # Plot boundary
    ax.plot(boundary_array[:, 0], boundary_array[:, 1], 'k-', linewidth=2.5, label='Site Boundary', zorder=100)

    # Plot original boundary spot levels with labels
    for x, y, z in boundary_spot_levels:
        ax.plot(x, y, 'ko', markersize=5, zorder=101)
        ax.text(x, y, f'{z:.2f}', fontsize=6, ha='center', va='bottom', 
                bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.8, edgecolor='black', linewidth=0.5),
                zorder=102)

    # Plot grid points (sample - not all to avoid clutter)
    sample_rate = max(1, len(grid_points_with_z) // 500)  # Show maximum 500 grid points
    for idx, (x, y, z) in enumerate(grid_points_with_z):
        if idx % sample_rate == 0:
            ax.plot(x, y, 'g.', markersize=2, alpha=0.5)

    # Add grid lines
    for x in x_grid:
        ax.axvline(x=x, color='gray', linewidth=0.2, alpha=0.3)
    for y in y_grid:
        ax.axhline(y=y, color='gray', linewidth=0.2, alpha=0.3)

    # Formatting
    ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
    ax.set_aspect('equal')
    ax.set_xlabel('X Coordinate (m)', fontsize=16, fontweight='bold')
    ax.set_ylabel('Y Coordinate (m)', fontsize=16, fontweight='bold')
    ax.set_title(f'Grid-Based Earthwork Cut & Fill Analysis\nGrid Size: {GRID_SIZE}m × {GRID_SIZE}m | Formation Level: {FORMATION_LEVEL}m', 
                 fontsize=20, fontweight='bold', pad=25)

    # Legend
    red_patch = mpatches.Patch(color='red', alpha=0.6, label=f'Cut: {cut_volume:,.2f} m³')
    blue_patch = mpatches.Patch(color='blue', alpha=0.6, label=f'Fill: {fill_volume:,.2f} m³')
    black_line = mpatches.Patch(color='black', label='Site Boundary')
    yellow_marker = mpatches.Patch(color='yellow', label='Original Spot Levels')
    green_marker = mpatches.Patch(color='green', label='Grid Points (sample)')

    ax.legend(handles=[red_patch, blue_patch, black_line, yellow_marker, green_marker], 
              loc='upper right', fontsize=12, framealpha=0.95)

    # Add detailed summary text box
    textstr = f"""GRID-BASED VOLUME SUMMARY
{'─'*40}
Grid Size:          {GRID_SIZE:.2f} m × {GRID_SIZE:.2f} m
Formation Level:    {FORMATION_LEVEL:.2f} m
{'─'*40}
Cut Volume:         {cut_volume:>15,.2f} m³
Fill Volume:        {fill_volume:>15,.2f} m³
Net Volume:         {net_volume:>15,.2f} m³
Status:             {('CUT' if net_volume > 0 else 'FILL'):>15}
{'─'*40}
Total Area:         {total_area:>15,.2f} m²
Grid Cells:         {len(grid_cells):>15,}
Boundary Spots:     {len(boundary_spot_levels):>15,}
Grid Corners:       {len(grid_points_with_z):>15,}
{'─'*40}
Method: Grid-based volume calculation
Interpolation: Clough-Tocher cubic
Grid points calculated from boundary spots
{'─'*40}"""

    props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.97, edgecolor='black', linewidth=2.5)
    ax.text(0.015, 0.985, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace', bbox=props, zorder=200)

    plt.tight_layout()

    # Save as PDF with high quality
    print("Saving PDF report (high quality)...")
    with PdfPages(OUTPUT_PDF) as pdf:
        pdf.savefig(fig, dpi=300, bbox_inches='tight')
        
        d = pdf.infodict()
        d['Title'] = 'Grid-Based Earthwork Volume Analysis Report'
        d['Author'] = 'DXF Volume Calculator - Termux Edition'
        d['Subject'] = f'Cut & Fill Analysis - Grid Method - Formation Level {FORMATION_LEVEL}m'
        d['Keywords'] = 'Earthwork, Cut, Fill, Volume, Grid, Civil Engineering, Termux'

    plt.close()

    print(f"PDF report saved: {OUTPUT_PDF}")
else:
    print("PDF generation skipped (GENERATE_PDF = False)")

# ============================================================================
# STEP 7: X-RANGE ANALYSIS (OPTIONAL)
# ============================================================================
if X_RANGE_MIN is not None and X_RANGE_MAX is not None:
    print(f"\n{'='*60}")
    print(f"X-RANGE ANALYSIS: X = {X_RANGE_MIN} to {X_RANGE_MAX}")
    print(f"{'='*60}")
    
    # Filter cells within X range
    xrange_cells = []
    for cell in grid_cells:
        corners = cell['corners']
        x_coords = [c[0] for c in corners]
        
        if min(x_coords) >= X_RANGE_MIN and max(x_coords) <= X_RANGE_MAX:
            xrange_cells.append(cell)
    
    # Calculate volumes for X range
    xrange_cut_volume = sum(c['volume'] for c in xrange_cells if c['type'] == 'cut')
    xrange_fill_volume = sum(c['volume'] for c in xrange_cells if c['type'] == 'fill')
    xrange_net_volume = xrange_cut_volume - xrange_fill_volume
    xrange_area = sum(c['area'] for c in xrange_cells)
    
    print(f"Cut Volume:  {xrange_cut_volume:,.2f} m³")
    print(f"Fill Volume: {xrange_fill_volume:,.2f} m³")
    print(f"Net Volume:  {xrange_net_volume:,.2f} m³ ({'CUT' if xrange_net_volume > 0 else 'FILL'})")
    print(f"Total Area:  {xrange_area:,.2f} m²")
    print(f"Grid Cells:  {len(xrange_cells):,}")
    print(f"{'='*60}\n")
    
    if GENERATE_PDF:
        # Generate X-range map
        plt.switch_backend('Agg')
        fig = plt.figure(figsize=(24, 18))
        ax = fig.add_subplot(111)
        
        # Plot cut cells
        cut_patches = []
        for cell in xrange_cells:
            if cell['type'] == 'cut':
                polygon_coords = np.array(cell['corners'])
                polygon = plt.Polygon(polygon_coords, closed=True)
                cut_patches.append(polygon)
        
        if cut_patches:
            cut_collection = PatchCollection(cut_patches, facecolor='red', alpha=0.6, edgecolor='darkred', linewidth=0.3)
            ax.add_collection(cut_collection)
        
        # Plot fill cells
        fill_patches = []
        for cell in xrange_cells:
            if cell['type'] == 'fill':
                polygon_coords = np.array(cell['corners'])
                polygon = plt.Polygon(polygon_coords, closed=True)
                fill_patches.append(polygon)
        
        if fill_patches:
            fill_collection = PatchCollection(fill_patches, facecolor='blue', alpha=0.6, edgecolor='darkblue', linewidth=0.3)
            ax.add_collection(fill_collection)
        
        # Plot boundary
        ax.plot(boundary_array[:, 0], boundary_array[:, 1], 'k--', linewidth=2, alpha=0.5, label='Site Boundary')
        
        # Plot X-range limits
        ax.axvline(x=X_RANGE_MIN, color='green', linewidth=3, linestyle='--', label='X Range Limits')
        ax.axvline(x=X_RANGE_MAX, color='green', linewidth=3, linestyle='--')
        
        # Plot original spot levels within range
        for x, y, z in boundary_spot_levels:
            if X_RANGE_MIN <= x <= X_RANGE_MAX:
                ax.plot(x, y, 'ko', markersize=5)
                ax.text(x, y, f'{z:.2f}', fontsize=6, ha='center', va='bottom',
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.8, edgecolor='black', linewidth=0.5))
        
        # Add grid lines within X range
        for x in x_grid:
            if X_RANGE_MIN <= x <= X_RANGE_MAX:
                ax.axvline(x=x, color='gray', linewidth=0.2, alpha=0.3)
        for y in y_grid:
            ax.axhline(y=y, color='gray', linewidth=0.2, alpha=0.3)
        
        ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
        ax.set_aspect('equal')
        ax.set_xlabel('X Coordinate (m)', fontsize=16, fontweight='bold')
        ax.set_ylabel('Y Coordinate (m)', fontsize=16, fontweight='bold')
        ax.set_title(f'Grid-Based Earthwork Cut & Fill Analysis - X Range\nX: {X_RANGE_MIN}m to {X_RANGE_MAX}m | Grid: {GRID_SIZE}m × {GRID_SIZE}m | Formation: {FORMATION_LEVEL}m', 
                    fontsize=20, fontweight='bold', pad=25)
        
        red_patch = mpatches.Patch(color='red', alpha=0.6, label=f'Cut: {xrange_cut_volume:,.2f} m³')
        blue_patch = mpatches.Patch(color='blue', alpha=0.6, label=f'Fill: {xrange_fill_volume:,.2f} m³')
        green_line = mpatches.Patch(color='green', label='X Range Limits')
        
        ax.legend(handles=[red_patch, blue_patch, green_line], loc='upper right', fontsize=12, framealpha=0.95)
        
        textstr = f"""X-RANGE GRID VOLUME SUMMARY
{'─'*40}
X Range:            {X_RANGE_MIN:.2f} - {X_RANGE_MAX:.2f} m
Grid Size:          {GRID_SIZE:.2f} m × {GRID_SIZE:.2f} m
Formation Level:    {FORMATION_LEVEL:.2f} m
{'─'*40}
Cut Volume:         {xrange_cut_volume:>15,.2f} m³
Fill Volume:        {xrange_fill_volume:>15,.2f} m³
Net Volume:         {xrange_net_volume:>15,.2f} m³
Status:             {('CUT' if xrange_net_volume > 0 else 'FILL'):>15}
{'─'*40}
Total Area:         {xrange_area:>15,.2f} m²
Grid Cells:         {len(xrange_cells):>15,}
{'─'*40}"""
        
        props = dict(boxstyle='round', facecolor='lightgreen', alpha=0.97, edgecolor='black', linewidth=2.5)
        ax.text(0.015, 0.985, textstr, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', fontfamily='monospace', bbox=props)
        
        plt.tight_layout()
        
        print("Saving X-range PDF report...")
        with PdfPages(OUTPUT_PDF_XRANGE) as pdf:
            pdf.savefig(fig, dpi=300, bbox_inches='tight')
            
            d = pdf.infodict()
            d['Title'] = f'Grid-Based Earthwork Analysis - X Range {X_RANGE_MIN}-{X_RANGE_MAX}m'
            d['Author'] = 'DXF Volume Calculator - Termux Edition'
            d['Subject'] = f'Cut & Fill Analysis - X Range - Grid Method'
            d['Keywords'] = 'Earthwork, Cut, Fill, Volume, Grid, X-Range, Termux'
        
        plt.close()
        print(f"X-Range PDF report saved: {OUTPUT_PDF_XRANGE}")
    else:
        print("X-Range PDF generation skipped (GENERATE_PDF = False)")

print("\n" + "="*60)
print("GRID-BASED PROCESSING COMPLETE")
print("="*60)
print(f"\nConfiguration:")
print(f"  - Input DXF:     {INPUT_DXF}")
print(f"  - Formation:     {FORMATION_LEVEL} m")
print(f"  - Grid Size:     {GRID_SIZE} m × {GRID_SIZE} m")
print(f"  - Generate PDF:  {GENERATE_PDF}")
print(f"\nGenerated files:")
if GENERATE_PDF:
    print(f"  - {OUTPUT_PDF}")
if X_RANGE_MIN is not None and X_RANGE_MAX is not None:
    if GENERATE_PDF:
        print(f"  - {OUTPUT_PDF_XRANGE}")
print("="*60)
print(f"\nMethod: Grid-based volume calculation ({GRID_SIZE}m × {GRID_SIZE}m)")
print(f"Interpolation: Clough-Tocher cubic with linear fallback")
print(f"Total grid cells analyzed: {len(grid_cells):,}")
print("="*60)
print("\nUSAGE EXAMPLES:")
print("  Basic usage:")
print("    python script.py")
print("\n  With custom parameters:")
print("    python script.py -i input.dxf -f 55.5 -g 1.0 -o output.pdf")
print("\n  With X-range analysis:")
print("    python script.py -xmin 0 -xmax 200 -ox output_xrange.pdf")
print("\n  All flags:")
print("    python script.py -i cloud.dxf -f 56.0 -g 0.5 -xmin 0 -xmax 200 -p true -o report.pdf -ox report_x.pdf")
print("="*60)
