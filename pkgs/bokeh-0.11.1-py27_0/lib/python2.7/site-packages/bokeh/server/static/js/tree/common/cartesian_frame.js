var CartesianFrame, CategoricalMapper, GridMapper, LayoutBox, LinearMapper, LogMapper, _, logging,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

LayoutBox = require("./layout_box");

logging = require("./logging").logging;

LinearMapper = require("../models/mappers/linear_mapper");

LogMapper = require("../models/mappers/log_mapper");

CategoricalMapper = require("../models/mappers/categorical_mapper");

GridMapper = require("../models/mappers/grid_mapper");

CartesianFrame = (function(superClass) {
  extend(CartesianFrame, superClass);

  function CartesianFrame() {
    return CartesianFrame.__super__.constructor.apply(this, arguments);
  }

  CartesianFrame.prototype.type = 'CartesianFrame';

  CartesianFrame.prototype.initialize = function(attrs, options) {
    CartesianFrame.__super__.initialize.call(this, attrs, options);
    this.register_property('x_ranges', function() {
      return this._get_ranges('x');
    }, true);
    this.add_dependencies('x_ranges', this, ['x_range', 'extra_x_ranges']);
    this.register_property('y_ranges', function() {
      return this._get_ranges('y');
    }, true);
    this.add_dependencies('y_ranges', this, ['y_range', 'extra_y_ranges']);
    this.register_property('x_mappers', function() {
      return this._get_mappers('x', this.get('x_ranges'), this.get('h_range'));
    }, true);
    this.add_dependencies('x_ranges', this, ['x_ranges', 'h_range']);
    this.register_property('y_mappers', function() {
      return this._get_mappers('y', this.get('y_ranges'), this.get('v_range'));
    }, true);
    this.add_dependencies('y_ranges', this, ['y_ranges', 'v_range']);
    this.register_property('mapper', function() {
      return new GridMapper.Model({
        domain_mapper: this.get('x_mapper'),
        codomain_mapper: this.get('y_mapper')
      });
    }, true);
    this.add_dependencies('mapper', this, ['x_mapper', 'y_mapper']);
    return this.listenTo(this.solver, 'layout_update', this._update_mappers);
  };

  CartesianFrame.prototype.map_to_screen = function(x, y, canvas, x_name, y_name) {
    var sx, sy, vx, vy;
    if (x_name == null) {
      x_name = 'default';
    }
    if (y_name == null) {
      y_name = 'default';
    }
    vx = this.get('x_mappers')[x_name].v_map_to_target(x);
    sx = canvas.v_vx_to_sx(vx);
    vy = this.get('y_mappers')[y_name].v_map_to_target(y);
    sy = canvas.v_vy_to_sy(vy);
    return [sx, sy];
  };

  CartesianFrame.prototype._get_ranges = function(dim) {
    var extra_ranges, name, range, ranges;
    ranges = {};
    ranges['default'] = this.get(dim + "_range");
    extra_ranges = this.get("extra_" + dim + "_ranges");
    if (extra_ranges != null) {
      for (name in extra_ranges) {
        range = extra_ranges[name];
        ranges[name] = this.resolve_ref(range);
      }
    }
    return ranges;
  };

  CartesianFrame.prototype._get_mappers = function(dim, ranges, frame_range) {
    var mapper_type, mappers, name, range;
    mappers = {};
    for (name in ranges) {
      range = ranges[name];
      if (range.type === "Range1d" || range.type === "DataRange1d") {
        if (this.get(dim + "_mapper_type") === "log") {
          mapper_type = LogMapper.Model;
        } else {
          mapper_type = LinearMapper.Model;
        }
      } else if (range.type === "FactorRange") {
        mapper_type = CategoricalMapper.Model;
      } else {
        logger.warn("unknown range type for range '" + name + "': " + range);
        return null;
      }
      mappers[name] = new mapper_type({
        source_range: range,
        target_range: frame_range
      });
    }
    return mappers;
  };

  CartesianFrame.prototype._update_mappers = function() {
    var mapper, name, ref, ref1, results;
    ref = this.get('x_mappers');
    for (name in ref) {
      mapper = ref[name];
      mapper.set('target_range', this.get('h_range'));
    }
    ref1 = this.get('y_mappers');
    results = [];
    for (name in ref1) {
      mapper = ref1[name];
      results.push(mapper.set('target_range', this.get('v_range')));
    }
    return results;
  };

  CartesianFrame.prototype.defaults = function() {
    return _.extend({}, CartesianFrame.__super__.defaults.call(this), {
      extra_x_ranges: {},
      extra_y_ranges: {}
    });
  };

  return CartesianFrame;

})(LayoutBox.Model);

module.exports = {
  Model: CartesianFrame
};
