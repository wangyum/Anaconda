var BBoxTileSource, MercatorTileSource, _,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

MercatorTileSource = require('./mercator_tile_source');

BBoxTileSource = (function(superClass) {
  extend(BBoxTileSource, superClass);

  function BBoxTileSource() {
    this.defaults = bind(this.defaults, this);
    return BBoxTileSource.__super__.constructor.apply(this, arguments);
  }

  BBoxTileSource.prototype.type = 'BBoxTileSource';

  BBoxTileSource.prototype.defaults = function() {
    return _.extend({}, BBoxTileSource.__super__.defaults.call(this), {
      use_latlon: false
    });
  };

  BBoxTileSource.prototype.get_image_url = function(x, y, z) {
    var image_url, ref, ref1, xmax, xmin, ymax, ymin;
    image_url = this.string_lookup_replace(this.get('url'), this.get('extra_url_vars'));
    if (this.get('use_latlon')) {
      ref = this.get_tile_geographic_bounds(x, y, z), xmin = ref[0], ymin = ref[1], xmax = ref[2], ymax = ref[3];
    } else {
      ref1 = this.get_tile_meter_bounds(x, y, z), xmin = ref1[0], ymin = ref1[1], xmax = ref1[2], ymax = ref1[3];
    }
    return image_url.replace("{XMIN}", xmin).replace("{YMIN}", ymin).replace("{XMAX}", xmax).replace("{YMAX}", ymax);
  };

  return BBoxTileSource;

})(MercatorTileSource);

module.exports = {
  Model: BBoxTileSource
};
