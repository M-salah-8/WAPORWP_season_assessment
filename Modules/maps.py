import os
import geopandas as gpd
import rasterio
import rasterio.mask
import matplotlib.patches as patches
import numpy as np

from matplotlib import pyplot as plt
# change the directory to where the modules are saved

class Maps():
  def __init__(self):
    self.master_dr = os.path.split(os.getcwd())[0]
    self.maps_dr = os.path.join(self.master_dr, "Data/maps")
    self.charts_dr = os.path.join(self.master_dr, "Data/charts")
    os.makedirs(self.charts_dr, exist_ok=True)
    self.map_meta = {
      'biomasstargetspots': {
        'title': 'Biomass Target Spots [-]',
        'cbar_lable': 'Biomass Target Spots [-]',
        'cmap': 'Greens',
      },
      'wpbtargetspots': {
        'title': 'WPb Target Spots [-]',
        'cbar_lable': 'WPb Target Spots [-]',
        'cmap': 'Greens',
      },
      'biomasslowspots': {
        'title': 'Biomass low Spots [-]',
        'cbar_lable': 'Biomass low Spots [-]',
        'cmap': 'Reds',
      },
      'wpblowspots': {
        'title': 'WPb Low Spots [-]',
        'cbar_lable': 'WPb Low Spots [-]',
        'cmap': 'Reds',
      },
      'uniformity': {
        'title': 'Uniformity [%]',
        'cbar_lable': 'Uniformity [%]',
        'cmap': 'Reds',
      },
      'rwd': {
        'title': 'Relative water Deficit [-]',
        'cbar_lable': 'Relative water Deficit [-]',
        'cmap': 'Reds',
      },
      'aeti': {
        'title': 'Actual evapotranspiration [mm/season]',
        'cbar_lable': 'ETa [mm/season]',
        'cmap': 'jet_r',
      },
      't': {
        'title': 'Transpiration [mm/season]',
        'cbar_lable': 'T [mm/season]',
        'cmap': 'jet_r',
      },
      'ret': {
        'title': 'Reference evapotranspiration [mm/season]',
        'cbar_lable': 'REF [mm/season]',
        'cmap': 'jet_r',
      },
      'pcp': {
        'title': 'precipitation [mm/season]',
        'cbar_lable': 'precipitation [mm/season]',
        'cmap': 'jet_r',
      },
      'npp': {
        'title': 'Net primary production [gC/m2/season]',
        'cbar_lable': 'NPP [gC/m2/season]',
        'cmap': 'jet_r',
      },
      'bf': {
        'title': 'Beneficial fraction [-]',
        'cbar_lable': 'BF [-]',
        'cmap': 'RdYlGn',
      },
      'adequacy': {
        'title': 'Adequacy [-]',
        'cbar_lable': 'Adequacy [-]',
        'cmap': 'RdYlGn',
      },
      'biomass': {
        'title': 'Above ground biomass [ton/ha/season]',
        'cbar_lable': 'Above ground biomass [ton/ha/season]',
        'cmap': 'RdYlGn',
      },
      'yield': {
        'title': 'Crop yield [ton/ha/season]',
        'cbar_lable': 'Crop yield [ton/ha/season]',
        'cmap': 'RdYlGn',
      },
      'wpb': {
        'title': 'Biomass water productivity [kg/m3]',
        'cbar_lable': 'WPb [kg/m3]',
        'cmap': 'RdYlGn',
      },
      'wpy': {
        'title': 'crop water productivity [kg/m3]',
        'cbar_lable': 'crop water productivity [kg/m3]',
        'cmap': 'RdYlGn',
      },
      'biomassgap': {
        'title': 'Biomass gaps [ton/ha/season]',
        'cbar_lable': 'Biomass gaps [ton/ha/season]',
        'cmap': 'RdYlGn',
      },
      'wpbgap': {
        'title': 'Biomass WP gaps [m3/season]',
        'cbar_lable': 'Biomass WP gaps [m3/season]',
        'cmap': 'RdYlGn',
      },
      'yieldgap': {
        'title': 'crop yield gaps [ton/ha/season]',
        'cbar_lable': 'crop yield gaps [ton/ha/season]',
        'cmap': 'RdYlGn',
      },
      'wpygap': {
        'title': 'crop WP gaps [m3/season]',
        'cbar_lable': 'crop WP gaps [m3/season]',
        'cmap': 'RdYlGn',
      },
      }
    
  def draw_north_arrow(self, ax, arrow_scale):
    ax.set_aspect('equal', adjustable='box')
    ax_length = ax.get_xlim()[1]-ax.get_xlim()[0]
    shape_length = ax_length * arrow_scale
    padding_length = ((1-arrow_scale)/2) * ax_length
    base_start= ax.get_xlim()[0] + padding_length
    base_end = base_start + shape_length
    height_start= ax.get_ylim()[0] + padding_length
    height_end = height_start + shape_length
    width = shape_length
    height = shape_length
    x_bottom_left ,y_bottom_left = base_start, height_start
    x_top, y_top = width / 2 + base_start, height_end
    x_bottom_right, y_bottom_right = base_end, height_start
    x_mid, y_mid = width / 2 + base_start, height / 4 + height_start
    polygon = patches.Polygon([[x_bottom_left, y_bottom_left], [x_top, y_top], [x_bottom_right, y_bottom_right],[x_mid,y_mid]],
                                facecolor= 'goldenrod', edgecolor= 'black', linewidth= shape_length*3)
    ax.add_patch(polygon)    
    text_x = width / 2 + base_start
    text_y = height / 2.2 + height_start
    ax.text(text_x, text_y, 'N', ha='center', va='center', fontsize=shape_length*20, fontweight='bold', color= 'black')
    ax.set_axis_off()

  def main_map(self, gdf, id_column):
    # Plot the raster map
    fig, map = plt.subplots(facecolor= '0.9')
    gdf.plot(
      ax= map,
      edgecolor= 'black',
      cmap= 'tab20b',
      column= id_column,
          )
    for _, row in gdf.iterrows():
        x,y= row['geometry'].centroid.x, row['geometry'].centroid.y
        map.text(x, y, row[id_column], ha='center', va='center', fontweight='bold', color='black')
    plt.yticks(rotation= 90)
    yb,ye = map.get_ylim()
    xb,xe = map.get_xlim()
    y = ye - yb
    x = xe - xb
    y1,y2,y3 = yb + y*2/8, yb + y*4/8, yb + y*6/8
    x1,x2,x3 = xb + x*2/8, xb + x*4/8, xb + x*6/8
    map.set_yticks([y1,y2,y3],[f"{y1:.2f}",f"{y2:.2f}",f"{y3:.2f}"])
    map.set_xticks([x1,x2,x3],[f"{x1:.2f}",f"{x2:.2f}",f"{x3:.2f}"])
    map.set_xlabel('Longitude ($^{\circ}$ East)', fontsize=14)  # add axes label
    map.set_ylabel('Latitude ($^{\circ}$ North)', fontsize=14)
    map.set_title(r'Field ID/name', fontsize=16, loc='center')
    self.draw_north_arraw(map, 0.1, 0.05)
    map.grid()
    plt.savefig(os.path.join(self.maps_dr, "main_map.png"))

  def data_maps(self, tifs, gdf, tifs_dr):
    for tif in tifs:
      data_name = os.path.basename(tif).split('.')[0].split('_')[1].strip().lower()
      tifs_dr = os.path.join(self.maps_dr, tifs_dr)
      os.makedirs(tifs_dr, exist_ok=True)
      src = rasterio.open(tif)
      array = src.read(1)
      x0, y0, x1, y1 = src.bounds
      mosiac =[
        ['map', 'by_area'],
        ['map', 'north_arrow'],
      ]
      fig, axs = plt.subplot_mosaic(mosaic=mosiac,facecolor= '0.9',
                    gridspec_kw={'width_ratios':[10,3]})
      map_plot = axs['map'].imshow(array, cmap=self.map_meta[data_name]['cmap'],
              vmin=np.nanmin(array), vmax=np.nanmax(array),
              extent=[x0,x1,y0,y1])
      gdf.boundary.plot(ax= axs['map'], color= 'red',)
      fig.colorbar(map_plot, shrink=0.75,
                  label=self.map_meta[data_name]['cbar_lable'],
                  ax=axs['map'],
                  pad= 0.05,
                  aspect=50)
      yb,ye = axs['map'].get_ylim()
      xb,xe = axs['map'].get_xlim()
      y = ye - yb
      x = xe - xb
      y1,y2,y3 = yb + y*2/8, yb + y*4/8, yb + y*6/8
      x1,x2,x3 = xb + x*2/8, xb + x*4/8, xb + x*6/8
      axs['map'].set_yticks([y1,y2,y3],[f"{y1:.2f}",f"{y2:.2f}",f"{y3:.2f}"])
      axs['map'].set_xticks([x1,x2,x3],[f"{x1:.2f}",f"{x2:.2f}",f"{x3:.2f}"])
      axs['map'].tick_params(axis='y', rotation=90)
      axs['map'].set_xlabel('Longitude ($^{\circ}$ East)', fontsize=14)  # add axes label
      axs['map'].set_ylabel('Latitude ($^{\circ}$ North)', fontsize=14)
      axs['map'].set_title(self.map_meta[data_name]['title'], fontsize=14, loc='center', pad= 10)
      self.draw_north_arrow(axs['north_arrow'], 0.5)
      axs['map'].grid()
      gdf.plot(
        ax= axs['by_area'], column= data_name,
        edgecolor= 'black', legend=True,
        cmap= self.map_meta[data_name]['cmap'],
        legend_kwds={'location':'bottom'})
      axs['by_area'].set_xticks([])
      axs['by_area'].set_yticks([])
      axs['by_area'].set_title('By Area', fontsize=10, loc='center')
      plt.savefig(os.path.join(tifs_dr, f"{data_name}.png"))

  def data_bar_charts(self, gdf, columns, id_column, c_dr):
    data_charts_dr = os.path.join(self.charts_dr,f'{c_dr}/by data')
    os.makedirs(data_charts_dr, exist_ok=True)
    if 'season' in c_dr:
      columns = gdf.drop([id_column, 'geometry', 'uniformity class'],axis= 1).columns
    else:
      columns = gdf.drop([id_column, 'geometry'],axis= 1).columns
    for column in columns[:]:
      plt.bar(gdf[id_column], gdf[column])
      plt.title(self.map_meta[column]['title'], fontsize=16, loc='center')
      plt.xlabel(r'Field Name/ID', fontsize=14)  # add axes label
      plt.ylabel(self.map_meta[column]['cbar_lable'], fontsize=14)
      plt.grid(axis='y', color='black', linestyle= '--')
      plt.savefig(os.path.join(data_charts_dr, f"{column}.png"))
      plt.show()

  def area_bar_charts(self, gdf, max_data, c_dr):
    area_charts_dr = os.path.join(self.charts_dr,f'{c_dr}/by area')
    os.makedirs(area_charts_dr, exist_ok=True)
    if 'season' in c_dr:
      gdf = gdf.drop(['geometry', 'uniformity class'],axis= 1)
    else:
      gdf = gdf.drop(['geometry'],axis= 1)
    for _,row in gdf.iterrows():
      name = row[0]
      ratios = row[1:]/max_data * 100
      _, ax = plt.subplots(layout= 'constrained')
      ratios.plot.bar(ax=ax)
      ax.set_ylabel("percentage from max")
      ax.set_xlabel("data", weight= 'bold')
      ax.set_title(f'Area {name}', pad=10, fontsize= 20, weight= 'bold')
      ax.set_ybound(upper=130)
      for idx, p in enumerate(ax.patches):
        if np.isnan(max_data[idx]):
          continue
        bar_max = round(max_data[idx],2)
        height = p.get_height()
        # print(height)
        ax.text(p.get_x()+p.get_width()/2.,
                105,
                bar_max,
                weight= 'bold',
                rotation= 'vertical',
                backgroundcolor= 'yellow',
                ha= "center")
      ax.grid(axis='y', color='black', linestyle= '--')
      ax.set_yticks([0,20,40,60,80,100])
      ax.text(ax.get_xlim()[0],
                135,
                'Bar Max',
                weight= 'bold',
                rotation= 'horizontal',
                backgroundcolor= 'yellow',
                ha= "center")
      plt.savefig(os.path.join(area_charts_dr, f"{name}.png"))