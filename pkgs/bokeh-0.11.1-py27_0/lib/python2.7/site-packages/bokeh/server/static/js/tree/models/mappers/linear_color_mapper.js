var LinearColorMapper, Model, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Model = require("../../model");

LinearColorMapper = (function(superClass) {
  extend(LinearColorMapper, superClass);

  function LinearColorMapper() {
    return LinearColorMapper.__super__.constructor.apply(this, arguments);
  }

  LinearColorMapper.prototype.initialize = function(attrs, options) {
    LinearColorMapper.__super__.initialize.call(this, attrs, options);
    this.palette = this._build_palette(this.get('palette'));
    this.little_endian = this._is_little_endian();
    if (this.get('reserve_color') != null) {
      this.reserve_color = parseInt(this.get('reserve_color').slice(1), 16);
      return this.reserve_val = this.get('reserve_val');
    }
  };

  LinearColorMapper.prototype.defaults = function() {
    return _.extend({}, LinearColorMapper.__super__.defaults.call(this), {
      high: null,
      low: null,
      palette: null,
      reserve_val: null,
      reserve_color: "#ffffff"
    });
  };

  LinearColorMapper.prototype.v_map_screen = function(data) {
    var N, buf, color, d, high, i, j, k, low, offset, ref, ref1, ref2, ref3, scale, value;
    buf = new ArrayBuffer(data.length * 4);
    color = new Uint32Array(buf);
    low = (ref = this.get('low')) != null ? ref : _.min(data);
    high = (ref1 = this.get('high')) != null ? ref1 : _.max(data);
    N = this.palette.length - 1;
    scale = N / (high - low);
    offset = -scale * low;
    if (this.little_endian) {
      for (i = j = 0, ref2 = data.length; 0 <= ref2 ? j < ref2 : j > ref2; i = 0 <= ref2 ? ++j : --j) {
        d = data[i];
        if (d === this.reserve_val) {
          value = this.reserve_color;
        } else {
          if (d > high) {
            d = high;
          }
          if (d < low) {
            d = low;
          }
          value = this.palette[Math.floor(d * scale + offset)];
        }
        color[i] = (0xff << 24) | ((value & 0xff0000) >> 16) | (value & 0xff00) | ((value & 0xff) << 16);
      }
    } else {
      for (i = k = 0, ref3 = data.length; 0 <= ref3 ? k < ref3 : k > ref3; i = 0 <= ref3 ? ++k : --k) {
        d = data[i];
        if (d === this.reserve_val) {
          value = this.reserve_color;
        } else {
          if (d > high) {
            d = high;
          }
          if (d < low) {
            d = low;
          }
          value = this.palette[Math.floor(d * scale + offset)];
        }
        color[i] = (value << 8) | 0xff;
      }
    }
    return buf;
  };

  LinearColorMapper.prototype._is_little_endian = function() {
    var buf, buf32, buf8, little_endian;
    buf = new ArrayBuffer(4);
    buf8 = new Uint8ClampedArray(buf);
    buf32 = new Uint32Array(buf);
    buf32[1] = 0x0a0b0c0d;
    little_endian = true;
    if (buf8[4] === 0x0a && buf8[5] === 0x0b && buf8[6] === 0x0c && buf8[7] === 0x0d) {
      little_endian = false;
    }
    return little_endian;
  };

  LinearColorMapper.prototype._build_palette = function(palette) {
    var _convert, i, j, new_palette, ref;
    new_palette = new Uint32Array(palette.length + 1);
    _convert = function(value) {
      if (_.isNumber(value)) {
        return value;
      } else {
        return parseInt(value.slice(1), 16);
      }
    };
    for (i = j = 0, ref = palette.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
      new_palette[i] = _convert(palette[i]);
    }
    new_palette[new_palette.length - 1] = _convert(palette[palette.length - 1]);
    return new_palette;
  };

  return LinearColorMapper;

})(Model);

module.exports = {
  Model: LinearColorMapper
};
