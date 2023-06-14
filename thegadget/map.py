import os
import time
import requests
import logging
from bs4 import BeautifulSoup
#from game import Data
from __version__ import PROGNAME
from utils import Data

import osmnx as ox
import osmnx

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


def query_place(place_name):

    # Specify the name that is used to seach for the data
    #place_name = "Hanford Site" # "Wendover Airfield, Utah" # "Los Alamos National Laboratory" #Malaysia
    #osmid = "680079366"

    #plt, ax = ox.plot_graph(ox.graph_from_place(place_name), node_size=0, node_color="red", show=True)

    #G = ox.graph_from_address('place_name', network_type='drive')
    #ox.plot_graph(G)

    #plt.show()

    #city = ox.geocode_to_gdf('Berkeley, California')
    #print(city)

    #G = ox.graph_from_xml("/home/mic/Desktop/14064419.xml")
    #ox.plot_graph(G)


    #%matplotlib inline

    # Fetch OSM street network from the location
    try:
        graph = ox.graph_from_place(place_name, simplify=True, network_type="drive")
        #graph = ox.graph_from_address(place_name, simplify=True)
    except ValueError:
        return
    print(type(graph))

    area = ox.geocode_to_gdf(place_name) # returns a GeoDataFrame based on the specified place name query
    #area = ox.geocode_to_gdf(osmid, by_osmid=True) # returns a GeoDataFrame based on the specified place name query
    print(type(area))

    buildings = ox.geometries_from_place(place_name, tags={'building':True}) # Retrieve buildings from the area:

    #print(buildings.columns)
    print(type(buildings))
    print(len(buildings))

    #restaurants = ox.geometries_from_place(place_name, 
    #                                  tags={"amenity": "restaurant"}
    #                                 )

    nodes, edges = ox.graph_to_gdfs(graph)

    fig, ax = plt.subplots()

    # Plot the footprint
    area.plot(ax=ax, facecolor='black')

    # Plot street edges
    edges.plot(ax=ax, linewidth=1, edgecolor='#BC8F8F')

    # Plot buildings
    buildings.plot(ax=ax, facecolor='green', alpha=0.7)

    # Plot restaurants
    #restaurants.plot(ax=ax, color='green', alpha=0.7, markersize=10)
    #plt.tight_layout()
    plt.show()

def query_place2():

    # Adjust OSMnx settings for reduced data usage
    ox.config(log_console=True, use_cache=True)

    # Define the geographical area (bounding box around the coordinates)
    dist = 2500  # Distance in meters from the center point

    # Create the street network graph
    north, south, east, west = ox.utils_geo.bbox_from_point((35.8789, -106.3035), dist=dist)

    G = ox.graph_from_bbox(north, south, east, west, network_type='all_private')
    #G = ox.graph_from_point((35.8789, -106.3035), dist=2500, network_type='drive', simplify=True)

    # Retrieve the building footprints within the specified area
    #buildings = ox.footprints.footprints_from_point((35.8789, -106.3035), dist=500, footprint_type='all', retain_invalid=False)
    #buildings = ox.geometries_from_point((35.8789, -106.3035), dist=500, tags={'building': True})
    buildings = ox.geometries_from_bbox(north, south, east, west, tags={'building': True})
    
    G.add_nodes_from(buildings)

    # Plot the street network and buildings together
    fig, ax = ox.plot_graph(ox.project_graph(G), node_size=0, edge_linewidth=0.5, bgcolor='w', show=False, close=False)

    # Plot the buildings
    gpd.plotting.plot_dataframe(buildings, ax=ax, facecolor='red', alpha=1)

    # Save the resulting map as an image file
    fig.savefig('osmnx_map.png', dpi=300)
    plt.show()

def query_place3():

    ox.config(log_console=True, use_cache=True)

    dist = 2500
    place_name = "Los Alamos"

    # Specify the building types to filter
    #building_types = ['industrial', 'government']
    building_types = True

    north, south, east, west = ox.utils_geo.bbox_from_point((35.8789, -106.3035), dist=dist)
    G = ox.graph_from_bbox(north, south, east, west, network_type='drive', simplify=True)

    #tags={'building': building_types}   

    area = ox.geocode_to_gdf(place_name)
    #area = ox.geometries_from_point((35.8789, -106.3035), dist=dist, tags={'building': building_types})
    area.plot()

    #buildings = ox.geometries_from_place(place_name, tags)
    #buildings.head()

    #buildings.plot()

def query_place4():
    # Adjust OSMnx settings for reduced data usage
    ox.config(log_console=True, use_cache=True)

    # Define the geographical area (bounding box around the coordinates)
    dist = 2500  # Distance in meters from the center point

    network_type='drive'

    # Calculate the bounding box coordinates
    north, south, east, west = ox.utils_geo.bbox_from_point((35.8789, -106.3035), dist=dist)

    # Create the street network graph
    G = ox.graph_from_bbox(north, south, east, west, network_type='drive', simplify=True)

    # Retrieve the building footprints within the specified area
    buildings = ox.geometries_from_bbox(north, south, east, west, tags={'building': True})

    # Add the building footprints to the graph
    #G = ox.footprints.add_footprints_to_graph(G, buildings)
    ox.plot.plot_footprints(buildings)

    # Plot the graph with buildings
    #fig, ax = ox.plot_graph(G, node_size=0, edge_linewidth=0.5, bgcolor='w', show=False, close=False)

    # Save the resulting map as an image file
    #fig.savefig('osmnx_map.png', dpi=300)

    default_width = 1
    street_widths = 1
    bldg_color = "red"

    #G.add_nodes_from(buildings)

    #gdf = ox.footprints.footprints_from_point(point=point, distance=dist)

    #fig, ax = ox.plot_figure_ground(G, point=(35.8789, -106.3035), edge_color='b', dist=dist, network_type=network_type, default_width=default_width, save=False, show=True, close=False)

    #fig, ax = ox.plot.plot_footprints(buildings, ax=ax, color=bldg_color, save=True, show=True, close=False) # , filename="place.png", dpi=300)
    #ox.plot(fig)
    #fig, ax = ox.plot_graph(G, node_size=0, edge_linewidth=0.5, bgcolor='w', show=False, close=False)

def query_place5():
    # configure logging/caching
    osmnx.config(log_console=True, use_cache=True)

    # configure the image display
    size = 256

    #building_types = ['industrial', 'government']
    building_types = True

    # load buildings from about 1.5km² around UCL
    point = (35.8789, -106.3035)
    dist = 2500
    gdf = osmnx.geometries_from_point(center_point=point, dist=dist, tags={'building': building_types})

    # preview image
    #gdf_proj = osmnx.project_gdf(gdf, to_crs={'init': 'epsg:3857'})
    fig, ax = osmnx.plot.plot_footprints(gdf, bgcolor='#ffffff', color='black',
                                save=False, show=True, close=False)
                                # filename='test_buildings_preview', dpi=600)

def query_place6():
    # Adjust OSMnx settings for reduced data usage
    ox.config(log_console=True, use_cache=True)

    # Define the geographical area (bounding box around the coordinates)
    dist = 500  # Distance in meters from the center point

    # Calculate the bounding box coordinates
    north, south, east, west = ox.utils_geo.bbox_from_point((35.8789, -106.3035), dist=dist)

    # Create the street network graph
    G = ox.graph_from_bbox(north, south, east, west, network_type='drive', simplify=True)

    nodes= ox.graph_to_gdfs(G, nodes=True, edges=False)
    edges= ox.graph_to_gdfs(G, edges=True, nodes=False)

    # Retrieve the building footprints within the specified area
    buildings = ox.geometries_from_bbox(north, south, east, west, tags={'building': True})

    #nodes = nodes.append(buildings, ignore_index = True)
    nodes = gpd.GeoDataFrame(pd.concat([nodes, buildings], ignore_index=False))
    graph2 = ox.graph_from_gdfs(nodes, edges)

    #ox.plot.plot_footprints(buildings)
    #ox.plot_footprints(buildings)

    # Plot the street network and buildings together
    fig, ax = ox.plot_graph(ox.project_graph(graph2), node_size=0, edge_linewidth=0.5, bgcolor='w', show=True, close=False)

    # Plot the buildings
    gpd.plotting.plot_dataframe(buildings, ax=ax, facecolor='gray', alpha=0.7)

    # Save the resulting map as an image file
    fig.savefig('osmnx_map.png', dpi=300)

def query_place7():
    place = "Hanford Site"
    G = ox.graph_from_place(place, network_type="drive")

    #Color helper functions

    #You can use the plot module to get colors for plotting.

    # get n evenly-spaced colors from some matplotlib colormap
    ox.plot.get_colors(n=5, cmap="plasma", return_hex=True)

    # get node colors by linearly mapping an attribute's values to a colormap
    nc = ox.plot.get_node_colors_by_attr(G, attr="y", cmap="plasma")
    fig, ax = ox.plot_graph(G, node_color=nc, edge_linewidth=0.3)

    # when num_bins is not None, bin the nodes/edges then assign one color to each bin
    # also set equal_size=True for equal-sized quantiles (requires unique bin edges!)
    ec = ox.plot.get_edge_colors_by_attr(G, attr="length", num_bins=5)

    # otherwise, when num_bins is None (default), linearly map one color to each node/edge by value
    ec = ox.plot.get_edge_colors_by_attr(G, attr="length")

    # plot the graph with colored edges
    fig, ax = ox.plot_graph(G, node_size=5, edge_color=ec, bgcolor="k")

def query_place8():
    import osmnx as ox

    ox.config(log_console=True, use_cache=True)
    #from IPython.display import Image

    #%matplotlib inline
    #ox.__version__

    # configure the inline image display
    img_folder = "images"
    extension = "png"
    size = 240

    # specify that we're retrieving building footprint geometries
    tags = {"building": True}

    # Building footprints within the city limits of Piedmont, California

    gdf = ox.geometries_from_place("Piedmont, California, USA", tags)
    gdf_proj = ox.project_gdf(gdf)
    fp = f"./{img_folder}/piedmont_bldgs.{extension}"
    fig, ax = ox.plot_footprints(gdf_proj, filepath=fp, dpi=400, save=False, show=True, close=False)
    #Image(fp, height=size, width=size)

    # save as a shapefile
    #gdf_save = gdf.applymap(lambda x: str(x) if isinstance(x, list) else x)
    #gdf_save.drop(labels="nodes", axis=1).to_file("./data/piedmont_bldgs.gpkg", driver="GPKG")

    # Now let's analyze the size of the building footprints...

    # calculate the area in projected units (meters) of each building footprint, then display first five
    areas = gdf_proj.area
    areas.head()

    # total area (sq m) covered by building footprints
    sum(areas)

    # get the total area within Piedmont's admin boundary in sq meters
    place = ox.geocode_to_gdf("Piedmont, California, USA")
    place_proj = ox.project_gdf(place)
    place_proj.area.iloc[0]

    # what proportion of piedmont is covered by building footprints?
    sum(areas) / place_proj.area.iloc[0]

    point = (48.873446, 2.294255)
    dist = 612
    gdf = ox.geometries_from_point(point, tags, dist=dist)
    gdf_proj = ox.project_gdf(gdf)
    bbox = ox.utils_geo.bbox_from_point(point=point, dist=dist, project_utm=True)
    fp = f"./{img_folder}/paris_bldgs.{extension}"
    fig, ax = ox.plot_footprints(
        gdf_proj,
        bbox=bbox,
        color="w",
        filepath=fp,
        dpi=90,
        save=False,
        show=True,
        close=False,
    )


def make_plot(
    place,
    point,
    network_type="drive",
    dpi=40,
    dist=805,
    default_width=4,
    street_widths=None,
):
    #building_types = ['industrial', 'government']
    building_types = True
    tags={'building': building_types}
    #fp = f"./{img_folder}/{place}.{extension}"
    gdf = ox.geometries_from_point(point, tags, dist=dist)
    fig, ax = ox.plot_figure_ground(
        point=point,
        dist=dist,
        network_type=network_type,
        default_width=default_width,
        street_widths=street_widths,
        save=False,
        show=False,
        close=True,
    )
    fig, ax = ox.plot_footprints(
        gdf, ax=ax, save=True, show=False, close=True
    )
    plt.show()

def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    
    loader = Data(os.path.join(os.path.dirname(__file__), 'resources', 'database', PROGNAME + ".db"))
    places_data = loader.load_table_data("Places")

    # query_place8()
    place = "monrovia_liberia_buildings"
    point = (6.340236, -10.747255)
    make_plot(place, point, network_type="all", default_width=2, street_widths={"primary": 6})

    exit()

    # Generate the names
    place_list =  []
    for place_name in places_data:
        place_list.append(place_name[1])

    results = {}

    for name in sorted(place_list):
        logging.info(f"Querying name: {name}")
        result = query_place(name)
        if result is not None:
            results[name] = result
        # time.sleep(0.5)

    # save_results_to_file(results)

if __name__ == '__main__':
    main()
