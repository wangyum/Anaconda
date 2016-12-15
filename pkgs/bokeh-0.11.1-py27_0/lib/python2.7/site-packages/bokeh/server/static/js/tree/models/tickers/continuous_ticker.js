var ContinuousTicker, Ticker, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Ticker = require("./ticker");

ContinuousTicker = (function(superClass) {
  extend(ContinuousTicker, superClass);

  function ContinuousTicker() {
    return ContinuousTicker.__super__.constructor.apply(this, arguments);
  }

  ContinuousTicker.prototype.type = 'ContinuousTicker';

  ContinuousTicker.prototype.get_interval = void 0;

  ContinuousTicker.prototype.get_min_interval = function() {
    return this.get('min_interval');
  };

  ContinuousTicker.prototype.get_max_interval = function() {
    var ref;
    return (ref = this.get('max_interval')) != null ? ref : Infinity;
  };

  ContinuousTicker.prototype.get_ideal_interval = function(data_low, data_high, desired_n_ticks) {
    var data_range;
    data_range = data_high - data_low;
    return data_range / desired_n_ticks;
  };

  ContinuousTicker.prototype.defaults = function() {
    return _.extend({}, ContinuousTicker.__super__.defaults.call(this), {
      num_minor_ticks: 5,
      desired_num_ticks: 6
    });
  };

  return ContinuousTicker;

})(Ticker.Model);

module.exports = {
  Model: ContinuousTicker
};
