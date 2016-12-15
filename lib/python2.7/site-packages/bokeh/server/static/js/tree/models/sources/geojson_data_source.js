var ColumnDataSource, GeoJSONDataSource, _, logger,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

logger = require("../../common/logging").logger;

ColumnDataSource = require("./column_data_source");

GeoJSONDataSource = (function(superClass) {
  extend(GeoJSONDataSource, superClass);

  function GeoJSONDataSource() {
    return GeoJSONDataSource.__super__.constructor.apply(this, arguments);
  }

  GeoJSONDataSource.prototype.type = 'GeoJSONDataSource';

  GeoJSONDataSource.prototype.initialize = function(options) {
    GeoJSONDataSource.__super__.initialize.call(this, options);
    this.geojson_to_column_data();
    this.register_property('data', this.geojson_to_column_data, true);
    return this.add_dependencies('data', this, ['geojson']);
  };

  GeoJSONDataSource.prototype.defaults = function() {
    return _.extend({}, GeoJSONDataSource.__super__.defaults.call(this), {
      geojson: null
    });
  };

  GeoJSONDataSource.prototype.nonserializable_attribute_names = function() {
    return GeoJSONDataSource.__super__.nonserializable_attribute_names.call(this).concat(['data']);
  };

  GeoJSONDataSource.prototype._get_new_list_array = function(length) {
    var array, list_array;
    array = new Array(length);
    list_array = _.map(array, function(x) {
      return [];
    });
    return list_array;
  };

  GeoJSONDataSource.prototype._get_new_nan_array = function(length) {
    var array, nan_array;
    array = new Array(length);
    nan_array = _.map(array, function(x) {
      return NaN;
    });
    return nan_array;
  };

  GeoJSONDataSource.prototype.geojson_to_column_data = function() {
    var coord_list, coords, data, exterior_ring, exterior_rings, flatten_function, flattened_coord_list, geojson, geometry, i, item, items, j, k, l, len, len1, len2, len3, len4, len5, m, n, o, p, polygon, property, ref, ref1, ref2, ref3, ref4, ref5, ref6;
    geojson = JSON.parse(this.get('geojson'));
    if ((ref = geojson.type) !== 'GeometryCollection' && ref !== 'FeatureCollection') {
      throw new Error('Bokeh only supports type GeometryCollection and FeatureCollection at top level');
    }
    if (geojson.type === 'GeometryCollection') {
      if (geojson.geometries == null) {
        throw new Error('No geometries found in GeometryCollection');
      }
      if (geojson.geometries.length === 0) {
        throw new Error('geojson.geometries must have one or more items');
      }
      items = geojson.geometries;
    }
    if (geojson.type === 'FeatureCollection') {
      if (geojson.features == null) {
        throw new Error('No features found in FeaturesCollection');
      }
      if (geojson.features.length === 0) {
        throw new Error('geojson.features must have one or more items');
      }
      items = geojson.features;
    }
    data = {
      'x': this._get_new_nan_array(items.length),
      'y': this._get_new_nan_array(items.length),
      'z': this._get_new_nan_array(items.length),
      'xs': this._get_new_list_array(items.length),
      'ys': this._get_new_list_array(items.length),
      'zs': this._get_new_list_array(items.length)
    };
    flatten_function = function(accumulator, currentItem) {
      return accumulator.concat([[NaN, NaN, NaN]]).concat(currentItem);
    };
    for (i = k = 0, len = items.length; k < len; i = ++k) {
      item = items[i];
      if (item.type === 'Feature') {
        geometry = item.geometry;
        for (property in item.properties) {
          if (!data.hasOwnProperty(property)) {
            data[property] = this._get_new_nan_array(items.length);
          }
          data[property][i] = item.properties[property];
        }
      } else {
        geometry = item;
      }
      switch (geometry.type) {
        case "Point":
          coords = geometry.coordinates;
          data.x[i] = coords[0];
          data.y[i] = coords[1];
          data.z[i] = (ref1 = coords[2]) != null ? ref1 : NaN;
          break;
        case "LineString":
          coord_list = geometry.coordinates;
          for (j = l = 0, len1 = coord_list.length; l < len1; j = ++l) {
            coords = coord_list[j];
            data.xs[i][j] = coords[0];
            data.ys[i][j] = coords[1];
            data.zs[i][j] = (ref2 = coords[2]) != null ? ref2 : NaN;
          }
          break;
        case "Polygon":
          if (geometry.coordinates.length > 1) {
            logger.warn('Bokeh does not support Polygons with holes in, only exterior ring used.');
          }
          exterior_ring = geometry.coordinates[0];
          for (j = m = 0, len2 = exterior_ring.length; m < len2; j = ++m) {
            coords = exterior_ring[j];
            data.xs[i][j] = coords[0];
            data.ys[i][j] = coords[1];
            data.zs[i][j] = (ref3 = coords[2]) != null ? ref3 : NaN;
          }
          break;
        case "MultiPoint":
          logger.warn('MultiPoint not supported in Bokeh');
          break;
        case "MultiLineString":
          flattened_coord_list = _.reduce(geometry.coordinates, flatten_function);
          for (j = n = 0, len3 = flattened_coord_list.length; n < len3; j = ++n) {
            coords = flattened_coord_list[j];
            data.xs[i][j] = coords[0];
            data.ys[i][j] = coords[1];
            data.zs[i][j] = (ref4 = coords[2]) != null ? ref4 : NaN;
          }
          break;
        case "MultiPolygon":
          exterior_rings = [];
          ref5 = geometry.coordinates;
          for (o = 0, len4 = ref5.length; o < len4; o++) {
            polygon = ref5[o];
            if (polygon.length > 1) {
              logger.warn('Bokeh does not support Polygons with holes in, only exterior ring used.');
            }
            exterior_rings.push(polygon[0]);
          }
          flattened_coord_list = _.reduce(exterior_rings, flatten_function);
          for (j = p = 0, len5 = flattened_coord_list.length; p < len5; j = ++p) {
            coords = flattened_coord_list[j];
            data.xs[i][j] = coords[0];
            data.ys[i][j] = coords[1];
            data.zs[i][j] = (ref6 = coords[2]) != null ? ref6 : NaN;
          }
          break;
        default:
          throw new Error('Invalid type ' + geometry.type);
      }
    }
    return data;
  };

  return GeoJSONDataSource;

})(ColumnDataSource.Model);

module.exports = {
  Model: GeoJSONDataSource
};
